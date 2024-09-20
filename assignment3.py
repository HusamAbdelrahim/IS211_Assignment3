import argparse
import requests
import csv
import re

def download_csv(URL):
    response = requests.get(URL)

    if response.status_code == 200:
        # open a file in write binary mode and write content of the response to file
        with open('weblog.csv', 'wb') as file:
            file.write(response.content)
        print("CSV file downloaded")
    else:
        print(f"Fail to download CSV file status code: {response.status_code}")
        

def process_file():
    processed_data = []
    try:
        with open('weblog.csv', 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                path, datetime_accessed, browser, status, request_size = row
                processed_data.append({
                    'path': path,
                    'datetime_accessed': datetime_accessed,
                    'browser': browser,
                    'status': status,
                    'request_size': request_size
                })
    except FileNotFoundError :
        print('The file weblog.csv does not exist or unable to process file.')

    return processed_data

def search_image_hits(DATA): 
    # define reg exp pattern for image file extensions
    image_pattern = re.compile(r'\.(jpg|gif|png)$', re.IGNORECASE)

    total_requests = len(DATA)
    image_requests = 0

    for entry in DATA:
        path = entry['path']
        if image_pattern.search(path):
            image_requests += 1

    # calculate percentage of image requests
    if total_requests > 0:
        percentage = (image_requests / total_requests) * 100
        print(f'Image requests account for {percentage:.1f}% of all requests.')
    else:
        print("No requests found to calc %")

def find_most_popular_browser(DATA):
    # define regular exp to identify browsers
    browsers = {
        'Firefox': re.compile(r'Firefox/'),
        'Chrome': re.compile(r'Chrome/'),
        'Internet Explorer': re.compile(r'MSIE|Trident/'),
        'Safari': re.compile(r'Safari/'),
    }
    
    # dict to count of each browser
    browser_counts = {
        'Firefox': 0,
        'Chrome': 0,
        'Internet Explorer': 0,
        'Safari': 0
    }
    
    for entry in DATA:
        user_agent = entry['browser']
        found = False
        for browser, pattern in browsers.items():
            if pattern.search(user_agent):
                browser_counts[browser] += 1
                found = True
                break
        # Optionally handle cases where no known browser is detected
        if not found:
            browser_counts['Other'] += 1
    
    # find most popular browser
    if browser_counts:
        most_popular_browser = max(browser_counts, key=browser_counts.get)
        print(f'The most popular browser is: {most_popular_browser}')
    else:
        print('No browser data available.') 

def main(URL):
    # download csv and save as weblog.csv file 
    download_csv(URL)
    
    # process csv data in memory as list of dictionaries
    processed_data = process_file()
    
    # search for image hits
    search_image_hits(processed_data)

    find_most_popular_browser(processed_data)

if __name__ == "__main__":
    # argument parser to get given --url input
    parser = argparse.ArgumentParser(description="process a url")
    parser.add_argument('--url', type=str, required=True);
    args = parser.parse_args()

    main(args.url)