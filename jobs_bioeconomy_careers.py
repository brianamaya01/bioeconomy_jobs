from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time

def main():
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")

    # Usar webdriver-manager para gestionar el Chromedriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # URL de la página web
    url = "https://bioeconomycareers.com/jobs"
    driver.get(url)

    job_ids = []
    job_titles = []
    job_links = []

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        job_listings = driver.find_elements(By.CLASS_NAME, "job-listings-item")

        for job_listing in job_listings:
            job_id = job_listing.get_attribute('data-jobid')
            job_ids.append(job_id)

            job_title_element = job_listing.find_element(By.CLASS_NAME, "job-details-link")
            job_title = job_title_element.text
            job_titles.append(job_title)

            job_link = job_title_element.get_attribute('href')
            job_links.append(job_link)

        # Encontrar el enlace 'Siguiente' a partir de la clase 'page-item' y el atributo 'rel="next"'
        next_button = None
        page_items = driver.find_elements(By.XPATH, '//ul[@class="pagination"]/li[not(contains(@class, "disabled"))]/a')
        for item in page_items:
            if item.get_attribute('rel') == 'next':
                next_button = item
                break

        if next_button and next_button.is_displayed():
            next_button.click()
            time.sleep(3)
        else:
            break

    # Definir la ruta del archivo CSV de salida
    output_dir = os.path.join('bioeconomy_careers', 'raw_data')
    output_file = '0.bioec_careers_links.csv'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)

    data = {
        'job_id': job_ids,
        'job_title': job_titles,
        'job_link': job_links
    }
    df = pd.DataFrame(data)

    # Guardar el DataFrame en un archivo CSV
    df.to_csv(output_path, index=False)

    print(f'Datos guardados en: {output_path}')

    driver.quit()

if __name__ == "__main__":
    main()
