#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Luis Trejo

"""
import sys
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

#### External Args
extrenarlArgs = getResolvedOptions(sys.argv, ['ENVIRONMENT','URLS'])
environment = ['ENVIRONMENT']
#page = extrenarlArgs['URLS']
page = 'https://www.amazon.com.mx/Luuna-Colchón-Memory-Látex-Matrimonial/dp/B019YBYBSC?th=1'
driver = webdriver.Chrome()
driver.get(page)
source = driver.page_source
#time.sleep(20)

def price(driver):
    # Obtiene la página actual
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Encuentra el ASIN
    asin_element = soup.find_all('span', class_='a-list-item')
    for element in asin_element:
        if 'ASIN' in element.text:
            asin = element.text.split()[-1]

    # Encuentra el precio
    price_element = soup.find('span', class_='a-price-whole')
    price = price_element.text if price_element else 'N/A'

    df = pd.DataFrame({
        'ASIN': [asin],
        'Price': [price]
    })
    return df


def product_details(driver):
    # Obtiene la página actual
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Encuentra el ASIN
    asin_element = soup.find_all('span', class_='a-list-item')
    for element in asin_element:
        if 'ASIN' in element.text:
            asin = element.text.split()[-1]
            break
    else:
        asin = 'N/A'

    # Encuentra el título del producto
    title_element = soup.find('span', id='productTitle')
    title = title_element.text.strip() if title_element else 'N/A'

    # Encuentra la descripción del producto
    description_element = soup.find('div', id='feature-bullets')
    description_items = description_element.find_all('span', class_='a-list-item') if description_element else []
    description = ' '.join(item.text.strip() for item in description_items)

    df = pd.DataFrame({
        'ASIN': [asin],
        'Title': [title],
        'Description': [description]
    })
    return df

def reviews_and_ratings(driver, number_of_reviews=5):
    # Obtiene la página actual
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Encuentra el ASIN
    asin_element = soup.find_all('span', class_='a-list-item')
    for element in asin_element:
        if 'ASIN' in element.text:
            asin = element.text.split()[-1]
            break
    else:
        asin = 'N/A'

    # Extraer reseñas y calificaciones
    reviews_elements = soup.find_all('div', {'data-hook': 'review'}, limit=number_of_reviews)
    reviews = []
    ratings = []
    for review_element in reviews_elements:
        # Extraer la reseña
        review_text_element = review_element.find('span', {'data-hook': 'review-body'})
        review_text = review_text_element.text.strip() if review_text_element else 'N/A'
        review_text = review_text.replace('Leer más', '').strip()
        reviews.append(review_text)

        # Extraer la calificación por estrellas
        rating_element = review_element.find('i', {'data-hook': 'review-star-rating'})
        rating = rating_element.text.strip().split(' ')[0] if rating_element else 'N/A'
        ratings.append(rating)

    df = pd.DataFrame({
        'ASIN': [asin] * len(reviews),
        'Reviews': reviews,
        'Ratings': ratings
    })

    return df

df_price = price(driver)
df_details = product_details(driver)
df_reviews = reviews_and_ratings(driver)