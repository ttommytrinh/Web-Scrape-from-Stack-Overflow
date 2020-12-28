import requests
from requests_html import HTML
import time
import pandas as pd

#removes the votes text in scrape
def remove_vote_text(text, keyname=None):
    if keyname == "votes":
        return text.replace("\nvotes", "")
    return text

#scrapes the text and creates a dictionary with the classes wanted
def parse_tagged_page(html):
    question_summary = html.find(".question-summary")
    data = []
    classes_needed = [".question-hyperlink", ".vote", ".tags"]
    key_names = ["question", "votes", "tags"]
    for element in question_summary:
        question_data = {}
        for i, x in enumerate(classes_needed):
            keyname = key_names[i]
            question_data[keyname] = remove_vote_text(element.find(x, first=True).text, keyname=keyname)
        data.append(question_data)
    return data

#grabs the html code from url
def extract_data_from_url(url):
    r = requests.get(url)
    if r.status_code not in range(200,299):
        return []
    html_string = r.text
    html = HTML(html=html_string)
    data = parse_tagged_page(html)
    return data

#what tag and filter
def scrape_tag(tag, filter = "Votes", max_pages=2, pagesize=25):
    data = []
    base_url = "https://stackoverflow.com/questions/tagged/"
    for page in range(1, max_pages+1):
        url = f"{base_url}{tag}?tab={filter}&page={page}&pagesize={pagesize}"
        data += extract_data_from_url(url)
        time.sleep(1.2)
    return data

def scrape_runner():
    tag_input = input("What tag would you like to search? ")
    filter_yn = input("Would you like to filter by something? Y/N ")
    if filter_yn == "Y":
        filter_input = input("What would you like me to filter by? ")
        data = scrape_tag(tag_input, filter_input)
        df = pd.DataFrame(data)
        df.to_csv(f"{tag_input}_SCRAPE.csv", index=False)
    else:       
        data = scrape_tag(tag_input)
        df = pd.DataFrame(data)
        df.to_csv(f"{tag_input}_SCRAPE.csv", index=False)
        
scrape_runner()
