# Galveston County Court Document Scraper

Automated tool for downloading court documents from Galveston County Public Access system.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r config/requirements.txt
   ```

2. **Run the scraper:**
   ```bash
   python court_scraper.py
   ```

3. **Enter a case number** (e.g., `25-CV-0880`)

4. **Choose browser visibility** (y/n)

5. **Wait for automatic processing:**
   - Navigates through 7-step court system process
   - Finds and parses all documents
   - Downloads documents to `downloads/[case-number]/`
   - Creates a manifest file

## How It Works

The scraper automates this 7-step process:

1. **Open** Galveston County Public Access website
2. **Click** "Civil and Family Case Records" 
3. **Select** "Case" search type
4. **Enter** case number and search
5. **Click** case number link (first time)
6. **Click** case number link (second time) - *crucial step*
7. **Extract** document links and download files

## Features

- **Automatic Navigation:** No manual clicking required
- **Document Parsing:** Extracts all available court documents
- **Smart Naming:** Uses descriptive filenames with dates
- **Duplicate Prevention:** Skips already downloaded files
- **Progress Tracking:** Shows detailed progress and status
- **Error Handling:** Retries failed navigation automatically
- **Manifest Creation:** Generates file listing with metadata

## Testing

Run tests to verify functionality:

```bash
python tests/test_scraper.py
```

## File Structure

```
gctx-downloader/
├── court_scraper.py          # Main script
├── downloads/               # Downloaded documents
├── tests/                  # Test scripts
└── config/                # Dependencies and config
    └── requirements.txt
```

## Requirements

- Python 3.8+
- Chrome browser (for Selenium automation)
- Internet connection

## Example Case Numbers

- `25-CV-0880` - Known working case
- `24-CV-1234` - Test different years  
- `23-CV-5678` - Test case variations

## Troubleshooting

**Navigation fails:** Try running with visible browser (`y`) to see what's happening

**No documents found:** Case may exist but have no available documents

**Download errors:** Check internet connection and court website status