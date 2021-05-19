from bs4 import BeautifulSoup
import requests
import csv
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def artist_name():
    value = input("Please enter the artist:\n")
    value = str(value)
    print(f'You entered {value}')
    return value

def html_parse(value):
    options = Options()
    options.page_load_strategy = 'eager'
    boo = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)
    driver.get('https://soundcloud.com/'+value+'/tracks')
    while(boo):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        if soup.find('div', class_='paging-eof') is None:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(0.5)
        else:
            boo = False
    return soup

def add_rows(value, soup):
    csv_file = open(f'{value}.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Song Name', 'Number of Plays'])
    for element in soup.find_all('li', class_='soundList__item'):
        #print(element)
        name = element.find('div', attrs={'role':'group', 'class':'sound streamContext'})['aria-label']
        name = name.split(" by ")[0].split('Track: ')[1]

        num = element.find_all('span', class_='sc-visuallyhidden')[1].text
        num = num.split(' ')[0].split(',')
        num = int(num[0]+num[1])
        csv_writer.writerow([name, num])
    print("done")
    csv_file.close()

if __name__ == "__main__":
    artist = artist_name()
    soup = html_parse(artist)
    add_rows(artist, soup)
