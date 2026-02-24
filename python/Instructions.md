# 🔥 Creviz Studio — Admin Panel
## Complete How-To-Use Guide

> **Two ways to manage your site:**
> - `admin.html` — runs in any browser, no installation needed
> - `creviz_admin.py` — desktop app, requires Python 3.9+

---

## 📋 Table of Contents

1. [Getting Started](#1-getting-started)
2. [admin.html — Browser Admin](#2-adminhtml--browser-admin)
3. [creviz_admin.py — Desktop Admin](#3-creviz_adminpy--desktop-admin)
4. [Dashboard](#4-dashboard)
5. [Portfolio Projects](#5-portfolio-projects)
6. [Marketplace Assets](#6-marketplace-assets)
7. [Export Code](#7-export-code)
8. [Patch Files Directly](#8-patch-files-directly)
9. [Git & Firebase Deploy](#9-git--firebase-deploy)
10. [Settings & Backups](#10-settings--backups)
11. [Project File Structure](#11-project-file-structure)
12. [FAQ & Troubleshooting](#12-faq--troubleshooting)

---

## 1. Getting Started

### Using `admin.html` (Browser)

```
No installation required.
Just open admin.html in any modern browser.
```

1. Place `admin.html` in the **root of your project folder** (same level as `index.html`)
2. Double-click `admin.html` — it opens in your browser
3. All data is saved automatically to your browser's **localStorage**
4. Use **Export Code** or **Patch Files** to apply changes to your actual site files

> ⚠️ **Important:** `admin.html` cannot write files directly to your disk.
> Use the **Export / Patch** workflow to update your site files.

---

### Using `creviz_admin.py` (Desktop App)

```
Requires Python 3.9 or higher.
No pip installs needed — uses stdlib only.
```

**Step 1 — Check Python is installed:**
```bash
python --version
# Should output: Python 3.9.x or higher
```

**Step 2 — Place the file in your project folder:**
```
your-project/
├── creviz_admin.py   ← place here
├── index.html
├── marketplace.html
├── 404.html
├── js/
│   └── marketplace.js
└── assets/
```

**Step 3 — Run it:**
```bash
python creviz_admin.py
```

> ✅ Data is saved to `creviz_data.json` in the same folder automatically.

---

## 2. `admin.html` — Browser Admin

### Opening the Panel

| Action | How |
|--------|-----|
| Open admin panel | Double-click `admin.html` |
| Navigate sections | Click items in the **left sidebar** |
| Save & go to export | Click **💾 Save & Export** in the top-right header |
| Preview your site | Click **🔗 Preview Site** in the top-right header |

### Unsaved Changes Indicator

When you make changes that haven't been exported yet, a small **🟠 orange dot**
appears next to the Save button in the header. It disappears once you save.

### Data Persistence

- All your data is stored in **browser localStorage** automatically
- Data persists between sessions as long as you use the same browser
- Use **Export JSON Backup** in Settings to keep a permanent copy
- Clearing browser data / cache will erase your admin data — always keep a JSON backup

---

## 3. `creviz_admin.py` — Desktop Admin

### Window Layout

```
┌─────────────────────────────────────────────────────────┐
│  ⬡ Creviz Studio  ADMIN        [🔗 Open Site] [💾 Save] │  ← Header
├──────────────┬──────────────────────────────────────────┤
│  NAVIGATION  │                                          │
│              │                                          │
│  📊 Dashboard│         Main Content Area               │
│  🖼 Portfolio│                                          │
│  🛒 Marketplace                                         │
│  💻 Export   │                                          │
│  🔀 Git      │                                          │
│  ⚙ Settings  │                                          │
│              │                                          │
│  LINKS       │                                          │
│  ↗ Portfolio │                                          │
│  ↗ Marketplace                                          │
└──────────────┴──────────────────────────────────────────┘
```

### Navigation

Click any item in the **left sidebar** to switch panels.
The active panel is highlighted in **orange**.

---

## 4. Dashboard

The Dashboard gives you a quick overview of all your content.

### Stat Cards

| Card | What it shows |
|------|--------------|
| 🖼 Portfolio Projects | Total number of portfolio items |
| 🛒 Marketplace Assets | Total number of marketplace products |
| 🌍 Environments | Projects with category = Environment |
| 🧍 Characters | Projects with category = Character |

### Quick Actions

| Button | What it does |
|--------|-------------|
| ＋ Add Portfolio Project | Opens the Add Project form directly |
| ＋ Add Marketplace Asset | Opens the Add Asset form directly |
| 💾 Save & Export | Saves data and switches to Export panel |
| 🔀 Git & Deploy *(desktop only)* | Jumps to the Git panel |

### Recent Projects

Shows the last **5–6 projects** with a quick **Edit** button next to each.
Click **Edit** to jump straight into that project's form.

---

## 5. Portfolio Projects

### Viewing Projects

- All projects are shown as **cards** in a grid
- Each card shows: **title**, **category badge**, **description**, **tool chips**
- Hover over a card to reveal the **fire border glow** effect

### Searching & Filtering

| Control | What it does |
|---------|-------------|
| 🔍 Search box | Filters by title or description (live, as you type) |
| Category dropdown | Filter by Environment / Character / Props & Assets |
| Sort dropdown *(browser only)* | Sort A→Z, Z→A, or by category |

### Adding a Project

1. Click **＋ Add Project** (top-right of the panel)
2. Fill in the form:

| Field | Required | Description |
|-------|----------|-------------|
| **Title** | ✅ Yes | The project name shown on the card |
| **Category** | ✅ Yes | Environment / Character / Props & Assets |
| **Description** | ✅ Yes | Short paragraph about the project |
| **Image** | ❌ Optional | Upload a file OR paste a URL/path |
| **FA Icon Class** | ❌ Optional | Font Awesome class used when no image is set (e.g. `fa-solid fa-mountain-sun`) |
| **Gradient Style** | ❌ Optional | Background tint when no image — env / char / prop |
| **Tools Used** | ❌ Optional | Comma-separated list (e.g. `Blender, ZBrush`) |

3. Click **💾 Save Project**

### Editing a Project

- Click **✏ Edit** on any card
- The same form opens pre-filled with the existing data
- Make your changes and click **💾 Save Project**

### Duplicating a Project

- Click **⎘ Dupe** on any card
- A copy is created instantly with `(Copy)` appended to the title
- Edit the duplicate to customise it

### Deleting a Project

- Click **🗑 Delete** on any card
- A **confirmation dialog** appears — click **Delete** to confirm
- This cannot be undone (use a JSON backup if you need recovery)

### Reordering Projects *(browser admin.html only)*

1. Click **↕ Reorder Mode** button (top-right of Portfolio panel)
2. **Drag and drop** cards to your preferred order
3. Click **✔ Done Reordering** — the order is saved
4. Re-export your code to apply the new order to the site

---

## 6. Marketplace Assets

### Viewing Assets

Assets are displayed as cards showing:
**title**, **category**, **price** (or Free), **rating**, **reviews**, **download count**

### Searching & Filtering

| Control | What it does |
|---------|-------------|
| 🔍 Search box | Filters by title or description |
| Category dropdown | Filter by Characters / Environments / Props / Textures / Vehicles |

### Adding an Asset

1. Click **＋ Add Asset**
2. Fill in the form:

| Field | Required | Description |
|-------|----------|-------------|
| **Title** | ✅ Yes | Product name |
| **Category** | ✅ Yes | Character / Environment / Prop / Texture / Vehicle |
| **Description** | ✅ Yes | Product description |
| **Price ₹** | ✅ Yes | Enter `0` for a free asset |
| **Original Price ₹** | ❌ Optional | Leave blank if there's no sale. If filled, a strikethrough price shows |
| **Star Rating** | ❌ Optional | 1 – 5 stars |
| **Reviews** | ❌ Optional | Number of reviews |
| **Downloads** | ❌ Optional | Download count |
| **Date Added** | ❌ Optional | Defaults to today |
| **Icon** | ❌ Optional | Font Awesome class used as placeholder |
| **Featured** | ❌ Optional | Yes = shown in the featured section |
| **Image** | ❌ Optional | Upload or paste URL |
| **Badges** | ❌ Optional | Comma-separated: `new`, `hot`, `sale`, `free` |
| **Software** | ❌ Optional | Comma-separated: `blender, zbrush, substance` |
| **File Formats** | ❌ Optional | Comma-separated: `fbx, blend, obj` |

3. Click **💾 Save Asset**

### Editing / Duplicating / Deleting

Same as Portfolio — use the **✏ Edit**, **⎘ Duplicate**, **🗑 Delete** buttons on each card.

---

## 7. Export Code

The Export panel generates ready-to-paste code from your current data.

### Portfolio HTML Export

```
What it generates:
  All your project cards as HTML <div> elements

Where to paste it:
  Inside  <div class="projects-grid" id="portfolioGrid">
  in your index.html file
```

**Steps:**
1. Go to **💻 Export Code** panel
2. Click **⎘ Copy to Clipboard** under "Portfolio Projects HTML"
3. Open `index.html` in your code editor
4. Find `<div class="projects-grid" id="portfolioGrid">`
5. Replace everything **between** the opening and closing `</div>` with the copied code
6. Save `index.html`

---

### Marketplace JS Export

```
What it generates:
  const PRODUCTS = [ ... ] JavaScript array

Where to paste it:
  Replace the existing const PRODUCTS = [...]; in marketplace.js
```

**Steps:**
1. Go to **💻 Export Code** panel
2. Click **⎘ Copy to Clipboard** under "Marketplace Products JS"
3. Open `js/marketplace.js` in your code editor
4. Find `const PRODUCTS = [` — select from that line all the way to the closing `];`
5. Replace it entirely with the copied code
6. Save `marketplace.js`

---

## 8. Patch Files Directly

Instead of manually copying and pasting, the admin can **patch your files automatically**.

### Patch `index.html`

1. Go to **💻 Export Code** panel
2. Scroll to **🔧 Patch index.html directly**
3. Click **📂 Upload index.html** and select your current `index.html`
4. The button turns **green** when the file is loaded
5. Click **⬇ Download Patched index.html**
6. A save dialog appears — save the file
7. **Replace** your old `index.html` with the downloaded file

```
What gets replaced automatically:
  Everything inside  <div id="portfolioGrid">...</div>
  is replaced with your updated project cards
```

---

### Patch `marketplace.js`

1. Scroll to **🔧 Patch marketplace.js directly**
2. Click **📂 Upload marketplace.js** and select your file
3. Click **⬇ Download Patched marketplace.js**
4. Save and **replace** your old `marketplace.js`

```
What gets replaced automatically:
  const PRODUCTS = [ ... ];
  is replaced with your updated products array
```

> ✅ **Your file is read in your browser/app memory only.**
> It is never uploaded to any server.

### Fallback Behaviour

If the admin cannot find the exact location to inject code, it will:

| Scenario | Fallback |
|----------|----------|
| `id="portfolioGrid"` not found | Tries `class="projects-grid"` |
| Neither found | Injects before `</main>` with a warning comment |
| `const PRODUCTS` not found in JS | Prepends array to top of file with a warning comment |

---

## 9. Git & Firebase Deploy

> **Desktop app only** (`creviz_admin.py`)
>
> Requires **Git** and **Firebase CLI** to be installed and on your system PATH.

### Setup

1. Open the **🔀 Git & Deploy** panel
2. The **Repository / Project Folder** field defaults to the folder
   where `creviz_admin.py` is located
3. Click **Browse** to change it if needed
4. All git and firebase commands run inside that folder

### Git Commands

#### `📋 git status`
Shows the current state of your working directory.
- Which files are modified
- Which files are staged
- Which branch you're on

```bash
# Equivalent terminal command:
git status
```

---

#### `📜 git log`
Shows the last **20 commits** with a visual branch graph.

```bash
# Equivalent terminal command:
git log --oneline --graph --decorate -20
```

---

#### `🔍 git diff`
Shows a summary of what has changed since the last commit.

```bash
# Equivalent terminal command:
git diff --stat
```

---

#### `➕ git add .`
Stages **all** changed, new, and deleted files for the next commit.

> ⚠️ A **confirmation dialog** appears before this runs.

```bash
# Equivalent terminal command:
git add .
```

---

#### `✔ git commit`
Opens a **Commit Message Dialog**:

```
┌─────────────────────────────────────────────┐
│  📝 Commit Message                          │
│                                             │
│  [ type your message here...             ]  │
│                                             │
│  Quick: [feat: update portfolio] [fix: ...]  │
│                                             │
│              [Cancel]  [✔ Commit]           │
└─────────────────────────────────────────────┘
```

- Type your message in the input field
- Or click a **Quick Preset** button to auto-fill a common message
- Press **Enter** or click **✔ Commit**

```bash
# Equivalent terminal command:
git commit -m "your message"
```

---

#### `⬆ git push`
Pushes your local commits to the remote repository (e.g. GitHub).

> ⚠️ A **confirmation dialog** appears before this runs.

```bash
# Equivalent terminal command:
git push
```

---

#### `⬇ git pull`
Pulls the latest changes from the remote repository.

```bash
# Equivalent terminal command:
git pull
```

---

### Firebase Commands

#### `🚀 firebase deploy`
Deploys your site to **Firebase Hosting**.

> ⚠️ A **confirmation dialog** appears. This publishes your site **live**.

```bash
# Equivalent terminal command:
firebase deploy
```

**Prerequisites:**
- Firebase CLI installed: `npm install -g firebase-tools`
- Logged in: `firebase login`
- Project initialised: `firebase.json` exists in the project folder

---

#### `firebase hosting:channel:list`
Lists all your active Firebase preview channels.

```bash
# Equivalent terminal command:
firebase hosting:channel:list
```

---

### ⚡ One-Click Full Workflow

The most powerful feature — runs the entire deploy pipeline in sequence:

```
Step 1 / 4  →  git add .
Step 2 / 4  →  Commit Message Dialog  →  git commit -m "..."
Step 3 / 4  →  git push
Step 4 / 4  →  firebase deploy
```

- Each step **waits** for the previous one to finish
- If any step **fails**, the pipeline stops and warns you
- The terminal shows clearly which step is running

> ⚠️ A confirmation dialog appears before the workflow starts.

---

### Terminal Output

The terminal at the bottom of the Git panel streams all command output live.

| Colour | Meaning |
|--------|---------|
| 🟠 Orange | The command being run |
| 🟢 Green | Success messages |
| 🔴 Red | Errors and failures |
| 🟡 Yellow | Warnings |
| 🔵 Blue | Info messages |
| 🟣 Purple | Section headers |

**Terminal buttons:**

| Button | Action |
|--------|--------|
| 🗑 Clear | Clears all terminal output |
| ⎘ Copy Output | Copies all terminal text to clipboard |

**Status indicator** (top-left of terminal):

| Indicator | Meaning |
|-----------|---------|
| `● Idle` | No command running |
| `● Running…` | Command in progress |
| `● Done` | Last command succeeded |
| `● Error (exit N)` | Last command failed with exit code N |

---

## 10. Settings & Backups

### Save Data

| Option | What it does |
|--------|-------------|
| **Save to JSON now** | Immediately writes `creviz_data.json` to disk *(desktop)* or localStorage *(browser)* |
| **Auto-save** *(browser)* | Saves automatically after every change — toggle on/off |

### Export JSON Backup

Downloads a complete backup of all your data:

```json
{
  "version": "1.0",
  "exportedAt": "2026-02-24",
  "projects": [ ... ],
  "market": [ ... ]
}
```

**Always export a backup before:**
- Resetting data
- Major content changes
- Clearing browser storage

---

### Import JSON Backup

Restores all data from a previously exported `.json` file.

> ⚠️ This **overwrites** your current data. Export a backup first if needed.

---

### Reset to Defaults

Permanently deletes all your custom projects and assets and reloads
the 9 built-in portfolio projects and 12 marketplace assets.

> ⚠️ This **cannot be undone**. Export a JSON backup first.

---

### Confirm Before Delete *(browser only)*

When enabled (default), a confirmation dialog appears before any item is deleted.
Toggle off in Settings if you prefer instant deletion.

---

## 11. Project File Structure

```
your-project/
│
├── index.html              ← Main portfolio page
├── marketplace.html        ← Marketplace page
├── 404.html                ← Custom 404 page
├── admin.html              ← Browser admin panel
├── creviz_admin.py         ← Desktop admin panel (Python)
├── creviz_data.json        ← Auto-generated data file (desktop)
├── HOW_TO_USE.md           ← This file
│
├── css/
│   ├── style.css           ← Portfolio styles
│   └── marketplace.css     ← Marketplace styles
│
├── js/
│   ├── script.js           ← Portfolio JS + Discord webhook
│   └── marketplace.js      ← Marketplace JS + PRODUCTS array
│
└── assets/
    └── images/
        ├── logo.png
        └── projects/
            ├── ember-wastes.jpg
            └── ...
```

---

## 12. FAQ & Troubleshooting

### ❓ My changes in the admin aren't showing on the site

The admin panel **does not edit your files automatically** (browser version).
You must use the **Export Code** or **Patch Files** workflow to apply changes.

---

### ❓ I cleared my browser data and lost everything

Browser localStorage was cleared.
This is why you should regularly use **Export JSON Backup** in Settings.
If you have a backup `.json` file, use **Import JSON Backup** to restore.

---

### ❓ `git` command says "not found"

Git is not installed or not on your PATH.

- **Windows:** Download from [git-scm.com](https://git-scm.com)
- **Mac:** Run `xcode-select --install` or install via Homebrew: `brew install git`
- **Linux:** `sudo apt install git` or `sudo dnf install git`

After installing, **restart** `creviz_admin.py`.

---

### ❓ `firebase` command says "not found"

Firebase CLI is not installed.

```bash
# Install globally via npm
npm install -g firebase-tools

# Log in
firebase login

# Initialise project (run once in your project folder)
firebase init hosting
```

---

### ❓ `git push` fails with "rejected"

Your local branch is behind the remote. Run **⬇ git pull** first,
resolve any conflicts, then push again.

---

### ❓ The patch didn't replace the right section in `index.html`

The admin looks for `id="portfolioGrid"` then `class="projects-grid"`.
Make sure at least one of these exists on your grid container:

```html
<!-- Make sure your grid div has this id -->
<div class="projects-grid" id="portfolioGrid">
  <!-- project cards go here -->
</div>
```

---

### ❓ Python won't start — "No module named tkinter"

On some Linux systems, Tkinter is not included by default.

```bash
# Ubuntu / Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

---

### ❓ Images I upload don't show on the live site

When you upload an image file in the admin, it's stored as a **base64 data URL**
inside the exported code. This works but makes large files.

**Recommended approach:**
1. Put your images in `assets/images/projects/`
2. In the image field, type the **relative path**: `assets/images/projects/my-image.jpg`
3. This keeps file sizes small and images cached properly by the browser

---

### ❓ How do I add a Discord webhook for commissions?

Open `js/script.js` and find:

```javascript
const DISCORD_WEBHOOK_URL = "YOUR_WEBHOOK_URL_HERE";
```

Replace `YOUR_WEBHOOK_URL_HERE` with your actual Discord webhook URL.
Do the same in `js/marketplace.js` for checkout notifications.

---

## 🔥 Quick Reference Card

```
DAILY WORKFLOW
══════════════════════════════════════════════════
1.  Open admin.html  OR  python creviz_admin.py
2.  Edit projects / assets as needed
3.  Click  💾 Save & Export
4.  Go to  💻 Export Code  panel
5.  Upload your index.html  →  Download patched file
6.  Upload your marketplace.js  →  Download patched file
7.  Replace old files in your project folder
8.  (Desktop) Go to  🔀 Git & Deploy
9.  Click  ⚡ Add → Commit → Push → Deploy
10. Your site is live! 🚀
══════════════════════════════════════════════════
```

---

*© 2026 Creviz Studio — Every polygon tells a story.*