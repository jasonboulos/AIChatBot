import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import unquote
import urllib3
import random

# File paths and configurations
medicaments_excel_file_path = './docs/excelData/Medicaments.xlsx'
news_excel_file_path = './docs/excelData/news.xlsx'
recommendation_excel_file_path = './docs/excelData/recommendation.xlsx'
base_directory = "./docs/pdfData/HAS"

# Configure requests session with retry logic
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"],
)
session.mount("https://", HTTPAdapter(max_retries=retries))

def load_urls_from_excel(file_path):
    urls = []
    try:
        excelFile = pd.ExcelFile(file_path)
        for sheet_name in excelFile.sheet_names:
            sheet_data = pd.read_excel(file_path, sheet_name= sheet_name)
            urls.extend(sheet_data['Url'].dropna().tolist())
    except Exception as e:
        print(f"Error loading URLs from {file_path}: {e}")
    return urls

def decode_proxied_url(proxied_url):
    if "core.xvox.fr" in proxied_url:
        encoded_url = proxied_url.split("has-sante.fr/")[-1]
        decoded_url = unquote(encoded_url)
        return decoded_url
    return proxied_url

def get_pdf_link(page_url):
    try:
        response = session.get(page_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        for link in soup.find_all("a", href=True):
            if link['href'].endswith(".pdf"):
                pdf_url = link['href']
                if not pdf_url.startswith("http"):
                    pdf_url = requests.compat.urljoin(page_url, pdf_url)
                pdf_url = decode_proxied_url(pdf_url)
                return pdf_url
    except Exception as e:
        print(f"Error fetching PDF link from {page_url}: {e}")
    return None

def download_pdf(pdf_url, save_directory):
    try:
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        
        pdf_name = pdf_url.split("/")[-1]
        pdf_path = os.path.join(save_directory, pdf_name)
        if os.path.exists(pdf_path):
            print(f"File already exists: {pdf_name}. Skipping download.")
            return
        
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = session.get(pdf_url, timeout=10, verify=False)
        response.raise_for_status()

        if "application/pdf" in response.headers.get("Content-Type", ""):
            with open(pdf_path, "wb") as pdf_file:
                pdf_file.write(response.content)
                print(f"Downloaded: {pdf_name}")
        else:
            print(f"Invalid content for {pdf_url}: Not a PDF.")
    except Exception as e:
        print(f"Failed to download {pdf_url}: {e}")

def process_urls(urls, section_name, base_directory, max_pdfs):
    section_directory = os.path.join(base_directory, section_name)
    downloaded_count = 0
    failed_urls = []

    for url in urls:
        if downloaded_count >= max_pdfs:
            break

        print(f"Processing: {url}")
        pdf_url = get_pdf_link(url)
        if pdf_url:
            print(f"PDF URL: {pdf_url}")
            download_pdf(pdf_url, section_directory)
            downloaded_count += 1
        else:
            print(f"No PDF found for: {url}")
            failed_urls.append(url)

    if failed_urls:
        log_file_name = f"failed_urls_{section_name}.log"
        with open(log_file_name, "w") as log_file:
            for url in failed_urls:
                log_file.write(f"{url}\n")
        print(f"Logged {len(failed_urls)} failed URLs to '{log_file_name}'.")

# Load URLs from the three Excel files
urls_medicaments = load_urls_from_excel(medicaments_excel_file_path)
urls_news = load_urls_from_excel(news_excel_file_path)
urls_recommendations = load_urls_from_excel(recommendation_excel_file_path)


all_urls = {
    "Medicaments": urls_medicaments,
    "News": urls_news,
    "Recommendations": urls_recommendations
}

pdf_limits = {
    "Medicaments": 50,  
    "News": 50,       
    "Recommendations": 50
}

# Run the script for each section
for section_name, urls in all_urls.items():
    random.shuffle(urls)  # Shuffle the URLs for variety
    process_urls(urls[:pdf_limits[section_name]], section_name, base_directory, pdf_limits[section_name])


