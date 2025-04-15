"""
Script to scrape DeepEval documentation and save it in a structured folder format.
This script fetches documentation pages from the DeepEval website and saves them as markdown files.
"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import html2text

# Base URL for DeepEval documentation
BASE_URL = "https://www.deepeval.com/docs/"
# Output directory for the documentation
OUTPUT_DIR = "deepeval-docs"
# Docs path prefix for link discovery
DOCS_PATH_PREFIX = "/docs/"

# Folder constants for mapping
FOLDER_ROOT = ""
FOLDER_EVALUATION = "evaluation"
FOLDER_SYNTHESIZER = "synthesizer"
FOLDER_METRICS = "metrics"
FOLDER_METRICS_MULTIMODAL = "metrics/multimodal"
FOLDER_BENCHMARKS = "benchmarks"
FOLDER_RED_TEAMING = "red-teaming"
FOLDER_RED_TEAMING_VULNERABILITIES = "red-teaming/vulnerabilities"
FOLDER_OTHERS = "others"

# List of main sections to scrape
SECTIONS = [
    # Getting Started
    "getting-started",

    # Evaluation
    "evaluation-introduction",
    "evaluation-test-cases",
    "evaluation-datasets",
    "evaluation-conversation-simulator",

    # Synthesizer
    "synthesizer-introduction",
    "synthesizer-generate-from-docs",
    "synthesizer-generate-from-contexts",
    "synthesizer-generate-from-scratch",
    "synthesizer-generate-from-goldens",

    # Metrics
    "metrics-introduction",
    "metrics-llm-evals",
    "metrics-dag",
    "metrics-answer-relevancy",
    "metrics-faithfulness",
    "metrics-contextual-precision",
    "metrics-contextual-recall",
    "metrics-contextual-relevancy",
    "metrics-task-completion",
    "metrics-tool-correctness",
    "metrics-bias",
    "metrics-toxicity",
    "metrics-summarization",
    "metrics-prompt-alignment",
    "metrics-hallucination",
    "metrics-json-correctness",
    "metrics-ragas",
    "metrics-custom",
    "metrics-conversational-g-eval",
    "multimodal-metrics-image-coherence",

    # Benchmarks
    "benchmarks-introduction",

    # Red Teaming
    "red-teaming-introduction",
    "red-teaming-attack-enhancements",
    "red-teaming-vulnerabilities",
    "red-teaming-vulnerabilities-bias",
    "red-teaming-vulnerabilities-misinformation",
    "red-teaming-vulnerabilities-toxicity",
    "red-teaming-vulnerabilities-illegal-activities",
    "red-teaming-vulnerabilities-personal-safety",
    "red-teaming-vulnerabilities-pii-leakage",
    "red-teaming-vulnerabilities-prompt-leakage",
    "red-teaming-vulnerabilities-unauthorized-access",
    "red-teaming-vulnerabilities-intellectual-property",
    "red-teaming-vulnerabilities-excessive-agency",
    "red-teaming-vulnerabilities-robustness",
    "red-teaming-vulnerabilities-graphic-content",
    "red-teaming-vulnerabilities-competition",

    # Others
    "data-privacy",
    "miscellaneous",
]

# Mapping of URL paths to folder structures
URL_TO_FOLDER_MAP = {
    # Getting Started
    "getting-started": FOLDER_ROOT,

    # Evaluation
    "evaluation-introduction": FOLDER_EVALUATION,
    "evaluation-test-cases": FOLDER_EVALUATION,
    "evaluation-datasets": FOLDER_EVALUATION,
    "evaluation-conversation-simulator": FOLDER_EVALUATION,

    # Synthesizer
    "synthesizer-introduction": FOLDER_SYNTHESIZER,
    "synthesizer-generate-from-docs": FOLDER_SYNTHESIZER,
    "synthesizer-generate-from-contexts": FOLDER_SYNTHESIZER,
    "synthesizer-generate-from-scratch": FOLDER_SYNTHESIZER,
    "synthesizer-generate-from-goldens": FOLDER_SYNTHESIZER,

    # Metrics
    "metrics-introduction": FOLDER_METRICS,
    "metrics-llm-evals": FOLDER_METRICS,
    "metrics-dag": FOLDER_METRICS,
    "metrics-answer-relevancy": FOLDER_METRICS,
    "metrics-faithfulness": FOLDER_METRICS,
    "metrics-contextual-precision": FOLDER_METRICS,
    "metrics-contextual-recall": FOLDER_METRICS,
    "metrics-contextual-relevancy": FOLDER_METRICS,
    "metrics-task-completion": FOLDER_METRICS,
    "metrics-tool-correctness": FOLDER_METRICS,
    "metrics-bias": FOLDER_METRICS,
    "metrics-toxicity": FOLDER_METRICS,
    "metrics-summarization": FOLDER_METRICS,
    "metrics-prompt-alignment": FOLDER_METRICS,
    "metrics-hallucination": FOLDER_METRICS,
    "metrics-json-correctness": FOLDER_METRICS,
    "metrics-ragas": FOLDER_METRICS,
    "metrics-custom": FOLDER_METRICS,
    "metrics-conversational-g-eval": FOLDER_METRICS,
    "multimodal-metrics-image-coherence": FOLDER_METRICS_MULTIMODAL,

    # Benchmarks
    "benchmarks-introduction": FOLDER_BENCHMARKS,

    # Red Teaming
    "red-teaming-introduction": FOLDER_RED_TEAMING,
    "red-teaming-attack-enhancements": FOLDER_RED_TEAMING,
    "red-teaming-vulnerabilities": FOLDER_RED_TEAMING,
    "red-teaming-vulnerabilities-bias": FOLDER_RED_TEAMING_VULNERABILITIES,
    "red-teaming-vulnerabilities-misinformation": FOLDER_RED_TEAMING_VULNERABILITIES,
    "red-teaming-vulnerabilities-toxicity": FOLDER_RED_TEAMING_VULNERABILITIES,
    "red-teaming-vulnerabilities-illegal-activities": FOLDER_RED_TEAMING_VULNERABILITIES,
    "red-teaming-vulnerabilities-personal-safety": FOLDER_RED_TEAMING_VULNERABILITIES,
    "red-teaming-vulnerabilities-pii-leakage": FOLDER_RED_TEAMING_VULNERABILITIES,
    "red-teaming-vulnerabilities-prompt-leakage": FOLDER_RED_TEAMING_VULNERABILITIES,
    "red-teaming-vulnerabilities-unauthorized-access": FOLDER_RED_TEAMING_VULNERABILITIES,
    "red-teaming-vulnerabilities-intellectual-property": FOLDER_RED_TEAMING_VULNERABILITIES,
    "red-teaming-vulnerabilities-excessive-agency": FOLDER_RED_TEAMING_VULNERABILITIES,
    "red-teaming-vulnerabilities-robustness": FOLDER_RED_TEAMING_VULNERABILITIES,
    "red-teaming-vulnerabilities-graphic-content": FOLDER_RED_TEAMING_VULNERABILITIES,
    "red-teaming-vulnerabilities-competition": FOLDER_RED_TEAMING_VULNERABILITIES,

    # Others
    "data-privacy": FOLDER_OTHERS,
    "miscellaneous": FOLDER_OTHERS,
}

# Headers to mimic a browser request
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def create_directory_structure():
    """Create the directory structure for the documentation."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Create subdirectories for each section
    for folder in set(URL_TO_FOLDER_MAP.values()):
        if folder:  # Skip empty string
            folder_path = os.path.join(OUTPUT_DIR, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)

    # Create additional nested directories
    nested_dirs = [
        os.path.join(OUTPUT_DIR, "metrics", "multimodal"),
        os.path.join(OUTPUT_DIR, "red-teaming", "vulnerabilities"),
    ]

    for nested_dir in nested_dirs:
        if not os.path.exists(nested_dir):
            os.makedirs(nested_dir, exist_ok=True)

def clean_html_content(html_content):
    """Clean HTML content and convert to markdown."""
    # Create an HTML to text converter
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0  # Don't wrap lines

    # Convert HTML to markdown
    markdown_content = h.handle(html_content)

    # Clean up the markdown
    markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)  # Remove excessive newlines

    return markdown_content

def extract_main_content(soup):
    """Extract the main content from the page."""
    # Find the main content area - adjust selectors based on the website structure
    main_content = soup.find('article')
    if not main_content:
        main_content = soup.find('main')
    if not main_content:
        main_content = soup.find('div', {'class': 'markdown'})

    if main_content:
        return str(main_content)
    else:
        # If we can't find a specific content area, return the body
        body = soup.find('body')
        return str(body) if body else str(soup)

def get_page_title(soup):
    """Extract the page title."""
    title_tag = soup.find('h1')
    if title_tag:
        return title_tag.text.strip()

    title_tag = soup.find('title')
    if title_tag:
        title = title_tag.text.strip()
        # Remove site name if present
        title = re.sub(r'\s*\|.*$', '', title)
        return title

    return "Untitled"

def scrape_page(url, path):
    """Scrape a single documentation page and save it as markdown."""
    print(f"Scraping: {url}")

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the page title
        title = get_page_title(soup)

        # Extract the main content
        content_html = extract_main_content(soup)

        # Convert to markdown
        content_md = clean_html_content(content_html)

        # Add title at the top
        content_md = f"# {title}\n\n{content_md}"

        # Save to file
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content_md)

        print(f"Saved: {path}")
        return True

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return False

def extract_doc_links(element):
    """Extract documentation links from an HTML element."""
    links = []
    if element:
        for a_tag in element.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith(DOCS_PATH_PREFIX):
                path = href.replace(DOCS_PATH_PREFIX, '')
                if path and not path.startswith('#'):
                    links.append(path)
    return links

def discover_links(url):
    """Discover additional documentation links from a page."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        # Look for navigation elements
        nav_elements = soup.find_all(['nav', 'aside', 'div'], class_=lambda c: c and ('nav' in c.lower() or 'sidebar' in c.lower() or 'menu' in c.lower()))

        # Also look for any div that might contain documentation links
        doc_divs = soup.find_all('div', class_=lambda c: c and ('docs' in c.lower() or 'documentation' in c.lower()))

        # Combine all potential navigation elements and extract links
        for element in nav_elements + doc_divs:
            links.extend(extract_doc_links(element))

        # Also look for links in the main content
        main_content = soup.find('article') or soup.find('main') or soup.find('div', {'class': 'markdown'})
        links.extend(extract_doc_links(main_content))

        # Remove duplicates and return
        return list(set(links))

    except Exception as e:
        print(f"Error discovering links from {url}: {e}")
        return []

def get_filename_from_url(url):
    """Generate a filename from a URL."""
    path = urlparse(url).path
    page_name = path.strip('/').split('/')[-1]

    # Map to folder
    folder = ""
    for url_part, folder_name in URL_TO_FOLDER_MAP.items():
        if url_part in path:
            folder = folder_name
            break

    # Convert URL path to filename
    filename = page_name.replace('-', '_') + '.md'

    if folder:
        return os.path.join(OUTPUT_DIR, folder, filename)
    else:
        return os.path.join(OUTPUT_DIR, filename)

def main():
    """Main function to scrape the documentation."""
    create_directory_structure()

    # Set to keep track of processed URLs
    processed_urls = set()

    # Start with the initial sections
    urls_to_process = [urljoin(BASE_URL, section) for section in SECTIONS]

    # Discover additional links from the main documentation page
    additional_links = discover_links(BASE_URL)
    for link in additional_links:
        full_url = urljoin(BASE_URL, link)
        if full_url not in urls_to_process:
            urls_to_process.append(full_url)

    # Also discover links from each section's page to ensure we get everything
    for section in SECTIONS:
        section_url = urljoin(BASE_URL, section)
        section_links = discover_links(section_url)
        for link in section_links:
            full_url = urljoin(BASE_URL, link)
            if full_url not in urls_to_process:
                urls_to_process.append(full_url)
                print(f"Discovered additional link: {full_url}")
        # Be nice to the server
        time.sleep(0.5)

    # Process all URLs
    for i, url in enumerate(urls_to_process):
        if url in processed_urls:
            continue

        processed_urls.add(url)

        # Get the output path
        output_path = get_filename_from_url(url)

        # Scrape the page
        scrape_page(url, output_path)

        # Print progress
        print(f"Progress: {i+1}/{len(urls_to_process)} pages processed")

        # Be nice to the server
        time.sleep(1)

    print(f"Documentation scraping complete. Files saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
