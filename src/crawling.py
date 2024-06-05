from random import randint
import time
import json
from typing import Iterable
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def _parse_seleinum_response(result):
    """ 크롤링한 셀레니움 객체를 title, text, url로 파싱 """
    data = []
    for content in result:
        title = content.text.split("\n")[0].split("[")[0].strip()
        text = content.text.split("\n")[1]
        url = content.find_elements(By.TAG_NAME, "a")[0].get_attribute("href")
        
        data.append({"title": title, "text": text, "url": url})
        
    return data

def _selenium_crawling(page_num: int):
    """ 셀레니움 크롤링 내부 함수"""
    
    options = Options()
    options.add_argument('--headless')
    
    url = "https://terms.naver.com/list.naver?cid=50871&categoryId=50871&page={idx}"
    url = url.format(idx=page_num)

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    result = driver.find_elements(By.CLASS_NAME, "info_area")
    data = _parse_seleinum_response(result)
    time.sleep(randint(0, 20))
    
    return data

def parallel_crawling(n_worker: int = None, iterables:Iterable = None):
    """ Multiprocessing으로 크롤링 병렬처리 """
    
    workers = cpu_count() - 3
    
    if n_worker:
        workers = n_worker
        
    if not iterables:
        raise ValueError("iterables are not setted.")
    
    with Pool(workers) as p:
        data = list(tqdm(p.imap(_selenium_crawling, iterables)))
        
    return data
    