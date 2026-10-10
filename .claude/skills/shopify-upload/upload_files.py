"""Upload local images to Shopify Files through the Admin GraphQL API.

Usage: python3 .claude/skills/shopify-upload/upload_files.py file.png [file2.png ...]
Needs SHOPIFY_STORE and SHOPIFY_ADMIN_TOKEN in the environment.
Prints "<local path> -> shopify://shop_images/<filename>" for each file.
"""
import json
import mimetypes
import os
import sys
import time
import urllib.request
import uuid

STORE = os.environ['SHOPIFY_STORE']
TOKEN = os.environ['SHOPIFY_ADMIN_TOKEN']
VERSION = os.environ.get('SHOPIFY_API_VERSION', '2025-07')
ENDPOINT = f'https://{STORE}/admin/api/{VERSION}/graphql.json'


def gql(query, variables):
    req = urllib.request.Request(
        ENDPOINT, data=json.dumps({'query': query, 'variables': variables}).encode(),
        headers={'Content-Type': 'application/json', 'X-Shopify-Access-Token': TOKEN})
    with urllib.request.urlopen(req) as r:
        body = json.load(r)
    if body.get('errors'):
        raise SystemExit(f'GraphQL errors: {body["errors"]}')
    return body['data']


def multipart(fields, file_field, filename, content, mime):
    boundary = uuid.uuid4().hex
    parts = []
    for name, value in fields:
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{file_field}"; '
                 f'filename="{filename}"\r\nContent-Type: {mime}\r\n\r\n'.encode() + content + b'\r\n')
    parts.append(f'--{boundary}--\r\n'.encode())
    return b''.join(parts), f'multipart/form-data; boundary={boundary}'


def upload(path):
    filename = os.path.basename(path)
    mime = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
    content = open(path, 'rb').read()

    staged = gql('''mutation($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) {
        stagedTargets { url resourceUrl parameters { name value } }
        userErrors { field message } } }''',
                 {'input': [{'filename': filename, 'mimeType': mime, 'httpMethod': 'POST',
                             'resource': 'FILE', 'fileSize': str(len(content))}]})['stagedUploadsCreate']
    if staged['userErrors']:
        raise SystemExit(f'{filename}: {staged["userErrors"]}')
    target = staged['stagedTargets'][0]

    body, ctype = multipart([(p['name'], p['value']) for p in target['parameters']],
                            'file', filename, content, mime)
    urllib.request.urlopen(urllib.request.Request(target['url'], data=body, headers={'Content-Type': ctype}))

    created = gql('''mutation($files: [FileCreateInput!]!) {
      fileCreate(files: $files) { files { id fileStatus } userErrors { field message } } }''',
                  {'files': [{'originalSource': target['resourceUrl'], 'contentType': 'IMAGE',
                              'filename': filename}]})['fileCreate']
    if created['userErrors']:
        raise SystemExit(f'{filename}: {created["userErrors"]}')
    file_id = created['files'][0]['id']

    for _ in range(30):
        node = gql('''query($id: ID!) { node(id: $id) { ... on MediaImage {
          fileStatus image { url } fileErrors { message } } } }''', {'id': file_id})['node']
        if node['fileStatus'] == 'READY':
            # The stored name can get a suffix if the file already exists.
            stored = node['image']['url'].split('?')[0].rsplit('/', 1)[-1]
            return f'shopify://shop_images/{stored}'
        if node['fileStatus'] == 'FAILED':
            raise SystemExit(f'{filename}: {node["fileErrors"]}')
        time.sleep(2)
    raise SystemExit(f'{filename}: still processing after 60s ({file_id})')


if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(f'{p} -> {upload(p)}')
