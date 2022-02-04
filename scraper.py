from selenium import webdriver
from selenium.webdriver.common.by import By
import time

YOUTUBE_TRENDING_URL: str = 'https://www.youtube.com/feed/trending'
CATEGORIES = ['short-trending', 'trending', 'recently-trending']

driver = webdriver.Edge()
driver.get(YOUTUBE_TRENDING_URL)
time.sleep(2)
print("Title :", driver.title)
contents = driver.find_element(By.ID, 'contents')
video_container = contents.find_elements(By.ID, 'grid-container')
scraped = {}

for container, category in zip(video_container, CATEGORIES):
    titles = container.find_elements(By.ID, 'title-wrapper')
    data = []
    for title in titles:
        data.append(title.text)
    scraped[category] = data
print(scraped)

driver.quit()
