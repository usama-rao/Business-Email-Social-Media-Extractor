from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="business-email-extractor",
    version="2.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python tool for extracting email addresses and social media links from business websites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/business-email-extractor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "business-extractor=business_email_extractor:main",
        ],
    },
    keywords="email extractor, social media, business contacts, web scraping, CSV processing",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/business-email-extractor/issues",
        "Source": "https://github.com/yourusername/business-email-extractor",
    },
)
