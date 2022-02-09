import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys


YOUTUBE_TRENDING_URL: str = 'https://www.youtube.com/feed/trending'


def get_driver():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Edge(options=options)
    return driver


def parse_video(video):
    thumbnail = video.find_element(By.ID, 'img')
    thumbnail_url = thumbnail.get_attribute('src')
    video_title_tag = video.find_element(By.ID, 'video-title')
    video_url = video_title_tag.get_attribute('href')
    video_title = video_title_tag.text
    spans = video.find_element(By.ID, 'metadata-line').find_elements(By.TAG_NAME, 'span')
    video_views = spans[0].text
    video_upload = spans[1].text
    data = {
        'title': video_title,
        'video_url': video_url,
        'thumbnail_url': thumbnail_url,
        'views': video_views,
        'upload_time': video_upload
    }
    return data


def get_videos(driver):
    scraped = {}
    contents = driver.find_element(By.ID, 'contents')
    video_containers = contents.find_elements(By.ID, 'grid-container')

    for i, video_container in enumerate(video_containers):
        videos = video_container.find_elements(By.TAG_NAME, 'ytd-video-renderer')
        datas = []
        for video in videos:
            video.location_once_scrolled_into_view
            data = parse_video(video)
            print(data)
            datas.append(data)
        scraped[f"container{i}"] = datas
        print(len(datas), end='\n\n')
    return scraped


if __name__ == "__main__":
    edge_driver = get_driver()
    edge_driver.get(YOUTUBE_TRENDING_URL)
    html = edge_driver.find_element(By.TAG_NAME, 'html')
    print("Title :", edge_driver.title)
    content = get_videos(edge_driver)

    edge_driver.close()
    edge_driver.quit()
