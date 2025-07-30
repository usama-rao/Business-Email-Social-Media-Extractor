# Business Email & Social Media Extractor v2.0

A Python tool for extracting email addresses and social media links from business websites. This tool reads business data from CSV files and outputs cleaned contact information with improved error handling, logging, and professional code structure.

## Features

- Extract email addresses from business websites
- Extract social media links (Facebook, LinkedIn, Instagram, Twitter/X)
- Clean and validate email addresses
- Remove duplicate and invalid emails
- Professional logging with file output
- Command-line interface
- Rate limiting to be respectful to websites
- Comprehensive error handling
- Progress tracking

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/business-email-extractor.git
cd business-email-extractor
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Basic usage:
```bash
python business_email_extractor.py businesses.csv
```

With custom output file:
```bash
python business_email_extractor.py businesses.csv -o results.csv
```

With custom timeout and delay:
```bash
python business_email_extractor.py businesses.csv -t 15 -d 2.0
```

### Command Line Options

- `input_file`: Path to input CSV file (required)
- `-o, --output`: Output CSV file name (default: `emails_extracted_v2.csv`)
- `-t, --timeout`: Request timeout in seconds (default: 10)
- `-d, --delay`: Delay between requests in seconds (default: 1.0)

### Input CSV Format

Your input CSV file should contain at least these columns:
- `Business Name`: Name of the business
- `Website`: Business website URL

Example:
```csv
Business Name,Website
Acme Corp,https://acmecorp.com
Local Bakery,localbakery.com
Tech Solutions,www.techsolutions.net
```

### Output CSV Format

The tool generates a CSV file with the following columns:
- `Business Name`: Original business name
- `Website`: Original website URL
- `Primary Email`: First valid email found
- `Secondary Email`: Second valid email found (if any)
- `Social Media`: Social media link (prioritized: Facebook > LinkedIn > Instagram > Twitter)
- `Emails Found`: Number of valid emails discovered
- `Has Contact`: "Yes" if any contact info found, "No" otherwise

## How It Works

1. **URL Normalization**: Cleans and validates website URLs
2. **Multi-page Scanning**: Checks homepage, contact, and about pages
3. **Email Extraction**: Uses regex to find email addresses in HTML content
4. **Email Cleaning**: Removes invalid, test, and file-extension emails
5. **Social Media Detection**: Finds social media links with platform priority
6. **Rate Limiting**: Adds delays between requests to be respectful
7. **Results Sorting**: Orders results with businesses having emails first

## Pages Checked

The tool automatically checks these pages on each website:
- Homepage (`/`)
- Contact page (`/contact`)
- About page (`/about`)
- Contact Us page (`/contact-us`)

## Email Validation

The tool automatically filters out:
- Empty or whitespace-only emails
- File extensions (images, documents, etc.)
- Test/placeholder emails (test@example.com, xxx@xxx.com, etc.)
- No-reply addresses
- Duplicate emails

## Social Media Priority

When multiple social media links are found, the tool prioritizes:
1. Facebook
2. LinkedIn
3. Instagram
4. Twitter/X

## Logging

The tool creates detailed logs:
- Console output for real-time progress
- `extractor.log` file for detailed logging
- Progress tracking with business count
- Success/failure statistics

## Error Handling

- Graceful handling of network timeouts
- Invalid URL detection and skipping
- Missing CSV columns validation
- Comprehensive exception logging

## Rate Limiting

The tool includes a 1-second delay between requests by default to be respectful to websites. You can adjust this with the `--delay` parameter.

## Requirements

- Python 3.7+
- pandas >= 1.5.0
- requests >= 2.28.0

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Changelog

### Version 2.0
- Complete code rewrite with object-oriented design
- Added command-line interface
- Improved error handling and logging
- Added rate limiting and timeout controls
- Enhanced email validation
- Better social media detection
- Professional code structure
- Comprehensive documentation

### Version 1.0
- Basic email and social media extraction
- Simple CSV processing

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

## Disclaimer

This tool is for legitimate business contact extraction only. Please respect website terms of service and robots.txt files. Use responsibly and consider the impact on target websites.
