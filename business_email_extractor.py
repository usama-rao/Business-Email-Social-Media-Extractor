"""
Business Email & Social Media Extractor v2.0
============================================

A Python tool for extracting email addresses and social media links from business websites.
Reads business data from CSV files and outputs cleaned contact information.

Author: Usama Rao
License: MIT
"""

import pandas as pd
import requests
import re
import logging
import time
from typing import List, Tuple, Optional
import argparse
import sys
from urllib.parse import urljoin, urlparse


class BusinessContactExtractor:
    """Extract email addresses and social media links from business websites."""
    
    def __init__(self, timeout: int = 10, delay: float = 1.0):
        """
        Initialize the extractor.
        
        Args:
            timeout: Request timeout in seconds
            delay: Delay between requests in seconds
        """
        self.timeout = timeout
        self.delay = delay
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('extractor.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def clean_emails(self, emails: List[str]) -> List[str]:
        """
        Clean and validate email addresses.
        
        Args:
            emails: List of raw email addresses
            
        Returns:
            List of cleaned, valid email addresses (max 2)
        """
        clean = []
        
        # Patterns to exclude
        file_extensions = r'\.(png|jpg|jpeg|gif|svg|pdf|html?|css|js|ico|mp4|mp3|zip|doc|docx)$'
        test_patterns = r'(xxx@xxx\.com|your@email\.com|test\.com|test@.*|example@.*|no-reply@.*|noreply@.*)'
        
        for email in emails:
            email = email.strip().lower()
            
            # Skip empty emails
            if not email:
                continue
                
            # Skip file extensions
            if re.search(file_extensions, email):
                continue
                
            # Skip test/placeholder emails
            if re.match(test_patterns, email):
                continue
                
            # Skip duplicates
            if email not in clean:
                clean.append(email)
                
            # Limit to 2 emails
            if len(clean) >= 2:
                break
                
        return clean
    
    def normalize_url(self, url: str) -> Optional[str]:
        """
        Normalize and validate URL.
        
        Args:
            url: Raw URL string
            
        Returns:
            Normalized URL or None if invalid
        """
        if pd.isna(url) or not url.strip():
            return None
            
        url = url.strip().rstrip('/')
        
        if not url.startswith("http"):
            url = "http://" + url
            
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return None
            return url
        except Exception:
            return None
    
    def extract_emails_from_html(self, html: str) -> List[str]:
        """Extract email addresses from HTML content."""
        email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        return re.findall(email_pattern, html, re.IGNORECASE)
    
    def extract_social_links(self, html: str) -> str:
        """
        Extract social media links from HTML content.
        Priority: Facebook > LinkedIn > Instagram > Twitter
        """
        social_patterns = [
            (r'https?://(www\.)?facebook\.com/[^"\'\s>]+', 'Facebook'),
            (r'https?://(www\.)?linkedin\.com/[^"\'\s>]+', 'LinkedIn'),
            (r'https?://(www\.)?instagram\.com/[^"\'\s>]+', 'Instagram'),
            (r'https?://(www\.)?twitter\.com/[^"\'\s>]+', 'Twitter'),
            (r'https?://(www\.)?x\.com/[^"\'\s>]+', 'X/Twitter')
        ]
        
        for pattern, platform in social_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                return match.group(0)
                
        return ''
    
    def fetch_page_content(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from a URL.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if failed
        """
        try:
            response = requests.get(url, timeout=self.timeout, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.logger.warning(f"Failed to fetch {url}: {e}")
            return None
    
    def extract_contacts(self, website_url: str) -> Tuple[List[str], str]:
        """
        Extract emails and social links from a website.
        
        Args:
            website_url: Business website URL
            
        Returns:
            Tuple of (email_list, social_link)
        """
        base_url = self.normalize_url(website_url)
        if not base_url:
            return [], ''
        
        # Pages to check for contact information
        pages_to_check = ['', '/contact', '/about', '/contact-us']
        all_emails = set()
        social_link = ''
        
        for path in pages_to_check:
            full_url = urljoin(base_url, path)
            html = self.fetch_page_content(full_url)
            
            if html:
                # Extract emails
                found_emails = self.extract_emails_from_html(html)
                all_emails.update(found_emails)
                
                # Extract social links (first found takes priority)
                if not social_link:
                    social_link = self.extract_social_links(html)
            
            # Add delay between requests
            time.sleep(self.delay)
        
        cleaned_emails = self.clean_emails(list(all_emails))
        return cleaned_emails, social_link
    
    def process_csv(self, input_file: str, output_file: str = 'emails_extracted_v2.csv'):
        """
        Process businesses from CSV file.
        
        Args:
            input_file: Path to input CSV file
            output_file: Path to output CSV file
        """
        try:
            df = pd.read_csv(input_file)
            self.logger.info(f"Loaded {len(df)} businesses from {input_file}")
        except FileNotFoundError:
            self.logger.error(f"Input file {input_file} not found")
            return
        except Exception as e:
            self.logger.error(f"Error reading CSV: {e}")
            return
        
        # Ensure required columns exist
        required_columns = ['Business Name', 'Website']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            self.logger.error(f"Missing required columns: {missing_columns}")
            return
        
        results = []
        total = len(df)
        
        self.logger.info("Starting email and social media extraction...")
        
        for index, row in df.iterrows():
            business_name = row.get('Business Name', '')
            website = row.get('Website', '')
            
            self.logger.info(f"Processing ({index + 1}/{total}): {business_name}")
            
            emails, social = self.extract_contacts(website)
            
            result = {
                'Business Name': business_name,
                'Website': website,
                'Primary Email': emails[0] if len(emails) > 0 else '',
                'Secondary Email': emails[1] if len(emails) > 1 else '',
                'Social Media': social,
                'Emails Found': len(emails),
                'Has Contact': 'Yes' if emails or social else 'No'
            }
            
            results.append(result)
            
            self.logger.info(
                f"Results - Emails: {emails} | Social: {social[:50]}{'...' if len(social) > 50 else ''}"
            )
        
        # Sort results: businesses with emails first
        results_sorted = sorted(results, key=lambda x: (x['Primary Email'] == '', x['Business Name']))
        
        # Save results
        try:
            output_df = pd.DataFrame(results_sorted)
            output_df.to_csv(output_file, index=False)
            
            # Print summary
            with_emails = sum(1 for r in results if r['Primary Email'])
            with_social = sum(1 for r in results if r['Social Media'])
            
            self.logger.info(f"\nExtraction completed successfully!")
            self.logger.info(f"Results saved to: {output_file}")
            self.logger.info(f"Total businesses processed: {total}")
            self.logger.info(f"Businesses with emails: {with_emails} ({with_emails/total*100:.1f}%)")
            self.logger.info(f"Businesses with social media: {with_social} ({with_social/total*100:.1f}%)")
            
        except Exception as e:
            self.logger.error(f"Error saving results: {e}")


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(description='Business Email & Social Media Extractor v2.0')
    parser.add_argument('input_file', help='Input CSV file containing business data')
    parser.add_argument('-o', '--output', default='emails_extracted_v2.csv', 
                       help='Output CSV file (default: emails_extracted_v2.csv)')
    parser.add_argument('-t', '--timeout', type=int, default=10,
                       help='Request timeout in seconds (default: 10)')
    parser.add_argument('-d', '--delay', type=float, default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')
    
    args = parser.parse_args()
    
    # Create extractor instance
    extractor = BusinessContactExtractor(timeout=args.timeout, delay=args.delay)
    
    # Process the CSV file
    extractor.process_csv(args.input_file, args.output)


if __name__ == "__main__":
    main()
