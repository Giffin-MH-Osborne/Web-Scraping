from user import write_user_data
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


import requests
import json
from Job import Job

from bs4 import BeautifulSoup


#global variables
USER = None
LOCATION = ""
URL = 'http://indeed.ca'
DRIVER_PATH = './webdrivers/chromedriver'
WINDOW_SIZE = "1920,1080"


#Run driver in background (WIP)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

#Customizable Options
hardcode_location = "Toronto, ON"
set_location = "Kincardine_ON"
number_of_pages = 10

#Job Titles to Search
search_jobs = [
    'Software Developer',
    'Software Engineer',
    'Data Engineer',
    'Data Scientist'
]

#Store jobs before writing
found_jobs = []

def get_user_data():
    global LOCATION

    user_found = False
    while(not user_found):
        print('getting user...\n')
        try:
            #Load the JSON file with the user data and set found to true
            print('found existing user!')
            USER = json.loads(open('user.txt').read())
            user_found = True
        except(FileNotFoundError):
            #Save new user data to JSON file
            print('saving user data!')
            write_user_data()
    LOCATION = USER['City'] +', ' + USER['Province']
    print("\n{0}\n".format(json.dumps(USER, indent=4)))

def search(job_title: str): 
    global set_location
    
    #Find the text inputs for Job Title and Job Location for search
    what = driver.find_element_by_id('text-input-what')
    where = driver.find_element_by_id('text-input-where')

    #Send the Job Title to the text field
    what.send_keys(job_title)

    #Clear the existing location in text
    #**CLEAR FUNCTION DOESNT WORK SO BACKSPACE FOR NOW**
    if(set_location != hardcode_location):
        for i in range(len(set_location) + 1):
            where.send_keys(Keys.BACKSPACE)
        set_location = hardcode_location
        where.send_keys(hardcode_location)
    #Send the location to search to the text field
    where.send_keys(Keys.RETURN)

#Get information from page
def scrape_page(page_source, page_num):
    global URL, found_jobs

    #initialize the scraper
    soup = BeautifulSoup(page_source, 'lxml')

    #Find all the job cards displayed and their relative links
    job_cards = soup.find_all('td', {'class': 'resultContent'})
    job_links = soup.find_all('a', {'role': 'button'})

    #Check if the page has pagination (More than one page of jobs)
    pagination = soup.find('ul', {'class': 'pagination-list'})

    #Convert the job cards into a readable string
    index = 0
    for card in job_cards:
        header_tag = card.find('h2', {'class': 'jobTitle'}).find_all('span')
        if(len(header_tag) > 1):
            title = str(header_tag[1].text).replace(',', ' ')
        else:
            title = str(header_tag[0].text).replace(',', ' ')
        
        company_name = str(card.find('span', {'class': 'companyName'}).text).replace(',', ' ')
        company_location = str(card.find('div', {'class': 'companyLocation'}).text).replace(',', ' ')
        span_tag = card.find('div', {'class': 'salary-snippet-container'})        
        if(span_tag != None):
            try:
                salary = str(span_tag.text)
                link = URL + job_links[index]['href']

                job = Job(title, company_name, company_location, salary, link)
                
                job.display()

                found_jobs.append(job)    
            except:
                continue
        index += 1

    #if there are multiple pages proceed to the next one
    pages = []
    if(pagination != None):
        pagination_links = pagination.find_all('a')
        for link in pagination_links:
            pages.append(link.attrs['href'])

        if(page_num < number_of_pages):
            new_url = URL + pages[page_num]
            print(new_url)
            driver.get(new_url)
            page_num += 1
            scrape_page(driver.page_source, page_num)
         
#Write the found jobs to a csv file
def write_to_csv():
    file = open('jobs.csv', 'w')

    headers = 'Title, Company, Location, Salary,Link\n'
    file.write(headers)

    for job in found_jobs:
        text_to_write = job.csv_format()
        file.write(text_to_write)

if __name__ == "__main__":
    get_user_data()

    #initialize the driver
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    
    #search for each job initialized above
    for job_title in search_jobs:
        driver.get(URL)
        print('Searching for {0}...'.format(job_title))
        search(job_title)
        scrape_page(driver.page_source, 0)

    driver.close()

    write_to_csv()

    print("Found {0} jobs!".format(len(found_jobs)))

    
    