/* ArtSpark — mobile menu, scroll reveal and the WhatsApp order form. */
(function () {
  // Mobile menu
  var nav = document.querySelector('.nav');
  var toggle = document.querySelector('.nav-toggle');
  if (nav && toggle) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('nav-open')) {
        nav.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
    nav.querySelectorAll('.nav-links a').forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-in'); });
  }

  // Deep links (order.html#form, #faq…): land on the target once fonts and images have settled
  if (location.hash.length > 1) {
    window.addEventListener('load', function () {
      var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (target) target.scrollIntoView();
    });
  }

  // Order form → WhatsApp / email
  var form = document.getElementById('order-form');
  if (!form) return;
  var preview = document.getElementById('order-preview');
  var error = document.getElementById('form-error');
  var emailLink = document.getElementById('email-brief');
  var number = form.getAttribute('data-wa');
  var brand = form.getAttribute('data-brand');

  var preset = new URLSearchParams(location.search).get('service');
  if (preset) {
    Array.prototype.forEach.call(form.elements.service.options, function (o) {
      if (o.text === preset) o.selected = true;
    });
  }

  var rows = [['Name', 'name'], ['Service', 'service'], ['Level', 'level'], ['Subject / module', 'subject'],
    ['Word count', 'words'], ['Deadline', 'deadline'], ['Referencing', 'referencing'],
    ['University', 'university'], ['Notes', 'notes']];

  function build() {
    var lines = ['*New brief for ' + brand + '*', ''];
    rows.forEach(function (r) {
      var el = form.elements[r[1]];
      var v = el && el.value ? el.value.trim() : '';
      if (r[1] === 'deadline' && v) {
        var d = new Date(v + 'T00:00:00');
        if (!isNaN(d)) v = d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });
      }
      if (v) lines.push(r[0] + ': ' + v);
    });
    lines.push('', 'Sent from ' + location.hostname);
    return lines.join('\n');
  }

  function refresh() {
    var text = build();
    preview.textContent = text;
    if (emailLink) emailLink.href = 'mailto:' + emailLink.href.replace(/^mailto:([^?]*).*$/, '$1') +
      '?subject=' + encodeURIComponent('New brief — ' + form.elements.service.value) +
      '&body=' + encodeURIComponent(text.replace(/\*/g, ''));
  }

  var today = new Date();
  form.elements.deadline.min = today.toISOString().slice(0, 10);
  form.addEventListener('input', refresh);
  form.addEventListener('change', refresh);
  refresh();

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = form.elements.name;
    if (!name.value.trim()) {
      error.hidden = false;
      name.setAttribute('aria-invalid', 'true');
      name.focus();
      return;
    }
    error.hidden = true;
    name.removeAttribute('aria-invalid');
    window.open('https://wa.me/' + number + '?text=' + encodeURIComponent(build()), '_blank', 'noopener');
  });
})();
