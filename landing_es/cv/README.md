# Francisco Caro Díaz — bilingual portfolio

Static English / Spanish portfolio and printable résumé, hosted on GitHub Pages.

- English: `/`
- Spanish: `/landing_es/`
- Résumé: `/cv/` and `/landing_es/cv/`
- Legacy portfolio URLs remain available at `/home/landing.html` and `/landing_es/home/landing.html`.

Edit content in `scripts/build_site.py`, then run `python3 scripts/build_site.py`. Shared styling is in `assets/site.css`. No packages or build service are required. Preview with `python3 -m http.server 8765` and use the résumé's print button to save a current PDF.

Current downloadable CVs: `files/cv/Francisco-Caro-Diaz-CV-EN.pdf` and `files/cv/Francisco-Caro-Diaz-CV-ES.pdf`. Generate with `scripts/build_cv.py` using Python with ReportLab. Legacy PDF URLs serve copies of these current documents. Template assets remain available for existing links.
