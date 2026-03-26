# setup.py

from setuptools import setup, find_packages
import os

# Vakio ny README raha misy
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Requests-HTML: HTML Parsing for Humans (Modified Version)"

# Vakio ny version avy amin'ny __init__.py
def get_version():
    version_file = os.path.join("requests_html", "__init__.py")
    try:
        with open(version_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        return "0.1.0"
    return "0.1.0"

setup(
    name="requests-html",           # Anaran'ny package (azonao ovaina)
    version=get_version(),                   # Version
    author="Trade999",                    # Soloy anaranao
    author_email="lariotantsa@gmail.com",        # Soloy email-nao
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Trade999/requests-html",  # Soloy ny URL-nao
    packages=find_packages(),                # Hitady ny package rehetra
    install_requires=[
        "requests",
        "aiohttp",
        "pyppeteer>=0.2.2",
        "pyquery>=1.4.0",
        "fake-useragent>=0.1.11",
        "lxml",
        "lxml_html_clean==0.4.4",
        "parse>=1.12.0",
        "w3lib>=1.21.0",
        "cssselect>=1.1.0",
    ],
    classifiers=[                            # Classification
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",                 # Python version minimum
    license="MIT",                           # Licence (azonao ovaina)
    keywords="html parser scraping web requests pyppeteer",
)
