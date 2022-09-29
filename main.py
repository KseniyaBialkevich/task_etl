import requests
import json
from bs4 import BeautifulSoup
import os
import sys
import pandas as pd



def read_input_data(input_file):
    with open (os.path.join(sys.path[0], input_file), "r") as f:
        input_data = json.load(f)
        return input_data


def create_dataFrame(output_file):
    df = pd.DataFrame(columns=[
        'request_url','status_code','elapsed_time', 'encoding', 'content_encoding', 'entity_tag', 'extract_link','specific_word', 'specific_word_exist'
        ])
    df.to_csv(os.path.join(sys.path[0], output_file), header=True, index=False)
    return df


def make_request(url):
    response = requests.get(url)
    return response


def parse_html(response_text):
    souptext = BeautifulSoup(response_text, 'html.parser')
    return souptext


def extract_links(souptext):
    set_links = set()
    for link in souptext.find_all('a'):
        url = link.get('href')
        set_links.add(url)
    links = list(set_links)
    return links


def check_specific_word(souptext, term):
    # Get string without tegs:
    cleantext = (souptext.get_text(strip=True)).lower()
    word_exist = False
    if term.lower() in cleantext:
        word_exist = True
    return word_exist


def run_process(input_file, output_file):
    # Open json file with input data:
    input_data = read_input_data(input_file)
    
    # Make the request:
    response = make_request(input_data["url"])

    data_dict = {
        'request_url': input_data["url"],
        'status_code': response.status_code,
        'elapsed_time': (response.elapsed).total_seconds(), 
        'encoding': response.encoding, 
        'content_encoding': response.headers["Content-Encoding"], 
        'entity_tag': response.headers["ETag"],
        'extract_link': None,
        'specific_word': None, 
        'specific_word_exist': None
        }

    # Create DataFrame:
    df = create_dataFrame(output_file)

    # Checking the status code:
    if 200 <= response.status_code < 300:
        # Parsing html document:
        souptext = parse_html(response.text)
        # Extract all links:
        links = extract_links(souptext)
        # Check the specific word:
        specific_word = input_data["specific_word"]
        word_exist = check_specific_word(souptext, specific_word)
        data_dict.update({'specific_word': specific_word, 'specific_word_exist': word_exist})
        if len(links) > 0:
            data_dict.update({'extract_link': links})
            df = pd.concat([df, pd.DataFrame(data_dict)], ignore_index = True)
        else:
            df = df.append(data_dict, ignore_index = True)    
    else:
        df = df.append(data_dict, ignore_index = True)

    # Write data to the output file:
    df.to_csv(os.path.join(sys.path[0], output_file), mode='a', header=False, index=False)
    

if __name__ == "__main__":
    # Arguments:
    input_file = "input/data.json"
    output_file = "output/data.csv"
    # Run process:
    run_process(input_file, output_file)