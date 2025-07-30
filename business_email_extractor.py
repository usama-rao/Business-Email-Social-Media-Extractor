import pandas as pd
import requests
import re

# Read your input file
input_file = 'businesses.csv'
df = pd.read_csv(input_file)

# Clean and validate emails
def clean_emails(emails):
    clean = []
    for email in emails:
        email = email.strip().lower()
        if not email:
            continue
        if re.search(r'\.(png|jpg|jpeg|gif|svg|pdf|html?|css|js|ico|mp4|mp3)$', email):
            continue
        if re.match(r'(xxx@xxx\.com|your@email\.com|test\.com|test@.*|example@.*)', email):
            continue
        if email not in clean:
            clean.append(email)
    return clean[:2]

# Extract emails and social links
def extract_emails_and_social(url):
    if pd.isna(url) or url.strip() == '':
        return [], ''

    base_url = url.strip().rstrip('/')
    if not base_url.startswith("http"):
        base_url = "http://" + base_url

    pages_to_check = ['', '/contact', '/about']
    all_emails = set()
    social_link = ''

    headers = {"User-Agent": "Mozilla/5.0"}

    for path in pages_to_check:
        full_url = base_url + path
        try:
            response = requests.get(full_url, timeout=10, headers=headers)
            if response.status_code == 200:
                html = response.text

                # Emails
                found_emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)
                all_emails.update(found_emails)

                # Social links (prioritized)
                if not social_link:
                    fb_match = re.search(r'https?://(www\.)?facebook\.com/[^"\' >]+', html)
                    if fb_match:
                        social_link = fb_match.group(0)
                if not social_link:
                    li_match = re.search(r'https?://(www\.)?linkedin\.com/[^"\' >]+', html)
                    if li_match:
                        social_link = li_match.group(0)
                if not social_link:
                    ig_match = re.search(r'https?://(www\.)?instagram\.com/[^"\' >]+', html)
                    if ig_match:
                        social_link = ig_match.group(0)

        except:
            continue

    return clean_emails(list(all_emails)), social_link

# Extract for all businesses
results = []

print("🔍 Extracting emails and socials...")
for _, row in df.iterrows():
    name = row.get('Business Name', '')
    website = row.get('Website', '')
    emails, social = extract_emails_and_social(website)
    print(f"✅ {website} → Emails: {emails} | Social: {social}")

    results.append({
        'Business Name': name,
        'Website': website,
        'Email': emails[0] if len(emails) > 0 else '',
        'Alternate Email': emails[1] if len(emails) > 1 else '',
        'Social': social if len(emails) == 0 else ''
    })

# Sort: emails first
results_sorted = sorted(results, key=lambda x: x['Email'] == '', reverse=False)

# Save output
output_file = 'emails_extracted_cleaned.csv'
pd.DataFrame(results_sorted).to_csv(output_file, index=False)
print(f"\n🎉 Done! Cleaned results saved to '{output_file}'")
