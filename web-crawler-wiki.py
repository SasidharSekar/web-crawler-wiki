import PyRTF.document
import PyRTF.document.section
import requests
import bs4
from bs4 import BeautifulSoup
import PyRTF
from PyRTF import Renderer
from PyRTF.Elements import Document
from PyRTF.document.section import Section
from PyRTF.document.paragraph import Paragraph
# This script fetches a Wikipedia page and prints its title and all the paragraphs.
def fetch_wiki_page(url):
    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def parse_wiki_page(html):
    soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
    h1_tag = soup.find('h1')
    title = h1_tag.text if h1_tag else "No title found"
    h2_tags = soup.find_all('h2')
    all_next_tags = []
    if h2_tags:
        current_tag = h2_tags[0]
        while True:
            next_tag = current_tag.find_next(['p', 'h2'])
            if next_tag is None:
                break
            all_next_tags.append(next_tag)
            current_tag = next_tag
    else:
        print("No H2 tags found in the document.")
        return title, []
    return title, all_next_tags

def create_rtf_file(title, all_next_tags):
    doc = Document()
    section = Section()
    doc.Sections.append(section)
    # Add title
    section.append(Paragraph(title))
    # Add all next tags
    for tag in all_next_tags:
        if tag.name == 'h2':
            section.append(Paragraph(tag.text))
        elif tag.name == 'p':
            section.append(Paragraph(tag.text))
    # Save the document
    with open(title+'.rtf', 'w') as f:
        Renderer.Renderer().Write(doc, f)

if __name__ == "__main__":
    URL = "https://en.wikipedia.org/wiki/Web_crawler"
    html_content = fetch_wiki_page(URL)
    if html_content:
        title, all_next_tags = parse_wiki_page(html_content)
        create_rtf_file(title, all_next_tags)
    else:
        print("Failed to retrieve the page.")