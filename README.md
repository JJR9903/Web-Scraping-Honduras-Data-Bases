# Web Scraping Honduras Data Bases

Web scraping and PDF table extraction for multiple Honduras data
sources, including ENDESA surveys, SEPOL statistics, and population
projections from the national statistics institute (INE). This
repository contains Python scripts that collect, parse, and export
structured data from web pages and PDFs.

------------------------------------------------------------------------

## 📁 Repository Structure

    ├── .gitattributes
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    ├── chromedriver
    ├── info.py
    ├── readpdf.py
    ├── Search interaction.py
    ├── Search interaction 2.py
    ├── smoketest.py
    ├── WebScraping.py
    ├── WebScraping_SEPOL.py
    ├── WebScraping_Poblacion_INE.py
    ├── tabula-py-readthedocs-io-en-latest.pdf
    ├── reports/
    └── venv/

------------------------------------------------------------------------

## 📌 Project Objective

This repository consolidates web scraping and automated data extraction
workflows for Honduran official data sources. The scripts automate:

-   Scraping statistical tables from web applications (e.g., SEPOL).
-   Automating HTML form interaction using Selenium and MechanicalSoup.
-   Extracting tabular data from PDF files using Tabula‑Py.
-   Exporting structured datasets for downstream quantitative analysis.

The objective is to create reproducible pipelines for collecting public
statistical data that would otherwise require manual extraction.

------------------------------------------------------------------------

## 🧠 Script Overview

### WebScraping.py

Basic scraping examples using BeautifulSoup and simulated form
interactions.

### WebScraping_SEPOL.py

Automates interaction with the SEPOL statistics portal using Selenium.
Extracts fatality data by department, municipality, year, and age group
into structured pandas DataFrames.

### WebScraping_Poblacion_INE.py

Automates extraction of population projections from INE. Iterates across
departments and municipalities and exports results to structured files.

### readpdf.py

Utility functions for reading and extracting tabular data from PDFs
using tabula‑py.

### Additional Utilities

-   Search interaction scripts for browser automation testing.
-   smoketest.py for environment verification.
-   info.py for helper configurations.

------------------------------------------------------------------------

## 📦 Requirements

Python 3.x

Core libraries: - selenium - beautifulsoup4 - mechanicalsoup - pandas -
numpy - lxml - tabula-py (requires Java)

Example installation:

``` bash
python3 -m venv venv
source venv/bin/activate
pip install selenium beautifulsoup4 mechanicalsoup pandas lxml tabula-py
```

------------------------------------------------------------------------

## 🚀 How to Run

1.  Activate your virtual environment.
2.  Ensure `chromedriver` matches your Chrome browser version.
3.  Run a specific scraper:

``` bash
python WebScraping_SEPOL.py
python WebScraping_Poblacion_INE.py
```

Outputs are typically exported as CSV or Excel files.

------------------------------------------------------------------------

## 📝 License

This repository, its code, analysis logic, and all associated materials
are proprietary and confidential to Econometria S.A. No usage, sharing,
redistribution, or modification is permitted without explicit written
authorization.

See LICENSE for full terms.

**Contact for Licensing or Permission Requests:**\
Email: jj.rincon@hotmail.com
