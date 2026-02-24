/**
 * Creviz Marketplace — marketplace.js  v1.0
 * ==========================================
 * Features:
 *  ★ Product data array (12 assets, easily extendable)
 *  ★ Live search (debounced)
 *  ★ Multi-filter: category, price range, software, format, star rating
 *  ★ Active filter pills with individual clear
 *  ★ Sort: Featured / Price / Rating / Newest / Most Popular
 *  ★ Grid & List view toggle
 *  ★ Pagination (9 per page)
 *  ★ Add to Cart with animated drawer
 *  ★ Remove from Cart
 *  ★ Cart subtotal + 18% GST + total
 *  ★ Wishlist toggle (per card)
 *  ★ Quick View modal
 *  ★ Toast notifications
 *  ★ Mobile sidebar toggle
 *  ★ Discord Webhook — "Buy Now" sends purchase intent embed
 *  ★ Checkout button placeholder
 *
 * Author  : Creviz Studio
 * Version : 1.0.0
 */

'use strict';

/* ============================================================
   ★  DISCORD WEBHOOK URL
   Replace the URL below with your actual Discord webhook URL.
   Format: https://discord.com/api/webhooks/{id}/{token}
============================================================ */
const DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1475451131705692304/TDLjOqCOYQSM8yL6HLu1ElUUqRtCdVPiUBODxUuEfjNRkLENv3Eyg_KYr7bPIUObPKnU';


/* ============================================================
   PRODUCT DATA
   To add a product copy one object, increment the id and fill in your details.
   image: Path to your render image, e.g. 'assets/images/market/filename.jpg'
          Set to null to show the placeholder icon instead.
============================================================ */
const PRODUCTS = [
  {
    id:            1,
    title:         'Iron Veil Warrior',
    category:      'character',
    desc:          'Battle-hardened female knight sculpted at 40M polys in ZBrush. Fully rigged, game-ready FBX with 4K PBR texture set including albedo, normal, roughness, metallic and AO.',
    price:         1499,
    originalPrice: 1999,
    rating:        5,
    reviews:       42,
    software:      ['zbrush', 'blender', 'substance'],
    formats:       ['fbx', 'blend', 'obj'],
    image:         null,
    icon:          'fa-solid fa-person',
    badges:        ['hot'],
    downloads:     318,
    featured:      true,
    dateAdded:     '2026-01-15',
  },
  {
    id:            2,
    title:         'Ember Wastes Environment',
    category:      'environment',
    desc:          'Post-apocalyptic volcanic landscape. Full scene .blend file, volumetric smoke setup, god-ray lighting rig and tileable lava-rock PBR materials at 4K.',
    price:         1299,
    originalPrice: null,
    rating:        5,
    reviews:       28,
    software:      ['blender', 'substance'],
    formats:       ['blend', 'fbx'],
    image:         null,
    icon:          'fa-solid fa-mountain-sun',
    badges:        ['new'],
    downloads:     201,
    featured:      true,
    dateAdded:     '2026-02-01',
  },
  {
    id:            3,
    title:         'Relic Weapon Pack (6 Models)',
    category:      'prop',
    desc:          'Six fantasy melee weapons baked from high-poly ZBrush sculpts. Each includes 4K albedo, normal, roughness and metallic maps. Fully game-engine ready.',
    price:         799,
    originalPrice: 1199,
    rating:        4,
    reviews:       64,
    software:      ['zbrush', 'substance'],
    formats:       ['fbx', 'obj', 'usdz'],
    image:         null,
    icon:          'fa-solid fa-khanda',
    badges:        ['sale'],
    downloads:     487,
    featured:      true,
    dateAdded:     '2025-11-20',
  },
  {
    id:            4,
    title:         'Neon Alley Scene',
    category:      'environment',
    desc:          'Rain-soaked cyberpunk back-alley. Full EEVEE scene with wet-surface shaders, neon light emission, holographic sign materials and volumetric fog.',
    price:         1099,
    originalPrice: null,
    rating:        5,
    reviews:       19,
    software:      ['blender'],
    formats:       ['blend'],
    image:         null,
    icon:          'fa-solid fa-city',
    badges:        ['new'],
    downloads:     145,
    featured:      false,
    dateAdded:     '2026-01-28',
  },
  {
    id:            5,
    title:         'Void Sorcerer Character',
    category:      'character',
    desc:          'Stylised dark-fantasy spellcaster with cloth simulation cache, particle robe system and emissive rune tattoos. Rigged and export-ready for Unreal Engine 5.',
    price:         1799,
    originalPrice: 2299,
    rating:        5,
    reviews:       37,
    software:      ['zbrush', 'blender', 'unreal'],
    formats:       ['fbx', 'blend'],
    image:         null,
    icon:          'fa-solid fa-hat-wizard',
    badges:        ['hot', 'sale'],
    downloads:     276,
    featured:      true,
    dateAdded:     '2025-12-10',
  },
  {
    id:            6,
    title:         'Mossy Rock PBR Pack',
    category:      'texture',
    desc:          '12 seamless mossy rock PBR materials at 4K resolution. Includes albedo, normal, height, roughness and AO maps. Compatible with Blender, Unreal and Unity.',
    price:         499,
    originalPrice: null,
    rating:        4,
    reviews:       93,
    software:      ['blender', 'substance', 'unreal', 'unity'],
    formats:       ['blend', 'usdz'],
    image:         null,
    icon:          'fa-solid fa-layer-group',
    badges:        [],
    downloads:     612,
    featured:      false,
    dateAdded:     '2025-10-05',
  },
  {
    id:            7,
    title:         'Kira — Sci-Fi Scout',
    category:      'character',
    desc:          'Hard-surface exo-suit character with visor glass shader, mechanical arm rigs and multiple LODs. Production-ready for Unity and Unreal Engine. Full 4K PBR.',
    price:         2199,
    originalPrice: 2699,
    rating:        5,
    reviews:       55,
    software:      ['zbrush', 'blender', 'substance', 'unreal', 'unity'],
    formats:       ['fbx', 'blend', 'obj'],
    image:         null,
    icon:          'fa-solid fa-user-astronaut',
    badges:        ['hot'],
    downloads:     344,
    featured:      true,
    dateAdded:     '2026-01-05',
  },
  {
    id:            8,
    title:         'Ancient Temple Grove',
    category:      'environment',
    desc:          'Overgrown jungle temple with Geometry Nodes scatter system for vines, moss and foliage. Water caustics shader and dynamic light linking included.',
    price:         1599,
    originalPrice: null,
    rating:        5,
    reviews:       22,
    software:      ['blender', 'substance'],
    formats:       ['blend'],
    image:         null,
    icon:          'fa-solid fa-torii-gate',
    badges:        ['new'],
    downloads:     178,
    featured:      false,
    dateAdded:     '2026-02-10',
  },
  {
    id:            9,
    title:         'Abandoned Diner Props',
    category:      'prop',
    desc:          'Retro diner hero prop set — booth, cracked tiles, broken neon sign and dusty counter. Full 4K texture maps. Clean UV unwrap, FBX and OBJ exports.',
    price:         699,
    originalPrice: null,
    rating:        4,
    reviews:       41,
    software:      ['blender', 'substance'],
    formats:       ['fbx', 'obj'],
    image:         null,
    icon:          'fa-solid fa-store',
    badges:        [],
    downloads:     289,
    featured:      false,
    dateAdded:     '2025-09-18',
  },
  {
    id:            10,
    title:         'Arctic Research Base',
    category:      'environment',
    desc:          'Sci-fi blizzard outpost with sub-surface ice scattering shader, wind-driven particle snow system and moody flickering interior lighting. Cycles-optimised.',
    price:         1399,
    originalPrice: 1799,
    rating:        4,
    reviews:       17,
    software:      ['blender'],
    formats:       ['blend', 'fbx'],
    image:         null,
    icon:          'fa-solid fa-snowflake',
    badges:        ['sale'],
    downloads:     132,
    featured:      false,
    dateAdded:     '2025-08-22',
  },
  {
    id:            11,
    title:         'Wet Concrete Texture Pack',
    category:      'texture',
    desc:          '8 wet and dry concrete PBR materials. Perfect for urban environments. Includes tiling albedo, normal, height, metallic and roughness maps at 4K resolution.',
    price:         0,
    originalPrice: null,
    rating:        5,
    reviews:       204,
    software:      ['blender', 'unreal', 'unity'],
    formats:       ['blend', 'usdz', 'obj'],
    image:         null,
    icon:          'fa-solid fa-layer-group',
    badges:        ['free'],
    downloads:     1841,
    featured:      true,
    dateAdded:     '2025-07-01',
  },
  {
    id:            12,
    title:         'Fantasy Ground Vehicle',
    category:      'vehicle',
    desc:          'Ornate steampunk carriage with animated wheel rig, aged leather shader and detailed wood-grain PBR materials. Unreal Engine 5 and Unity compatible.',
    price:         1899,
    originalPrice: 2399,
    rating:        4,
    reviews:       14,
    software:      ['blender', 'substance', 'unreal'],
    formats:       ['fbx', 'blend'],
    image:         null,
    icon:          'fa-solid fa-car',
    badges:        ['sale'],
    downloads:     98,
    featured:      false,
    dateAdded:     '2026-02-18',
  },
];


/* ============================================================
   CONSTANTS
============================================================ */
const ITEMS_PER_PAGE = 9;
const GST_RATE       = 0.18;   // 18%

const BADGE_LABELS = {
  new:  { label: 'New',     cls: 'mk-badge-new'  },
  hot:  { label: '🔥 Hot',  cls: 'mk-badge-hot'  },
  sale: { label: 'Sale',    cls: 'mk-badge-sale'  },
  free: { label: 'Free',    cls: 'mk-badge-free'  },
};

const CATEGORY_LABELS = {
  character:   'Characters',
  environment: 'Environments',
  prop:        'Props & Weapons',
  texture:     'Texture Packs',
  vehicle:     'Vehicles',
};

const SOFTWARE_LABELS = {
  blender:   'Blender',
  zbrush:    'ZBrush',
  substance: 'Substance Painter',
  unreal:    'Unreal Engine',
  unity:     'Unity',
};

const FORMAT_LABELS = {
  fbx:   'FBX',
  obj:   'OBJ',
  blend: 'BLEND',
  usdz:  'USDZ',
};


/* ============================================================
   STATE
============================================================ */
let state = {
  search:     '',
  categories: [],       // empty = all
  software:   [],
  formats:    [],
  minRating:  0,
  maxPrice:   Infinity,
  sort:       'featured',
  page:       1,
  view:       'grid',   // 'grid' | 'list'
  cart:       [],       // array of product objects
  wishlist:   new Set(),
};


/* ============================================================
   DOM REFERENCES
============================================================ */
const dom = {
  productGrid:   document.getElementById('productGrid'),
  resultCount:   document.getElementById('resultCount'),
  pagination:    document.getElementById('pagination'),
  noResults:     document.getElementById('noResults'),
  searchInput:   document.getElementById('searchInput'),
  sortSelect:    document.getElementById('sortSelect'),
  priceRange:    document.getElementById('priceRange'),
  priceRangeVal: document.getElementById('priceRangeVal'),
  priceMin:      document.getElementById('priceMin'),
  priceMax:      document.getElementById('priceMax'),
  cartBtn:       document.getElementById('cartBtn'),
  cartCount:     document.getElementById('cartCount'),
  cartDrawer:    document.getElementById('cartDrawer'),
  cartOverlay:   document.getElementById('cartOverlay'),
  cartClose:     document.getElementById('cartClose'),
  cartEmpty:     document.getElementById('cartEmpty'),
  cartItems:     document.getElementById('cartItems'),
  cartFooter:    document.getElementById('cartFooter'),
  cartSubtotal:  document.getElementById('cartSubtotal'),
  cartGst:       document.getElementById('cartGst'),
  cartTotal:     document.getElementById('cartTotal'),
  checkoutBtn:   document.getElementById('checkoutBtn'),
  modalOverlay:  document.getElementById('modalOverlay'),
  modalClose:    document.getElementById('modalClose'),
  modalInner:    document.getElementById('modalInner'),
  toastWrap:     document.getElementById('toastWrap'),
  activeFilters: document.getElementById('activeFilters'),
  clearFilters:  document.getElementById('clearFilters'),
  gridViewBtn:   document.getElementById('gridViewBtn'),
  listViewBtn:   document.getElementById('listViewBtn'),
  filterToggle:  document.getElementById('filterToggle'),
  mkSidebar:     document.getElementById('mkSidebar'),
  starFilter:    document.getElementById('starFilter'),
  mkNavbar:      document.getElementById('mkNavbar'),
};


/* ============================================================
   UTILITY FUNCTIONS
============================================================ */

/** Format a price number as Indian Rupee string */
function formatPrice(n) {
  if (n === 0) return 'Free';
  return '₹' + n.toLocaleString('en-IN');
}

/** Render filled/empty stars string */
function renderStars(rating) {
  return '★'.repeat(Math.round(rating)) + '☆'.repeat(5 - Math.round(rating));
}

/** Simple debounce */
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}

/** Build badge HTML for a product */
function buildBadges(badges) {
  if (!badges || badges.length === 0) return '';
  return badges.map(b => {
    const cfg = BADGE_LABELS[b];
    if (!cfg) return '';
    return `<span class="mk-badge ${cfg.cls}">${cfg.label}</span>`;
  }).join('');
}

/** Format file sizes for display */
function capFirst(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}


/* ============================================================
   FILTER & SORT
============================================================ */
function getFilteredProducts() {
  let list = [...PRODUCTS];

  // ── Search ──────────────────────────────────────────────
  if (state.search.trim()) {
    const q = state.search.trim().toLowerCase();
    list = list.filter(p =>
      p.title.toLowerCase().includes(q)    ||
      p.desc.toLowerCase().includes(q)     ||
      p.category.toLowerCase().includes(q) ||
      p.software.some(s => s.includes(q))
    );
  }

  // ── Category ────────────────────────────────────────────
  if (state.categories.length > 0) {
    list = list.filter(p => state.categories.includes(p.category));
  }

  // ── Price (max) ─────────────────────────────────────────
  if (state.maxPrice < Infinity) {
    list = list.filter(p => p.price <= state.maxPrice);
  }

  // ── Software ────────────────────────────────────────────
  if (state.software.length > 0) {
    list = list.filter(p =>
      state.software.some(sw => p.software.includes(sw))
    );
  }

  // ── Format ──────────────────────────────────────────────
  if (state.formats.length > 0) {
    list = list.filter(p =>
      state.formats.some(f => p.formats.includes(f))
    );
  }

  // ── Minimum Rating ──────────────────────────────────────
  if (state.minRating > 0) {
    list = list.filter(p => p.rating >= state.minRating);
  }

  // ── Sort ────────────────────────────────────────────────
  switch (state.sort) {
    case 'price-asc':
      list.sort((a, b) => a.price - b.price);
      break;
    case 'price-desc':
      list.sort((a, b) => b.price - a.price);
      break;
    case 'rating':
      list.sort((a, b) => b.rating - a.rating || b.reviews - a.reviews);
      break;
    case 'newest':
      list.sort((a, b) => new Date(b.dateAdded) - new Date(a.dateAdded));
      break;
    case 'popular':
      list.sort((a, b) => b.downloads - a.downloads);
      break;
    default: // 'featured'
      list.sort((a, b) => (b.featured ? 1 : 0) - (a.featured ? 1 : 0));
      break;
  }

  return list;
}


/* ============================================================
   RENDER — PRODUCT CARD (Grid)
============================================================ */
function buildCardHTML(product) {
  const inCart     = state.cart.some(c => c.id === product.id);
  const inWishlist = state.wishlist.has(product.id);

  const priceHTML = product.price === 0
    ? `<span class="mk-price-free">Free</span>`
    : `<div class="mk-price-wrap">
         <span class="mk-price">${formatPrice(product.price)}</span>
         ${product.originalPrice
           ? `<span class="mk-price-original">${formatPrice(product.originalPrice)}</span>`
           : ''}
       </div>`;

  const imgHTML = product.image
    ? `<img src="${product.image}" alt="${product.title}" loading="lazy" />`
    : `<div class="mk-card-img-placeholder"><i class="${product.icon}"></i></div>`;

  const formatsHTML = product.formats
    .map(f => `<span class="mk-format-tag">${f.toUpperCase()}</span>`)
    .join('');

  const buyLabel = inCart ? '✓ Added' : (product.price === 0 ? 'Get Free' : 'Add to Cart');
  const buyClass = inCart ? 'mk-buy-btn added' : 'mk-buy-btn';

  // Discount % badge
  let discountHTML = '';
  if (product.originalPrice && product.price > 0) {
    const pct = Math.round((1 - product.price / product.originalPrice) * 100);
    discountHTML = `<span class="mk-badge mk-badge-sale">-${pct}%</span>`;
  }

  return `
    <div class="mk-card" data-id="${product.id}">

      <!-- Image / Placeholder -->
      <div class="mk-card-img">
        ${imgHTML}

        <!-- Badges -->
        <div class="mk-card-badges">
          ${buildBadges(product.badges)}
          ${discountHTML}
        </div>

        <!-- Wishlist -->
        <button
          class="mk-wishlist-btn ${inWishlist ? 'active' : ''}"
          data-id="${product.id}"
          aria-label="${inWishlist ? 'Remove from wishlist' : 'Add to wishlist'}"
          title="${inWishlist ? 'Remove from wishlist' : 'Add to wishlist'}"
        >
          <i class="${inWishlist ? 'fa-solid' : 'fa-regular'} fa-heart"></i>
        </button>

        <!-- Quick View overlay -->
        <div class="mk-card-overlay">
          <button class="mk-quick-view-btn" data-id="${product.id}">
            <i class="fa-solid fa-eye"></i> Quick View
          </button>
        </div>
      </div>

      <!-- Card Body -->
      <div class="mk-card-body">

        <!-- Main info (used for list-view layout) -->
        <div class="mk-card-main">
          <span class="mk-card-category">${CATEGORY_LABELS[product.category] || capFirst(product.category)}</span>
          <h3 class="mk-card-title">${product.title}</h3>
          <p class="mk-card-desc">${product.desc}</p>

          <!-- File format tags -->
          <div class="mk-card-formats">${formatsHTML}</div>

          <!-- Star Rating -->
          <div class="mk-card-rating">
            <span class="mk-stars" aria-label="${product.rating} out of 5 stars">${renderStars(product.rating)}</span>
            <span class="mk-rating-count">(${product.reviews.toLocaleString()})</span>
            <span class="mk-rating-count" style="margin-left:6px;">
              <i class="fa-solid fa-download" style="font-size:.65rem; color:var(--orange);"></i>
              ${product.downloads.toLocaleString()}
            </span>
          </div>
        </div>

        <!-- Footer: price + buy -->
        <div class="mk-card-footer">
          ${priceHTML}
          <button
            class="${buyClass}"
            data-id="${product.id}"
            aria-label="Add ${product.title} to cart"
          >
            <i class="fa-solid ${inCart ? 'fa-check' : 'fa-cart-plus'}"></i>
            ${buyLabel}
          </button>
        </div>

      </div>
    </div>
  `;
}


/* ============================================================
   RENDER — FULL PRODUCT GRID + PAGINATION
============================================================ */
function renderProducts() {
  const all     = getFilteredProducts();
  const total   = all.length;
  const totalPages = Math.ceil(total / ITEMS_PER_PAGE);

  // Clamp page if filters reduced total
  if (state.page > totalPages && totalPages > 0) state.page = totalPages;
  if (state.page < 1) state.page = 1;

  const start = (state.page - 1) * ITEMS_PER_PAGE;
  const paged = all.slice(start, start + ITEMS_PER_PAGE);

  // ── Result count ───────────────────────────────────────
  dom.resultCount.innerHTML =
    `Showing <strong>${Math.min(start + 1, total)}–${Math.min(start + paged.length, total)}</strong>
     of <strong>${total}</strong> asset${total !== 1 ? 's' : ''}`;

  // ── No results ─────────────────────────────────────────
  dom.noResults.classList.toggle('hidden', total > 0);
  dom.productGrid.classList.toggle('hidden', total === 0);

  // ── Products HTML ──────────────────────────────────────
  dom.productGrid.innerHTML = paged.map(p => buildCardHTML(p)).join('');

  // Apply current view
  dom.productGrid.className = 'mk-product-grid' + (state.view === 'list' ? ' list-view' : '');

  // ── Pagination ─────────────────────────────────────────
  renderPagination(totalPages);

  // ── Re-attach card event listeners ─────────────────────
  attachCardListeners();

  // ── Render active filter pills ─────────────────────────
  renderActiveFilters();
}


/* ============================================================
   RENDER — PAGINATION
============================================================ */
function renderPagination(totalPages) {
  if (totalPages <= 1) {
    dom.pagination.innerHTML = '';
    return;
  }

  let html = '';

  // Prev button
  html += `<button class="mk-page-btn" data-page="${state.page - 1}"
    ${state.page === 1 ? 'disabled aria-disabled="true"' : ''}
    aria-label="Previous page">
    <i class="fa-solid fa-chevron-left"></i>
  </button>`;

  // Page number buttons
  for (let i = 1; i <= totalPages; i++) {
    if (
      i === 1 ||
      i === totalPages ||
      (i >= state.page - 1 && i <= state.page + 1)
    ) {
      html += `<button
        class="mk-page-btn ${i === state.page ? 'active' : ''}"
        data-page="${i}"
        aria-label="Page ${i}"
        ${i === state.page ? 'aria-current="page"' : ''}
      >${i}</button>`;
    } else if (i === state.page - 2 || i === state.page + 2) {
      html += `<span class="mk-page-btn" style="pointer-events:none;opacity:.4;">…</span>`;
    }
  }

  // Next button
  html += `<button class="mk-page-btn" data-page="${state.page + 1}"
    ${state.page === totalPages ? 'disabled aria-disabled="true"' : ''}
    aria-label="Next page">
    <i class="fa-solid fa-chevron-right"></i>
  </button>`;

  dom.pagination.innerHTML = html;

  // Listeners
  dom.pagination.querySelectorAll('.mk-page-btn[data-page]').forEach(btn => {
    btn.addEventListener('click', () => {
      const p = parseInt(btn.dataset.page, 10);
      if (!isNaN(p)) {
        state.page = p;
        renderProducts();
        // Scroll to top of product area
        dom.productGrid.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}


/* ============================================================
   RENDER — ACTIVE FILTER PILLS
============================================================ */
function renderActiveFilters() {
  const pills = [];

  if (state.search) {
    pills.push({ label: `Search: "${state.search}"`, action: () => {
      state.search = '';
      dom.searchInput.value = '';
    }});
  }

  state.categories.forEach(cat => {
    pills.push({ label: CATEGORY_LABELS[cat] || capFirst(cat), action: () => {
      state.categories = state.categories.filter(c => c !== cat);
      // Uncheck the matching checkbox
      const cb = dom.mkSidebar.querySelector(
        `input[data-filter-type="category"][value="${cat}"]`
      );
      if (cb) cb.checked = false;
    }});
  });

  if (state.maxPrice < Infinity) {
    pills.push({ label: `Under ${formatPrice(state.maxPrice)}`, action: () => {
      state.maxPrice = Infinity;
      dom.priceRange.value = dom.priceRange.max;
      dom.priceRangeVal.textContent = `₹${Number(dom.priceRange.max).toLocaleString('en-IN')}+`;
    }});
  }

  state.software.forEach(sw => {
    pills.push({ label: SOFTWARE_LABELS[sw] || capFirst(sw), action: () => {
      state.software = state.software.filter(s => s !== sw);
      const cb = dom.mkSidebar.querySelector(
        `input[data-filter-type="software"][value="${sw}"]`
      );
      if (cb) cb.checked = false;
    }});
  });

  state.formats.forEach(fmt => {
    pills.push({ label: FORMAT_LABELS[fmt] || fmt.toUpperCase(), action: () => {
      state.formats = state.formats.filter(f => f !== fmt);
      const cb = dom.mkSidebar.querySelector(
        `input[data-filter-type="format"][value="${fmt}"]`
      );
      if (cb) cb.checked = false;
    }});
  });

  if (state.minRating > 0) {
    pills.push({ label: `${state.minRating}★+`, action: () => {
      state.minRating = 0;
      dom.starFilter.querySelectorAll('.mk-star-btn').forEach(b => b.classList.remove('active'));
      dom.starFilter.querySelector('[data-stars="0"]').classList.add('active');
    }});
  }

  if (pills.length === 0) {
    dom.activeFilters.innerHTML = '';
    return;
  }

  dom.activeFilters.innerHTML = pills.map((pill, idx) => `
    <span class="mk-pill">
      ${pill.label}
      <button data-pill="${idx}" aria-label="Remove filter: ${pill.label}">
        <i class="fa-solid fa-xmark"></i>
      </button>
    </span>
  `).join('');

  // Attach pill remove listeners
  dom.activeFilters.querySelectorAll('button[data-pill]').forEach(btn => {
    btn.addEventListener('click', () => {
      const idx = parseInt(btn.dataset.pill, 10);
      pills[idx].action();
      state.page = 1;
      renderProducts();
    });
  });
}


/* ============================================================
   ATTACH CARD EVENT LISTENERS
   (called after each re-render)
============================================================ */
function attachCardListeners() {
  // ── Buy / Add to Cart buttons ──────────────────────────
  dom.productGrid.querySelectorAll('.mk-buy-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = parseInt(btn.dataset.id, 10);
      addToCart(id, btn);
    });
  });

  // ── Wishlist buttons ───────────────────────────────────
  dom.productGrid.querySelectorAll('.mk-wishlist-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = parseInt(btn.dataset.id, 10);
      toggleWishlist(id, btn);
    });
  });

  // ── Quick View buttons ─────────────────────────────────
  dom.productGrid.querySelectorAll('.mk-quick-view-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const id = parseInt(btn.dataset.id, 10);
      openQuickView(id);
    });
  });
}


/* ============================================================
   CART — ADD
============================================================ */
function addToCart(productId, btnEl) {
  const product = PRODUCTS.find(p => p.id === productId);
  if (!product) return;

  const alreadyInCart = state.cart.some(c => c.id === productId);

  if (alreadyInCart) {
    // If already in cart, open the cart drawer
    openCart();
    return;
  }

  // Add to state
  state.cart.push({ ...product });

  // Update button visually
  if (btnEl) {
    btnEl.classList.add('added');
    btnEl.innerHTML = '<i class="fa-solid fa-check"></i> Added';
  }

  // Update cart count badge
  updateCartCount();

  // Re-render cart drawer items
  renderCartItems();

  // Toast notification
  showToast(
    'Added to Cart',
    `${product.title} → ${formatPrice(product.price)}`,
    'cart'
  );
}


/* ============================================================
   CART — REMOVE
============================================================ */
function removeFromCart(productId) {
  state.cart = state.cart.filter(c => c.id !== productId);
  updateCartCount();
  renderCartItems();

  // Re-render products to update buy buttons
  renderProducts();
}


/* ============================================================
   CART — COUNT BADGE
============================================================ */
function updateCartCount() {
  const count = state.cart.length;
  dom.cartCount.textContent = count;

  // Bump animation
  dom.cartCount.classList.remove('bump');
  void dom.cartCount.offsetWidth; // reflow
  dom.cartCount.classList.add('bump');
  setTimeout(() => dom.cartCount.classList.remove('bump'), 400);
}


/* ============================================================
   CART — RENDER ITEMS + TOTALS
============================================================ */
function renderCartItems() {
  const empty = state.cart.length === 0;

  dom.cartEmpty.style.display  = empty ? 'flex'  : 'none';
  dom.cartItems.style.display  = empty ? 'none'  : 'flex';
  dom.cartFooter.style.display = empty ? 'none'  : 'block';

  if (empty) return;

  // Items HTML
  dom.cartItems.innerHTML = state.cart.map(item => `
    <li class="mk-cart-item" data-id="${item.id}">
      <div class="mk-cart-item-img">
        ${item.image
          ? `<img src="${item.image}" alt="${item.title}" />`
          : `<i class="${item.icon}"></i>`
        }
      </div>
      <div class="mk-cart-item-info">
        <p class="mk-cart-item-title">${item.title}</p>
        <p class="mk-cart-item-price">${formatPrice(item.price)}</p>
      </div>
      <button
        class="mk-cart-item-remove"
        data-id="${item.id}"
        aria-label="Remove ${item.title} from cart"
        title="Remove"
      >
        <i class="fa-solid fa-trash-can"></i>
      </button>
    </li>
  `).join('');

  // Remove listeners
  dom.cartItems.querySelectorAll('.mk-cart-item-remove').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = parseInt(btn.dataset.id, 10);
      removeFromCart(id);
    });
  });

  // Totals
  const subtotal = state.cart.reduce((sum, item) => sum + item.price, 0);
  const gst      = Math.round(subtotal * GST_RATE);
  const total    = subtotal + gst;

  dom.cartSubtotal.textContent = formatPrice(subtotal);
  dom.cartGst.textContent      = formatPrice(gst);
  dom.cartTotal.textContent    = formatPrice(total);
}


/* ============================================================
   CART — OPEN / CLOSE DRAWER
============================================================ */
function openCart() {
  dom.cartDrawer.classList.add('open');
  dom.cartOverlay.classList.add('open');
  dom.cartDrawer.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
}

function closeCart() {
  dom.cartDrawer.classList.remove('open');
  dom.cartOverlay.classList.remove('open');
  dom.cartDrawer.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}


/* ============================================================
   WISHLIST — TOGGLE
============================================================ */
function toggleWishlist(productId, btnEl) {
  const product  = PRODUCTS.find(p => p.id === productId);
  if (!product) return;

  const isAdding = !state.wishlist.has(productId);

  if (isAdding) {
    state.wishlist.add(productId);
    showToast('Wishlist', `${product.title} saved to wishlist!`, 'heart');
  } else {
    state.wishlist.delete(productId);
    showToast('Wishlist', `${product.title} removed from wishlist.`, 'info');
  }

  // Update this button immediately without full re-render
  if (btnEl) {
    btnEl.classList.toggle('active', isAdding);
    btnEl.innerHTML = `<i class="${isAdding ? 'fa-solid' : 'fa-regular'} fa-heart"></i>`;
    btnEl.setAttribute('aria-label', isAdding ? 'Remove from wishlist' : 'Add to wishlist');

    // Spring animation
    btnEl.animate(
      [
        { transform: 'scale(1)' },
        { transform: 'scale(1.5)' },
        { transform: 'scale(1)' },
      ],
      { duration: 400, easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)' }
    );
  }
}


/* ============================================================
   QUICK VIEW MODAL
============================================================ */
function openQuickView(productId) {
  const p = PRODUCTS.find(prod => prod.id === productId);
  if (!p) return;

  const inCart     = state.cart.some(c => c.id === p.id);
  const inWishlist = state.wishlist.has(p.id);

  const discountPct = p.originalPrice && p.price > 0
    ? Math.round((1 - p.price / p.originalPrice) * 100)
    : 0;

  const imgPaneContent = p.image
    ? `<img src="${p.image}" alt="${p.title}" />`
    : `<i class="${p.icon}"></i>`;

  dom.modalInner.innerHTML = `
    <!-- Image Pane -->
    <div class="mk-modal-img-pane">
      ${imgPaneContent}
    </div>

    <!-- Info Pane -->
    <div class="mk-modal-info">

      <span class="mk-modal-cat">${CATEGORY_LABELS[p.category] || capFirst(p.category)}</span>

      <h2 class="mk-modal-title" id="modalTitle">${p.title}</h2>

      <div class="mk-modal-rating">
        <span class="mk-stars">${renderStars(p.rating)}</span>
        <span style="font-size:.84rem;color:var(--muted);">
          ${p.rating}.0 &nbsp;·&nbsp; ${p.reviews.toLocaleString()} reviews
          &nbsp;·&nbsp;
          <i class="fa-solid fa-download" style="color:var(--orange);font-size:.75rem;"></i>
          ${p.downloads.toLocaleString()} downloads
        </span>
      </div>

      <p class="mk-modal-desc">${p.desc}</p>

      <!-- Meta grid -->
      <div class="mk-modal-meta">
        <div class="mk-meta-item">
          <label>Category</label>
          <span>${CATEGORY_LABELS[p.category] || capFirst(p.category)}</span>
        </div>
        <div class="mk-meta-item">
          <label>File Formats</label>
          <span>${p.formats.map(f => f.toUpperCase()).join(', ')}</span>
        </div>
        <div class="mk-meta-item">
          <label>Software</label>
          <span>${p.software.map(s => SOFTWARE_LABELS[s] || capFirst(s)).join(', ')}</span>
        </div>
        <div class="mk-meta-item">
          <label>Date Added</label>
          <span>${new Date(p.dateAdded).toLocaleDateString('en-IN', { day:'2-digit', month:'short', year:'numeric' })}</span>
        </div>
        ${discountPct > 0 ? `
        <div class="mk-meta-item">
          <label>Discount</label>
          <span style="color:var(--yellow);font-weight:700;">${discountPct}% OFF</span>
        </div>` : ''}
        <div class="mk-meta-item">
          <label>Texture Resolution</label>
          <span>Up to 4K</span>
        </div>
      </div>

      <!-- Price + Actions -->
      <div class="mk-modal-price-row">

        <div>
          ${p.price === 0
            ? `<span class="mk-price-free" style="font-size:2rem;">Free</span>`
            : `<span class="mk-modal-price">${formatPrice(p.price)}</span>
               ${p.originalPrice
                 ? `<span style="font-size:.85rem;color:var(--muted);text-decoration:line-through;margin-left:8px;">${formatPrice(p.originalPrice)}</span>`
                 : ''
               }`
          }
        </div>

        <div class="mk-modal-actions">

          <!-- Wishlist -->
          <button
            class="btn-mk-outline mk-modal-wish-btn ${inWishlist ? 'active' : ''}"
            data-id="${p.id}"
            aria-label="Add to wishlist"
            style="${inWishlist ? 'background:rgba(255,45,45,.12);border-color:var(--red);color:var(--red);' : ''}"
          >
            <i class="${inWishlist ? 'fa-solid' : 'fa-regular'} fa-heart"></i>
          </button>

          <!-- Buy / Cart -->
          <button
            class="${inCart ? 'btn-mk-primary' : 'btn-mk-primary'} mk-modal-cart-btn ${inCart ? 'added' : ''}"
            data-id="${p.id}"
            style="${inCart ? 'background:linear-gradient(135deg,#4ade80,#16a34a);' : ''}"
          >
            <i class="fa-solid ${inCart ? 'fa-check' : 'fa-cart-plus'}"></i>
            ${inCart ? 'In Cart — View' : (p.price === 0 ? 'Get Free' : 'Add to Cart')}
          </button>

        </div>
      </div>
    </div>
  `;

  // Open modal
  dom.modalOverlay.classList.add('open');
  dom.modalOverlay.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';

  // Modal cart button
  dom.modalInner.querySelector('.mk-modal-cart-btn')?.addEventListener('click', () => {
    const id = parseInt(dom.modalInner.querySelector('.mk-modal-cart-btn').dataset.id, 10);
    if (state.cart.some(c => c.id === id)) {
      closeModal();
      openCart();
    } else {
      addToCart(id);
      // Update button
      const btn = dom.modalInner.querySelector('.mk-modal-cart-btn');
      if (btn) {
        btn.style.background = 'linear-gradient(135deg,#4ade80,#16a34a)';
        btn.innerHTML = '<i class="fa-solid fa-check"></i> In Cart — View';
        btn.classList.add('added');
      }
    }
  });

  // Modal wishlist button
  dom.modalInner.querySelector('.mk-modal-wish-btn')?.addEventListener('click', (e) => {
    const wishBtn = e.currentTarget;
    const id      = parseInt(wishBtn.dataset.id, 10);
    toggleWishlist(id, null);
    const nowIn = state.wishlist.has(id);
    wishBtn.innerHTML = `<i class="${nowIn ? 'fa-solid' : 'fa-regular'} fa-heart"></i>`;
    wishBtn.style.cssText = nowIn
      ? 'background:rgba(255,45,45,.12);border-color:var(--red);color:var(--red);'
      : '';
  });
}

function closeModal() {
  dom.modalOverlay.classList.remove('open');
  dom.modalOverlay.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}


/* ============================================================
   TOAST NOTIFICATIONS
============================================================ */
const TOAST_ICONS = {
  cart:  { icon: 'fa-cart-shopping', cls: '' },
  heart: { icon: 'fa-heart',         cls: '' },
  info:  { icon: 'fa-circle-info',   cls: '' },
  error: { icon: 'fa-circle-xmark',  cls: 'error' },
  ok:    { icon: 'fa-circle-check',  cls: 'success' },
};

function showToast(title, message, type = 'info') {
  const cfg   = TOAST_ICONS[type] || TOAST_ICONS.info;
  const toast = document.createElement('div');
  toast.className = 'mk-toast';

  toast.innerHTML = `
    <div class="mk-toast-icon ${cfg.cls}">
      <i class="fa-solid ${cfg.icon}"></i>
    </div>
    <div class="mk-toast-body">
      <p class="mk-toast-title">${title}</p>
      <p class="mk-toast-msg">${message}</p>
    </div>
  `;

  dom.toastWrap.appendChild(toast);

  // Auto-remove after 3.5s
  setTimeout(() => {
    toast.classList.add('removing');
    toast.addEventListener('animationend', () => toast.remove(), { once: true });
  }, 3500);
}


/* ============================================================
   DISCORD WEBHOOK — Send purchase intent embed
   Called when user clicks "Proceed to Checkout" in cart.
   Sends a rich embed to your Discord channel.
============================================================ */
async function sendDiscordPurchaseIntent() {
  if (!DISCORD_WEBHOOK_URL || DISCORD_WEBHOOK_URL.includes('YOUR_WEBHOOK')) {
    console.warn('Creviz Marketplace: Discord webhook URL not configured.');
    showToast('Checkout', 'Redirecting to payment…', 'ok');
    return;
  }

  const subtotal = state.cart.reduce((s, i) => s + i.price, 0);
  const gst      = Math.round(subtotal * GST_RATE);
  const total    = subtotal + gst;

  const itemLines = state.cart.map(item =>
    `• **${item.title}** — ${formatPrice(item.price)}`
  ).join('\n');

  const now = new Date();
  const timestamp = now.toISOString();

  // Build Discord embed payload
  const payload = {
    username: 'Creviz Marketplace',
    avatar_url: 'https://cdn.discordapp.com/embed/avatars/0.png',
    embeds: [
      {
        title: '🛒 New Marketplace Purchase Intent',
        description: `A customer has initiated checkout on **Creviz Marketplace**.\n\n${itemLines}`,
        color: 0xff6b1a,   // orange
        fields: [
          {
            name: '📦 Items in Cart',
            value: `${state.cart.length} asset${state.cart.length !== 1 ? 's' : ''}`,
            inline: true,
          },
          {
            name: '💰 Subtotal',
            value: formatPrice(subtotal),
            inline: true,
          },
          {
            name: '🏛️ GST (18%)',
            value: formatPrice(gst),
            inline: true,
          },
          {
            name: '✅ Total Payable',
            value: `**${formatPrice(total)}**`,
            inline: true,
          },
          {
            name: '📁 Asset Titles',
            value: state.cart.map(i => i.title).join(', '),
            inline: false,
          },
        ],
        footer: {
          text: 'Creviz Marketplace · Checkout initiated',
        },
        timestamp,
        thumbnail: {
          url: 'https://img.icons8.com/fluency/48/rupee-exchange.png',
        },
      },
    ],
  };

  try {
    const res = await fetch(DISCORD_WEBHOOK_URL, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });

    if (!res.ok) throw new Error(`Discord webhook responded with ${res.status}`);

    showToast('Checkout', 'Order received! We\'ll contact you shortly.', 'ok');

  } catch (err) {
    console.error('Discord webhook error:', err);
    showToast('Checkout', 'Proceeding — please check your email.', 'info');
  }
}


/* ============================================================
   FILTER SIDEBAR — EVENT LISTENERS
============================================================ */
function initFilters() {

  // ── Category checkboxes ────────────────────────────────
  dom.mkSidebar.querySelectorAll('input[data-filter-type="category"]').forEach(cb => {
    cb.addEventListener('change', () => {
      if (cb.value === 'all') {
        // "All" selected — clear other category checks
        state.categories = [];
        dom.mkSidebar.querySelectorAll('input[data-filter-type="category"]').forEach(c => {
          if (c.value !== 'all') c.checked = false;
        });
      } else {
        // Uncheck "All"
        const allCb = dom.mkSidebar.querySelector('input[data-filter-type="category"][value="all"]');
        if (allCb) allCb.checked = false;

        if (cb.checked) {
          state.categories.push(cb.value);
        } else {
          state.categories = state.categories.filter(c => c !== cb.value);
        }

        // If nothing selected, re-check "All"
        if (state.categories.length === 0 && allCb) {
          allCb.checked = true;
        }
      }
      state.page = 1;
      renderProducts();
    });
  });

  // ── Software checkboxes ────────────────────────────────
  dom.mkSidebar.querySelectorAll('input[data-filter-type="software"]').forEach(cb => {
    cb.addEventListener('change', () => {
      if (cb.checked) {
        state.software.push(cb.value);
      } else {
        state.software = state.software.filter(s => s !== cb.value);
      }
      state.page = 1;
      renderProducts();
    });
  });

  // ── Format checkboxes ──────────────────────────────────
  dom.mkSidebar.querySelectorAll('input[data-filter-type="format"]').forEach(cb => {
    cb.addEventListener('change', () => {
      if (cb.checked) {
        state.formats.push(cb.value);
      } else {
        state.formats = state.formats.filter(f => f !== cb.value);
      }
      state.page = 1;
      renderProducts();
    });
  });

  // ── Price range slider ────────────────────────────────
  dom.priceRange.addEventListener('input', () => {
    const val = parseInt(dom.priceRange.value, 10);
    state.maxPrice  = val >= parseInt(dom.priceRange.max, 10) ? Infinity : val;
    dom.priceRangeVal.textContent =
      val >= parseInt(dom.priceRange.max, 10)
        ? `₹${parseInt(dom.priceRange.max, 10).toLocaleString('en-IN')}+`
        : `₹${val.toLocaleString('en-IN')}`;
    state.page = 1;
    renderProducts();
  });

  // ── Price max input ────────────────────────────────────
  dom.priceMax?.addEventListener('change', () => {
    const val = parseInt(dom.priceMax.value, 10);
    if (!isNaN(val) && val > 0) {
      state.maxPrice = val;
      dom.priceRange.value = Math.min(val, dom.priceRange.max);
      dom.priceRangeVal.textContent = `₹${val.toLocaleString('en-IN')}`;
      state.page = 1;
      renderProducts();
    }
  });

  // ── Star filter buttons ────────────────────────────────
  dom.starFilter.querySelectorAll('.mk-star-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      dom.starFilter.querySelectorAll('.mk-star-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.minRating = parseInt(btn.dataset.stars, 10);
      state.page = 1;
      renderProducts();
    });
  });

  // ── Clear all filters ──────────────────────────────────
  dom.clearFilters.addEventListener('click', () => {
    state.search     = '';
    state.categories = [];
    state.software   = [];
    state.formats    = [];
    state.minRating  = 0;
    state.maxPrice   = Infinity;
    state.page       = 1;

    dom.searchInput.value   = '';
    dom.priceRange.value    = dom.priceRange.max;
    dom.priceRangeVal.textContent = `₹${parseInt(dom.priceRange.max, 10).toLocaleString('en-IN')}+`;

    dom.mkSidebar.querySelectorAll('.mk-checkbox').forEach(cb => {
      cb.checked = cb.value === 'all';
    });

    dom.starFilter.querySelectorAll('.mk-star-btn').forEach(b => b.classList.remove('active'));
    dom.starFilter.querySelector('[data-stars="0"]')?.classList.add('active');

    renderProducts();
    showToast('Filters Cleared', 'Showing all assets.', 'info');
  });
}


/* ============================================================
   TOOLBAR — SORT, VIEW TOGGLE, SEARCH
============================================================ */
function initToolbar() {

  // ── Sort ───────────────────────────────────────────────
  dom.sortSelect.addEventListener('change', () => {
    state.sort = dom.sortSelect.value;
    state.page = 1;
    renderProducts();
  });

  // ── Grid view ──────────────────────────────────────────
  dom.gridViewBtn.addEventListener('click', () => {
    state.view = 'grid';
    dom.gridViewBtn.classList.add('active');
    dom.listViewBtn.classList.remove('active');
    dom.productGrid.classList.remove('list-view');
    renderProducts();
  });

  // ── List view ──────────────────────────────────────────
  dom.listViewBtn.addEventListener('click', () => {
    state.view = 'list';
    dom.listViewBtn.classList.add('active');
    dom.gridViewBtn.classList.remove('active');
    renderProducts();
  });

  // ── Live search (debounced 320ms) ──────────────────────
  dom.searchInput.addEventListener(
    'input',
    debounce(() => {
      state.search = dom.searchInput.value;
      state.page   = 1;
      renderProducts();
    }, 320)
  );

  // ── Search form submit ─────────────────────────────────
  document.getElementById('searchForm')?.addEventListener('submit', (e) => {
    e.preventDefault();
    state.search = dom.searchInput.value;
    state.page   = 1;
    renderProducts();
  });
}


/* ============================================================
   CART + MODAL — EVENT LISTENERS
============================================================ */
function initCartAndModal() {

  // Open cart drawer
  dom.cartBtn.addEventListener('click', () => {
    renderCartItems();
    openCart();
  });

  // Close cart drawer via X button
  dom.cartClose.addEventListener('click', closeCart);

  // Close cart by clicking overlay
  dom.cartOverlay.addEventListener('click', closeCart);

  // Checkout button — sends Discord embed then shows confirmation
  dom.checkoutBtn.addEventListener('click', async () => {
    if (state.cart.length === 0) return;
    dom.checkoutBtn.disabled     = true;
    dom.checkoutBtn.innerHTML    = '<i class="fa-solid fa-spinner fa-spin"></i> Processing…';

    await sendDiscordPurchaseIntent();

    dom.checkoutBtn.disabled     = false;
    dom.checkoutBtn.innerHTML    = '<i class="fa-solid fa-lock"></i> Proceed to Checkout';
  });

  // Close modal via X button
  dom.modalClose.addEventListener('click', closeModal);

  // Close modal by clicking overlay (outside modal box)
  dom.modalOverlay.addEventListener('click', (e) => {
    if (e.target === dom.modalOverlay) closeModal();
  });

  // Keyboard: Escape to close cart / modal / sidebar
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (dom.modalOverlay.classList.contains('open')) closeModal();
      else if (dom.cartDrawer.classList.contains('open')) closeCart();
      else if (dom.mkSidebar.classList.contains('open')) closeMobileSidebar();
    }
  });
}


/* ============================================================
   MOBILE SIDEBAR
============================================================ */
let sidebarOverlay = null;

function openMobileSidebar() {
  dom.mkSidebar.classList.add('open');
  document.body.style.overflow = 'hidden';

  // Create overlay if not exists
  if (!sidebarOverlay) {
    sidebarOverlay = document.createElement('div');
    sidebarOverlay.className = 'mk-cart-overlay';
    sidebarOverlay.style.zIndex = '1040';
    document.body.appendChild(sidebarOverlay);
  }

  setTimeout(() => {
    sidebarOverlay.classList.add('open');
    sidebarOverlay.addEventListener('click', closeMobileSidebar, { once: true });
  }, 10);
}

function closeMobileSidebar() {
  dom.mkSidebar.classList.remove('open');
  document.body.style.overflow = '';
  if (sidebarOverlay) {
    sidebarOverlay.classList.remove('open');
  }
}

function initMobileSidebar() {
  dom.filterToggle.addEventListener('click', () => {
    if (dom.mkSidebar.classList.contains('open')) {
      closeMobileSidebar();
    } else {
      openMobileSidebar();
    }
  });
}


/* ============================================================
   NAVBAR — Scroll glass effect
============================================================ */
function initNavbar() {
  if (!dom.mkNavbar) return;

  const onScroll = () => {
    dom.mkNavbar.style.boxShadow = window.scrollY > 20
      ? '0 4px 30px rgba(0,0,0,.5)'
      : '';
  };

  window.addEventListener('scroll', onScroll, { passive: true });
}


/* ============================================================
   INIT — Bootstrap everything
============================================================ */
function init() {
  // Initial product render
  renderProducts();

  // Wire up all feature modules
  initFilters();
  initToolbar();
  initCartAndModal();
  initMobileSidebar();
  initNavbar();

  // Initial cart render (for page refresh with state)
  renderCartItems();
  updateCartCount();

  // Console branding
  console.info(
    '%c 🛒 Creviz Marketplace v1.0 ',
    'background:linear-gradient(135deg,#ff2d2d,#ff6b1a,#ffc93c);' +
    'color:#fff;padding:7px 18px;border-radius:20px;' +
    'font-weight:800;font-size:13px;'
  );
}

// Boot on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}