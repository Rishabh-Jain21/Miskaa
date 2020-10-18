'''1. Your assignment is to scrape information from urls(Use Python/Beautiful soup) as a list of json elements. 
Each json element should contain attributes extracted from a url web page like
scraped_url,header_title,youtube_url,image_url,viewt,favourit_coune_count,comment_count and steps
 titles (as list) and supplies (as list if data is available on page).
URLS
1. https://www.instructables.com/Building-a-Self-Driving-Boat-ArduPilot-Rover/
2. https://www.instructables.com/Hydraulic-Craft-Stick-Box/
3. https://www.instructables.com/How-to-Make-a-Self-Watering-Plant-Stand/
Assignment Guidelines:
● Share assignment solution and instructions to run as a github repo link.
● The deadline for submission will be 24 hours.'''

import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from time import sleep


def get_page_source(link):
    
    driver_path = r"D:\Python\my_codes\chromedriver.exe"
    driver = webdriver.Chrome(driver_path)
    driver.get(link)
    sleep(5)
    source = driver.page_source
    driver.close()
    return source


def supply_list(page_soup, supplies_list, attributes):
    supplies = page_soup.find("h3", {"class": "supplies-heading"})
    attributes['supplies'] = None
    if supplies:
        if len(supplies.findChildren()) == 0:
            try:
                for supply in supplies.parent.find('ul').findAll("li"):
                    supplies_list.append(supply.text)
                    attributes['supplies'] = supplies_list
            except:
                pass
        else:
            for supply in page_soup.find("h3").parent.findAll('p')[2:]:
                supplies_list.append(supply.text.lstrip("·       "))
                attributes['supplies'] = supplies_list


def steps_list(page_soup, steps, attributes):
    for step in page_soup.findAll('h2', {'class': 'step-title'})[1:]:
        steps.append(step.text)
    attributes['steps'] = steps


def correction(status_code):
    if len(status_code) != 0:
        status_code = "".join(status_code[0].text.split(','))
        try:
            status_code = int(status_code)
            return status_code
        except ValueError:
            return 0
    return 0


def header_status(page_soup, attributes):
    views = correction(page_soup.select(".view-count"))
    favourite = correction(page_soup.select(".favorite-count"))
    comment = correction(page_soup.select(".comment-count"))

    attributes['views_count'] = views
    attributes['favourites_count'] = favourite
    attributes['comments_count'] = comment


def images_url_list(page_soup, images_url, attributes):
    for image in page_soup.find("div", {"class": "photoset"}).findAll("img"):
        images_url.append(image['src'])
    attributes['image_url'] = images_url


def json_conversion(answer):
    return json.dumps(answer, indent=4)


def main():
    links = ["https://www.instructables.com/Hydraulic-Craft-Stick-Box/", "https://www.instructables.com/Building-a-Self-Driving-Boat-ArduPilot-Rover/", "https://www.instructables.com/How-to-Make-a-Self-Watering-Plant-Stand/"
             ]
    answer = {}
    for link in links:
        steps = []
        images_url = []
        supplies_list = []
        attributes = dict()
        source = get_page_source(link)
        soup = BeautifulSoup(source, 'lxml')
        key = link.split("/")[-2]
        attributes["url"] = link
        attributes['title'] = soup.find('title').text

        supply_list(soup, supplies_list, attributes)
        steps_list(soup, steps, attributes)
        header_status(soup, attributes)
        images_url_list(soup, images_url, attributes)

        answer[key] = attributes

    json_data = json_conversion(answer)
    print(json_data)


if __name__ == '__main__':
    main()
