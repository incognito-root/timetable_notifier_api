import os
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from datetime import datetime, timedelta
import difflib

TIMETABLE_URL = 'https://lahore.comsats.edu.pk/student/time-table.aspx'
SEARCH_WORD = 'FA23-BCS-C'
PDF_FOLDER = './data'
PREVIOUS_PDF_PATH = os.path.join(PDF_FOLDER, 'previous_timetable.pdf')
NEW_PDF_PATH = os.path.join(PDF_FOLDER, 'new_timetable.pdf')


def download_pdf(pdf_url, save_path):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded and saved PDF to {save_path}")
    else:
        print(f"Failed to download PDF from {pdf_url}")


def get_timetable_pdf_link():
    response = requests.get(TIMETABLE_URL)
    if response.status_code != 200:
        print("Failed to fetch the timetable webpage.")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    link = soup.find('a', string='Undergraduate and Graduate Classes Timetable')
    
    print(link)
    if link:
        pdf_url = 'https://lahore.comsats.edu.pk/student/' + link['href']
        print(f"Found PDF link: {pdf_url}")
        return pdf_url
    else:
        print("Could not find the timetable link.")
        return None


def extract_text_from_pdf(pdf_path, search_word):
    try:
        with open(pdf_path, 'rb') as f:
            pdf_reader = PdfReader(f)
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if search_word in page_text:
                    print(f"'{search_word}' found on page {page_num + 1}")
                    return page_text
        print(f"'{search_word}' not found in the PDF.")
        return None
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None


def compare_pdfs_text(prev_text, new_text):
    if prev_text == new_text:
        print("The content is identical in both PDFs.")
        return "The content is identical in both PDFs."
    else:
        diff = difflib.ndiff(prev_text.splitlines(), new_text.splitlines())
        print("Differences found:")
        for line in diff:
            if line.startswith('+ ') or line.startswith('- '):
                print(line)


def check_and_update_timetable(section):
    SEARCH_WORD = section
    pdf_url = get_timetable_pdf_link()
    if not pdf_url:
        return
    
    os.makedirs(PDF_FOLDER, exist_ok=True)
    download_pdf(pdf_url, NEW_PDF_PATH)

    new_text = extract_text_from_pdf(NEW_PDF_PATH, SEARCH_WORD)
    if not new_text:
        return
    
    textToReturn = ""
    if os.path.exists(PREVIOUS_PDF_PATH):
        prev_text = extract_text_from_pdf(PREVIOUS_PDF_PATH, SEARCH_WORD)
        if prev_text:
            textToReturn = compare_pdfs_text(prev_text, new_text)
            os.replace(NEW_PDF_PATH, PREVIOUS_PDF_PATH)
            return textToReturn;

    
    os.replace(NEW_PDF_PATH, PREVIOUS_PDF_PATH)
    textToReturn = "New PDF saved as the previous PDF for future comparisons."
    return textToReturn;


def should_check_for_new_timetable():
    try:
        if not os.path.exists(PREVIOUS_PDF_PATH):
            return True

        last_modified_time = datetime.fromtimestamp(os.path.getmtime(PREVIOUS_PDF_PATH))
        return datetime.now() > last_modified_time + timedelta(days=3)
    except Exception as e:
        print(f"Error checking last update time: {e}")
        return True


# check_and_update_timetable()
# if should_check_for_new_timetable():
# else:
#     print("No need to check for a new timetable yet.")
