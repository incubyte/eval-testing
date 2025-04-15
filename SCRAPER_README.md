# DeepEval Documentation Scraper

This tool scrapes the DeepEval documentation website and saves it in a structured folder format for offline reference.

## Features

- Automatically scrapes the DeepEval documentation website
- Organizes content into a logical folder structure
- Converts HTML content to Markdown format
- Preserves links and images where possible
- Discovers additional documentation pages

## Requirements

- Python 3.6 or higher
- Internet connection
- Required Python packages (installed automatically by the scripts):
  - requests
  - beautifulsoup4
  - markdown
  - html2text

## How to Use

### On Windows

1. Simply double-click the `run_scraper.bat` file
2. Wait for the script to complete
3. The documentation will be saved in the `deepeval-docs` folder

### On macOS/Linux

1. Open a terminal in the directory containing the scripts
2. Make the shell script executable:
   ```
   chmod +x run_scraper.sh
   ```
3. Run the script:
   ```
   ./run_scraper.sh
   ```
4. The documentation will be saved in the `deepeval-docs` folder

### Manual Execution

If you prefer to run the script manually:

1. Install the required packages:
   ```
   pip install -r scrape_requirements.txt
   ```
2. Run the script:
   ```
   python scrape_deepeval_docs.py
   ```

## Folder Structure

The documentation will be organized into the following structure:

```
deepeval-docs/
├── getting_started.md
├── evaluation/
│   ├── introduction.md
│   ├── test_cases.md
│   ├── datasets.md
│   └── ...
├── metrics/
│   ├── introduction.md
│   ├── answer_relevancy.md
│   ├── faithfulness.md
│   └── ...
├── synthesizer/
│   ├── introduction.md
│   ├── generate_from_docs.md
│   └── ...
└── red-teaming/
    ├── introduction.md
    └── ...
```

## Customization

You can modify the `scrape_deepeval_docs.py` file to:

- Add or remove specific documentation pages to scrape
- Change the output directory
- Adjust the folder structure
- Modify the HTML-to-Markdown conversion settings

## Notes

- This script respects the website's server by adding a delay between requests
- The script may need updates if the DeepEval website structure changes
- Some formatting or interactive elements may not be perfectly preserved in the Markdown conversion
