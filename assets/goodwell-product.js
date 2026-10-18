(() => {
  const initialize = (root) => {
    if (root.dataset.gwInitialized) return;
    root.dataset.gwInitialized = 'true';
    const form = root.querySelector('.gw-form');
    const radios = [...root.querySelectorAll('[data-gw-variant]')];
    const submit = root.querySelector('[data-gw-submit]');
    const updateVariant = (input) => {
      if (!input || !submit) return;
      root.querySelectorAll('[data-gw-price]').forEach((price) => {
        price.textContent = input.dataset.price;
      });
      const available = input.dataset.available === 'true';
      submit.disabled = !available;
      submit.querySelector('[data-gw-submit-label]').textContent = available
        ? submit.dataset.availableLabel : submit.dataset.unavailableLabel;
    };
    radios.forEach((radio) => radio.addEventListener('change', () => updateVariant(radio)));
    updateVariant(radios.find((radio) => radio.checked));
    // Native Shopify submission is preserved. A bundle is one sellable variant.
    if (form) form.addEventListener('submit', () => { form.elements.quantity.value = '1'; });

    const gallery = root.querySelector('[data-gw-gallery]');
    const slides = [...root.querySelectorAll('[data-gw-slide]')];
    const thumbnails = [...root.querySelectorAll('[data-gw-thumbnail]')];
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    thumbnails.forEach((thumbnail) => thumbnail.addEventListener('click', (event) => {
      const slide = slides[Number(thumbnail.dataset.gwThumbnail)];
      if (!slide || !gallery) return;
      event.preventDefault();
      gallery.scrollTo({ left: slide.offsetLeft - gallery.offsetLeft, behavior: reducedMotion ? 'auto' : 'smooth' });
    }));
    if (gallery && 'IntersectionObserver' in window) {
      const galleryObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const selectedIndex = slides.indexOf(entry.target);
          thumbnails.forEach((thumbnail, index) => {
            if (index === selectedIndex) thumbnail.setAttribute('aria-current', 'true');
            else thumbnail.removeAttribute('aria-current');
          });
        });
      }, { root: gallery, threshold: 0.6 });
      slides.forEach((slide) => galleryObserver.observe(slide));
    }
    const offer = root.querySelector('[data-gw-offer]');
    const sticky = root.querySelector('[data-gw-sticky]');
    if (offer && sticky && 'IntersectionObserver' in window) {
      const observer = new IntersectionObserver(([entry]) => {
        sticky.hidden = entry.isIntersecting || entry.boundingClientRect.top > 0;
      }, { threshold: 0 });
      observer.observe(offer);
    }
  };
  const scan = (scope = document) => {
    scope.querySelectorAll('[data-goodwell-product]').forEach(initialize);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => scan());
  else scan();
  document.addEventListener('shopify:section:load', (event) => scan(event.target));
})();
