"""
Creviz Studio — Desktop Admin Panel
=====================================
Full-featured GUI built with Tkinter + ttk.
Manages portfolio projects and marketplace assets,
generates patched index.html and marketplace.js.

Requirements: Python 3.9+  (stdlib only — no pip installs needed)
Run:  python creviz_admin.py
"""

import json
import os
import re
import sys
import tkinter as tk
import webbrowser
from copy import deepcopy
from datetime import date
from tkinter import filedialog, messagebox, ttk

# ──────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────────────────────────────────────
APP_TITLE   = "Creviz Studio — Admin Panel"
DATA_FILE   = "creviz_data.json"
WIN_W, WIN_H = 1280, 780

FIRE_ORANGE = "#ff6b1a"
FIRE_RED    = "#ff2d2d"
FIRE_YELLOW = "#ffc93c"
BG_DARK     = "#0c0a09"
BG_MID      = "#181210"
BG_CARD     = "#1f1612"
BG_INPUT    = "#242018"
TEXT_MAIN   = "#f0ece8"
TEXT_MUTED  = "#9e9189"
GREEN       = "#4ade80"
BLUE        = "#60a5fa"
RED_ERR     = "#ff4d4d"
BORDER      = "#2a2420"

CAT_LABELS_PROJ = {
    "environment": "Environment",
    "character":   "Character",
    "prop":        "Props & Assets",
}
CAT_LABELS_MKT = {
    "character":   "Characters",
    "environment": "Environments",
    "prop":        "Props & Weapons",
    "texture":     "Texture Packs",
    "vehicle":     "Vehicles",
}
GRADIENT_OPTIONS = [
    "env-gradient",
    "char-gradient",
    "prop-gradient",
]

# ──────────────────────────────────────────────────────────────────────────────
# DEFAULT DATA
# ──────────────────────────────────────────────────────────────────────────────
DEFAULT_PROJECTS = [
    {"id":1,"title":"Ember Wastes",        "category":"environment","desc":"Post-apocalyptic volcanic landscape rendered in Cycles. Hand-sculpted rock formations, volumetric smoke and god rays.",         "tools":["Blender","Substance"],"icon":"fa-solid fa-mountain-sun",   "gradient":"env-gradient", "image":None},
    {"id":2,"title":"Iron Veil Warrior",   "category":"character",  "desc":"Battle-hardened female knight with intricate plate armour, sculpted at 40M polys in ZBrush and retopologised for real-time.", "tools":["ZBrush","Substance"],  "icon":"fa-solid fa-person",         "gradient":"char-gradient","image":None},
    {"id":3,"title":"Neon Alley",          "category":"environment","desc":"Rain-soaked cyberpunk back-alley with neon reflections, wet concrete, holographic signage and fog in EEVEE.",                 "tools":["Blender","PBR"],       "icon":"fa-solid fa-city",           "gradient":"env-gradient", "image":None},
    {"id":4,"title":"Void Sorcerer",       "category":"character",  "desc":"Stylised dark-fantasy spellcaster with cloth simulation, particle-based robe fabric and emissive rune tattoos.",              "tools":["ZBrush","Blender"],    "icon":"fa-solid fa-hat-wizard",     "gradient":"char-gradient","image":None},
    {"id":5,"title":"Ancient Temple Grove","category":"environment","desc":"Overgrown jungle temple with moss, vines, water caustics and dynamic lighting via Blender Geometry Nodes.",                   "tools":["Blender","Substance"], "icon":"fa-solid fa-torii-gate",     "gradient":"env-gradient", "image":None},
    {"id":6,"title":"Relic Weapon Pack",   "category":"prop",       "desc":"Pack of 6 fantasy melee weapons with full PBR texture sets baked from high-poly ZBrush sculpts, game-engine ready.",         "tools":["ZBrush","Substance"],  "icon":"fa-solid fa-khanda",         "gradient":"prop-gradient","image":None},
    {"id":7,"title":"Kira — Sci-Fi Scout", "category":"character",  "desc":"Full-body sci-fi character with hard-surface exo-suit, visor glass shader, mechanical arms and rigged for animation.",        "tools":["ZBrush","Blender"],    "icon":"fa-solid fa-user-astronaut", "gradient":"char-gradient","image":None},
    {"id":8,"title":"Abandoned Diner",     "category":"prop",       "desc":"Hero prop set — retro diner booth, cracked floor tiles, broken neon sign and dusty counter with full 4K texture maps.",       "tools":["Blender","Substance"], "icon":"fa-solid fa-store",          "gradient":"prop-gradient","image":None},
    {"id":9,"title":"Arctic Research Base","category":"environment","desc":"Isolated sci-fi outpost in a blizzard with sub-surface ice scattering, wind-driven particle snow and moody interior light.",  "tools":["Blender","PBR"],       "icon":"fa-solid fa-snowflake",      "gradient":"env-gradient", "image":None},
]

DEFAULT_MARKET = [
    {"id":1, "title":"Iron Veil Warrior",         "category":"character",  "desc":"Battle-hardened female knight sculpted at 40M polys. Fully rigged, game-ready FBX with 4K PBR texture set.",             "price":1499,"originalPrice":1999,"rating":5,"reviews":42, "software":["zbrush","blender","substance"],         "formats":["fbx","blend","obj"],  "image":None,"icon":"fa-solid fa-person",         "badges":["hot"],       "downloads":318, "featured":True, "dateAdded":"2026-01-15"},
    {"id":2, "title":"Ember Wastes Environment",  "category":"environment","desc":"Post-apocalyptic volcanic landscape. Full .blend file, volumetric smoke, god-ray lighting rig.",                         "price":1299,"originalPrice":None,"rating":5,"reviews":28, "software":["blender","substance"],                  "formats":["blend","fbx"],        "image":None,"icon":"fa-solid fa-mountain-sun",  "badges":["new"],       "downloads":201, "featured":True, "dateAdded":"2026-02-01"},
    {"id":3, "title":"Relic Weapon Pack",         "category":"prop",       "desc":"Six fantasy melee weapons baked from high-poly ZBrush sculpts. 4K albedo, normal, roughness and metallic maps.",         "price":799, "originalPrice":1199,"rating":4,"reviews":64, "software":["zbrush","substance"],                   "formats":["fbx","obj","usdz"],   "image":None,"icon":"fa-solid fa-khanda",         "badges":["sale"],      "downloads":487, "featured":True, "dateAdded":"2025-11-20"},
    {"id":4, "title":"Neon Alley Scene",          "category":"environment","desc":"Rain-soaked cyberpunk back-alley. Full EEVEE scene with wet-surface shaders, neon emission and volumetric fog.",          "price":1099,"originalPrice":None,"rating":5,"reviews":19, "software":["blender"],                              "formats":["blend"],              "image":None,"icon":"fa-solid fa-city",           "badges":["new"],       "downloads":145, "featured":False,"dateAdded":"2026-01-28"},
    {"id":5, "title":"Void Sorcerer Character",   "category":"character",  "desc":"Stylised dark-fantasy spellcaster with cloth sim, particle robe and emissive rune tattoos. Rigged for Unreal Engine 5.", "price":1799,"originalPrice":2299,"rating":5,"reviews":37, "software":["zbrush","blender","unreal"],             "formats":["fbx","blend"],        "image":None,"icon":"fa-solid fa-hat-wizard",     "badges":["hot","sale"],"downloads":276, "featured":True, "dateAdded":"2025-12-10"},
    {"id":6, "title":"Mossy Rock PBR Pack",       "category":"texture",    "desc":"12 seamless mossy rock PBR materials at 4K. Albedo, Normal, Height, Roughness and AO maps included.",                   "price":499, "originalPrice":None,"rating":4,"reviews":93, "software":["blender","substance","unreal","unity"],  "formats":["blend","usdz"],       "image":None,"icon":"fa-solid fa-layer-group",   "badges":[],            "downloads":612, "featured":False,"dateAdded":"2025-10-05"},
    {"id":7, "title":"Kira — Sci-Fi Scout",       "category":"character",  "desc":"Hard-surface exo-suit with visor glass, mechanical arm rigs and multiple LODs. Full 4K PBR.",                           "price":2199,"originalPrice":2699,"rating":5,"reviews":55, "software":["zbrush","blender","substance","unreal","unity"],"formats":["fbx","blend","obj"],"image":None,"icon":"fa-solid fa-user-astronaut","badges":["hot"],      "downloads":344, "featured":True, "dateAdded":"2026-01-05"},
    {"id":8, "title":"Ancient Temple Grove",      "category":"environment","desc":"Overgrown jungle temple with Geometry Nodes scatter for vines, moss and foliage. Water caustics shader.",                "price":1599,"originalPrice":None,"rating":5,"reviews":22, "software":["blender","substance"],                  "formats":["blend"],              "image":None,"icon":"fa-solid fa-torii-gate",     "badges":["new"],       "downloads":178, "featured":False,"dateAdded":"2026-02-10"},
    {"id":9, "title":"Abandoned Diner Props",     "category":"prop",       "desc":"Retro diner hero prop set. Cracked tiles, broken neon sign and dusty counter. Full 4K texture maps.",                   "price":699, "originalPrice":None,"rating":4,"reviews":41, "software":["blender","substance"],                  "formats":["fbx","obj"],          "image":None,"icon":"fa-solid fa-store",          "badges":[],            "downloads":289, "featured":False,"dateAdded":"2025-09-18"},
    {"id":10,"title":"Arctic Research Base",      "category":"environment","desc":"Sci-fi blizzard outpost with sub-surface ice scattering and wind-driven particle snow.",                                 "price":1399,"originalPrice":1799,"rating":4,"reviews":17, "software":["blender"],                              "formats":["blend","fbx"],        "image":None,"icon":"fa-solid fa-snowflake",      "badges":["sale"],      "downloads":132, "featured":False,"dateAdded":"2025-08-22"},
    {"id":11,"title":"Wet Concrete Texture Pack", "category":"texture",    "desc":"8 wet/dry concrete PBR materials. Tiling albedo, normal, height, metallic and roughness at 4K.",                       "price":0,   "originalPrice":None,"rating":5,"reviews":204,"software":["blender","unreal","unity"],              "formats":["blend","usdz","obj"], "image":None,"icon":"fa-solid fa-layer-group",   "badges":["free"],      "downloads":1841,"featured":True, "dateAdded":"2025-07-01"},
    {"id":12,"title":"Fantasy Ground Vehicle",    "category":"vehicle",    "desc":"Ornate steampunk carriage with animated wheel rig, aged leather shader and wood-grain PBR materials.",                  "price":1899,"originalPrice":2399,"rating":4,"reviews":14, "software":["blender","substance","unreal"],          "formats":["fbx","blend"],        "image":None,"icon":"fa-solid fa-car",            "badges":["sale"],      "downloads":98,  "featured":False,"dateAdded":"2026-02-18"},
]


# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def esc_js(s: str) -> str:
    return (s or "").replace("\\", "\\\\").replace("'", "\\'")


def cat_label(cat: str, mkt=False) -> str:
    lbl = CAT_LABELS_MKT if mkt else CAT_LABELS_PROJ
    return lbl.get(cat, cat.capitalize() if cat else "Other")


def js_val(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return json.dumps(v)
    return f"'{esc_js(str(v))}'"


# ──────────────────────────────────────────────────────────────────────────────
# DATA STORE
# ──────────────────────────────────────────────────────────────────────────────
class DataStore:
    def __init__(self):
        self.projects: list[dict] = []
        self.market:   list[dict] = []
        self.load()

    def load(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.projects = data.get("projects", deepcopy(DEFAULT_PROJECTS))
                self.market   = data.get("market",   deepcopy(DEFAULT_MARKET))
                return
            except Exception:
                pass
        self.projects = deepcopy(DEFAULT_PROJECTS)
        self.market   = deepcopy(DEFAULT_MARKET)

    def save(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"projects": self.projects, "market": self.market}, f, indent=2)

    def export_backup(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {"version":"1.0","exportedAt":str(date.today()),
                 "projects":self.projects,"market":self.market},
                f, indent=2
            )

    def import_backup(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "projects" in data:
            self.projects = data["projects"]
        if "market" in data:
            self.market = data["market"]
        self.save()

    def reset(self):
        self.projects = deepcopy(DEFAULT_PROJECTS)
        self.market   = deepcopy(DEFAULT_MARKET)
        self.save()

    # ── Code generation ──────────────────────────────────────────
    def portfolio_html(self) -> str:
        cards = []
        for p in self.projects:
            img_html = (
                f'<img src="{p["image"]}" alt="{p["title"]}" loading="lazy" />'
                if p.get("image")
                else f'<div class="img-placeholder"><i class="{p["icon"]}"></i></div>'
            )
            tools_html = "\n".join(
                f'          <span class="project-tool">{t}</span>'
                for t in (p.get("tools") or [])
            )
            cards.append(f"""      <div class="project-card reveal" data-category="{p['category']}">
        <div class="project-img {p.get('gradient','env-gradient')}">
          {img_html}
          <div class="project-overlay">
            <div class="project-links">
              <button class="project-link-btn" aria-label="View {p['title']}">
                <i class="fa-solid fa-eye"></i>
              </button>
            </div>
          </div>
        </div>
        <div class="project-info">
          <span class="project-cat">{cat_label(p['category'])}</span>
          <h3 class="project-title">{p['title']}</h3>
          <p class="project-desc">{p['desc']}</p>
          <div class="project-tools">
{tools_html}
          </div>
        </div>
      </div>""")
        return "\n\n".join(cards)

    def products_js(self) -> str:
        items = []
        for i, m in enumerate(self.market):
            comma = "," if i < len(self.market) - 1 else ""
            items.append(f"""  {{
    id:            {m['id']},
    title:         '{esc_js(m['title'])}',
    category:      '{m['category']}',
    desc:          '{esc_js(m['desc'])}',
    price:         {m['price']},
    originalPrice: {js_val(m.get('originalPrice'))},
    rating:        {m['rating']},
    reviews:       {m['reviews']},
    software:      {json.dumps(m.get('software',[]))},
    formats:       {json.dumps(m.get('formats',[]))},
    image:         {js_val(m.get('image'))},
    icon:          '{esc_js(m['icon'])}',
    badges:        {json.dumps(m.get('badges',[]))},
    downloads:     {m['downloads']},
    featured:      {'true' if m['featured'] else 'false'},
    dateAdded:     '{m['dateAdded']}',
  }}{comma}""")
        return "const PRODUCTS = [\n" + "\n".join(items) + "\n];"

    # ── File patchers ─────────────────────────────────────────────
    def patch_index(self, original: str) -> tuple[str, str]:
        """Returns (patched_html, status_message)."""
        cards = self.portfolio_html()
        replacement = f"\\1\n{cards}\n      \\3"

        by_id    = re.compile(
            r'(<div[^>]*\bid=["\']portfolioGrid["\'][^>]*>)([\s\S]*?)'
            r'(<\/div>(?=\s*(?:<!--|<\/section>|<\/main>|<footer|<div|<section|$)))',
            re.IGNORECASE,
        )
        by_class = re.compile(
            r'(<div[^>]*\bclass=["\'][^"\']*projects-grid[^"\']*["\'][^>]*>)([\s\S]*?)'
            r'(<\/div>(?=\s*(?:<!--|<\/section>|<\/main>|<footer|<div|<section|$)))',
            re.IGNORECASE,
        )

        if by_id.search(original):
            patched = by_id.sub(replacement, original, count=1)
            return patched, 'Replaced by id="portfolioGrid" ✓'
        if by_class.search(original):
            patched = by_class.sub(replacement, original, count=1)
            return patched, 'Replaced by class="projects-grid" ✓'
        # fallback
        patched = original.replace(
            "</main>",
            f"<!-- CREVIZ ADMIN: paste into your projects-grid div -->\n{cards}\n</main>",
            1,
        )
        return patched, "⚠ Could not locate projects-grid — code inserted before </main>, review manually."

    def patch_marketplace_js(self, original: str) -> tuple[str, str]:
        """Returns (patched_js, status_message)."""
        products = self.products_js()
        pattern  = re.compile(r'const\s+PRODUCTS\s*=\s*\[[\s\S]*?\];')
        if pattern.search(original):
            patched = pattern.sub(products, original, count=1)
            return patched, "PRODUCTS array replaced ✓"
        patched = f"/* CREVIZ ADMIN: inserted — remove any existing duplicate below */\n{products}\n\n{original}"
        return patched, "⚠ Could not locate PRODUCTS array — prepended to file, review manually."


# ──────────────────────────────────────────────────────────────────────────────
# STYLED WIDGETS
# ──────────────────────────────────────────────────────────────────────────────
def styled_btn(parent, text, cmd, color=FIRE_ORANGE, fg="#fff",
               icon=None, width=None, small=False):
    full = f"{icon}  {text}" if icon else text
    kw   = dict(
        text=full, command=cmd, fg=fg, bg=color,
        activeforeground=fg, activebackground=color,
        relief="flat", bd=0, cursor="hand2",
        font=("Helvetica", 9 if small else 10, "bold"),
        padx=14 if small else 18, pady=5 if small else 8,
    )
    if width:
        kw["width"] = width
    btn = tk.Button(parent, **kw)
    btn.bind("<Enter>", lambda e: btn.config(bg=_lighten(color)))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn


def _lighten(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    r = min(255, r + 25)
    g = min(255, g + 20)
    b = min(255, b + 20)
    return f"#{r:02x}{g:02x}{b:02x}"


def entry_widget(parent, textvariable=None, placeholder="", width=38):
    e = tk.Entry(
        parent, textvariable=textvariable, width=width,
        bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
        relief="flat", bd=0,
        font=("Helvetica", 10),
        highlightthickness=1, highlightbackground=BORDER,
        highlightcolor=FIRE_ORANGE,
    )
    return e


def text_widget(parent, height=4, width=52):
    t = tk.Text(
        parent, height=height, width=width,
        bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
        relief="flat", bd=0,
        font=("Helvetica", 10),
        wrap="word",
        highlightthickness=1, highlightbackground=BORDER,
        highlightcolor=FIRE_ORANGE,
        spacing3=2,
    )
    return t


def combo_widget(parent, values, textvariable=None, width=28):
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Dark.TCombobox",
        fieldbackground=BG_INPUT, background=BG_INPUT,
        foreground=TEXT_MAIN, selectbackground=BG_INPUT,
        selectforeground=TEXT_MAIN, arrowcolor=FIRE_ORANGE,
        bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
    )
    cb = ttk.Combobox(
        parent, values=values, textvariable=textvariable,
        width=width, state="readonly", style="Dark.TCombobox",
        font=("Helvetica", 10),
    )
    return cb


def section_label(parent, text):
    f = tk.Frame(parent, bg=BG_DARK)
    tk.Label(f, text=text, bg=BG_DARK, fg=FIRE_ORANGE,
             font=("Helvetica", 10, "bold")).pack(side="left")
    tk.Frame(f, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, padx=(8,0), pady=6)
    return f


def scrolled_frame(parent):
    """Returns (outer_frame, inner_frame) with vertical scrollbar."""
    outer = tk.Frame(parent, bg=BG_DARK)
    canvas = tk.Canvas(outer, bg=BG_DARK, bd=0, highlightthickness=0)
    vsb = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    inner = tk.Frame(canvas, bg=BG_DARK)
    win_id = canvas.create_window((0,0), window=inner, anchor="nw")

    def _on_configure(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(win_id, width=canvas.winfo_width())

    inner.bind("<Configure>", _on_configure)
    canvas.bind("<Configure>", _on_configure)

    def _mousewheel(e):
        canvas.yview_scroll(int(-1*(e.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", _mousewheel)
    return outer, inner


# ──────────────────────────────────────────────────────────────────────────────
# PROJECT FORM DIALOG
# ──────────────────────────────────────────────────────────────────────────────
class ProjectDialog(tk.Toplevel):
    def __init__(self, parent, store: DataStore, project: dict | None = None, on_save=None):
        super().__init__(parent)
        self.store    = store
        self.project  = project
        self.on_save  = on_save
        self.result   = None

        self.title("Edit Project" if project else "Add Project")
        self.configure(bg=BG_DARK)
        self.geometry("620x600")
        self.resizable(True, True)
        self.grab_set()

        self._build()
        if project:
            self._populate()

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=BG_MID, pady=12)
        hdr.pack(fill="x")
        icon = "✏  " if self.project else "＋  "
        tk.Label(hdr, text=icon + ("Edit Project" if self.project else "Add New Project"),
                 bg=BG_MID, fg=TEXT_MAIN, font=("Helvetica",13,"bold")).pack(padx=20, side="left")

        outer, inner = scrolled_frame(self)
        outer.pack(fill="both", expand=True, padx=0, pady=0)
        pad = dict(padx=20, pady=6)

        # Title
        section_label(inner, "Project Title *").pack(fill="x", **pad)
        self.v_title = tk.StringVar()
        entry_widget(inner, self.v_title, width=55).pack(fill="x", **pad)

        # Category + Gradient row
        row = tk.Frame(inner, bg=BG_DARK)
        row.pack(fill="x", **pad)
        lf = tk.Frame(row, bg=BG_DARK)
        lf.pack(side="left", fill="x", expand=True, padx=(0,8))
        section_label(lf, "Category *").pack(fill="x")
        self.v_cat = tk.StringVar(value="environment")
        combo_widget(lf, list(CAT_LABELS_PROJ.keys()), self.v_cat, width=22).pack(fill="x", pady=4)

        rf = tk.Frame(row, bg=BG_DARK)
        rf.pack(side="left", fill="x", expand=True)
        section_label(rf, "Gradient Style").pack(fill="x")
        self.v_grad = tk.StringVar(value="env-gradient")
        combo_widget(rf, GRADIENT_OPTIONS, self.v_grad, width=22).pack(fill="x", pady=4)

        # Description
        section_label(inner, "Description *").pack(fill="x", **pad)
        self.w_desc = text_widget(inner, height=4, width=55)
        self.w_desc.pack(fill="x", **pad)

        # Icon
        section_label(inner, "Font Awesome Icon Class").pack(fill="x", **pad)
        self.v_icon = tk.StringVar(value="fa-solid fa-cube")
        entry_widget(inner, self.v_icon, width=55).pack(fill="x", **pad)

        # Image path
        section_label(inner, "Image Path / URL (optional)").pack(fill="x", **pad)
        img_row = tk.Frame(inner, bg=BG_DARK)
        img_row.pack(fill="x", **pad)
        self.v_image = tk.StringVar()
        entry_widget(img_row, self.v_image, width=44).pack(side="left", fill="x", expand=True)
        styled_btn(img_row, "Browse", self._browse_image, color=BG_CARD, small=True
                   ).pack(side="left", padx=(6,0))

        # Tools
        section_label(inner, "Tools Used (comma-separated)").pack(fill="x", **pad)
        self.v_tools = tk.StringVar()
        entry_widget(inner, self.v_tools, width=55).pack(fill="x", **pad)
        tk.Label(inner, text="e.g.  Blender, ZBrush, Substance Painter",
                 bg=BG_DARK, fg=TEXT_MUTED, font=("Helvetica",8)).pack(anchor="w", padx=20)

        # Footer
        foot = tk.Frame(self, bg=BG_MID, pady=10)
        foot.pack(fill="x", side="bottom")
        styled_btn(foot, "Cancel", self.destroy, color=BG_CARD, fg=TEXT_MUTED, small=True
                   ).pack(side="right", padx=(0,12))
        styled_btn(foot, "💾  Save Project", self._save, small=True
                   ).pack(side="right", padx=(0,8))

    def _populate(self):
        p = self.project
        self.v_title.set(p.get("title",""))
        self.v_cat.set(p.get("category","environment"))
        self.v_grad.set(p.get("gradient","env-gradient"))
        self.v_icon.set(p.get("icon","fa-solid fa-cube"))
        self.v_image.set(p.get("image") or "")
        self.v_tools.set(", ".join(p.get("tools") or []))
        self.w_desc.insert("1.0", p.get("desc",""))

    def _browse_image(self):
        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files","*.png *.jpg *.jpeg *.webp *.gif"), ("All","*.*")]
        )
        if path:
            self.v_image.set(path)

    def _save(self):
        title = self.v_title.get().strip()
        desc  = self.w_desc.get("1.0","end").strip()
        if not title:
            messagebox.showerror("Validation", "Project title is required.", parent=self)
            return
        if not desc:
            messagebox.showerror("Validation", "Description is required.", parent=self)
            return
        tools = [t.strip() for t in self.v_tools.get().split(",") if t.strip()]
        image = self.v_image.get().strip() or None

        if self.project:
            self.project.update(
                title=title, category=self.v_cat.get(), desc=desc,
                icon=self.v_icon.get().strip() or "fa-solid fa-cube",
                gradient=self.v_grad.get(), tools=tools, image=image,
            )
        else:
            new_id = max((p["id"] for p in self.store.projects), default=0) + 1
            self.store.projects.append(dict(
                id=new_id, title=title, category=self.v_cat.get(),
                desc=desc, icon=self.v_icon.get().strip() or "fa-solid fa-cube",
                gradient=self.v_grad.get(), tools=tools, image=image,
            ))

        self.store.save()
        if self.on_save:
            self.on_save()
        self.destroy()


# ──────────────────────────────────────────────────────────────────────────────
# MARKET ASSET FORM DIALOG
# ──────────────────────────────────────────────────────────────────────────────
class MarketDialog(tk.Toplevel):
    def __init__(self, parent, store: DataStore, asset: dict | None = None, on_save=None):
        super().__init__(parent)
        self.store   = store
        self.asset   = asset
        self.on_save = on_save

        self.title("Edit Asset" if asset else "Add Asset")
        self.configure(bg=BG_DARK)
        self.geometry("680x720")
        self.resizable(True, True)
        self.grab_set()

        self._build()
        if asset:
            self._populate()

    def _build(self):
        hdr = tk.Frame(self, bg=BG_MID, pady=12)
        hdr.pack(fill="x")
        icon = "✏  " if self.asset else "＋  "
        tk.Label(hdr, text=icon + ("Edit Asset" if self.asset else "Add New Asset"),
                 bg=BG_MID, fg=TEXT_MAIN, font=("Helvetica",13,"bold")).pack(padx=20, side="left")

        outer, inner = scrolled_frame(self)
        outer.pack(fill="both", expand=True)
        pad = dict(padx=20, pady=5)

        # Title + Category
        row = tk.Frame(inner, bg=BG_DARK)
        row.pack(fill="x", **pad)
        lf = tk.Frame(row, bg=BG_DARK)
        lf.pack(side="left", fill="x", expand=True, padx=(0,8))
        section_label(lf, "Title *").pack(fill="x")
        self.v_title = tk.StringVar()
        entry_widget(lf, self.v_title, width=28).pack(fill="x", pady=4)

        rf = tk.Frame(row, bg=BG_DARK)
        rf.pack(side="left", fill="x", expand=True)
        section_label(rf, "Category *").pack(fill="x")
        self.v_cat = tk.StringVar(value="character")
        combo_widget(rf, list(CAT_LABELS_MKT.keys()), self.v_cat, width=22).pack(fill="x", pady=4)

        # Description
        section_label(inner, "Description *").pack(fill="x", **pad)
        self.w_desc = text_widget(inner, height=3, width=60)
        self.w_desc.pack(fill="x", **pad)

        # Price row
        row2 = tk.Frame(inner, bg=BG_DARK)
        row2.pack(fill="x", **pad)
        for label, attr, placeholder in [
            ("Price ₹ (0=free)","v_price","1499"),
            ("Original Price ₹ (blank=none)","v_orig","1999"),
            ("Reviews","v_reviews","42"),
            ("Downloads","v_dl","318"),
        ]:
            f = tk.Frame(row2, bg=BG_DARK)
            f.pack(side="left", fill="x", expand=True, padx=(0,6))
            tk.Label(f, text=label, bg=BG_DARK, fg=TEXT_MUTED,
                     font=("Helvetica",8,"bold")).pack(anchor="w")
            setattr(self, attr, tk.StringVar())
            entry_widget(f, getattr(self,attr), width=10).pack(fill="x", pady=2)

        # Rating + Featured + Date
        row3 = tk.Frame(inner, bg=BG_DARK)
        row3.pack(fill="x", **pad)
        rf1 = tk.Frame(row3, bg=BG_DARK)
        rf1.pack(side="left", fill="x", expand=True, padx=(0,6))
        section_label(rf1, "Rating").pack(fill="x")
        self.v_rating = tk.StringVar(value="5")
        combo_widget(rf1, ["5","4","3","2","1"], self.v_rating, width=8).pack(fill="x", pady=4)

        rf2 = tk.Frame(row3, bg=BG_DARK)
        rf2.pack(side="left", fill="x", expand=True, padx=(0,6))
        section_label(rf2, "Featured").pack(fill="x")
        self.v_featured = tk.StringVar(value="Yes")
        combo_widget(rf2, ["Yes","No"], self.v_featured, width=8).pack(fill="x", pady=4)

        rf3 = tk.Frame(row3, bg=BG_DARK)
        rf3.pack(side="left", fill="x", expand=True)
        section_label(rf3, "Date Added").pack(fill="x")
        self.v_date = tk.StringVar(value=str(date.today()))
        entry_widget(rf3, self.v_date, width=14).pack(fill="x", pady=4)

        # Icon
        section_label(inner, "Font Awesome Icon Class").pack(fill="x", **pad)
        self.v_icon = tk.StringVar(value="fa-solid fa-cube")
        entry_widget(inner, self.v_icon, width=55).pack(fill="x", **pad)

        # Image
        section_label(inner, "Image Path / URL (optional)").pack(fill="x", **pad)
        irow = tk.Frame(inner, bg=BG_DARK)
        irow.pack(fill="x", **pad)
        self.v_image = tk.StringVar()
        entry_widget(irow, self.v_image, width=44).pack(side="left", fill="x", expand=True)
        styled_btn(irow, "Browse", self._browse_image, color=BG_CARD, small=True
                   ).pack(side="left", padx=(6,0))

        # Software / Formats / Badges
        for label, attr in [
            ("Software (comma-separated)","v_software"),
            ("File Formats (comma-separated)","v_formats"),
            ("Badges  (new · hot · sale · free)","v_badges"),
        ]:
            section_label(inner, label).pack(fill="x", **pad)
            setattr(self, attr, tk.StringVar())
            entry_widget(inner, getattr(self, attr), width=55).pack(fill="x", **pad)

        # Footer
        foot = tk.Frame(self, bg=BG_MID, pady=10)
        foot.pack(fill="x", side="bottom")
        styled_btn(foot, "Cancel", self.destroy, color=BG_CARD, fg=TEXT_MUTED, small=True
                   ).pack(side="right", padx=(0,12))
        styled_btn(foot, "💾  Save Asset", self._save, small=True
                   ).pack(side="right", padx=(0,8))

    def _populate(self):
        a = self.asset
        self.v_title.set(a.get("title",""))
        self.v_cat.set(a.get("category","character"))
        self.v_icon.set(a.get("icon","fa-solid fa-cube"))
        self.v_image.set(a.get("image") or "")
        self.v_price.set(str(a.get("price",0)))
        self.v_orig.set(str(a.get("originalPrice","") or ""))
        self.v_rating.set(str(a.get("rating",5)))
        self.v_reviews.set(str(a.get("reviews",0)))
        self.v_dl.set(str(a.get("downloads",0)))
        self.v_date.set(a.get("dateAdded",str(date.today())))
        self.v_featured.set("Yes" if a.get("featured") else "No")
        self.v_software.set(", ".join(a.get("software") or []))
        self.v_formats.set(", ".join(a.get("formats") or []))
        self.v_badges.set(", ".join(a.get("badges") or []))
        self.w_desc.insert("1.0", a.get("desc",""))

    def _browse_image(self):
        path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files","*.png *.jpg *.jpeg *.webp"), ("All","*.*")]
        )
        if path:
            self.v_image.set(path)

    def _parse_list(self, attr):
        return [x.strip() for x in getattr(self, attr).get().split(",") if x.strip()]

    def _save(self):
        title = self.v_title.get().strip()
        desc  = self.w_desc.get("1.0","end").strip()
        if not title:
            messagebox.showerror("Validation","Asset title is required.", parent=self); return
        if not desc:
            messagebox.showerror("Validation","Description is required.", parent=self); return

        def to_int(v, default=0):
            try: return int(v.get().strip())
            except: return default

        orig_raw = self.v_orig.get().strip()
        orig     = int(orig_raw) if orig_raw.isdigit() else None

        data = dict(
            title=title, category=self.v_cat.get(), desc=desc,
            price=to_int(self.v_price), originalPrice=orig,
            rating=to_int(self.v_rating,5), reviews=to_int(self.v_reviews),
            downloads=to_int(self.v_dl),
            dateAdded=self.v_date.get().strip() or str(date.today()),
            icon=self.v_icon.get().strip() or "fa-solid fa-cube",
            featured=self.v_featured.get()=="Yes",
            image=self.v_image.get().strip() or None,
            software=self._parse_list("v_software"),
            formats=self._parse_list("v_formats"),
            badges=self._parse_list("v_badges"),
        )

        if self.asset:
            self.asset.update(data)
        else:
            new_id = max((m["id"] for m in self.store.market), default=0) + 1
            self.store.market.append({"id": new_id, **data})

        self.store.save()
        if self.on_save:
            self.on_save()
        self.destroy()


# ──────────────────────────────────────────────────────────────────────────────
# CARD ROW WIDGET (used in list panels)
# ──────────────────────────────────────────────────────────────────────────────
class CardRow(tk.Frame):
    def __init__(self, parent, item: dict, on_edit, on_delete, on_duplicate,
                 is_market=False, **kwargs):
        super().__init__(parent, bg=BG_CARD, **kwargs)
        self.configure(highlightthickness=1, highlightbackground=BORDER)
        self._build(item, on_edit, on_delete, on_duplicate, is_market)
        self.bind("<Enter>",  lambda e: self.config(highlightbackground=FIRE_ORANGE))
        self.bind("<Leave>",  lambda e: self.config(highlightbackground=BORDER))

    def _build(self, item, on_edit, on_delete, on_duplicate, is_market):
        # Left colour bar
        bar_color = {
            "environment": FIRE_ORANGE,
            "character":   FIRE_RED,
            "prop":        FIRE_YELLOW,
            "texture":     BLUE,
            "vehicle":     GREEN,
        }.get(item.get("category",""), FIRE_ORANGE)
        tk.Frame(self, bg=bar_color, width=4).pack(side="left", fill="y")

        body = tk.Frame(self, bg=BG_CARD, padx=12, pady=8)
        body.pack(side="left", fill="both", expand=True)

        # Top row — title + category badge + price (market)
        top = tk.Frame(body, bg=BG_CARD)
        top.pack(fill="x")

        tk.Label(top, text=item.get("title","—"),
                 bg=BG_CARD, fg=TEXT_MAIN,
                 font=("Helvetica",11,"bold")).pack(side="left")

        cat_text = cat_label(item.get("category",""), mkt=is_market)
        tk.Label(top, text=f"  {cat_text}",
                 bg=BG_CARD, fg=FIRE_ORANGE,
                 font=("Helvetica",8,"bold")).pack(side="left", padx=6)

        if is_market:
            price = item.get("price",0)
            price_str = "Free" if price == 0 else f"₹{price:,}"
            tk.Label(top, text=price_str,
                     bg=BG_CARD, fg=GREEN if price==0 else FIRE_YELLOW,
                     font=("Helvetica",10,"bold")).pack(side="right", padx=6)

        # Description (truncated)
        desc = (item.get("desc","") or "")
        short = desc[:110] + ("…" if len(desc)>110 else "")
        tk.Label(body, text=short,
                 bg=BG_CARD, fg=TEXT_MUTED,
                 font=("Helvetica",9), wraplength=540, justify="left"
                 ).pack(anchor="w", pady=(2,4))

        # Tools / Software chips
        chips_raw = item.get("tools") or item.get("software") or []
        if chips_raw:
            chip_row = tk.Frame(body, bg=BG_CARD)
            chip_row.pack(anchor="w")
            for chip in chips_raw[:6]:
                tk.Label(chip_row, text=chip,
                         bg=BG_MID, fg=TEXT_MUTED,
                         font=("Helvetica",8), padx=6, pady=2,
                         relief="flat").pack(side="left", padx=(0,4))

        # Buttons
        btn_row = tk.Frame(self, bg=BG_CARD, pady=8, padx=8)
        btn_row.pack(side="right", fill="y")
        styled_btn(btn_row, "✏ Edit",      on_edit,      color="#2a1e14", fg=FIRE_ORANGE, small=True).pack(fill="x", pady=2)
        styled_btn(btn_row, "⎘ Duplicate", on_duplicate, color="#141c28", fg=BLUE,        small=True).pack(fill="x", pady=2)
        styled_btn(btn_row, "🗑 Delete",   on_delete,    color="#2a1414", fg=RED_ERR,      small=True).pack(fill="x", pady=2)


# ──────────────────────────────────────────────────────────────────────────────
# MAIN APPLICATION
# ──────────────────────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.configure(bg=BG_DARK)
        self.minsize(900, 600)

        self.store = DataStore()

        # Search / filter state
        self.proj_search  = tk.StringVar()
        self.proj_cat_f   = tk.StringVar(value="All")
        self.mkt_search   = tk.StringVar()
        self.mkt_cat_f    = tk.StringVar(value="All")

        self.proj_search.trace_add("write", lambda *_: self._refresh_projects())
        self.proj_cat_f.trace_add("write",  lambda *_: self._refresh_projects())
        self.mkt_search.trace_add("write",  lambda *_: self._refresh_market())
        self.mkt_cat_f.trace_add("write",   lambda *_: self._refresh_market())

        self._build_ui()
        self._refresh_all()

    # ── UI Construction ───────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        container = tk.Frame(self, bg=BG_DARK)
        container.pack(fill="both", expand=True)
        self._build_sidebar(container)
        self._build_main(container)

    def _build_header(self):
        hdr = tk.Frame(self, bg=BG_MID, height=56,
                       highlightthickness=1, highlightbackground=BORDER)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)

        # Logo
        logo = tk.Frame(hdr, bg=BG_MID)
        logo.pack(side="left", padx=18, pady=8)
        tk.Label(logo, text="⬡", bg=FIRE_ORANGE, fg="#fff",
                 font=("Helvetica",14,"bold"), padx=6, pady=2).pack(side="left")
        tk.Label(logo, text="  Creviz Studio", bg=BG_MID, fg=TEXT_MAIN,
                 font=("Helvetica",13,"bold")).pack(side="left")
        tk.Label(logo, text=" ADMIN", bg=BG_DARK, fg=FIRE_ORANGE,
                 font=("Helvetica",8,"bold"), padx=6, pady=2).pack(side="left", padx=6)

        # Right actions
        right = tk.Frame(hdr, bg=BG_MID)
        right.pack(side="right", padx=16)
        styled_btn(right, "💾  Save & Export", self._save_and_export, small=True
                   ).pack(side="right", padx=(6,0))
        styled_btn(right, "🔗  Open Site", lambda: webbrowser.open("index.html"),
                   color=BG_CARD, fg=TEXT_MUTED, small=True
                   ).pack(side="right", padx=(0,6))

    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=BG_MID, width=200,
                      highlightthickness=1, highlightbackground=BORDER)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        tk.Label(sb, text="NAVIGATION", bg=BG_MID, fg=TEXT_MUTED,
                 font=("Helvetica",8,"bold")).pack(anchor="w", padx=16, pady=(18,6))

        self._nav_btns: list[tk.Button] = []
        pages = [
            ("📊  Dashboard",   "dashboard"),
            ("🖼  Portfolio",   "portfolio"),
            ("🛒  Marketplace", "marketplace"),
            ("💻  Export Code", "export"),
            ("⚙  Settings",    "settings"),
        ]
        for label, key in pages:
            btn = tk.Button(sb, text=label, anchor="w",
                            bg=BG_MID, fg=TEXT_MUTED,
                            activebackground=BG_DARK, activeforeground=TEXT_MAIN,
                            relief="flat", bd=0, cursor="hand2",
                            font=("Helvetica",10), padx=16, pady=9,
                            command=lambda k=key: self._switch_panel(k))
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e,b=btn: b.config(bg=BG_DARK, fg=TEXT_MAIN))
            btn.bind("<Leave>", lambda e,b=btn,k=key: b.config(
                bg=BG_DARK if getattr(self,"_current_panel","dashboard")==k else BG_MID,
                fg=TEXT_MAIN if getattr(self,"_current_panel","dashboard")==k else TEXT_MUTED))
            self._nav_btns.append((key, btn))

        tk.Frame(sb, bg=BORDER, height=1).pack(fill="x", padx=12, pady=12)
        tk.Label(sb, text="LINKS", bg=BG_MID, fg=TEXT_MUTED,
                 font=("Helvetica",8,"bold")).pack(anchor="w", padx=16, pady=(0,6))
        styled_btn(sb, "↗  Portfolio Site",    lambda: webbrowser.open("index.html"),
                   color=BG_MID, fg=TEXT_MUTED, small=True).pack(fill="x", padx=8, pady=2)
        styled_btn(sb, "↗  Marketplace",       lambda: webbrowser.open("marketplace.html"),
                   color=BG_MID, fg=TEXT_MUTED, small=True).pack(fill="x", padx=8, pady=2)

    def _build_main(self, parent):
        self._main = tk.Frame(parent, bg=BG_DARK)
        self._main.pack(side="left", fill="both", expand=True)

        self._panels: dict[str, tk.Frame] = {}
        for name in ["dashboard","portfolio","marketplace","export","settings"]:
            f = tk.Frame(self._main, bg=BG_DARK)
            self._panels[name] = f

        self._build_dashboard(self._panels["dashboard"])
        self._build_portfolio(self._panels["portfolio"])
        self._build_marketplace(self._panels["marketplace"])
        self._build_export(self._panels["export"])
        self._build_settings(self._panels["settings"])

        self._current_panel = "dashboard"
        self._panels["dashboard"].pack(fill="both", expand=True)

    # ── Panel switcher ────────────────────────────────────────────
    def _switch_panel(self, name: str):
        self._panels[self._current_panel].pack_forget()
        self._current_panel = name
        self._panels[name].pack(fill="both", expand=True)
        for key, btn in self._nav_btns:
            if key == name:
                btn.config(bg=BG_DARK, fg=FIRE_ORANGE,
                           font=("Helvetica",10,"bold"))
            else:
                btn.config(bg=BG_MID, fg=TEXT_MUTED,
                           font=("Helvetica",10))
        if name == "export":
            self._refresh_export()
        if name == "dashboard":
            self._refresh_dashboard()

    # ── DASHBOARD ────────────────────────────────────────────────
    def _build_dashboard(self, parent):
        # Title
        hdr = tk.Frame(parent, bg=BG_DARK, pady=16)
        hdr.pack(fill="x", padx=24)
        tk.Label(hdr, text="📊  Dashboard", bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",16,"bold")).pack(side="left")

        # Stat cards row
        self._stat_frame = tk.Frame(parent, bg=BG_DARK)
        self._stat_frame.pack(fill="x", padx=24, pady=(0,18))

        self._stat_labels: dict[str,tk.Label] = {}
        stat_defs = [
            ("total_proj", "🖼", "Portfolio Projects", FIRE_ORANGE),
            ("total_mkt",  "🛒", "Marketplace Assets", FIRE_RED),
            ("envs",       "🌍", "Environments",       BLUE),
            ("chars",      "🧍", "Characters",         GREEN),
        ]
        for key, ico, label, color in stat_defs:
            card = tk.Frame(self._stat_frame, bg=BG_CARD, padx=18, pady=14,
                            highlightthickness=1, highlightbackground=BORDER)
            card.pack(side="left", fill="x", expand=True, padx=(0,10))
            tk.Label(card, text=ico, bg=BG_CARD, fg=color,
                     font=("Helvetica",18)).pack(anchor="w")
            lbl = tk.Label(card, text="0", bg=BG_CARD, fg=color,
                           font=("Helvetica",22,"bold"))
            lbl.pack(anchor="w")
            tk.Label(card, text=label, bg=BG_CARD, fg=TEXT_MUTED,
                     font=("Helvetica",8,"bold")).pack(anchor="w")
            self._stat_labels[key] = lbl

        # Quick actions
        qa = tk.Frame(parent, bg=BG_DARK, padx=24)
        qa.pack(fill="x", pady=(0,18))
        tk.Label(qa, text="⚡  Quick Actions", bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",11,"bold")).pack(anchor="w", pady=(0,8))
        btns = tk.Frame(qa, bg=BG_DARK)
        btns.pack(anchor="w")
        styled_btn(btns, "＋  Add Portfolio Project",
                   lambda: (self._switch_panel("portfolio"), self._add_project())
                   ).pack(side="left", padx=(0,8))
        styled_btn(btns, "＋  Add Marketplace Asset",
                   lambda: (self._switch_panel("marketplace"), self._add_market()),
                   color=BG_CARD, fg=TEXT_MUTED
                   ).pack(side="left", padx=(0,8))
        styled_btn(btns, "💾  Save & Export",
                   self._save_and_export, color=GREEN, fg=BG_DARK
                   ).pack(side="left")

        # Recent projects
        tk.Label(parent, text="🕐  Recent Projects",
                 bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",11,"bold")).pack(anchor="w", padx=24, pady=(0,8))
        outer, self._recent_inner = scrolled_frame(parent)
        outer.pack(fill="both", expand=True, padx=24, pady=(0,12))

    def _refresh_dashboard(self):
        self._stat_labels["total_proj"].config(text=str(len(self.store.projects)))
        self._stat_labels["total_mkt"].config(text=str(len(self.store.market)))
        self._stat_labels["envs"].config(
            text=str(sum(1 for p in self.store.projects if p["category"]=="environment")))
        self._stat_labels["chars"].config(
            text=str(sum(1 for p in self.store.projects if p["category"]=="character")))

        for w in self._recent_inner.winfo_children():
            w.destroy()
        for p in self.store.projects[:6]:
            row = tk.Frame(self._recent_inner, bg=BG_CARD, pady=8, padx=12,
                           highlightthickness=1, highlightbackground=BORDER)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=p["title"], bg=BG_CARD, fg=TEXT_MAIN,
                     font=("Helvetica",10,"bold")).pack(side="left")
            tk.Label(row, text=f"  {cat_label(p['category'])}",
                     bg=BG_CARD, fg=FIRE_ORANGE,
                     font=("Helvetica",9)).pack(side="left")
            styled_btn(row, "Edit",
                       lambda pid=p["id"]: (self._switch_panel("portfolio"),
                                            self._edit_project_by_id(pid)),
                       color=BG_MID, fg=FIRE_ORANGE, small=True
                       ).pack(side="right")

    # ── PORTFOLIO PANEL ───────────────────────────────────────────
    def _build_portfolio(self, parent):
        # Header
        hdr = tk.Frame(parent, bg=BG_DARK, pady=14)
        hdr.pack(fill="x", padx=24)
        tk.Label(hdr, text="🖼  Portfolio Projects", bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",15,"bold")).pack(side="left")
        styled_btn(hdr, "＋  Add Project", self._add_project, small=True
                   ).pack(side="right")

        # Toolbar
        tb = tk.Frame(parent, bg=BG_DARK, padx=24)
        tb.pack(fill="x", pady=(0,10))
        tk.Label(tb, text="🔍", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",11)).pack(side="left")
        entry_widget(tb, self.proj_search, width=30).pack(side="left", padx=(4,12))
        tk.Label(tb, text="Category:", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",9)).pack(side="left")
        combo_widget(tb, ["All"] + list(CAT_LABELS_PROJ.keys()),
                     self.proj_cat_f, width=16).pack(side="left", padx=6)

        # List
        outer, self._proj_list = scrolled_frame(parent)
        outer.pack(fill="both", expand=True, padx=24, pady=(0,12))

    def _refresh_projects(self):
        for w in self._proj_list.winfo_children():
            w.destroy()

        q   = self.proj_search.get().lower()
        cat = self.proj_cat_f.get()
        items = [
            p for p in self.store.projects
            if (not q or q in p["title"].lower() or q in p["desc"].lower())
            and (cat == "All" or p["category"] == cat)
        ]
        if not items:
            tk.Label(self._proj_list, text="No projects found.",
                     bg=BG_DARK, fg=TEXT_MUTED,
                     font=("Helvetica",11)).pack(pady=40)
            return

        for p in items:
            card = CardRow(
                self._proj_list, p,
                on_edit=lambda pid=p["id"]: self._edit_project_by_id(pid),
                on_delete=lambda pid=p["id"]: self._delete_project(pid),
                on_duplicate=lambda pid=p["id"]: self._dup_project(pid),
            )
            card.pack(fill="x", pady=4)

    def _add_project(self):
        ProjectDialog(self, self.store, on_save=self._refresh_all)

    def _edit_project_by_id(self, pid: int):
        p = next((x for x in self.store.projects if x["id"]==pid), None)
        if p:
            ProjectDialog(self, self.store, project=p, on_save=self._refresh_all)

    def _delete_project(self, pid: int):
        p = next((x for x in self.store.projects if x["id"]==pid), None)
        if not p: return
        if messagebox.askyesno("Delete Project",
                               f'Delete "{p["title"]}"?\nThis cannot be undone.',
                               parent=self):
            self.store.projects = [x for x in self.store.projects if x["id"]!=pid]
            self.store.save()
            self._refresh_all()

    def _dup_project(self, pid: int):
        p = next((x for x in self.store.projects if x["id"]==pid), None)
        if not p: return
        clone = deepcopy(p)
        clone["id"]    = max((x["id"] for x in self.store.projects), default=0) + 1
        clone["title"] = p["title"] + " (Copy)"
        self.store.projects.append(clone)
        self.store.save()
        self._refresh_all()

    # ── MARKETPLACE PANEL ─────────────────────────────────────────
    def _build_marketplace(self, parent):
        hdr = tk.Frame(parent, bg=BG_DARK, pady=14)
        hdr.pack(fill="x", padx=24)
        tk.Label(hdr, text="🛒  Marketplace Assets", bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",15,"bold")).pack(side="left")
        styled_btn(hdr, "＋  Add Asset", self._add_market, small=True
                   ).pack(side="right")

        tb = tk.Frame(parent, bg=BG_DARK, padx=24)
        tb.pack(fill="x", pady=(0,10))
        tk.Label(tb, text="🔍", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",11)).pack(side="left")
        entry_widget(tb, self.mkt_search, width=30).pack(side="left", padx=(4,12))
        tk.Label(tb, text="Category:", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",9)).pack(side="left")
        combo_widget(tb, ["All"] + list(CAT_LABELS_MKT.keys()),
                     self.mkt_cat_f, width=16).pack(side="left", padx=6)

        outer, self._mkt_list = scrolled_frame(parent)
        outer.pack(fill="both", expand=True, padx=24, pady=(0,12))

    def _refresh_market(self):
        for w in self._mkt_list.winfo_children():
            w.destroy()

        q   = self.mkt_search.get().lower()
        cat = self.mkt_cat_f.get()
        items = [
            m for m in self.store.market
            if (not q or q in m["title"].lower() or q in m["desc"].lower())
            and (cat == "All" or m["category"] == cat)
        ]
        if not items:
            tk.Label(self._mkt_list, text="No assets found.",
                     bg=BG_DARK, fg=TEXT_MUTED,
                     font=("Helvetica",11)).pack(pady=40)
            return

        for m in items:
            card = CardRow(
                self._mkt_list, m,
                on_edit=lambda mid=m["id"]: self._edit_market_by_id(mid),
                on_delete=lambda mid=m["id"]: self._delete_market(mid),
                on_duplicate=lambda mid=m["id"]: self._dup_market(mid),
                is_market=True,
            )
            card.pack(fill="x", pady=4)

    def _add_market(self):
        MarketDialog(self, self.store, on_save=self._refresh_all)

    def _edit_market_by_id(self, mid: int):
        m = next((x for x in self.store.market if x["id"]==mid), None)
        if m:
            MarketDialog(self, self.store, asset=m, on_save=self._refresh_all)

    def _delete_market(self, mid: int):
        m = next((x for x in self.store.market if x["id"]==mid), None)
        if not m: return
        if messagebox.askyesno("Delete Asset",
                               f'Delete "{m["title"]}"?\nThis cannot be undone.',
                               parent=self):
            self.store.market = [x for x in self.store.market if x["id"]!=mid]
            self.store.save()
            self._refresh_all()

    def _dup_market(self, mid: int):
        m = next((x for x in self.store.market if x["id"]==mid), None)
        if not m: return
        clone = deepcopy(m)
        clone["id"]    = max((x["id"] for x in self.store.market), default=0) + 1
        clone["title"] = m["title"] + " (Copy)"
        self.store.market.append(clone)
        self.store.save()
        self._refresh_all()

    # ── EXPORT PANEL ─────────────────────────────────────────────
    def _build_export(self, parent):
        hdr = tk.Frame(parent, bg=BG_DARK, pady=14)
        hdr.pack(fill="x", padx=24)
        tk.Label(hdr, text="💻  Export & Patch Files", bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",15,"bold")).pack(side="left")
        styled_btn(hdr, "🔄  Regenerate", self._refresh_export, small=True
                   ).pack(side="right")

        outer, inner = scrolled_frame(parent)
        outer.pack(fill="both", expand=True, padx=24, pady=(0,12))

        # ── Section 1: Portfolio HTML ───────────────────────────
        self._build_export_section(
            inner,
            title="🖼  Portfolio Projects HTML",
            subtitle='Paste inside  <div class="projects-grid" id="portfolioGrid">  in index.html',
            code_attr="_port_code",
            bg_accent=FIRE_ORANGE,
        )

        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=16)

        # ── Section 2: Marketplace JS ───────────────────────────
        self._build_export_section(
            inner,
            title="🛒  Marketplace Products JS",
            subtitle="Replace the entire  const PRODUCTS = [...]  array in marketplace.js",
            code_attr="_mkt_code",
            bg_accent=FIRE_YELLOW,
        )

        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=16)

        # ── Section 3: Patch index.html ─────────────────────────
        self._build_patch_section(
            inner,
            heading="🔧  Patch  index.html  directly",
            description=(
                "Upload your current index.html — the admin will replace the\n"
                '<div class="projects-grid" id="portfolioGrid"> block automatically\n'
                "and download the updated file. Just replace the old file in your project folder."
            ),
            upload_label="📂  Upload index.html",
            upload_accept=[("HTML files","*.html *.htm"),("All","*.*")],
            upload_attr="_index_content",
            upload_name_attr="_index_name",
            upload_status_attr="_index_status_lbl",
            download_label="⬇  Download Patched index.html",
            download_cmd=self._patch_and_download_index,
            download_btn_attr="_index_dl_btn",
            accent=FIRE_ORANGE,
        )

        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=16)

        # ── Section 4: Patch marketplace.js ─────────────────────
        self._build_patch_section(
            inner,
            heading="🔧  Patch  marketplace.js  directly",
            description=(
                "Upload your current marketplace.js — the admin will replace the\n"
                "const PRODUCTS = [...] array automatically\n"
                "and download the updated file. Just replace the old file in js/ folder."
            ),
            upload_label="📂  Upload marketplace.js",
            upload_accept=[("JS files","*.js"),("All","*.*")],
            upload_attr="_js_content",
            upload_name_attr="_js_name",
            upload_status_attr="_js_status_lbl",
            download_label="⬇  Download Patched marketplace.js",
            download_cmd=self._patch_and_download_js,
            download_btn_attr="_js_dl_btn",
            accent=FIRE_YELLOW,
        )

    def _build_export_section(self, parent, title, subtitle, code_attr, bg_accent):
        tk.Label(parent, text=title, bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",12,"bold")).pack(anchor="w", pady=(0,2))
        tk.Label(parent, text=subtitle, bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",9)).pack(anchor="w", pady=(0,8))

        code_frame = tk.Frame(parent, bg=BG_MID, highlightthickness=1,
                              highlightbackground=BORDER)
        code_frame.pack(fill="x", pady=(0,6))

        # Copy button
        copy_row = tk.Frame(code_frame, bg=BG_MID)
        copy_row.pack(fill="x", padx=8, pady=(6,0))
        copy_btn = styled_btn(copy_row, "⎘  Copy to Clipboard",
                              lambda a=code_attr: self._copy_code(a),
                              color=BG_CARD, fg=FIRE_ORANGE, small=True)
        copy_btn.pack(side="right")

        # Code area
        code_text = tk.Text(
            code_frame, height=10, bg="#0a0806", fg="#f0ece8",
            insertbackground=TEXT_MAIN, relief="flat", bd=0,
            font=("Courier New", 9), wrap="none",
            highlightthickness=0, padx=12, pady=8, spacing1=1,
        )
        # Horizontal scrollbar
        hsb = tk.Scrollbar(code_frame, orient="horizontal", command=code_text.xview)
        code_text.configure(xscrollcommand=hsb.set)
        code_text.pack(fill="both", expand=True, padx=6, pady=4)
        hsb.pack(fill="x", padx=6, pady=(0,6))

        setattr(self, code_attr, code_text)

    def _build_patch_section(self, parent, heading, description,
                              upload_label, upload_accept,
                              upload_attr, upload_name_attr, upload_status_attr,
                              download_label, download_cmd, download_btn_attr,
                              accent):
        box = tk.Frame(parent, bg=BG_CARD, padx=20, pady=16,
                       highlightthickness=1,
                       highlightbackground=accent if accent==FIRE_ORANGE else FIRE_YELLOW)
        box.pack(fill="x", pady=(0,8))

        tk.Label(box, text=heading, bg=BG_CARD, fg=TEXT_MAIN,
                 font=("Helvetica",12,"bold")).pack(anchor="w", pady=(0,4))
        tk.Label(box, text=description, bg=BG_CARD, fg=TEXT_MUTED,
                 font=("Helvetica",9), justify="left").pack(anchor="w", pady=(0,10))

        # Warning strip
        warn = tk.Frame(box, bg="#1a1500", padx=10, pady=6,
                        highlightthickness=1, highlightbackground="#3a3000")
        warn.pack(fill="x", pady=(0,12))
        tk.Label(warn,
                 text="⚠  Your file is read in-browser memory only — never uploaded to any server.",
                 bg="#1a1500", fg=FIRE_YELLOW, font=("Helvetica",8)).pack(anchor="w")

        btn_row = tk.Frame(box, bg=BG_CARD)
        btn_row.pack(anchor="w")

        # Upload button
        setattr(self, upload_attr, None)
        setattr(self, upload_name_attr, "")

        def do_upload(ua=upload_attr, una=upload_name_attr,
                      usa=upload_status_attr, dba=download_btn_attr, acc=upload_accept):
            path = filedialog.askopenfilename(title="Select file", filetypes=acc)
            if not path:
                return
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                setattr(self, ua, f.read())
            setattr(self, una, os.path.basename(path))
            getattr(self, usa).config(
                text=f"✔  {os.path.basename(path)} loaded", fg=GREEN)
            getattr(self, dba).config(state="normal", bg=accent,
                                      fg=BG_DARK if accent==FIRE_YELLOW else "#fff")

        up_btn = styled_btn(btn_row, upload_label, do_upload,
                            color=BG_MID, fg=TEXT_MAIN, small=True)
        up_btn.pack(side="left", padx=(0,10))

        dl_btn = styled_btn(btn_row, download_label, download_cmd,
                            color=accent,
                            fg=BG_DARK if accent==FIRE_YELLOW else "#fff",
                            small=True)
        dl_btn.config(state="disabled", bg=BG_MID, fg=TEXT_MUTED)
        dl_btn.pack(side="left")
        setattr(self, download_btn_attr, dl_btn)

        status = tk.Label(box, text="No file uploaded yet.",
                          bg=BG_CARD, fg=TEXT_MUTED, font=("Helvetica",9))
        status.pack(anchor="w", pady=(8,0))
        setattr(self, upload_status_attr, status)

    def _patch_and_download_index(self):
        if not self._index_content:
            messagebox.showerror("No file", "Please upload index.html first."); return
        patched, msg = self.store.patch_index(self._index_content)
        out = filedialog.asksaveasfilename(
            title="Save patched index.html",
            defaultextension=".html",
            initialfile="index.html",
            filetypes=[("HTML","*.html"),("All","*.*")],
        )
        if not out: return
        with open(out, "w", encoding="utf-8") as f:
            f.write(patched)
        messagebox.showinfo("Done", f"{msg}\n\nSaved to:\n{out}")

    def _patch_and_download_js(self):
        if not self._js_content:
            messagebox.showerror("No file", "Please upload marketplace.js first."); return
        patched, msg = self.store.patch_marketplace_js(self._js_content)
        out = filedialog.asksaveasfilename(
            title="Save patched marketplace.js",
            defaultextension=".js",
            initialfile="marketplace.js",
            filetypes=[("JavaScript","*.js"),("All","*.*")],
        )
        if not out: return
        with open(out, "w", encoding="utf-8") as f:
            f.write(patched)
        messagebox.showinfo("Done", f"{msg}\n\nSaved to:\n{out}")

    def _refresh_export(self):
        # Portfolio
        html = self.store.portfolio_html()
        self._port_code.config(state="normal")
        self._port_code.delete("1.0","end")
        self._port_code.insert("1.0", html)
        self._port_code.config(state="disabled")
        # Marketplace
        js = self.store.products_js()
        self._mkt_code.config(state="normal")
        self._mkt_code.delete("1.0","end")
        self._mkt_code.insert("1.0", js)
        self._mkt_code.config(state="disabled")

    def _copy_code(self, attr: str):
        widget: tk.Text = getattr(self, attr)
        widget.config(state="normal")
        text = widget.get("1.0","end")
        widget.config(state="disabled")
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Copied", "Code copied to clipboard!")

    # ── SETTINGS PANEL ────────────────────────────────────────────
    def _build_settings(self, parent):
        hdr = tk.Frame(parent, bg=BG_DARK, pady=14)
        hdr.pack(fill="x", padx=24)
        tk.Label(hdr, text="⚙  Settings", bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",15,"bold")).pack(side="left")

        outer, inner = scrolled_frame(parent)
        outer.pack(fill="both", expand=True, padx=24, pady=(0,12))

        def section(title):
            tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=(18,12))
            tk.Label(inner, text=title, bg=BG_DARK, fg=FIRE_ORANGE,
                     font=("Helvetica",10,"bold")).pack(anchor="w")

        def row(label, desc, widget_factory):
            f = tk.Frame(inner, bg=BG_CARD, padx=16, pady=12,
                         highlightthickness=1, highlightbackground=BORDER)
            f.pack(fill="x", pady=4)
            info = tk.Frame(f, bg=BG_CARD)
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=label, bg=BG_CARD, fg=TEXT_MAIN,
                     font=("Helvetica",10,"bold")).pack(anchor="w")
            tk.Label(info, text=desc, bg=BG_CARD, fg=TEXT_MUTED,
                     font=("Helvetica",8), wraplength=520, justify="left"
                     ).pack(anchor="w", pady=(2,0))
            w = widget_factory(f)
            w.pack(side="right", padx=(12,0))

        section("💾  Data Management")

        row("Save to JSON now",
            f"Saves all projects and assets to  {DATA_FILE}  in the same folder as this script.",
            lambda p: styled_btn(p, "Save", self._do_save, small=True))

        row("Export JSON backup",
            "Download a full backup of all your data as a dated JSON file.",
            lambda p: styled_btn(p, "⬇  Export", self._export_json,
                                 color=BG_MID, fg=TEXT_MAIN, small=True))

        row("Import JSON backup",
            "Restore data from a previously exported JSON file.",
            lambda p: styled_btn(p, "⬆  Import", self._import_json,
                                 color=BG_MID, fg=TEXT_MAIN, small=True))

        row("Reset to defaults",
            "Permanently deletes all projects and assets and reloads the built-in sample data.",
            lambda p: styled_btn(p, "⚠  Reset All", self._confirm_reset,
                                 color="#3a1414", fg=RED_ERR, small=True))

        section("🌐  Site Paths")

        path_frame = tk.Frame(inner, bg=BG_CARD, padx=16, pady=14,
                              highlightthickness=1, highlightbackground=BORDER)
        path_frame.pack(fill="x", pady=4)
        tk.Label(path_frame,
                 text="The Export panel uploads and patches files at any path you choose via the file browser.\n"
                      "No hardcoded paths are needed — just open your files directly.",
                 bg=BG_CARD, fg=TEXT_MUTED, font=("Helvetica",9),
                 justify="left").pack(anchor="w")

        section("ℹ  About")
        info_frame = tk.Frame(inner, bg=BG_CARD, padx=16, pady=14,
                              highlightthickness=1, highlightbackground=BORDER)
        info_frame.pack(fill="x", pady=4)
        for line in [
            "Creviz Studio — Desktop Admin Panel  v1.0",
            "Built with Python 3  +  Tkinter  (stdlib only)",
            "Data stored in:  creviz_data.json  (same folder as script)",
            "",
            "© 2026 Creviz Studio",
        ]:
            tk.Label(info_frame, text=line, bg=BG_CARD,
                     fg=TEXT_MAIN if "©" in line or "v1.0" in line else TEXT_MUTED,
                     font=("Helvetica", 9, "bold" if "v1.0" in line else "normal")
                     ).pack(anchor="w")

    # ── Settings actions ──────────────────────────────────────────
    def _do_save(self):
        self.store.save()
        messagebox.showinfo("Saved", f"Data saved to {DATA_FILE}")

    def _export_json(self):
        path = filedialog.asksaveasfilename(
            title="Export JSON backup",
            defaultextension=".json",
            initialfile=f"creviz-backup-{date.today()}.json",
            filetypes=[("JSON","*.json"),("All","*.*")],
        )
        if path:
            self.store.export_backup(path)
            messagebox.showinfo("Exported", f"Backup saved to:\n{path}")

    def _import_json(self):
        path = filedialog.askopenfilename(
            title="Import JSON backup",
            filetypes=[("JSON","*.json"),("All","*.*")],
        )
        if not path: return
        try:
            self.store.import_backup(path)
            self._refresh_all()
            messagebox.showinfo("Imported",
                f"Loaded {len(self.store.projects)} projects and "
                f"{len(self.store.market)} assets.")
        except Exception as e:
            messagebox.showerror("Import Failed", f"Invalid JSON file.\n\n{e}")

    def _confirm_reset(self):
        if messagebox.askyesno("Reset All Data",
                               "This will permanently delete all your projects and "
                               "marketplace assets and restore the defaults.\n\n"
                               "This cannot be undone. Continue?",
                               icon="warning"):
            self.store.reset()
            self._refresh_all()
            messagebox.showinfo("Reset Complete", "All data restored to defaults.")

    # ── Global helpers ────────────────────────────────────────────
    def _save_and_export(self):
        self.store.save()
        self._switch_panel("export")
        self._refresh_export()
        messagebox.showinfo("Saved & Exported",
                            f"Data saved to {DATA_FILE}\n\n"
                            "Switch to the Export tab to copy or download patched files.")

    def _refresh_all(self):
        self._refresh_dashboard()
        self._refresh_projects()
        self._refresh_market()
        if self._current_panel == "export":
            self._refresh_export()

    # Stub attributes so _build_patch_section doesn't fail before first upload
    _index_content = None
    _index_name    = ""
    _js_content    = None
    _js_name       = ""


# ──────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()