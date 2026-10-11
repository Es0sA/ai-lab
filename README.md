# AI Lab: MIT No-Code AI & ML Learning Tracker

An interactive dashboard, curriculum roadmap, and progress-tracking portal built for the MIT No-Code Artificial Intelligence & Machine Learning Program (October 2 to December 31, 2026).

---

## Overview

AI Lab provides a structured, responsive web interface to manage course materials, track completion status across 13 weeks of coursework, and search through all program resources. Progress is tracked locally in the browser so learners can monitor their advancement toward program completion.

---

## Key Features

1. **Global Progress Dashboard (`index.html`)**:
   * Real-time calculation of overall completion percentage.
   * Total resource counter and completed items counter.
   * Visual weekly roadmap cards covering Pre-work through Week 13 with individual progress indicators and direct links.
   * Program deadline milestone indicator.

2. **Weekly Study Modules (`weeks/`)**:
   * Dedicated pages for Pre-work and Weeks 1 through 13 (`prework.html`, `w1.html` to `w13.html`).
   * Granular itemization of video lectures, core readings, graded quizzes, and hands-on lab exercises.
   * Interactive checkboxes that dynamically update module and global progress.

3. **Master Resource Library (`resources.html`)**:
   * Centralized archive of all program readings, reference papers, and tool guides.
   * Category filtering and quick links to external study materials.

4. **Client-Side State Persistence (`js/progress.js`, `js/sync.js`)**:
   * Uses browser `localStorage` for zero-backend tracking.
   * Automatic cross-tab and cross-page synchronization of completion states.

5. **Curriculum Generator Tool (`generate_weeks.py`)**:
   * Python automation script that parses structured syllabus data to generate or update consistent HTML pages across all weekly modules.

---

## Project Structure

```
ai-lab/
|-- css/
|   `-- styles.css           # Design tokens, progress bars, dark/light styling
|-- js/
|   |-- progress.js          # Core progress calculation and checkbox handlers
|   `-- sync.js              # State synchronization across modules
|-- weeks/
|   |-- prework.html         # Program setup and foundational concepts
|   |-- w1.html - w13.html   # Weekly curriculum breakdowns (Weeks 1 to 13)
|-- generate_weeks.py        # Automation script to scaffold weekly HTML files
|-- index.html               # Main learning dashboard
|-- resources.html           # Comprehensive resource index
|-- .gitignore               # Ignored files and local artifacts
`-- README.md                # Project documentation
```

---

## Getting Started

Because the application is built with standard web technologies (HTML5, CSS3, vanilla JavaScript), no build steps or package managers are required.

### Running Locally

Serve the repository directory with any local static HTTP server:

Using Python:
```bash
python3 -m http.server 8000
```

Using Node.js:
```bash
npx serve .
```

Open `http://localhost:8000` in your web browser.

---

## Regenerating Weekly Modules

To update or regenerate weekly study pages from the Python curriculum generator:

```bash
python3 generate_weeks.py
```

---

## License

Personal learning project. All rights reserved.
