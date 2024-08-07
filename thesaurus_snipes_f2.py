#import pandas as pd
#import time
#import undetected_chromedriver as uc
#from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
#import signal
#import sys
#
## Configurar el controlador de Chrome
#chromedriver_path = r"C:/Users/brian.amaya/Documents/2.Proyectos/Bedex/chromedriver-win64/chromedriver-win64/chromedriver.exe"
#chrome_options = uc.ChromeOptions()
#chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--lang=es")
#chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--start-maximized")
#
#driver = uc.Chrome(options=chrome_options)
#
#
## URL de inicio
#url = "http://vocabularios.caicyt.gov.ar/spines/index.php?tema=1223&/agricultura"
#driver.get(url)
#time.sleep(5)  # Esperar a que la página cargue completamente
#
## Extraer el keyword
#keyword_element = driver.find_element(By.CLASS_NAME, "estado_termino13")
#keyword = keyword_element.text.strip()
#
## Extraer los términos y keywords
#terms_data = []
#
#tab_content = driver.find_element(By.ID, "tabContent")
#terms_sections = tab_content.find_elements(By.TAG_NAME, 'ul')
#for section in terms_sections:
#    acronym_elements = section.find_elements(By.CLASS_NAME, 'thesacronym')
#    for acronym_element in acronym_elements:
#        term_text = acronym_element.text.strip()
#        parent_li = acronym_element.find_element(By.XPATH, './..')
#        link_elements = parent_li.find_elements(By.TAG_NAME, 'a')
#        for link_element in link_elements:
#            keyword_text = link_element.text.strip()
#            if keyword_text:  # Verificar si keyword_text no está vacío
#                terms_data.append((term_text, keyword_text))
#
## Construir el DataFrame
#data = []
#for term_text, keyword_text in terms_data:
#    data.append({
#        "keyword": keyword,
#        "terminos": term_text,
#        "keywords": keyword_text
#    })
#
#df = pd.DataFrame(data)
#
## Guardar el DataFrame en un archivo CSV
#df.to_csv('scraping_results.csv', index=False)
#
#print("El archivo scraping_results.csv ha sido creado con éxito.")
#
## Cerrar el navegador
#driver.quit()


#import pandas as pd
#import time
#import undetected_chromedriver as uc
#from selenium.webdriver.common.by import By
#import signal
#import sys
#import os
#
## Crear un DataFrame vacío para almacenar los resultados globalmente
#results_df = pd.DataFrame(columns=["keyword", "terminos", "keywords"])
#
## Función para manejar interrupciones y guardar el progreso
#def signal_handler(sig, frame):
#    global results_df
#    print("Interrupción detectada, guardando el progreso...")
#    results_df.to_csv('scraping_results.csv', index=False)
#    driver.quit()
#    sys.exit(0)
#
#signal.signal(signal.SIGINT, signal_handler)
#
## Leer los enlaces desde el archivo CSV
#vocabularios_df = pd.read_csv('vocabularios_spines.csv')
#
## Configurar el controlador de Chrome
#chromedriver_path = r"C:/Users/brian.amaya/Documents/2.Proyectos/Bedex/chromedriver-win64/chromedriver-win64/chromedriver.exe"
#chrome_options = uc.ChromeOptions()
#chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--lang=es")
#chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--start-maximized")
#driver = uc.Chrome(options=chrome_options)
#
## Iterar sobre cada enlace en la columna 'word_link'
#for index, row in vocabularios_df.iterrows():
#    url = row['word_link']
#    driver.get(url)
#    time.sleep(5)  # Esperar a que la página cargue completamente
#
#    try:
#        # Extraer el keyword
#        keyword_element = driver.find_element(By.CLASS_NAME, "estado_termino13")
#        keyword = keyword_element.text.strip()
#
#        # Extraer los términos y keywords
#        terms_data = []
#
#        tab_content = driver.find_element(By.ID, "tabContent")
#        terms_sections = tab_content.find_elements(By.TAG_NAME, 'ul')
#        for section in terms_sections:
#            acronym_elements = section.find_elements(By.CLASS_NAME, 'thesacronym')
#            for acronym_element in acronym_elements:
#                term_text = acronym_element.text.strip()
#                parent_li = acronym_element.find_element(By.XPATH, './..')
#                link_elements = parent_li.find_elements(By.TAG_NAME, 'a')
#                for link_element in link_elements:
#                    keyword_text = link_element.text.strip()
#                    if keyword_text:  # Verificar si keyword_text no está vacío
#                        terms_data.append((term_text, keyword_text))
#
#        # Construir el DataFrame temporal
#        temp_df = pd.DataFrame([{
#            "keyword": keyword,
#            "terminos": term_text,
#            "keywords": keyword_text
#        } for term_text, keyword_text in terms_data])
#
#        # Añadir los datos al DataFrame de resultados
#        results_df = pd.concat([results_df, temp_df], ignore_index=True)
#
#        # Guardar el progreso al instante
#        results_df.to_csv('scraping_results.csv', index=False)
#    except Exception as e:
#        print(f"Error al procesar la URL: {url}")
#        print(e)
#        continue
#
#print("El archivo scraping_results.csv ha sido creado con éxito.")
#
## Cerrar el navegador
#driver.quit()
#

#import time
#import pandas as pd 
#import undetected_chromedriver as uc
#from selenium.webdriver.common.by import By
#import signal
#import sys
#
## Crear un DataFrame vacío para almacenar los resultados globalmente
#results_df = pd.DataFrame(columns=["keyword", "terminos", "keywords"])
#tree_df = pd.read_csv('vocabularios_spines.csv')
#
## Función para manejar interrupciones y guardar el progreso
#def signal_handler(sig, frame):
#    global results_df, tree_df
#    print("Interrupción detectada, guardando el progreso...")
#    results_df.to_csv('scraping_results.csv', index=False)
#    tree_df.to_csv('vocabularios_spines.csv', index=False)
#    driver.quit()
#    sys.exit(0)
#
#signal.signal(signal.SIGINT, signal_handler)
#
## Configurar el controlador de Chrome
#chromedriver_path = r"C:/Users/brian.amaya/Documents/2.Proyectos/Bedex/chromedriver-win64/chromedriver-win64/chromedriver.exe"
#chrome_options = uc.ChromeOptions()
#chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--lang=es")
#chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--start-maximized")
#driver = uc.Chrome(options=chrome_options)
#
## Iterar sobre cada enlace en la columna 'word_link'
#for index, row in tree_df.iterrows():
#    url = row['word_link']
#    driver.get(url)
#    time.sleep(5)  # Esperar a que la página cargue completamente
#
#    try:
#        # Extraer el keyword
#        keyword_element = driver.find_element(By.CLASS_NAME, "estado_termino13")
#        keyword = keyword_element.text.strip()
#
#        # Extraer los términos y keywords
#        terms_data = []
#
#        tab_content = driver.find_element(By.ID, "tabContent")
#        terms_sections = tab_content.find_elements(By.TAG_NAME, 'ul')
#        for section in terms_sections:
#            acronym_elements = section.find_elements(By.CLASS_NAME, 'thesacronym')
#            for acronym_element in acronym_elements:
#                term_text = acronym_element.text.strip()
#                parent_li = acronym_element.find_element(By.XPATH, './..')
#                link_elements = parent_li.find_elements(By.TAG_NAME, 'a')
#                for link_element in link_elements:
#                    keyword_text = link_element.text.strip()
#                    if keyword_text:  # Verificar si keyword_text no está vacío
#                        terms_data.append((term_text, keyword_text))
#
#        # Extraer el texto de la clase breadcrumb y construir la cadena delimitada por "|"
#        breadcrumb_elements = driver.find_elements(By.CSS_SELECTOR, "ol.breadcrumb li")
#        breadcrumb_texts = [element.text.strip() for element in breadcrumb_elements]
#        breadcrumb_tree = " | ".join(breadcrumb_texts)
#
#        # Añadir la columna 'tree' al DataFrame de vocabularios
#        tree_df.at[index, 'tree'] = breadcrumb_tree
#
#        # Construir el DataFrame temporal para resultados
#        temp_df = pd.DataFrame([{
#            "keyword": keyword,
#            "terminos": term_text,
#            "keywords": keyword_text
#        } for term_text, keyword_text in terms_data])
#
#        # Añadir los datos al DataFrame de resultados
#        results_df = pd.concat([results_df, temp_df], ignore_index=True)
#
#        # Guardar el progreso al instante
#        results_df.to_csv('scraping_results.csv', index=False)
#        tree_df.to_csv('vocabularios_spines.csv', index=False)
#    except Exception as e:
#        print(f"Error al procesar la URL: {url}")
#        print(e)
#        continue
#
#print("El archivo scraping_results.csv ha sido creado con éxito.")
#print("El archivo vocabularios_spines.csv ha sido actualizado con éxito.")
#
## Cerrar el navegador
#driver.quit()
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import signal
import sys

# Crear un DataFrame vacío para almacenar los resultados globalmente
results_df = pd.DataFrame(columns=["keyword", "terminos", "keywords"])

# Leer los datos existentes de los CSV
tree_df = pd.read_csv('raw_data/thesaurus/vocabularios_spines.csv')
existing_results_df = pd.read_csv('raw_data/thesaurus/thesaurus_spines.csv')

# Filtrar las filas que no tienen información en la columna 'tree' sin eliminar las filas del DataFrame original
rows_to_process = tree_df[tree_df['tree'].isnull()]

# Función para manejar interrupciones y guardar el progreso
def signal_handler(sig, frame):
    global results_df, tree_df, existing_results_df
    print("Interrupción detectada, guardando el progreso...")
    results_df = pd.concat([existing_results_df, results_df], ignore_index=True)
    results_df.to_csv('scraping_results.csv', index=False)
    tree_df.to_csv('vocabularios_spines.csv', index=False)
    driver.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Configurar el controlador de Chrome usando webdriver-manager
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--lang=es")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Iterar sobre cada enlace en la columna 'word_link' de las filas filtradas
for index, row in rows_to_process.iterrows():
    url = row['word_link']
    driver.get(url)
    time.sleep(5)  # Esperar a que la página cargue completamente

    try:
        # Extraer el keyword
        keyword_element = driver.find_element(By.CLASS_NAME, "estado_termino13")
        keyword = keyword_element.text.strip()

        # Extraer los términos y keywords
        terms_data = []

        tab_content = driver.find_element(By.ID, "tabContent")
        terms_sections = tab_content.find_elements(By.TAG_NAME, 'ul')
        for section in terms_sections:
            acronym_elements = section.find_elements(By.CLASS_NAME, 'thesacronym')
            for acronym_element in acronym_elements:
                term_text = acronym_element.text.strip()
                parent_li = acronym_element.find_element(By.XPATH, './..')
                link_elements = parent_li.find_elements(By.TAG_NAME, 'a')
                for link_element in link_elements:
                    keyword_text = link_element.text.strip()
                    if keyword_text:  # Verificar si keyword_text no está vacío
                        terms_data.append((term_text, keyword_text))

        # Extraer el texto de la clase breadcrumb y construir la cadena delimitada por "|"
        breadcrumb_elements = driver.find_elements(By.CSS_SELECTOR, "ol.breadcrumb li")
        breadcrumb_texts = [element.text.strip() for element in breadcrumb_elements]
        breadcrumb_tree = " | ".join(breadcrumb_texts)

        # Añadir la columna 'tree' al DataFrame de vocabularios
        tree_df.at[index, 'tree'] = breadcrumb_tree

        # Construir el DataFrame temporal para resultados
        temp_df = pd.DataFrame([{
            "keyword": keyword,
            "terminos": term_text,
            "keywords": keyword_text
        } for term_text, keyword_text in terms_data])

        # Añadir los datos al DataFrame de resultados
        results_df = pd.concat([results_df, temp_df], ignore_index=True)

        # Guardar el progreso al instante
        combined_results_df = pd.concat([existing_results_df, results_df], ignore_index=True)
        combined_results_df.to_csv('raw_data/thesaurus/thesaurus_spines.csv', index=False)
        tree_df.to_csv('raw_data/thesaurus/vocabularios_spines.csv', index=False)
    except Exception as e:
        print(f"Error al procesar la URL: {url}")
        print(e)
        continue

print("El archivo scraping_results.csv ha sido creado con éxito.")
print("El archivo vocabularios_spines.csv ha sido actualizado con éxito.")

# Cerrar el navegador
driver.quit()
