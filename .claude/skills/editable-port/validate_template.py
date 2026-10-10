"""Check a JSON template against its sections' {% schema %} blocks.

Usage: python3 .claude/skills/editable-port/validate_template.py templates/product.<name>.json

Reports settings and block types that the schema doesn't define, select
values outside the allowed options, block_order/blocks mismatches, and
sections missing from (or extra in) the order list. Exits 1 on any problem.
"""
import json
import re
import sys


def load_schema(section_type):
    src = open(f'sections/{section_type}.liquid').read()
    m = re.search(r'\{%-?\s*schema\s*-?%\}(.*?)\{%-?\s*endschema', src, re.S)
    # Some theme schemas have trailing commas, which Shopify tolerates.
    return json.loads(re.sub(r',(\s*[\]}])', r'\1', m.group(1)))


def check_settings(where, values, defs, problems):
    for key, val in values.items():
        d = defs.get(key)
        if d is None:
            problems.append(f'{where}: unknown setting "{key}"')
        elif d['type'] == 'select' and val not in [o['value'] for o in d['options']]:
            problems.append(f'{where}: "{key}" = {val!r} is not an allowed option')


def main(path):
    raw = open(path).read()
    raw = re.sub(r'^\s*/\*.*?\*/', '', raw, flags=re.S)  # Shopify's header comment
    tpl = json.loads(raw)
    problems = []
    sections = tpl['sections']
    if set(tpl['order']) != set(sections):
        problems.append(f'order/sections mismatch: {set(tpl["order"]) ^ set(sections)}')
    for key, sec in sections.items():
        schema = load_schema(sec['type'])
        defs = {s['id']: s for s in schema.get('settings', []) if 'id' in s}
        check_settings(key, sec.get('settings', {}), defs, problems)
        block_defs = {b['type']: {s['id']: s for s in b.get('settings', []) if 'id' in s}
                      for b in schema.get('blocks', [])}
        if set(sec.get('block_order', [])) != set(sec.get('blocks', {})):
            problems.append(f'{key}: block_order/blocks mismatch')
        for bkey, block in sec.get('blocks', {}).items():
            if block['type'] not in block_defs:
                problems.append(f'{key}/{bkey}: unknown block type "{block["type"]}"')
                continue
            check_settings(f'{key}/{bkey}', block.get('settings', {}), block_defs[block['type']], problems)
    for p in problems:
        print(p)
    print(f'{len(problems)} problem(s)')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
