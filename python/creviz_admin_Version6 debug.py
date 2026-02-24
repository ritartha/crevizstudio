"""
Creviz Studio — Desktop Admin Panel
=====================================
Full-featured GUI built with Tkinter + ttk.
Manages portfolio projects and marketplace assets,
generates patched index.html and marketplace.js.
Includes Git & Firebase deploy panel.

Requirements: Python 3.9+  (stdlib only — no pip installs needed)
Run:  python creviz_admin.py
"""

import json
import os
import re
import subprocess
import sys
import threading
import tkinter as tk
import webbrowser
from copy import deepcopy
from datetime import date
from tkinter import filedialog, messagebox, ttk

# ──────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────────────────────────────────────
APP_TITLE    = "Creviz Studio — Admin Panel"
DATA_FILE    = "creviz_data.json"
WIN_W, WIN_H = 1280, 800

FIRE_ORANGE  = "#ff6b1a"
FIRE_RED     = "#ff2d2d"
FIRE_YELLOW  = "#ffc93c"
BG_DARK      = "#0c0a09"
BG_MID       = "#181210"
BG_CARD      = "#1f1612"
BG_INPUT     = "#242018"
TEXT_MAIN    = "#f0ece8"
TEXT_MUTED   = "#9e9189"
GREEN        = "#4ade80"
BLUE         = "#60a5fa"
RED_ERR      = "#ff4d4d"
BORDER       = "#2a2420"
PURPLE       = "#c084fc"

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
GRADIENT_OPTIONS = ["env-gradient", "char-gradient", "prop-gradient"]


# ──────────────────────────────────────────────────────────────────────────────
# DEFAULT DATA
# ──────────────────────────────────────────────────────────────────────────────
DEFAULT_PROJECTS = [
    {"id":1,"title":"Ember Wastes",         "category":"environment","desc":"Post-apocalyptic volcanic landscape rendered in Cycles. Hand-sculpted rock formations, volumetric smoke and god rays.",          "tools":["Blender","Substance"],"icon":"fa-solid fa-mountain-sun",   "gradient":"env-gradient", "image":None},
    {"id":2,"title":"Iron Veil Warrior",    "category":"character",  "desc":"Battle-hardened female knight with intricate plate armour, sculpted at 40M polys in ZBrush and retopologised for real-time.",  "tools":["ZBrush","Substance"],  "icon":"fa-solid fa-person",         "gradient":"char-gradient","image":None},
    {"id":3,"title":"Neon Alley",           "category":"environment","desc":"Rain-soaked cyberpunk back-alley with neon reflections, wet concrete, holographic signage and fog in EEVEE.",                  "tools":["Blender","PBR"],       "icon":"fa-solid fa-city",           "gradient":"env-gradient", "image":None},
    {"id":4,"title":"Void Sorcerer",        "category":"character",  "desc":"Stylised dark-fantasy spellcaster with cloth simulation, particle-based robe fabric and emissive rune tattoos.",               "tools":["ZBrush","Blender"],    "icon":"fa-solid fa-hat-wizard",     "gradient":"char-gradient","image":None},
    {"id":5,"title":"Ancient Temple Grove", "category":"environment","desc":"Overgrown jungle temple with moss, vines, water caustics and dynamic lighting via Blender Geometry Nodes.",                    "tools":["Blender","Substance"], "icon":"fa-solid fa-torii-gate",     "gradient":"env-gradient", "image":None},
    {"id":6,"title":"Relic Weapon Pack",    "category":"prop",       "desc":"Pack of 6 fantasy melee weapons with full PBR texture sets baked from high-poly ZBrush sculpts, game-engine ready.",          "tools":["ZBrush","Substance"],  "icon":"fa-solid fa-khanda",         "gradient":"prop-gradient","image":None},
    {"id":7,"title":"Kira — Sci-Fi Scout",  "category":"character",  "desc":"Full-body sci-fi character with hard-surface exo-suit, visor glass shader, mechanical arms and rigged for animation.",         "tools":["ZBrush","Blender"],    "icon":"fa-solid fa-user-astronaut", "gradient":"char-gradient","image":None},
    {"id":8,"title":"Abandoned Diner",      "category":"prop",       "desc":"Hero prop set — retro diner booth, cracked floor tiles, broken neon sign and dusty counter with full 4K texture maps.",        "tools":["Blender","Substance"], "icon":"fa-solid fa-store",          "gradient":"prop-gradient","image":None},
    {"id":9,"title":"Arctic Research Base", "category":"environment","desc":"Isolated sci-fi outpost in a blizzard with sub-surface ice scattering, wind-driven particle snow and moody interior light.",   "tools":["Blender","PBR"],       "icon":"fa-solid fa-snowflake",      "gradient":"env-gradient", "image":None},
]

DEFAULT_MARKET = [
    {"id":1, "title":"Iron Veil Warrior",         "category":"character",  "desc":"Battle-hardened female knight sculpted at 40M polys. Fully rigged, game-ready FBX with 4K PBR.",             "price":1499,"originalPrice":1999,"rating":5,"reviews":42, "software":["zbrush","blender","substance"],         "formats":["fbx","blend","obj"],  "image":None,"icon":"fa-solid fa-person",         "badges":["hot"],       "downloads":318, "featured":True, "dateAdded":"2026-01-15"},
    {"id":2, "title":"Ember Wastes Environment",  "category":"environment","desc":"Post-apocalyptic volcanic landscape. Full .blend file, volumetric smoke, god-ray lighting rig.",             "price":1299,"originalPrice":None,"rating":5,"reviews":28, "software":["blender","substance"],                  "formats":["blend","fbx"],        "image":None,"icon":"fa-solid fa-mountain-sun",  "badges":["new"],       "downloads":201, "featured":True, "dateAdded":"2026-02-01"},
    {"id":3, "title":"Relic Weapon Pack",         "category":"prop",       "desc":"Six fantasy melee weapons baked from high-poly ZBrush sculpts. 4K albedo, normal, roughness and metallic.", "price":799, "originalPrice":1199,"rating":4,"reviews":64, "software":["zbrush","substance"],                   "formats":["fbx","obj","usdz"],   "image":None,"icon":"fa-solid fa-khanda",         "badges":["sale"],      "downloads":487, "featured":True, "dateAdded":"2025-11-20"},
    {"id":4, "title":"Neon Alley Scene",          "category":"environment","desc":"Rain-soaked cyberpunk back-alley. Full EEVEE scene with wet-surface shaders and volumetric fog.",            "price":1099,"originalPrice":None,"rating":5,"reviews":19, "software":["blender"],                              "formats":["blend"],              "image":None,"icon":"fa-solid fa-city",           "badges":["new"],       "downloads":145, "featured":False,"dateAdded":"2026-01-28"},
    {"id":5, "title":"Void Sorcerer Character",   "category":"character",  "desc":"Stylised dark-fantasy spellcaster with cloth sim, particle robe and emissive rune tattoos. UE5 rig.",       "price":1799,"originalPrice":2299,"rating":5,"reviews":37, "software":["zbrush","blender","unreal"],             "formats":["fbx","blend"],        "image":None,"icon":"fa-solid fa-hat-wizard",     "badges":["hot","sale"],"downloads":276, "featured":True, "dateAdded":"2025-12-10"},
    {"id":6, "title":"Mossy Rock PBR Pack",       "category":"texture",    "desc":"12 seamless mossy rock PBR materials at 4K. Albedo, Normal, Height, Roughness and AO maps.",               "price":499, "originalPrice":None,"rating":4,"reviews":93, "software":["blender","substance","unreal","unity"],  "formats":["blend","usdz"],       "image":None,"icon":"fa-solid fa-layer-group",   "badges":[],            "downloads":612, "featured":False,"dateAdded":"2025-10-05"},
    {"id":7, "title":"Kira — Sci-Fi Scout",       "category":"character",  "desc":"Hard-surface exo-suit with visor glass, mechanical arm rigs and multiple LODs. Full 4K PBR.",               "price":2199,"originalPrice":2699,"rating":5,"reviews":55, "software":["zbrush","blender","substance","unreal","unity"],"formats":["fbx","blend","obj"],"image":None,"icon":"fa-solid fa-user-astronaut","badges":["hot"],"downloads":344,"featured":True,"dateAdded":"2026-01-05"},
    {"id":8, "title":"Ancient Temple Grove",      "category":"environment","desc":"Overgrown jungle temple with Geometry Nodes scatter for vines, moss and foliage. Water caustics shader.",   "price":1599,"originalPrice":None,"rating":5,"reviews":22, "software":["blender","substance"],                  "formats":["blend"],              "image":None,"icon":"fa-solid fa-torii-gate",     "badges":["new"],       "downloads":178, "featured":False,"dateAdded":"2026-02-10"},
    {"id":9, "title":"Abandoned Diner Props",     "category":"prop",       "desc":"Retro diner hero prop set. Cracked tiles, broken neon sign and dusty counter. Full 4K texture maps.",       "price":699, "originalPrice":None,"rating":4,"reviews":41, "software":["blender","substance"],                  "formats":["fbx","obj"],          "image":None,"icon":"fa-solid fa-store",          "badges":[],            "downloads":289, "featured":False,"dateAdded":"2025-09-18"},
    {"id":10,"title":"Arctic Research Base",      "category":"environment","desc":"Sci-fi blizzard outpost with sub-surface ice scattering and wind-driven particle snow.",                   "price":1399,"originalPrice":1799,"rating":4,"reviews":17, "software":["blender"],                              "formats":["blend","fbx"],        "image":None,"icon":"fa-solid fa-snowflake",      "badges":["sale"],      "downloads":132, "featured":False,"dateAdded":"2025-08-22"},
    {"id":11,"title":"Wet Concrete Texture Pack", "category":"texture",    "desc":"8 wet/dry concrete PBR materials. Tiling albedo, normal, height, metallic and roughness at 4K.",           "price":0,   "originalPrice":None,"rating":5,"reviews":204,"software":["blender","unreal","unity"],              "formats":["blend","usdz","obj"], "image":None,"icon":"fa-solid fa-layer-group",   "badges":["free"],      "downloads":1841,"featured":True, "dateAdded":"2025-07-01"},
    {"id":12,"title":"Fantasy Ground Vehicle",    "category":"vehicle",    "desc":"Ornate steampunk carriage with animated wheel rig, aged leather shader and wood-grain PBR materials.",     "price":1899,"originalPrice":2399,"rating":4,"reviews":14, "software":["blender","substance","unreal"],          "formats":["fbx","blend"],        "image":None,"icon":"fa-solid fa-car",            "badges":["sale"],      "downloads":98,  "featured":False,"dateAdded":"2026-02-18"},
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
    if v is None:             return "null"
    if isinstance(v, bool):   return "true" if v else "false"
    if isinstance(v, (int, float)): return str(v)
    if isinstance(v, list):   return json.dumps(v)
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
            json.dump({"version":"1.0","exportedAt":str(date.today()),
                       "projects":self.projects,"market":self.market}, f, indent=2)

    def import_backup(self, path: str):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
        if "projects" in data: self.projects = data["projects"]
        if "market"   in data: self.market   = data["market"]
        self.save()

    def reset(self):
        self.projects = deepcopy(DEFAULT_PROJECTS)
        self.market   = deepcopy(DEFAULT_MARKET)
        self.save()

    # ── Code generators ───────────────────────────────────────────
    def portfolio_html(self) -> str:
        cards = []
        for p in self.projects:
            img_html   = (f'<img src="{p["image"]}" alt="{p["title"]}" loading="lazy" />'
                          if p.get("image")
                          else f'<div class="img-placeholder"><i class="{p["icon"]}"></i></div>')
            tools_html = "\n".join(
                f'          <span class="project-tool">{t}</span>'
                for t in (p.get("tools") or []))
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
        cards       = self.portfolio_html()
        replacement = f"\\1\n{cards}\n      \\3"
        by_id    = re.compile(
            r'(<div[^>]*\bid=["\']portfolioGrid["\'][^>]*>)([\s\S]*?)'
            r'(<\/div>(?=\s*(?:<!--|<\/section>|<\/main>|<footer|<div|<section|$)))',
            re.IGNORECASE)
        by_class = re.compile(
            r'(<div[^>]*\bclass=["\'][^"\']*projects-grid[^"\']*["\'][^>]*>)([\s\S]*?)'
            r'(<\/div>(?=\s*(?:<!--|<\/section>|<\/main>|<footer|<div|<section|$)))',
            re.IGNORECASE)
        if by_id.search(original):
            return by_id.sub(replacement, original, count=1), 'Replaced by id="portfolioGrid" ✓'
        if by_class.search(original):
            return by_class.sub(replacement, original, count=1), 'Replaced by class="projects-grid" ✓'
        patched = original.replace("</main>",
            f"<!-- CREVIZ ADMIN: paste into your projects-grid div -->\n{cards}\n</main>", 1)
        return patched, "⚠ Could not locate projects-grid — inserted before </main>, review manually."

    def patch_marketplace_js(self, original: str) -> tuple[str, str]:
        products = self.products_js()
        pattern  = re.compile(r'const\s+PRODUCTS\s*=\s*\[[\s\S]*?\];')
        if pattern.search(original):
            return pattern.sub(products, original, count=1), "PRODUCTS array replaced ✓"
        patched = f"/* CREVIZ ADMIN: inserted — remove any existing duplicate below */\n{products}\n\n{original}"
        return patched, "⚠ Could not locate PRODUCTS array — prepended to file, review manually."


# ──────────────────────────────────────────────────────────────────────────────
# STYLED WIDGETS
# ──────────────────────────────────────────────────────────────────────────────
def styled_btn(parent, text, cmd, color=FIRE_ORANGE, fg="#fff",
               width=None, small=False, state="normal"):
    kw = dict(text=text, command=cmd, fg=fg, bg=color,
              activeforeground=fg, activebackground=color,
              relief="flat", bd=0, cursor="hand2",
              font=("Helvetica", 9 if small else 10, "bold"),
              padx=14 if small else 18, pady=5 if small else 8,
              state=state)
    if width: kw["width"] = width
    btn = tk.Button(parent, **kw)
    if state == "normal":
        btn.bind("<Enter>", lambda e: btn.config(bg=_lighten(color)))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn

def _lighten(hex_color: str) -> str:
    h = hex_color.lstrip("#")
    r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f"#{min(255,r+25):02x}{min(255,g+20):02x}{min(255,b+20):02x}"

def entry_widget(parent, textvariable=None, width=38):
    return tk.Entry(parent, textvariable=textvariable, width=width,
                    bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
                    relief="flat", bd=0, font=("Helvetica",10),
                    highlightthickness=1, highlightbackground=BORDER,
                    highlightcolor=FIRE_ORANGE)

def text_widget(parent, height=4, width=52):
    return tk.Text(parent, height=height, width=width,
                   bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
                   relief="flat", bd=0, font=("Helvetica",10),
                   wrap="word", highlightthickness=1,
                   highlightbackground=BORDER, highlightcolor=FIRE_ORANGE, spacing3=2)

def combo_widget(parent, values, textvariable=None, width=28):
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Dark.TCombobox",
        fieldbackground=BG_INPUT, background=BG_INPUT,
        foreground=TEXT_MAIN, selectbackground=BG_INPUT,
        selectforeground=TEXT_MAIN, arrowcolor=FIRE_ORANGE,
        bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER)
    return ttk.Combobox(parent, values=values, textvariable=textvariable,
                        width=width, state="readonly", style="Dark.TCombobox",
                        font=("Helvetica",10))

def section_label(parent, text):
    f = tk.Frame(parent, bg=BG_DARK)
    tk.Label(f, text=text, bg=BG_DARK, fg=FIRE_ORANGE,
             font=("Helvetica",10,"bold")).pack(side="left")
    tk.Frame(f, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, padx=(8,0), pady=6)
    return f

def scrolled_frame(parent):
    outer  = tk.Frame(parent, bg=BG_DARK)
    canvas = tk.Canvas(outer, bg=BG_DARK, bd=0, highlightthickness=0)
    vsb    = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    inner  = tk.Frame(canvas, bg=BG_DARK)
    win_id = canvas.create_window((0,0), window=inner, anchor="nw")
    def _cfg(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(win_id, width=canvas.winfo_width())
    inner.bind("<Configure>", _cfg)
    canvas.bind("<Configure>", _cfg)
    canvas.bind_all("<MouseWheel>",
                    lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    return outer, inner


# ──────────────────────────────────────────────────────────────────────────────
# PROJECT FORM DIALOG
# ──────────────────────────────────────────────────────────────────────────────
class ProjectDialog(tk.Toplevel):
    def __init__(self, parent, store: DataStore, project=None, on_save=None):
        super().__init__(parent)
        self.store   = store
        self.project = project
        self.on_save = on_save
        self.title("Edit Project" if project else "Add Project")
        self.configure(bg=BG_DARK)
        self.geometry("620x600")
        self.resizable(True, True)
        self.grab_set()
        self._build()
        if project: self._populate()

    def _build(self):
        hdr = tk.Frame(self, bg=BG_MID, pady=12)
        hdr.pack(fill="x")
        tk.Label(hdr, text=("✏  Edit Project" if self.project else "＋  Add New Project"),
                 bg=BG_MID, fg=TEXT_MAIN, font=("Helvetica",13,"bold")).pack(padx=20, side="left")
        outer, inner = scrolled_frame(self)
        outer.pack(fill="both", expand=True)
        pad = dict(padx=20, pady=6)

        section_label(inner,"Project Title *").pack(fill="x",**pad)
        self.v_title = tk.StringVar()
        entry_widget(inner, self.v_title, width=55).pack(fill="x", **pad)

        row = tk.Frame(inner, bg=BG_DARK); row.pack(fill="x", **pad)
        lf  = tk.Frame(row, bg=BG_DARK);  lf.pack(side="left", fill="x", expand=True, padx=(0,8))
        section_label(lf,"Category *").pack(fill="x")
        self.v_cat = tk.StringVar(value="environment")
        combo_widget(lf, list(CAT_LABELS_PROJ.keys()), self.v_cat, width=22).pack(fill="x", pady=4)
        rf = tk.Frame(row, bg=BG_DARK);   rf.pack(side="left", fill="x", expand=True)
        section_label(rf,"Gradient Style").pack(fill="x")
        self.v_grad = tk.StringVar(value="env-gradient")
        combo_widget(rf, GRADIENT_OPTIONS, self.v_grad, width=22).pack(fill="x", pady=4)

        section_label(inner,"Description *").pack(fill="x",**pad)
        self.w_desc = text_widget(inner, height=4, width=55)
        self.w_desc.pack(fill="x", **pad)

        section_label(inner,"Font Awesome Icon Class").pack(fill="x",**pad)
        self.v_icon = tk.StringVar(value="fa-solid fa-cube")
        entry_widget(inner, self.v_icon, width=55).pack(fill="x", **pad)

        section_label(inner,"Image Path / URL (optional)").pack(fill="x",**pad)
        ir = tk.Frame(inner, bg=BG_DARK); ir.pack(fill="x", **pad)
        self.v_image = tk.StringVar()
        entry_widget(ir, self.v_image, width=44).pack(side="left", fill="x", expand=True)
        styled_btn(ir,"Browse",self._browse_image,color=BG_CARD,small=True).pack(side="left",padx=(6,0))

        section_label(inner,"Tools Used (comma-separated)").pack(fill="x",**pad)
        self.v_tools = tk.StringVar()
        entry_widget(inner, self.v_tools, width=55).pack(fill="x", **pad)
        tk.Label(inner,text="e.g.  Blender, ZBrush, Substance Painter",
                 bg=BG_DARK,fg=TEXT_MUTED,font=("Helvetica",8)).pack(anchor="w",padx=20)

        foot = tk.Frame(self, bg=BG_MID, pady=10); foot.pack(fill="x", side="bottom")
        styled_btn(foot,"Cancel",self.destroy,color=BG_CARD,fg=TEXT_MUTED,small=True).pack(side="right",padx=(0,12))
        styled_btn(foot,"💾  Save Project",self._save,small=True).pack(side="right",padx=(0,8))

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
            filetypes=[("Image files","*.png *.jpg *.jpeg *.webp"),("All","*.*")])
        if path: self.v_image.set(path)

    def _save(self):
        title = self.v_title.get().strip()
        desc  = self.w_desc.get("1.0","end").strip()
        if not title: messagebox.showerror("Validation","Project title is required.",parent=self); return
        if not desc:  messagebox.showerror("Validation","Description is required.",parent=self);   return
        tools = [t.strip() for t in self.v_tools.get().split(",") if t.strip()]
        image = self.v_image.get().strip() or None
        data  = dict(title=title, category=self.v_cat.get(), desc=desc,
                     icon=self.v_icon.get().strip() or "fa-solid fa-cube",
                     gradient=self.v_grad.get(), tools=tools, image=image)
        if self.project:
            self.project.update(data)
        else:
            nid = max((p["id"] for p in self.store.projects), default=0) + 1
            self.store.projects.append({"id": nid, **data})
        self.store.save()
        if self.on_save: self.on_save()
        self.destroy()


# ──────────────────────────────────────────────────────────────────────────────
# MARKET ASSET FORM DIALOG
# ──────────────────────────────────────────────────────────────────────────────
class MarketDialog(tk.Toplevel):
    def __init__(self, parent, store: DataStore, asset=None, on_save=None):
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
        if asset: self._populate()

    def _build(self):
        hdr = tk.Frame(self, bg=BG_MID, pady=12); hdr.pack(fill="x")
        tk.Label(hdr, text=("✏  Edit Asset" if self.asset else "＋  Add New Asset"),
                 bg=BG_MID, fg=TEXT_MAIN, font=("Helvetica",13,"bold")).pack(padx=20, side="left")
        outer, inner = scrolled_frame(self)
        outer.pack(fill="both", expand=True)
        pad = dict(padx=20, pady=5)

        row = tk.Frame(inner, bg=BG_DARK); row.pack(fill="x", **pad)
        lf  = tk.Frame(row, bg=BG_DARK);  lf.pack(side="left", fill="x", expand=True, padx=(0,8))
        section_label(lf,"Title *").pack(fill="x")
        self.v_title = tk.StringVar()
        entry_widget(lf, self.v_title, width=28).pack(fill="x", pady=4)
        rf  = tk.Frame(row, bg=BG_DARK);  rf.pack(side="left", fill="x", expand=True)
        section_label(rf,"Category *").pack(fill="x")
        self.v_cat = tk.StringVar(value="character")
        combo_widget(rf, list(CAT_LABELS_MKT.keys()), self.v_cat, width=22).pack(fill="x", pady=4)

        section_label(inner,"Description *").pack(fill="x",**pad)
        self.w_desc = text_widget(inner, height=3, width=60); self.w_desc.pack(fill="x",**pad)

        row2 = tk.Frame(inner, bg=BG_DARK); row2.pack(fill="x", **pad)
        for label, attr, _ in [
            ("Price ₹ (0=free)","v_price","1499"),
            ("Original Price ₹","v_orig","1999"),
            ("Reviews","v_reviews","42"),
            ("Downloads","v_dl","318"),
        ]:
            f = tk.Frame(row2, bg=BG_DARK); f.pack(side="left", fill="x", expand=True, padx=(0,6))
            tk.Label(f, text=label, bg=BG_DARK, fg=TEXT_MUTED, font=("Helvetica",8,"bold")).pack(anchor="w")
            setattr(self, attr, tk.StringVar())
            entry_widget(f, getattr(self,attr), width=10).pack(fill="x", pady=2)

        row3 = tk.Frame(inner, bg=BG_DARK); row3.pack(fill="x", **pad)
        for label, attr, vals in [
            ("Rating","v_rating",["5","4","3","2","1"]),
            ("Featured","v_featured",["Yes","No"]),
        ]:
            f = tk.Frame(row3, bg=BG_DARK); f.pack(side="left", fill="x", expand=True, padx=(0,6))
            section_label(f, label).pack(fill="x")
            setattr(self, attr, tk.StringVar(value=vals[0]))
            combo_widget(f, vals, getattr(self,attr), width=10).pack(fill="x", pady=4)
        rf3 = tk.Frame(row3, bg=BG_DARK); rf3.pack(side="left", fill="x", expand=True)
        section_label(rf3,"Date Added").pack(fill="x")
        self.v_date = tk.StringVar(value=str(date.today()))
        entry_widget(rf3, self.v_date, width=14).pack(fill="x", pady=4)

        section_label(inner,"Font Awesome Icon Class").pack(fill="x",**pad)
        self.v_icon = tk.StringVar(value="fa-solid fa-cube")
        entry_widget(inner, self.v_icon, width=55).pack(fill="x", **pad)

        section_label(inner,"Image Path / URL (optional)").pack(fill="x",**pad)
        irow = tk.Frame(inner, bg=BG_DARK); irow.pack(fill="x",**pad)
        self.v_image = tk.StringVar()
        entry_widget(irow, self.v_image, width=44).pack(side="left", fill="x", expand=True)
        styled_btn(irow,"Browse",self._browse_image,color=BG_CARD,small=True).pack(side="left",padx=(6,0))

        for label, attr in [
            ("Software (comma-separated)","v_software"),
            ("File Formats (comma-separated)","v_formats"),
            ("Badges  (new · hot · sale · free)","v_badges"),
        ]:
            section_label(inner, label).pack(fill="x", **pad)
            setattr(self, attr, tk.StringVar())
            entry_widget(inner, getattr(self,attr), width=55).pack(fill="x", **pad)

        foot = tk.Frame(self, bg=BG_MID, pady=10); foot.pack(fill="x", side="bottom")
        styled_btn(foot,"Cancel",self.destroy,color=BG_CARD,fg=TEXT_MUTED,small=True).pack(side="right",padx=(0,12))
        styled_btn(foot,"💾  Save Asset",self._save,small=True).pack(side="right",padx=(0,8))

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
            filetypes=[("Image files","*.png *.jpg *.jpeg *.webp"),("All","*.*")])
        if path: self.v_image.set(path)

    def _parse_list(self, attr):
        return [x.strip() for x in getattr(self,attr).get().split(",") if x.strip()]

    def _save(self):
        title = self.v_title.get().strip()
        desc  = self.w_desc.get("1.0","end").strip()
        if not title: messagebox.showerror("Validation","Asset title is required.",parent=self); return
        if not desc:  messagebox.showerror("Validation","Description is required.",parent=self);  return
        def to_int(v, d=0):
            try: return int(v.get().strip())
            except: return d
        orig_raw = self.v_orig.get().strip()
        orig     = int(orig_raw) if orig_raw.isdigit() else None
        data = dict(title=title, category=self.v_cat.get(), desc=desc,
                    price=to_int(self.v_price), originalPrice=orig,
                    rating=to_int(self.v_rating,5), reviews=to_int(self.v_reviews),
                    downloads=to_int(self.v_dl),
                    dateAdded=self.v_date.get().strip() or str(date.today()),
                    icon=self.v_icon.get().strip() or "fa-solid fa-cube",
                    featured=self.v_featured.get()=="Yes",
                    image=self.v_image.get().strip() or None,
                    software=self._parse_list("v_software"),
                    formats=self._parse_list("v_formats"),
                    badges=self._parse_list("v_badges"))
        if self.asset:
            self.asset.update(data)
        else:
            nid = max((m["id"] for m in self.store.market), default=0) + 1
            self.store.market.append({"id":nid, **data})
        self.store.save()
        if self.on_save: self.on_save()
        self.destroy()


# ──────────────────────────────────────────────────────────────────────────────
# CARD ROW WIDGET
# ──────────────────────────────────────────────────────────────────────────────
class CardRow(tk.Frame):
    def __init__(self, parent, item, on_edit, on_delete, on_duplicate,
                 is_market=False, **kwargs):
        super().__init__(parent, bg=BG_CARD, **kwargs)
        self.configure(highlightthickness=1, highlightbackground=BORDER)
        self._build(item, on_edit, on_delete, on_duplicate, is_market)
        self.bind("<Enter>", lambda e: self.config(highlightbackground=FIRE_ORANGE))
        self.bind("<Leave>", lambda e: self.config(highlightbackground=BORDER))

    def _build(self, item, on_edit, on_delete, on_duplicate, is_market):
        bar_color = {"environment":FIRE_ORANGE,"character":FIRE_RED,
                     "prop":FIRE_YELLOW,"texture":BLUE,"vehicle":GREEN
                     }.get(item.get("category",""), FIRE_ORANGE)
        tk.Frame(self, bg=bar_color, width=4).pack(side="left", fill="y")
        body = tk.Frame(self, bg=BG_CARD, padx=12, pady=8)
        body.pack(side="left", fill="both", expand=True)
        top = tk.Frame(body, bg=BG_CARD); top.pack(fill="x")
        tk.Label(top, text=item.get("title","—"), bg=BG_CARD, fg=TEXT_MAIN,
                 font=("Helvetica",11,"bold")).pack(side="left")
        tk.Label(top, text=f"  {cat_label(item.get('category',''), mkt=is_market)}",
                 bg=BG_CARD, fg=FIRE_ORANGE, font=("Helvetica",8,"bold")).pack(side="left", padx=6)
        if is_market:
            price = item.get("price",0)
            tk.Label(top, text="Free" if price==0 else f"₹{price:,}",
                     bg=BG_CARD, fg=GREEN if price==0 else FIRE_YELLOW,
                     font=("Helvetica",10,"bold")).pack(side="right", padx=6)
        desc  = (item.get("desc","") or "")
        short = desc[:110] + ("…" if len(desc)>110 else "")
        tk.Label(body, text=short, bg=BG_CARD, fg=TEXT_MUTED,
                 font=("Helvetica",9), wraplength=540, justify="left"
                 ).pack(anchor="w", pady=(2,4))
        chips = item.get("tools") or item.get("software") or []
        if chips:
            cr = tk.Frame(body, bg=BG_CARD); cr.pack(anchor="w")
            for c in chips[:6]:
                tk.Label(cr, text=c, bg=BG_MID, fg=TEXT_MUTED,
                         font=("Helvetica",8), padx=6, pady=2).pack(side="left", padx=(0,4))
        btn_row = tk.Frame(self, bg=BG_CARD, pady=8, padx=8)
        btn_row.pack(side="right", fill="y")
        styled_btn(btn_row,"✏ Edit",     on_edit,     color="#2a1e14",fg=FIRE_ORANGE,small=True).pack(fill="x",pady=2)
        styled_btn(btn_row,"⎘ Duplicate",on_duplicate,color="#141c28",fg=BLUE,       small=True).pack(fill="x",pady=2)
        styled_btn(btn_row,"🗑 Delete",  on_delete,   color="#2a1414",fg=RED_ERR,     small=True).pack(fill="x",pady=2)


# ──────────────────────────────────────────────────────────────────────────────
# COMMIT MESSAGE DIALOG
# ──────────────────────────────────────────────────────────────────────────────
class CommitDialog(tk.Toplevel):
    def __init__(self, parent, on_confirm):
        super().__init__(parent)
        self.on_confirm = on_confirm
        self.title("Git Commit")
        self.configure(bg=BG_DARK)
        self.geometry("480x240")
        self.resizable(False, False)
        self.grab_set()
        self._build()

    def _build(self):
        tk.Label(self, text="📝  Commit Message", bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",13,"bold")).pack(padx=24, pady=(20,8), anchor="w")
        tk.Label(self,
                 text="Write a clear, descriptive commit message.\nPress Ctrl+Enter or click Commit.",
                 bg=BG_DARK, fg=TEXT_MUTED, font=("Helvetica",9)).pack(padx=24, anchor="w")
        self.msg_var = tk.StringVar()
        e = entry_widget(self, self.msg_var, width=52)
        e.pack(padx=24, pady=12, fill="x")
        e.focus_set()
        e.bind("<Return>", lambda _: self._commit())

        # quick preset buttons
        presets = tk.Frame(self, bg=BG_DARK); presets.pack(padx=24, anchor="w")
        tk.Label(presets, text="Quick:", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",8)).pack(side="left", padx=(0,6))
        for label in ["feat: update portfolio", "fix: bug fix", "chore: update assets",
                      "style: UI improvements"]:
            styled_btn(presets, label,
                       lambda l=label: self.msg_var.set(l),
                       color=BG_CARD, fg=TEXT_MUTED, small=True
                       ).pack(side="left", padx=2)

        foot = tk.Frame(self, bg=BG_MID, pady=10); foot.pack(fill="x", side="bottom")
        styled_btn(foot,"Cancel",self.destroy,color=BG_CARD,fg=TEXT_MUTED,small=True).pack(side="right",padx=(0,12))
        styled_btn(foot,"✔  Commit",self._commit,color=FIRE_ORANGE,small=True).pack(side="right",padx=(0,8))

    def _commit(self):
        msg = self.msg_var.get().strip()
        if not msg:
            messagebox.showerror("Empty message",
                                 "Please enter a commit message.", parent=self); return
        self.destroy()
        self.on_confirm(msg)


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

        self.store        = DataStore()
        self.proj_search  = tk.StringVar()
        self.proj_cat_f   = tk.StringVar(value="All")
        self.mkt_search   = tk.StringVar()
        self.mkt_cat_f    = tk.StringVar(value="All")
        self.repo_path    = tk.StringVar(value=os.getcwd())

        self.proj_search.trace_add("write", lambda *_: self._refresh_projects())
        self.proj_cat_f.trace_add("write",  lambda *_: self._refresh_projects())
        self.mkt_search.trace_add("write",  lambda *_: self._refresh_market())
        self.mkt_cat_f.trace_add("write",   lambda *_: self._refresh_market())

        # File patch state
        self._index_content = None
        self._js_content    = None

        self._build_ui()
        self._refresh_all()

    # ── UI ────────────────────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        container = tk.Frame(self, bg=BG_DARK)
        container.pack(fill="both", expand=True)
        self._build_sidebar(container)
        self._build_main(container)

    def _build_header(self):
        hdr = tk.Frame(self, bg=BG_MID, height=56,
                       highlightthickness=1, highlightbackground=BORDER)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        logo = tk.Frame(hdr, bg=BG_MID); logo.pack(side="left", padx=18, pady=8)
        tk.Label(logo, text="⬡", bg=FIRE_ORANGE, fg="#fff",
                 font=("Helvetica",14,"bold"), padx=6, pady=2).pack(side="left")
        tk.Label(logo, text="  Creviz Studio", bg=BG_MID, fg=TEXT_MAIN,
                 font=("Helvetica",13,"bold")).pack(side="left")
        tk.Label(logo, text=" ADMIN", bg=BG_DARK, fg=FIRE_ORANGE,
                 font=("Helvetica",8,"bold"), padx=6, pady=2).pack(side="left", padx=6)
        right = tk.Frame(hdr, bg=BG_MID); right.pack(side="right", padx=16)
        styled_btn(right,"💾  Save & Export",self._save_and_export,small=True).pack(side="right",padx=(6,0))
        styled_btn(right,"🔗  Open Site",lambda: webbrowser.open("index.html"),
                   color=BG_CARD,fg=TEXT_MUTED,small=True).pack(side="right",padx=(0,6))

    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=BG_MID, width=210,
                      highlightthickness=1, highlightbackground=BORDER)
        sb.pack(side="left", fill="y"); sb.pack_propagate(False)
        tk.Label(sb, text="NAVIGATION", bg=BG_MID, fg=TEXT_MUTED,
                 font=("Helvetica",8,"bold")).pack(anchor="w", padx=16, pady=(18,6))
        self._nav_btns = []
        pages = [
            ("📊  Dashboard",    "dashboard"),
            ("🖼  Portfolio",    "portfolio"),
            ("🛒  Marketplace",  "marketplace"),
            ("💻  Export Code",  "export"),
            ("🔀  Git & Deploy", "git"),
            ("⚙  Settings",     "settings"),
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
        styled_btn(sb,"↗  Portfolio Site", lambda: webbrowser.open("index.html"),
                   color=BG_MID,fg=TEXT_MUTED,small=True).pack(fill="x",padx=8,pady=2)
        styled_btn(sb,"↗  Marketplace",    lambda: webbrowser.open("marketplace.html"),
                   color=BG_MID,fg=TEXT_MUTED,small=True).pack(fill="x",padx=8,pady=2)

    def _build_main(self, parent):
        self._main   = tk.Frame(parent, bg=BG_DARK)
        self._main.pack(side="left", fill="both", expand=True)
        self._panels = {}
        for name in ["dashboard","portfolio","marketplace","export","git","settings"]:
            f = tk.Frame(self._main, bg=BG_DARK)
            self._panels[name] = f
        self._build_dashboard(self._panels["dashboard"])
        self._build_portfolio(self._panels["portfolio"])
        self._build_marketplace(self._panels["marketplace"])
        self._build_export(self._panels["export"])
        self._build_git(self._panels["git"])
        self._build_settings(self._panels["settings"])
        self._current_panel = "dashboard"
        self._panels["dashboard"].pack(fill="both", expand=True)

    def _switch_panel(self, name: str):
        self._panels[self._current_panel].pack_forget()
        self._current_panel = name
        self._panels[name].pack(fill="both", expand=True)
        for key, btn in self._nav_btns:
            btn.config(
                bg=BG_DARK if key==name else BG_MID,
                fg=FIRE_ORANGE if key==name else TEXT_MUTED,
                font=("Helvetica",10,"bold" if key==name else "normal"))
        if name == "export":    self._refresh_export()
        if name == "dashboard": self._refresh_dashboard()
        if name == "git":       self._git_auto_status()

    # ─────────────────────────────────────────────────────────────
    # DASHBOARD
    # ─────────────────────────────────────────────────────────────
    def _build_dashboard(self, parent):
        hdr = tk.Frame(parent, bg=BG_DARK, pady=16); hdr.pack(fill="x", padx=24)
        tk.Label(hdr, text="📊  Dashboard", bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",16,"bold")).pack(side="left")
        self._stat_frame = tk.Frame(parent, bg=BG_DARK)
        self._stat_frame.pack(fill="x", padx=24, pady=(0,18))
        self._stat_labels = {}
        for key, ico, label, color in [
            ("total_proj","🖼","Portfolio Projects",FIRE_ORANGE),
            ("total_mkt", "🛒","Marketplace Assets",FIRE_RED),
            ("envs",      "🌍","Environments",      BLUE),
            ("chars",     "🧍","Characters",        GREEN),
        ]:
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
        qa = tk.Frame(parent, bg=BG_DARK, padx=24); qa.pack(fill="x", pady=(0,18))
        tk.Label(qa, text="⚡  Quick Actions", bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",11,"bold")).pack(anchor="w", pady=(0,8))
        btns = tk.Frame(qa, bg=BG_DARK); btns.pack(anchor="w")
        styled_btn(btns,"＋  Add Project",
                   lambda:(self._switch_panel("portfolio"),self._add_project())
                   ).pack(side="left",padx=(0,8))
        styled_btn(btns,"＋  Add Asset",
                   lambda:(self._switch_panel("marketplace"),self._add_market()),
                   color=BG_CARD,fg=TEXT_MUTED
                   ).pack(side="left",padx=(0,8))
        styled_btn(btns,"💾  Save & Export",
                   self._save_and_export,color=GREEN,fg=BG_DARK
                   ).pack(side="left",padx=(0,8))
        styled_btn(btns,"🔀  Git & Deploy",
                   lambda:self._switch_panel("git"),
                   color=PURPLE,fg="#fff"
                   ).pack(side="left")
        tk.Label(parent, text="🕐  Recent Projects", bg=BG_DARK, fg=TEXT_MAIN,
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
        for w in self._recent_inner.winfo_children(): w.destroy()
        for p in self.store.projects[:6]:
            row = tk.Frame(self._recent_inner, bg=BG_CARD, pady=8, padx=12,
                           highlightthickness=1, highlightbackground=BORDER)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=p["title"], bg=BG_CARD, fg=TEXT_MAIN,
                     font=("Helvetica",10,"bold")).pack(side="left")
            tk.Label(row, text=f"  {cat_label(p['category'])}", bg=BG_CARD, fg=FIRE_ORANGE,
                     font=("Helvetica",9)).pack(side="left")
            styled_btn(row,"Edit",
                       lambda pid=p["id"]:(self._switch_panel("portfolio"),
                                           self._edit_project_by_id(pid)),
                       color=BG_MID,fg=FIRE_ORANGE,small=True
                       ).pack(side="right")

    # ─────────────────────────────────────────────────────────────
    # PORTFOLIO
    # ─────────────────────────────────────────────────────────────
    def _build_portfolio(self, parent):
        hdr = tk.Frame(parent, bg=BG_DARK, pady=14); hdr.pack(fill="x", padx=24)
        tk.Label(hdr, text="🖼  Portfolio Projects", bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",15,"bold")).pack(side="left")
        styled_btn(hdr,"＋  Add Project",self._add_project,small=True).pack(side="right")
        tb = tk.Frame(parent, bg=BG_DARK, padx=24); tb.pack(fill="x", pady=(0,10))
        tk.Label(tb, text="🔍", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",11)).pack(side="left")
        entry_widget(tb, self.proj_search, width=30).pack(side="left", padx=(4,12))
        tk.Label(tb, text="Category:", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",9)).pack(side="left")
        combo_widget(tb, ["All"]+list(CAT_LABELS_PROJ.keys()),
                     self.proj_cat_f, width=16).pack(side="left", padx=6)
        outer, self._proj_list = scrolled_frame(parent)
        outer.pack(fill="both", expand=True, padx=24, pady=(0,12))

    def _refresh_projects(self):
        for w in self._proj_list.winfo_children(): w.destroy()
        q   = self.proj_search.get().lower()
        cat = self.proj_cat_f.get()
        items = [p for p in self.store.projects
                 if (not q or q in p["title"].lower() or q in p["desc"].lower())
                 and (cat=="All" or p["category"]==cat)]
        if not items:
            tk.Label(self._proj_list, text="No projects found.", bg=BG_DARK,
                     fg=TEXT_MUTED, font=("Helvetica",11)).pack(pady=40); return
        for p in items:
            CardRow(self._proj_list, p,
                    on_edit=lambda pid=p["id"]: self._edit_project_by_id(pid),
                    on_delete=lambda pid=p["id"]: self._delete_project(pid),
                    on_duplicate=lambda pid=p["id"]: self._dup_project(pid),
                    ).pack(fill="x", pady=4)

    def _add_project(self):
        ProjectDialog(self, self.store, on_save=self._refresh_all)

    def _edit_project_by_id(self, pid):
        p = next((x for x in self.store.projects if x["id"]==pid), None)
        if p: ProjectDialog(self, self.store, project=p, on_save=self._refresh_all)

    def _delete_project(self, pid):
        p = next((x for x in self.store.projects if x["id"]==pid), None)
        if p and messagebox.askyesno("Delete",f'Delete "{p["title"]}"?',parent=self):
            self.store.projects = [x for x in self.store.projects if x["id"]!=pid]
            self.store.save(); self._refresh_all()

    def _dup_project(self, pid):
        p = next((x for x in self.store.projects if x["id"]==pid), None)
        if not p: return
        clone = deepcopy(p)
        clone["id"]    = max((x["id"] for x in self.store.projects), default=0)+1
        clone["title"] = p["title"]+" (Copy)"
        self.store.projects.append(clone)
        self.store.save(); self._refresh_all()

    # ─────────────────────────────────────────────────────────────
    # MARKETPLACE
    # ─────────────────────────────────────────────────────────────
    def _build_marketplace(self, parent):
        hdr = tk.Frame(parent, bg=BG_DARK, pady=14); hdr.pack(fill="x", padx=24)
        tk.Label(hdr, text="🛒  Marketplace Assets", bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",15,"bold")).pack(side="left")
        styled_btn(hdr,"＋  Add Asset",self._add_market,small=True).pack(side="right")
        tb = tk.Frame(parent, bg=BG_DARK, padx=24); tb.pack(fill="x", pady=(0,10))
        tk.Label(tb, text="🔍", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",11)).pack(side="left")
        entry_widget(tb, self.mkt_search, width=30).pack(side="left", padx=(4,12))
        tk.Label(tb, text="Category:", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",9)).pack(side="left")
        combo_widget(tb, ["All"]+list(CAT_LABELS_MKT.keys()),
                     self.mkt_cat_f, width=16).pack(side="left", padx=6)
        outer, self._mkt_list = scrolled_frame(parent)
        outer.pack(fill="both", expand=True, padx=24, pady=(0,12))

    def _refresh_market(self):
        for w in self._mkt_list.winfo_children(): w.destroy()
        q   = self.mkt_search.get().lower()
        cat = self.mkt_cat_f.get()
        items = [m for m in self.store.market
                 if (not q or q in m["title"].lower() or q in m["desc"].lower())
                 and (cat=="All" or m["category"]==cat)]
        if not items:
            tk.Label(self._mkt_list, text="No assets found.", bg=BG_DARK,
                     fg=TEXT_MUTED, font=("Helvetica",11)).pack(pady=40); return
        for m in items:
            CardRow(self._mkt_list, m,
                    on_edit=lambda mid=m["id"]: self._edit_market_by_id(mid),
                    on_delete=lambda mid=m["id"]: self._delete_market(mid),
                    on_duplicate=lambda mid=m["id"]: self._dup_market(mid),
                    is_market=True).pack(fill="x", pady=4)

    def _add_market(self):
        MarketDialog(self, self.store, on_save=self._refresh_all)

    def _edit_market_by_id(self, mid):
        m = next((x for x in self.store.market if x["id"]==mid), None)
        if m: MarketDialog(self, self.store, asset=m, on_save=self._refresh_all)

    def _delete_market(self, mid):
        m = next((x for x in self.store.market if x["id"]==mid), None)
        if m and messagebox.askyesno("Delete",f'Delete "{m["title"]}"?',parent=self):
            self.store.market = [x for x in self.store.market if x["id"]!=mid]
            self.store.save(); self._refresh_all()

    def _dup_market(self, mid):
        m = next((x for x in self.store.market if x["id"]==mid), None)
        if not m: return
        clone = deepcopy(m)
        clone["id"]    = max((x["id"] for x in self.store.market), default=0)+1
        clone["title"] = m["title"]+" (Copy)"
        self.store.market.append(clone)
        self.store.save(); self._refresh_all()

    # ─────────────────────────────────────────────────────────────
    # EXPORT
    # ─────────────────────────────────────────────────────────────
    def _build_export(self, parent):
        hdr = tk.Frame(parent, bg=BG_DARK, pady=14); hdr.pack(fill="x", padx=24)
        tk.Label(hdr, text="💻  Export & Patch Files", bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",15,"bold")).pack(side="left")
        styled_btn(hdr,"🔄  Regenerate",self._refresh_export,small=True).pack(side="right")
        outer, inner = scrolled_frame(parent)
        outer.pack(fill="both", expand=True, padx=24, pady=(0,12))

        self._build_export_section(inner,
            "🖼  Portfolio Projects HTML",
            'Paste inside  <div class="projects-grid" id="portfolioGrid">  in index.html',
            "_port_code")
        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=16)
        self._build_export_section(inner,
            "🛒  Marketplace Products JS",
            "Replace the entire  const PRODUCTS = [...]  array in marketplace.js",
            "_mkt_code")
        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=16)
        self._build_patch_section(inner,
            "🔧  Patch  index.html  directly",
            'Upload your current index.html — replaces <div id="portfolioGrid"> automatically.',
            "📂  Upload index.html", [("HTML","*.html *.htm"),("All","*.*")],
            "_index_content","_index_name","_index_status_lbl",
            "⬇  Download Patched index.html", self._patch_and_download_index,
            "_index_dl_btn", FIRE_ORANGE)
        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=16)
        self._build_patch_section(inner,
            "🔧  Patch  marketplace.js  directly",
            "Upload your current marketplace.js — replaces const PRODUCTS = [...] automatically.",
            "📂  Upload marketplace.js", [("JS","*.js"),("All","*.*")],
            "_js_content","_js_name","_js_status_lbl",
            "⬇  Download Patched marketplace.js", self._patch_and_download_js,
            "_js_dl_btn", FIRE_YELLOW)

    def _build_export_section(self, parent, title, subtitle, code_attr):
        tk.Label(parent, text=title, bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",12,"bold")).pack(anchor="w", pady=(0,2))
        tk.Label(parent, text=subtitle, bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",9)).pack(anchor="w", pady=(0,8))
        frame = tk.Frame(parent, bg=BG_MID, highlightthickness=1,
                         highlightbackground=BORDER)
        frame.pack(fill="x", pady=(0,6))
        cr = tk.Frame(frame, bg=BG_MID); cr.pack(fill="x", padx=8, pady=(6,0))
        styled_btn(cr,"⎘  Copy to Clipboard",
                   lambda a=code_attr: self._copy_code(a),
                   color=BG_CARD,fg=FIRE_ORANGE,small=True).pack(side="right")
        ct = tk.Text(frame, height=10, bg="#0a0806", fg="#f0ece8",
                     insertbackground=TEXT_MAIN, relief="flat", bd=0,
                     font=("Courier New",9), wrap="none",
                     highlightthickness=0, padx=12, pady=8, spacing1=1)
        hsb = tk.Scrollbar(frame, orient="horizontal", command=ct.xview)
        ct.configure(xscrollcommand=hsb.set)
        ct.pack(fill="both", expand=True, padx=6, pady=4)
        hsb.pack(fill="x", padx=6, pady=(0,6))
        setattr(self, code_attr, ct)

    def _build_patch_section(self, parent, heading, desc,
                              upload_label, upload_accept,
                              upload_attr, upload_name_attr, upload_status_attr,
                              download_label, download_cmd, download_btn_attr, accent):
        box = tk.Frame(parent, bg=BG_CARD, padx=20, pady=16,
                       highlightthickness=1, highlightbackground=accent)
        box.pack(fill="x", pady=(0,8))
        tk.Label(box, text=heading, bg=BG_CARD, fg=TEXT_MAIN,
                 font=("Helvetica",12,"bold")).pack(anchor="w", pady=(0,4))
        tk.Label(box, text=desc, bg=BG_CARD, fg=TEXT_MUTED,
                 font=("Helvetica",9), justify="left").pack(anchor="w", pady=(0,10))
        warn = tk.Frame(box, bg="#1a1500", padx=10, pady=6,
                        highlightthickness=1, highlightbackground="#3a3000")
        warn.pack(fill="x", pady=(0,12))
        tk.Label(warn, text="⚠  File is read locally — never uploaded to any server.",
                 bg="#1a1500", fg=FIRE_YELLOW, font=("Helvetica",8)).pack(anchor="w")
        br = tk.Frame(box, bg=BG_CARD); br.pack(anchor="w")

        def do_upload(ua=upload_attr, una=upload_name_attr,
                      usa=upload_status_attr, dba=download_btn_attr, acc=upload_accept):
            path = filedialog.askopenfilename(title="Select file", filetypes=acc)
            if not path: return
            with open(path,"r",encoding="utf-8",errors="replace") as f:
                setattr(self, ua, f.read())
            setattr(self, una, os.path.basename(path))
            getattr(self, usa).config(text=f"✔  {os.path.basename(path)} loaded", fg=GREEN)
            dl = getattr(self, dba)
            dl.config(state="normal", bg=accent,
                      fg=BG_DARK if accent==FIRE_YELLOW else "#fff")
            dl.bind("<Enter>", lambda e: dl.config(bg=_lighten(accent)))
            dl.bind("<Leave>", lambda e: dl.config(bg=accent))

        styled_btn(br, upload_label, do_upload,
                   color=BG_MID, fg=TEXT_MAIN, small=True).pack(side="left", padx=(0,10))
        dl_btn = styled_btn(br, download_label, download_cmd,
                            color=BG_MID, fg=TEXT_MUTED, small=True, state="disabled")
        dl_btn.pack(side="left")
        setattr(self, download_btn_attr, dl_btn)
        status = tk.Label(box, text="No file uploaded yet.",
                          bg=BG_CARD, fg=TEXT_MUTED, font=("Helvetica",9))
        status.pack(anchor="w", pady=(8,0))
        setattr(self, upload_status_attr, status)

    def _patch_and_download_index(self):
        if not self._index_content:
            messagebox.showerror("No file","Please upload index.html first."); return
        patched, msg = self.store.patch_index(self._index_content)
        out = filedialog.asksaveasfilename(title="Save patched index.html",
            defaultextension=".html", initialfile="index.html",
            filetypes=[("HTML","*.html"),("All","*.*")])
        if not out: return
        with open(out,"w",encoding="utf-8") as f: f.write(patched)
        messagebox.showinfo("Done", f"{msg}\n\nSaved to:\n{out}")

    def _patch_and_download_js(self):
        if not self._js_content:
            messagebox.showerror("No file","Please upload marketplace.js first."); return
        patched, msg = self.store.patch_marketplace_js(self._js_content)
        out = filedialog.asksaveasfilename(title="Save patched marketplace.js",
            defaultextension=".js", initialfile="marketplace.js",
            filetypes=[("JavaScript","*.js"),("All","*.*")])
        if not out: return
        with open(out,"w",encoding="utf-8") as f: f.write(patched)
        messagebox.showinfo("Done", f"{msg}\n\nSaved to:\n{out}")

    def _refresh_export(self):
        for attr, getter in [("_port_code", self.store.portfolio_html),
                             ("_mkt_code",  self.store.products_js)]:
            w: tk.Text = getattr(self, attr)
            w.config(state="normal")
            w.delete("1.0","end")
            w.insert("1.0", getter())
            w.config(state="disabled")

    def _copy_code(self, attr):
        w: tk.Text = getattr(self, attr)
        w.config(state="normal")
        text = w.get("1.0","end")
        w.config(state="disabled")
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Copied","Code copied to clipboard!")

    # ─────────────────────────────────────────────────────────────
    # GIT & FIREBASE PANEL  ← NEW
    # ─────────────────────────────────────────────────────────────
    def _build_git(self, parent):
        # ── Header ───────────────────────────────────────────────
        hdr = tk.Frame(parent, bg=BG_DARK, pady=14)
        hdr.pack(fill="x", padx=24)
        tk.Label(hdr, text="🔀  Git & Firebase Deploy",
                 bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",15,"bold")).pack(side="left")

        # ── Repo path selector ───────────────────────────────────
        path_box = tk.Frame(parent, bg=BG_CARD, padx=16, pady=12,
                            highlightthickness=1, highlightbackground=BORDER)
        path_box.pack(fill="x", padx=24, pady=(0,16))
        tk.Label(path_box, text="📁  Repository / Project Folder",
                 bg=BG_CARD, fg=TEXT_MAIN,
                 font=("Helvetica",10,"bold")).pack(anchor="w", pady=(0,6))
        pr = tk.Frame(path_box, bg=BG_CARD); pr.pack(fill="x")
        entry_widget(pr, self.repo_path, width=62).pack(side="left", fill="x", expand=True)
        styled_btn(pr, "Browse", self._browse_repo,
                   color=BG_MID, fg=TEXT_MUTED, small=True
                   ).pack(side="left", padx=(8,0))
        tk.Label(path_box,
                 text="All git and firebase commands will run in this folder.",
                 bg=BG_CARD, fg=TEXT_MUTED, font=("Helvetica",8)
                 ).pack(anchor="w", pady=(6,0))

        # ── Button grid ──────────────────────────────────────────
        btn_area = tk.Frame(parent, bg=BG_DARK, padx=24)
        btn_area.pack(fill="x", pady=(0,16))

        # Row 1 — Git info commands
        tk.Label(btn_area, text="GIT INFO", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",8,"bold")).pack(anchor="w", pady=(0,6))
        row1 = tk.Frame(btn_area, bg=BG_DARK); row1.pack(fill="x", pady=(0,10))

        self._make_git_btn(row1, "📋  git status",
                           color="#1a2233", fg=BLUE,
                           cmd=lambda: self._run_git(["git","status"])).pack(side="left", padx=(0,8))
        self._make_git_btn(row1, "📜  git log",
                           color="#1a2233", fg=BLUE,
                           cmd=lambda: self._run_git(
                               ["git","log","--oneline","--graph","--decorate","-20"])
                           ).pack(side="left", padx=(0,8))
        self._make_git_btn(row1, "🔍  git diff",
                           color="#1a2233", fg=BLUE,
                           cmd=lambda: self._run_git(["git","diff","--stat"])
                           ).pack(side="left")

        # Row 2 — Git write commands
        tk.Label(btn_area, text="GIT ACTIONS", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",8,"bold")).pack(anchor="w", pady=(0,6))
        row2 = tk.Frame(btn_area, bg=BG_DARK); row2.pack(fill="x", pady=(0,10))

        self._make_git_btn(row2, "➕  git add .",
                           color="#1a2a1a", fg=GREEN,
                           cmd=lambda: self._run_git(["git","add","."]),
                           confirm="Stage ALL changes?  (git add .)"
                           ).pack(side="left", padx=(0,8))
        self._make_git_btn(row2, "✔  git commit",
                           color="#1a2a1a", fg=GREEN,
                           cmd=self._git_commit
                           ).pack(side="left", padx=(0,8))
        self._make_git_btn(row2, "⬆  git push",
                           color="#1a2a1a", fg=GREEN,
                           cmd=lambda: self._run_git(["git","push"]),
                           confirm="Push commits to remote?"
                           ).pack(side="left", padx=(0,8))
        self._make_git_btn(row2, "⬇  git pull",
                           color="#1a2a1a", fg=GREEN,
                           cmd=lambda: self._run_git(["git","pull"])
                           ).pack(side="left")

        # ── Row 3 — Firebase ──────────────────────────────────────────
        tk.Label(btn_area, text="FIREBASE", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",8,"bold")).pack(anchor="w", pady=(0,6))
        row3 = tk.Frame(btn_area, bg=BG_DARK); row3.pack(fill="x", pady=(0,10))

        self._make_git_btn(
            row3, "🚀  firebase deploy",
            color="#1a1a2a", fg=FIRE_YELLOW,
            cmd=self._firebase_deploy,
            confirm="Deploy to Firebase Hosting?\nThis will publish your site live.",
            width=22,
        ).pack(side="left", padx=(0,8))

        self._make_git_btn(
            row3, "📋  firebase hosting:channel:list",
            color="#1a1a2a", fg=FIRE_YELLOW,
            cmd=lambda: self._run_git(self._firebase_cmd("hosting:channel:list")),
        ).pack(side="left")

        # Row 4 — One-click workflow
        tk.Label(btn_area, text="ONE-CLICK WORKFLOW", bg=BG_DARK, fg=TEXT_MUTED,
                 font=("Helvetica",8,"bold")).pack(anchor="w", pady=(0,6))
        row4 = tk.Frame(btn_area, bg=BG_DARK); row4.pack(fill="x", pady=(0,4))

        self._make_git_btn(row4,
                           "⚡  Add → Commit → Push → Deploy",
                           color=FIRE_ORANGE, fg="#fff",
                           cmd=self._full_workflow,
                           confirm="Run full workflow?\n\ngit add .\ngit commit\ngit push\nfirebase deploy",
                           width=32
                           ).pack(side="left")

        # ── Terminal output ──────────────────────────────────────
        tk.Label(parent, text="🖥  Terminal Output",
                 bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",10,"bold")).pack(anchor="w", padx=24, pady=(8,4))

        term_frame = tk.Frame(parent, bg="#050403",
                              highlightthickness=1, highlightbackground=BORDER)
        term_frame.pack(fill="both", expand=True, padx=24, pady=(0,12))

        # Toolbar
        tbar = tk.Frame(term_frame, bg="#0a0806"); tbar.pack(fill="x")
        styled_btn(tbar, "🗑  Clear", self._clear_terminal,
                   color="#0a0806", fg=TEXT_MUTED, small=True).pack(side="right", padx=4, pady=3)
        styled_btn(tbar, "⎘  Copy Output", self._copy_terminal,
                   color="#0a0806", fg=TEXT_MUTED, small=True).pack(side="right", padx=4, pady=3)
        self._git_status_label = tk.Label(tbar, text="● Idle",
                                          bg="#0a0806", fg=TEXT_MUTED,
                                          font=("Courier New",9))
        self._git_status_label.pack(side="left", padx=8)

        # Output text widget
        self._terminal = tk.Text(
            term_frame, bg="#050403", fg="#c8ffa0",
            insertbackground=GREEN,
            relief="flat", bd=0,
            font=("Courier New", 10),
            wrap="word",
            highlightthickness=0,
            padx=12, pady=10,
            state="disabled",
        )
        vsb = tk.Scrollbar(term_frame, orient="vertical",
                           command=self._terminal.yview)
        self._terminal.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self._terminal.pack(fill="both", expand=True)

        # Colour tags for terminal
        self._terminal.tag_configure("cmd",     foreground=FIRE_ORANGE, font=("Courier New",10,"bold"))
        self._terminal.tag_configure("ok",      foreground=GREEN)
        self._terminal.tag_configure("err",     foreground=RED_ERR)
        self._terminal.tag_configure("info",    foreground=BLUE)
        self._terminal.tag_configure("warning", foreground=FIRE_YELLOW)
        self._terminal.tag_configure("section", foreground=PURPLE, font=("Courier New",10,"bold"))

        self._terminal_write("Creviz Studio Admin — Git & Firebase Terminal\n", "section")
        self._terminal_write(f"Working directory: {self.repo_path.get()}\n", "info")
        self._terminal_write("─" * 60 + "\n", "info")

    def _make_git_btn(self, parent, text, cmd, color, fg,
                      confirm=None, width=None):
        """Factory for terminal-action buttons with optional confirm dialog."""
        def wrapped():
            if confirm:
                if not messagebox.askyesno("Confirm", confirm, parent=self):
                    return
            cmd()
        kw = dict(text=text, command=wrapped,
                  fg=fg, bg=color,
                  activeforeground=fg, activebackground=color,
                  relief="flat", bd=0, cursor="hand2",
                  font=("Helvetica",10,"bold"),
                  padx=18, pady=10,
                  highlightthickness=1, highlightbackground=color)
        if width: kw["width"] = width
        btn = tk.Button(parent, **kw)
        btn.bind("<Enter>", lambda e: btn.config(bg=_lighten(color),
                                                  highlightbackground=fg))
        btn.bind("<Leave>", lambda e: btn.config(bg=color,
                                                  highlightbackground=color))
        return btn

    # ── Terminal helpers ──────────────────────────────────────────
    def _terminal_write(self, text: str, tag: str = ""):
        self._terminal.config(state="normal")
        if tag:
            self._terminal.insert("end", text, tag)
        else:
            self._terminal.insert("end", text)
        self._terminal.see("end")
        self._terminal.config(state="disabled")

    def _clear_terminal(self):
        self._terminal.config(state="normal")
        self._terminal.delete("1.0","end")
        self._terminal.config(state="disabled")
        self._terminal_write("Terminal cleared.\n","info")

    def _copy_terminal(self):
        self._terminal.config(state="normal")
        text = self._terminal.get("1.0","end")
        self._terminal.config(state="disabled")
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Copied","Terminal output copied to clipboard!")

    def _set_git_status(self, text: str, color: str):
        self._git_status_label.config(text=text, fg=color)

    # ── Command runner (threaded) ─────────────────────────────────
      # ── Command runner (threaded) ─────────────────────────────────
    def _run_git(self, cmd: list[str], cwd: str = None,
                 on_done=None, silent=False):
        """
        Run a shell command in a background thread, stream output to terminal.

        Key fixes for firebase / npm globals on Windows:
          1. shell=True  — lets Windows find .cmd wrappers (firebase.cmd, npm.cmd)
          2. Pass cmd as a joined string when shell=True on Windows
          3. Inherit the full parent process environment (os.environ.copy())
          4. creationflags=CREATE_NO_WINDOW hides the black console popup
        """
        cwd = cwd or self.repo_path.get().strip() or os.getcwd()

        if not silent:
            self._terminal_write(f"\n$ {' '.join(cmd)}\n", "cmd")
            self._set_git_status("● Running…", FIRE_ORANGE)

        # On Windows, npm-installed CLIs like `firebase` are .cmd batch files.
        # subprocess can only find them when shell=True.
        use_shell = sys.platform == "win32"

        # When shell=True on Windows, the command must be a single string.
        cmd_arg = " ".join(cmd) if use_shell else cmd

        def worker():
            try:
                env = os.environ.copy()   # ← inherit full PATH from the OS

                proc = subprocess.Popen(
                    cmd_arg,
                    cwd=cwd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    env=env,              # ← pass full environment
                    shell=use_shell,      # ← True on Windows, False on mac/linux
                    creationflags=(
                        subprocess.CREATE_NO_WINDOW
                        if sys.platform == "win32" else 0
                    ),
                )

                for line in proc.stdout:
                    lower = line.lower()
                    if any(w in lower for w in
                           ("error","fatal","failed","conflict","exception")):
                        tag = "err"
                    elif any(w in lower for w in ("warning","warn","deprecated")):
                        tag = "warning"
                    elif any(w in lower for w in
                             ("success","complete","done","deployed",
                              "pushed","up-to-date","hosting","live")):
                        tag = "ok"
                    else:
                        tag = ""
                    self.after(0, self._terminal_write, line, tag)

                proc.wait()
                rc = proc.returncode

                if not silent:
                    if rc == 0:
                        self.after(0, self._terminal_write,
                                   "✔  Command completed successfully (exit 0)\n", "ok")
                        self.after(0, self._set_git_status, "● Done", GREEN)
                    else:
                        self.after(0, self._terminal_write,
                                   f"✖  Command exited with code {rc}\n", "err")
                        self.after(0, self._set_git_status,
                                   f"● Error (exit {rc})", RED_ERR)

                if on_done:
                    self.after(0, on_done, rc, "")

            except FileNotFoundError:
                # More helpful message that explains the .cmd issue
                msg = (
                    f"✖  '{cmd[0]}' was not found.\n\n"
                    f"  Possible reasons:\n"
                    f"  • {cmd[0]} is not installed\n"
                    f"  • {cmd[0]} is installed but not on your system PATH\n"
                    f"  • On Windows, npm globals (firebase, node) are .cmd files —\n"
                    f"    they require shell=True to run via Python subprocess.\n\n"
                    f"  Fix: make sure '{cmd[0]}' works in a NEW cmd/terminal window.\n"
                    f"  Then restart this app so it picks up the updated PATH.\n"
                )
                self.after(0, self._terminal_write, msg, "err")
                self.after(0, self._set_git_status,
                           f"● '{cmd[0]}' not found", RED_ERR)
                if on_done:
                    self.after(0, on_done, -1, msg)

            except Exception as ex:
                msg = f"✖  Unexpected error: {ex}\n"
                self.after(0, self._terminal_write, msg, "err")
                self.after(0, self._set_git_status, "● Error", RED_ERR)
                if on_done:
                    self.after(0, on_done, -1, msg)

        threading.Thread(target=worker, daemon=True).start()

    # ── Individual git/firebase actions ──────────────────────────
    def _browse_repo(self):
        path = filedialog.askdirectory(title="Select Repository Folder",
                                       initialdir=self.repo_path.get())
        if path:
            self.repo_path.set(path)
            self._terminal_write(f"\n📁 Working directory changed to:\n   {path}\n","info")

        # ── Firebase helpers ──────────────────────────────────────────────────────
    def _firebase_cmd(self, *args) -> list[str]:
        """
        Build the correct firebase command for the current OS.

        On Windows:  firebase is firebase.cmd installed by npm into
                     %APPDATA%\\npm\\  — subprocess can't find .cmd files
                     unless we resolve the path explicitly via 'where firebase'
                     or fall back to shell=True.

        On mac/linux: it's a plain shell script on PATH — just use 'firebase'.
        """
        if sys.platform == "win32":
            # Try to locate firebase.cmd via 'where firebase'
            try:
                result = subprocess.run(
                    ["where", "firebase"],
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
                for line in result.stdout.splitlines():
                    line = line.strip()
                    if line.lower().endswith(".cmd") and os.path.isfile(line):
                        return [line] + list(args)   # e.g. ['C:\\...\\firebase.cmd', 'deploy']
            except Exception:
                pass
            # Fallback — shell=True in _run_git will handle it
            return ["firebase"] + list(args)
        else:
            # mac / linux — plain executable on PATH
            return ["firebase"] + list(args)

    def _git_auto_status(self):
        """Run git status automatically when the Git panel is opened."""
        self._terminal_write("\n─── Opened Git Panel ───\n", "section")
        self._run_git(["git", "status"])

    def _git_commit(self):
        """Open commit message dialog then run git commit."""
        def do_commit(msg: str):
            self._run_git(["git", "commit", "-m", msg])
        CommitDialog(self, on_confirm=do_commit)

    def _firebase_deploy(self):
        """Deploy to Firebase Hosting using the resolved firebase command."""
        self._terminal_write("\n🚀  Starting Firebase deployment…\n", "section")
        self._run_git(self._firebase_cmd("deploy"))   # ← uses resolved path

    def _full_workflow(self):
        """
        Sequential pipeline:
        Step 1 — git add .
        Step 2 — Commit Message Dialog → git commit -m "..."
        Step 3 — git push
        Step 4 — firebase deploy
        Each step waits for the previous; stops the chain on any failure.
        """
        def step4_deploy(rc, _):
            if rc != 0:
                self._terminal_write(
                    "⚠  Push failed — skipping Firebase deploy.\n", "warning")
                return
            self._terminal_write(
                "\n─── Step 4 / 4 — firebase deploy ───\n", "section")
            self._run_git(self._firebase_cmd("deploy"))  # ← uses resolved path

        def step3_push(msg: str):
            def after_commit(rc, _):
                if rc != 0:
                    self._terminal_write(
                        "⚠  Commit failed — skipping push & deploy.\n", "warning")
                    return
                self._terminal_write(
                    "\n─── Step 3 / 4 — git push ───\n", "section")
                self._run_git(["git", "push"], on_done=step4_deploy)
            self._run_git(["git", "commit", "-m", msg], on_done=after_commit)

        def after_add(rc, _):
            if rc != 0:
                self._terminal_write(
                    "⚠  git add failed — aborting workflow.\n", "warning")
                return
            self._terminal_write(
                "\n─── Step 2 / 4 — git commit ───\n", "section")
            CommitDialog(self, on_confirm=step3_push)

        self._terminal_write(
            "\n══════════════════════════════════════\n", "section")
        self._terminal_write(
            "⚡  FULL WORKFLOW — Add → Commit → Push → Deploy\n", "section")
        self._terminal_write(
            "══════════════════════════════════════\n", "section")
        self._terminal_write(
            "\n─── Step 1 / 4 — git add . ───\n", "section")
        self._run_git(["git", "add", "."], on_done=after_add)

    # ─────────────────────────────────────────────────────────────
    # SETTINGS
    # ─────────────────────────────────────────────────────────────
    def _build_settings(self, parent):
        hdr = tk.Frame(parent, bg=BG_DARK, pady=14); hdr.pack(fill="x", padx=24)
        tk.Label(hdr, text="⚙  Settings", bg=BG_DARK, fg=TEXT_MAIN,
                 font=("Helvetica",15,"bold")).pack(side="left")
        outer, inner = scrolled_frame(parent)
        outer.pack(fill="both", expand=True, padx=24, pady=(0,12))

        def section(title):
            tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=(18,12))
            tk.Label(inner, text=title, bg=BG_DARK, fg=FIRE_ORANGE,
                     font=("Helvetica",10,"bold")).pack(anchor="w")

        def row(label, desc, wf):
            f = tk.Frame(inner, bg=BG_CARD, padx=16, pady=12,
                         highlightthickness=1, highlightbackground=BORDER)
            f.pack(fill="x", pady=4)
            info = tk.Frame(f, bg=BG_CARD); info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=label, bg=BG_CARD, fg=TEXT_MAIN,
                     font=("Helvetica",10,"bold")).pack(anchor="w")
            tk.Label(info, text=desc, bg=BG_CARD, fg=TEXT_MUTED,
                     font=("Helvetica",8), wraplength=520, justify="left"
                     ).pack(anchor="w", pady=(2,0))
            wf(f).pack(side="right", padx=(12,0))

        section("💾  Data Management")
        row("Save to JSON now",
            f"Saves all data to  {DATA_FILE}  next to this script.",
            lambda p: styled_btn(p,"Save",self._do_save,small=True))
        row("Export JSON backup",
            "Download a full backup as a dated JSON file.",
            lambda p: styled_btn(p,"⬇  Export",self._export_json,
                                  color=BG_MID,fg=TEXT_MAIN,small=True))
        row("Import JSON backup",
            "Restore data from a previously exported JSON file.",
            lambda p: styled_btn(p,"⬆  Import",self._import_json,
                                  color=BG_MID,fg=TEXT_MAIN,small=True))
        row("Reset to defaults",
            "Permanently deletes all data and reloads built-in sample data.",
            lambda p: styled_btn(p,"⚠  Reset All",self._confirm_reset,
                                  color="#3a1414",fg=RED_ERR,small=True))

        section("🌐  Site & Deploy")
        pf = tk.Frame(inner, bg=BG_CARD, padx=16, pady=14,
                      highlightthickness=1, highlightbackground=BORDER)
        pf.pack(fill="x", pady=4)
        tk.Label(pf,
                 text="Use the  🔀 Git & Deploy  panel to run git commands and firebase deploy.\n"
                      "Set your project folder path there before running any commands.",
                 bg=BG_CARD, fg=TEXT_MUTED, font=("Helvetica",9),
                 justify="left").pack(anchor="w")

        section("ℹ  About")
        af = tk.Frame(inner, bg=BG_CARD, padx=16, pady=14,
                      highlightthickness=1, highlightbackground=BORDER)
        af.pack(fill="x", pady=4)
        for line in ["Creviz Studio — Desktop Admin Panel  v1.1",
                     "Built with Python 3  +  Tkinter  (stdlib only — zero pip installs)",
                     f"Data file:  {DATA_FILE}  (same folder as script)",
                     "","© 2026 Creviz Studio"]:
            tk.Label(af, text=line, bg=BG_CARD,
                     fg=TEXT_MAIN if ("v1.1" in line or "©" in line) else TEXT_MUTED,
                     font=("Helvetica",9,"bold" if "v1.1" in line else "normal")
                     ).pack(anchor="w")

    # ── Settings actions ──────────────────────────────────────────
    def _do_save(self):
        self.store.save()
        messagebox.showinfo("Saved", f"Data saved to {DATA_FILE}")

    def _export_json(self):
        path = filedialog.asksaveasfilename(
            title="Export JSON backup", defaultextension=".json",
            initialfile=f"creviz-backup-{date.today()}.json",
            filetypes=[("JSON","*.json"),("All","*.*")])
        if path:
            self.store.export_backup(path)
            messagebox.showinfo("Exported", f"Backup saved to:\n{path}")

    def _import_json(self):
        path = filedialog.askopenfilename(
            title="Import JSON backup",
            filetypes=[("JSON","*.json"),("All","*.*")])
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
                               "This cannot be undone. Continue?", icon="warning"):
            self.store.reset()
            self._refresh_all()
            messagebox.showinfo("Reset Complete","All data restored to defaults.")

    # ── Global ────────────────────────────────────────────────────
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
        if self._current_panel == "export": self._refresh_export()


# ──────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()