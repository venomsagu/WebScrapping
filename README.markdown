# Odisha RERA Web Scraper

This Python script scrapes project details from the Odisha Real Estate Regulatory Authority (RERA) website (`https://rera.odisha.gov.in/projects/project-list`). It extracts key information such as RERA Registration Number, Project Name, Promoter Name, Promoter Address, and GST Number for up to 6 projects and saves the data in JSON and CSV formats.

## Features
- Uses **Playwright** for reliable web scraping of dynamic content.
- Handles SweetAlert2 modals (e.g., location access popups) to ensure uninterrupted scraping.
- Robust error handling for timeouts, missing elements, and navigation issues.
- Outputs data in both JSON (`rera_projects.json`) and CSV (`rera_projects.csv`) formats.
- Configurable parameters (e.g., max projects, timeouts) via a `CONFIG` dictionary.

## Prerequisites
- Python 3.8 or higher
- Playwright for Python
- Operating System: Windows, macOS, or Linux

## Installation
1. **Install Python**: Ensure Python 3.8+ is installed. Download from [python.org](https://www.python.org/downloads/).
2. **Install Playwright**:
   ```bash
   pip install playwright
   playwright install
   ```
   This installs the Playwright library and necessary browser binaries.

## Usage
1. **Clone or Download**: Save the script as `sc.py`.
2. **Run the Script**:
   ```bash
   python sc.py
   ```
3. **Output**:
   - The script scrapes details for up to 6 projects.
   - Results are saved to:
     - `rera_projects.json`: JSON file with structured data.
     - `rera_projects.csv`: CSV file with tabulated data.
   - Logs are printed to the console, detailing navigation, modal handling, and errors.

## Configuration
The script uses a `CONFIG` dictionary in `sc.py` to customize settings:
- `BASE_URL`: URL of the project list page (`https://rera.odisha.gov.in/projects/project-list`).
- `OUTPUT_JSON_FILE`: Output JSON file name (`rera_projects.json`).
- `OUTPUT_CSV_FILE`: Output CSV file name (`rera_projects.csv`).
- `MAX_PROJECTS`: Number of projects to scrape (default: 6).
- `PAGE_TIMEOUT`: Navigation timeout in milliseconds (default: 60000).
- `WAIT_AFTER_LOAD`: Wait time after page load in milliseconds (default: 2000).

To modify, edit the `CONFIG` dictionary in `sc.py`.

## Output Format
### JSON (`rera_projects.json`)
```json
[
  {
    "Rera Regd. No": "RP/01/2023/1234",
    "Project Name": "Sample Project",
    "Promoter Name": "ABC Builders",
    "Address of the Promoter": "123 Main St, Bhubaneswar",
    "GST No": "21ABCDE1234F1Z5"
  },
  ...
]
```

### CSV (`rera_projects.csv`)
```csv
Rera Regd. No,Project Name,Promoter Name,Address of the Promoter,GST No
RP/01/2023/1234,Sample Project,ABC Builders,"123 Main St, Bhubaneswar",21ABCDE1234F1Z5
...
```

## Error Handling
- **Timeouts**: Logs and skips projects if navigation or element loading exceeds `PAGE_TIMEOUT`.
- **Missing Elements**: Sets fields to "N/A" if data (e.g., GST No) is not found.
- **Modals**: Automatically closes SweetAlert2 location access popups by clicking the "OK" button.
- **Navigation**: Retries fetching "View Details" links to handle dynamic page updates.

## Notes
- The script runs in **non-headless mode** (`headless=False`) for debugging, showing the browser UI. To run silently, set `headless=True` in `sc.py`.
- Respects the website by limiting to 6 projects and including delays (`WAIT_AFTER_LOAD`) to avoid overloading the server.
- If the website introduces CAPTCHAs or rate-limiting, manual intervention may be needed in non-headless mode.

## Challenges Overcome
- **SweetAlert2 Modal**: Handled a location access popup by detecting and closing it automatically.
- **Dynamic Content**: Used Playwright’s robust selectors and wait mechanisms to handle JavaScript-rendered pages.
- **Stale Elements**: Re-fetched "View Details" links after each navigation to prevent DOM-related errors.

## License
This project is for educational purposes and part of an internship assessment. Use responsibly and respect the Odisha RERA website’s terms of service.