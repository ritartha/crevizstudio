/**
 * Creviz Studio — Portfolio JavaScript  v3.1
 * ============================================
 *  ★ v3.0 all features retained
 *  ★ NEW: Commission brief → Discord webhook rich embed
 *
 * Author  : Creviz Studio
 * Version : 3.1.0
 */

'use strict';

/* ============================================================
   ★  DISCORD WEBHOOK URL
   Replace the URL below with your actual Discord webhook URL.
   Format: https://discord.com/api/webhooks/{id}/{token}

   HOW TO GET IT:
   1. Open Discord → go to the channel you want briefs in
   2. ⚙️ Edit Channel → Integrations → Webhooks → New Webhook
   3. Copy the Webhook URL and paste it below
============================================================ */
const DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1401852284127805460/IcS7v21Y5I_OGA3P2fRdoQRkjLT_Pw_lyun8oM4xXHHKP2QAIsOOdl0L-ug7H7zKmZRu';


/* ============================================================
   UTILITIES
============================================================ */
const $  = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];
const clamp = (v, lo, hi) => Math.min(Math.max(v, lo), hi);
const lerp  = (a, b, t)   => a + (b - a) * t;


/* ============================================================
   DOM REFERENCES
============================================================ */
const pageLoader     = $('#pageLoader');
const loaderBar      = $('#loaderBar');
const loaderCaption  = pageLoader ? $('.loader-caption', pageLoader) : null;
const navbar         = $('#navbar');
const hamburger      = $('#hamburger');
const navLinks       = $('#navLinks');
const navLinkEls     = $$('.nav-link');
const backToTop      = $('#backToTop');
const contactForm    = $('#contactForm');
const formFeedback   = $('#formFeedback');
const scrollProgBar  = $('#scrollProgressBar');
const heroCanvas     = $('#heroCanvas');
const cursorGlow     = $('#cursorGlow');
const sections       = $$('section[id]');
const countUpEls     = $$('.count-up');
const skillFills     = $$('.skill-fill');
const revealEls      = $$('.reveal');
const pricingCards   = $$('.pricing-card');
const filterBtns     = $$('.filter-btn');
const portfolioCards = $$('.project-card');


/* ============================================================
   1. PAGE LOADER
   Cycles through render-themed captions while loading.
============================================================ */
(function initLoader() {
  const captions = [
    'Rendering your experience…',
    'Subdividing polygons…',
    'Baking ambient occlusion…',
    'Applying PBR materials…',
    'Compiling shaders…',
    'Tracing light paths…',
    'Unwrapping UVs…',
    'Sculpting details…',
  ];

  let capIdx   = 0;
  let progress = 0;

  // Cycle loader captions
  const capTimer = setInterval(() => {
    capIdx = (capIdx + 1) % captions.length;
    if (loaderCaption) loaderCaption.textContent = captions[capIdx];
  }, 300);

  // Ease the progress bar towards 100
  const tick = setInterval(() => {
    const remaining = 100 - progress;
    progress += remaining * 0.06 + Math.random() * 2;
    progress  = clamp(progress, 0, 99);
    if (loaderBar) loaderBar.style.width = `${progress}%`;
  }, 30);

  // Complete and hide loader
  setTimeout(() => {
    clearInterval(tick);
    clearInterval(capTimer);
    if (loaderBar) loaderBar.style.width = '100%';
    setTimeout(() => {
      pageLoader?.classList.add('hide');
      document.body.classList.add('loaded');
    }, 350);
  }, 1800);
})();


/* ============================================================
   2. SCROLL PROGRESS BAR
============================================================ */
function updateScrollProgress() {
  if (!scrollProgBar) return;
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  scrollProgBar.style.width = docHeight > 0
    ? `${(scrollTop / docHeight) * 100}%`
    : '0%';
}


/* ============================================================
   3. HERO CANVAS — Animated fire-tone mesh gradient
============================================================ */
(function initHeroCanvas() {
  if (!heroCanvas) return;
  const ctx = heroCanvas.getContext('2d');

  const orbColors = [
    'rgba(255, 45,  45,',
    'rgba(255, 107, 26,',
    'rgba(255, 201, 60,',
    'rgba(255, 70,  10,',
    'rgba(220, 20,  20,',
    'rgba(255, 140,  0,',
    'rgba(255, 80,  30,',
    'rgba(200, 30,  10,',
  ];

  let orbs = [];
  let raf;

  function resize() {
    heroCanvas.width  = heroCanvas.offsetWidth;
    heroCanvas.height = heroCanvas.offsetHeight;
  }

  function createOrbs() {
    orbs = Array.from({ length: 8 }, (_, i) => ({
      x:     Math.random() * heroCanvas.width,
      y:     Math.random() * heroCanvas.height,
      r:     100 + Math.random() * 220,
      vx:    (Math.random() - 0.5) * 0.45,
      vy:    (Math.random() - 0.5) * 0.45,
      alpha: 0.04 + Math.random() * 0.09,
      color: orbColors[i % orbColors.length],
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, heroCanvas.width, heroCanvas.height);

    orbs.forEach(o => {
      o.x += o.vx;
      o.y += o.vy;

      if (o.x < -o.r)                    o.x = heroCanvas.width  + o.r;
      if (o.x > heroCanvas.width  + o.r) o.x = -o.r;
      if (o.y < -o.r)                    o.y = heroCanvas.height + o.r;
      if (o.y > heroCanvas.height + o.r) o.y = -o.r;

      const g = ctx.createRadialGradient(o.x, o.y, 0, o.x, o.y, o.r);
      g.addColorStop(0,   `${o.color}${o.alpha})`);
      g.addColorStop(0.5, `${o.color}${o.alpha * 0.5})`);
      g.addColorStop(1,   `${o.color}0)`);

      ctx.beginPath();
      ctx.arc(o.x, o.y, o.r, 0, Math.PI * 2);
      ctx.fillStyle = g;
      ctx.fill();
    });

    raf = requestAnimationFrame(draw);
  }

  function start() { resize(); createOrbs(); draw(); }

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => { cancelAnimationFrame(raf); start(); }, 150);
  });

  setTimeout(start, 400);
})();


/* ============================================================
   4. CURSOR GLOW (desktop only)
============================================================ */
(function initCursorGlow() {
  if (!cursorGlow || window.innerWidth <= 768) return;

  let mx = 0, my = 0, cx = 0, cy = 0;

  document.addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    document.body.classList.add('cursor-active');
  });

  document.addEventListener('mouseleave', () => {
    document.body.classList.remove('cursor-active');
  });

  (function animateCursor() {
    cx = lerp(cx, mx, 0.1);
    cy = lerp(cy, my, 0.1);
    cursorGlow.style.left = `${cx}px`;
    cursorGlow.style.top  = `${cy}px`;
    requestAnimationFrame(animateCursor);
  })();
})();


/* ============================================================
   5. MAGNETIC BUTTONS
============================================================ */
function initMagneticButtons() {
  if (window.innerWidth <= 768) return;

  $$('.magnetic').forEach(btn => {
    btn.addEventListener('mousemove', e => {
      const rect = btn.getBoundingClientRect();
      const relX = e.clientX - rect.left  - rect.width  / 2;
      const relY = e.clientY - rect.top   - rect.height / 2;
      btn.style.transform = `translate(${relX * 0.3}px, ${relY * 0.3}px)`;
    });
    btn.addEventListener('mouseleave', () => { btn.style.transform = ''; });
  });
}

initMagneticButtons();


/* ============================================================
   6. RIPPLE CLICK EFFECT
============================================================ */
document.addEventListener('click', e => {
  const btn = e.target.closest('.btn');
  if (!btn) return;

  const rect   = btn.getBoundingClientRect();
  const size   = Math.max(rect.width, rect.height) * 2;
  const ripple = document.createElement('span');

  Object.assign(ripple.style, {
    position:      'absolute',
    width:         `${size}px`,
    height:        `${size}px`,
    left:          `${e.clientX - rect.left - size / 2}px`,
    top:           `${e.clientY - rect.top  - size / 2}px`,
    borderRadius:  '50%',
    background:    'rgba(255, 255, 255, 0.2)',
    transform:     'scale(0)',
    animation:     'ripple-expand 0.6s ease-out forwards',
    pointerEvents: 'none',
    zIndex:        '0',
  });

  btn.appendChild(ripple);
  ripple.addEventListener('animationend', () => ripple.remove());
});

const rippleStyle = document.createElement('style');
rippleStyle.textContent = `@keyframes ripple-expand { to { transform: scale(1); opacity: 0; } }`;
document.head.appendChild(rippleStyle);


/* ============================================================
   7. 3D TILT EFFECT — Pricing Cards
============================================================ */
function initTiltEffect() {
  if (window.innerWidth <= 768) return;

  pricingCards.forEach(card => {
    const inner = card.querySelector('.pricing-card-inner');
    if (!inner) return;

    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const relX = (e.clientX - rect.left) / rect.width  - 0.5;
      const relY = (e.clientY - rect.top)  / rect.height - 0.5;
      inner.style.transform = `rotateX(${relY * -12}deg) rotateY(${relX * 12}deg) scale(1.02)`;
    });

    card.addEventListener('mouseleave', () => { inner.style.transform = ''; });
  });
}

initTiltEffect();


/* ============================================================
   8. PORTFOLIO FILTER TABS
============================================================ */
function initPortfolioFilter() {
  if (!filterBtns.length) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;

      filterBtns.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      portfolioCards.forEach((card, idx) => {
        const category = card.dataset.category;
        const matches  = filter === 'all' || category === filter;

        if (matches) {
          card.classList.remove('hidden');
          card.classList.remove('revealed');
          setTimeout(() => card.classList.add('revealed'), idx * 60);
        } else {
          card.classList.add('hidden');
          card.classList.remove('revealed');
        }
      });
    });
  });
}

initPortfolioFilter();


/* ============================================================
   9. MOBILE HAMBURGER MENU
============================================================ */
function toggleMobileMenu() {
  const isOpen = navLinks.classList.toggle('open');
  hamburger.classList.toggle('active', isOpen);
  hamburger.setAttribute('aria-expanded', String(isOpen));
  document.body.style.overflow = isOpen ? 'hidden' : '';
}

function closeMobileMenu() {
  navLinks.classList.remove('open');
  hamburger.classList.remove('active');
  hamburger.setAttribute('aria-expanded', 'false');
  document.body.style.overflow = '';
}

hamburger?.addEventListener('click', toggleMobileMenu);
navLinkEls.forEach(link => link.addEventListener('click', closeMobileMenu));

document.addEventListener('click', e => {
  if (navLinks.classList.contains('open') && !navbar.contains(e.target)) {
    closeMobileMenu();
  }
});

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeMobileMenu();
});


/* ============================================================
   10. SCROLL HANDLER (rAF throttled)
============================================================ */
function handleScroll() {
  const y = window.scrollY;
  navbar.classList.toggle('scrolled', y > 50);
  backToTop?.classList.toggle('visible', y > 400);
  updateScrollProgress();
  updateActiveNavLink(y);
}

function updateActiveNavLink(y) {
  const offset = navbar.offsetHeight + 30;
  let current  = '';

  sections.forEach(sec => {
    const top    = sec.offsetTop - offset;
    const bottom = top + sec.offsetHeight;
    if (y >= top && y < bottom) current = sec.id;
  });

  navLinkEls.forEach(link => {
    link.classList.toggle('active',
      link.getAttribute('href') === `#${current}`
    );
  });
}

let scrollTicking = false;
window.addEventListener('scroll', () => {
  if (!scrollTicking) {
    requestAnimationFrame(() => { handleScroll(); scrollTicking = false; });
    scrollTicking = true;
  }
}, { passive: true });

handleScroll();


/* ============================================================
   11. SMOOTH SCROLL
============================================================ */
function smoothScrollTo(id) {
  const target = document.getElementById(id);
  if (!target) return;
  window.scrollTo({
    top: target.getBoundingClientRect().top + window.scrollY - navbar.offsetHeight,
    behavior: 'smooth',
  });
}

document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const href = a.getAttribute('href');
    if (href === '#') return;
    e.preventDefault();
    smoothScrollTo(href.slice(1));
  });
});

backToTop?.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});


/* ============================================================
   12. SCROLL REVEAL
============================================================ */
function initScrollReveal() {
  if (!revealEls.length) return;

  const io = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.10, rootMargin: '0px 0px -50px 0px' }
  );

  revealEls.forEach(el => io.observe(el));
}


/* ============================================================
   13. SKILL BAR ANIMATION
============================================================ */
function initSkillBars() {
  if (!skillFills.length) return;

  const io = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.style.width = `${entry.target.dataset.width}%`;
          }, 250);
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.3 }
  );

  skillFills.forEach(bar => io.observe(bar));
}


/* ============================================================
   14. COUNT-UP ANIMATION
============================================================ */
function animateCountUp(el) {
  const target    = parseInt(el.dataset.target, 10);
  const duration  = 1800;
  const startTime = performance.now();

  (function tick(now) {
    const t     = clamp((now - startTime) / duration, 0, 1);
    const eased = 1 - Math.pow(1 - t, 3);
    el.textContent = Math.round(eased * target);
    if (t < 1) requestAnimationFrame(tick);
    else el.textContent = target;
  })(startTime);
}

function initCountUp() {
  if (!countUpEls.length) return;

  const io = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCountUp(entry.target);
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.5 }
  );

  countUpEls.forEach(el => io.observe(el));
}


/* ============================================================
   15. NAV LINK HOVER GLOW
============================================================ */
navLinkEls.forEach(link => {
  link.addEventListener('mouseenter', () => {
    link.style.textShadow = '0 0 20px rgba(255, 107, 26, 0.5)';
  });
  link.addEventListener('mouseleave', () => {
    link.style.textShadow = '';
  });
});


/* ============================================================
   16. FORM VALIDATION HELPERS
============================================================ */

/**
 * Validate a single field and display inline error if invalid.
 * @param {HTMLElement} field
 * @param {HTMLElement|null} errorEl
 * @returns {boolean}
 */
function validateField(field, errorEl) {
  const value = field.value.trim();

  field.classList.remove('input-error');
  if (errorEl) errorEl.textContent = '';

  if (!value) {
    setFieldError(field, errorEl, `${getFieldLabel(field)} is required.`);
    return false;
  }

  if (field.type === 'email') {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      setFieldError(field, errorEl, 'Please enter a valid email address.');
      return false;
    }
  }

  if (field.tagName === 'TEXTAREA' && value.length < 20) {
    setFieldError(field, errorEl, 'Please describe your project (min. 20 characters).');
    return false;
  }

  return true;
}

/** Mark field invalid, show error text and play a shake animation */
function setFieldError(field, errorEl, message) {
  field.classList.add('input-error');
  if (errorEl) errorEl.textContent = message;

  field.animate(
    [
      { transform: 'translateX(0)' },
      { transform: 'translateX(-6px)' },
      { transform: 'translateX(6px)' },
      { transform: 'translateX(-4px)' },
      { transform: 'translateX(4px)' },
      { transform: 'translateX(0)' },
    ],
    { duration: 350, easing: 'ease-in-out' }
  );
}

/** Read the <label> text for a field to use in error messages */
function getFieldLabel(field) {
  const label = document.querySelector(`label[for="${field.id}"]`);
  return label ? label.textContent.trim() : 'This field';
}

/**
 * Show a form-level banner message.
 * Auto-clears after 6 seconds.
 * @param {string} message
 * @param {'success'|'error'} type
 */
function showFormFeedback(message, type) {
  if (!formFeedback) return;
  formFeedback.textContent = message;
  formFeedback.className   = `form-feedback ${type}`;

  formFeedback.animate(
    [
      { opacity: 0, transform: 'translateY(8px)' },
      { opacity: 1, transform: 'translateY(0)' },
    ],
    { duration: 300, fill: 'both' }
  );

  setTimeout(() => {
    formFeedback.textContent = '';
    formFeedback.className   = 'form-feedback';
  }, 6000);
}


/* ============================================================
   17. DISCORD WEBHOOK — Commission Brief Embed
   ★ This is the core integration.
   Sends a rich orange-themed embed to your Discord channel
   every time a visitor submits the commission brief form.
============================================================ */

/**
 * Builds and sends a Discord embed containing all brief details.
 * @param {{ name: string, email: string, projectType: string, budget: string, message: string }} data
 * @returns {Promise<boolean>} true if sent successfully, false on error
 */
async function sendCommissionToDiscord(data) {

  // Guard: if webhook URL hasn't been set, skip silently in dev
  if (!DISCORD_WEBHOOK_URL || DISCORD_WEBHOOK_URL.includes('YOUR_WEBHOOK')) {
    console.warn(
      '%c Creviz Studio: Discord webhook not configured. ' +
      'Set DISCORD_WEBHOOK_URL at the top of script.js ',
      'background:#ff6b1a;color:#fff;padding:4px 8px;border-radius:4px;'
    );
    return true; // Resolve as success so the UI still shows confirmation
  }

  const now       = new Date();
  const timestamp = now.toISOString();

  // Truncate message to Discord embed field limit (1024 chars)
  const msgPreview = data.message.length > 900
    ? data.message.slice(0, 900) + '…'
    : data.message;

  // ── Build the embed payload ──────────────────────────────
  const payload = {
    username:   'Comission Work Alerter',
    avatar_url: 'https://img.icons8.com/external-lineal-color-zulfa-mahendra/48/external-postman-postal-services-lineal-color-zulfa-mahendra.png',
    embeds: [
      {
        // Fire-orange colour bar (left side of embed)
        color: 0xff6b1a,

        // Title with emoji
        title: '🎨 New Commission Brief Received!',

        // Intro description
        description:
          `A new commission brief has arrived on **Creviz Studio**.\n` +
          `Please review the details below and respond within **24 hours**.`,

        // Fields grid
        fields: [
          {
            name:   '👤 Client Name',
            value:  data.name,
            inline: true,
          },
          {
            name:   '📧 Email Address',
            value:  data.email,
            inline: true,
          },
          {
            name:   '🎯 Project Type',
            value:  data.projectType || 'Not specified',
            inline: true,
          },
          {
            name:   '💰 Budget Range',
            value:  data.budget || 'Not specified',
            inline: true,
          },
          {
            name:   '📅 Date Received',
            value:  now.toLocaleDateString('en-IN', {
              weekday: 'long',
              day:     '2-digit',
              month:   'long',
              year:    'numeric',
            }),
            inline: true,
          },
          {
            name:   '🕐 Time (IST)',
            value:  now.toLocaleTimeString('en-IN', {
              hour:     '2-digit',
              minute:   '2-digit',
              timeZone: 'Asia/Kolkata',
            }),
            inline: true,
          },
          {
            // Full-width project description
            name:   '📝 Project Description',
            value:  msgPreview,
            inline: false,
          },
        ],

        // Footer + timestamp
        footer: {
          text: 'Creviz Studio · Commission Brief · Reply within 24 hours',
        },

        // Discord renders this as a relative timestamp
        timestamp,
      },
    ],
  };

  // ── POST to Discord ──────────────────────────────────────
  try {
    const response = await fetch(DISCORD_WEBHOOK_URL, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });

    if (!response.ok) {
      // Discord returns 204 No Content on success; anything else is an error
      const errText = await response.text().catch(() => '');
      throw new Error(`Discord responded ${response.status}: ${errText}`);
    }

    return true;

  } catch (err) {
    console.error('Creviz Studio — Discord webhook error:', err);
    return false;
  }
}


/* ============================================================
   18. CONTACT FORM — Submit Handler
   Validates → sends Discord embed → shows UI feedback
============================================================ */
async function handleFormSubmit(e) {
  e.preventDefault();

  // ── Gather fields ────────────────────────────────────────
  const nameField        = $('#name',        contactForm);
  const emailField       = $('#email',       contactForm);
  const projectTypeField = $('#projectType', contactForm);
  const messageField     = $('#message',     contactForm);

  // ── Error span elements ──────────────────────────────────
  const nameError        = $('#nameError');
  const emailError       = $('#emailError');
  const projectTypeError = $('#projectTypeError');
  const messageError     = $('#messageError');

  // ── Validate all (bitwise & — no short-circuit) ──────────
  const isValid =
    validateField(nameField,        nameError)        &
    validateField(emailField,       emailError)       &
    validateField(projectTypeField, projectTypeError) &
    validateField(messageField,     messageError);

  if (!isValid) {
    // Focus first broken field for accessibility
    contactForm.querySelector('.input-error')?.focus();
    return;
  }

  // ── Collect form data ────────────────────────────────────
  const formData = {
    name:        nameField.value.trim(),
    email:       emailField.value.trim(),
    projectType: projectTypeField.value,
    budget:      $('#budget', contactForm)?.value || 'Not specified',
    message:     messageField.value.trim(),
  };

  // ── Loading state ────────────────────────────────────────
  const submitBtn  = contactForm.querySelector('button[type="submit"]');
  const btnTextEl  = submitBtn.querySelector('.btn-text');

  submitBtn.disabled  = true;
  btnTextEl.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending Brief…';

  // ── Send to Discord ──────────────────────────────────────
  const sent = await sendCommissionToDiscord(formData);

  // ── Reset button state ───────────────────────────────────
  submitBtn.disabled  = false;
  btnTextEl.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Send Commission Brief';

  if (sent) {
    // Success — clear form and show confirmation
    contactForm.reset();
    showFormFeedback(
      '🎨 Commission brief received! I\'ll review it and get back to you within 24 hours.',
      'success'
    );

  } else {
    // Webhook failed — still show a polite message + keep data in form
    showFormFeedback(
      '⚠️ Something went wrong sending your brief. Please email us directly at crevizstudio@gmail.com',
      'error'
    );
  }
}

// ── Real-time per-field validation on blur ───────────────────
$$('.contact-form input, .contact-form textarea, .contact-form select').forEach(field => {

  field.addEventListener('blur', () => {
    const errorEl = $(`#${field.id}Error`);
    if (errorEl) validateField(field, errorEl);
  });

  field.addEventListener('input', () => {
    const errorEl = $(`#${field.id}Error`);
    if (errorEl && field.classList.contains('input-error')) {
      field.classList.remove('input-error');
      errorEl.textContent = '';
    }
  });

  field.addEventListener('change', () => {
    const errorEl = $(`#${field.id}Error`);
    if (errorEl && field.classList.contains('input-error')) {
      field.classList.remove('input-error');
      errorEl.textContent = '';
    }
  });
});

// Wire up the form
contactForm?.addEventListener('submit', handleFormSubmit);


/* ============================================================
   19. CARD HOVER PARALLAX (portfolio cards — desktop only)
============================================================ */
function initCardParallax() {
  if (window.innerWidth <= 768) return;

  portfolioCards.forEach(card => {
    const placeholder = card.querySelector('.img-placeholder');
    if (!placeholder) return;

    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const relX = (e.clientX - rect.left)  / rect.width  - 0.5;
      const relY = (e.clientY - rect.top)   / rect.height - 0.5;

      placeholder.style.transform = `
        scale(1.15)
        rotate(-5deg)
        translate(${relX * -12}px, ${relY * -12}px)
      `;
    });

    card.addEventListener('mouseleave', () => {
      placeholder.style.transform = '';
    });
  });
}

initCardParallax();


/* ============================================================
   20. LOGO ICON 3D SPIN — Easter egg on click
============================================================ */
$$('.logo-icon').forEach(icon => {
  icon.addEventListener('click', () => {
    icon.animate(
      [
        { transform: 'rotateY(0deg)   scale(1)'   },
        { transform: 'rotateY(180deg) scale(1.2)' },
        { transform: 'rotateY(360deg) scale(1)'   },
      ],
      { duration: 600, easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)' }
    );
  });
});


/* ============================================================
   21. SECTION TAG PULSE on reveal
============================================================ */
(function initSectionTagPulse() {
  const tags = $$('.section-tag');
  if (!tags.length) return;

  const s = document.createElement('style');
  s.textContent = `
    @keyframes tag-pulse {
      0%   { box-shadow: 0 0 0 0    rgba(255,107,26,0.5); }
      70%  { box-shadow: 0 0 0 14px rgba(255,107,26,0); }
      100% { box-shadow: 0 0 0 0    rgba(255,107,26,0); }
    }
    .tag-animate { animation: tag-pulse 0.7s ease-out; }
  `;
  document.head.appendChild(s);

  const io = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('tag-animate');
          entry.target.addEventListener(
            'animationend',
            () => entry.target.classList.remove('tag-animate'),
            { once: true }
          );
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.8 }
  );

  tags.forEach(tag => io.observe(tag));
})();


/* ============================================================
   22. PRICING CARD FEATURE LIST STAGGER
============================================================ */
(function initPricingFeatureStagger() {
  const cards = $$('.pricing-card');
  if (!cards.length) return;

  const s = document.createElement('style');
  s.textContent = `
    .plan-features li {
      opacity: 0;
      transform: translateX(-12px);
      transition: opacity 0.35s ease, transform 0.35s ease;
    }
    .pricing-card.features-revealed .plan-features li {
      opacity: 1;
      transform: translateX(0);
    }
    ${Array.from({ length: 7 }, (_, i) =>
      `.pricing-card.features-revealed .plan-features li:nth-child(${i + 1})
       { transition-delay: ${i * 0.07}s; }`
    ).join('\n')}
  `;
  document.head.appendChild(s);

  const io = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('features-revealed');
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.25 }
  );

  cards.forEach(card => io.observe(card));
})();


/* ============================================================
   23. INIT
============================================================ */
function init() {
  initScrollReveal();
  initSkillBars();
  initCountUp();

  // Console branding
  console.info(
    '%c 🔥 Creviz Studio v3.1 ',
    'background:linear-gradient(135deg,#ff2d2d,#ff6b1a,#ffc93c);' +
    'color:#fff;padding:7px 18px;border-radius:20px;' +
    'font-weight:800;font-size:13px;letter-spacing:.05em;'
  );
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}