import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import signal
import sys
import os

# Función para guardar los resultados en un archivo CSV
def save_results():
    df = pd.DataFrame(results, columns=columns)
    if os.path.exists(output_file):
        df_existing = pd.read_csv(output_file)
        df = pd.concat([df_existing, df], ignore_index=True)
    df.to_csv(output_file, index=False)
    print(f"Resultados guardados en {output_file}")

# Manejador de la señal SIGINT para guardar los resultados al interrumpir el script
def signal_handler(sig, frame):
    print('Interrupción detectada. Guardando resultados...')
    save_results()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Archivo de keywords y archivo de resultados
keywords_file = "raw_data/jobs/keyword_status.csv"
output_file = "faoterm_results.csv"

# Leer las keywords desde el archivo CSV
keywords_df = pd.read_csv(keywords_file)
keywords = keywords_df['keyword'].tolist()  # Ajusta el nombre de la columna según corresponda

# Leer las keywords ya procesadas desde el archivo de resultados (si existe)
if os.path.exists(output_file):
    processed_df = pd.read_csv(output_file)
    processed_keywords = processed_df['Keyword'].unique().tolist()
else:
    processed_keywords = []

# Filtrar las keywords para procesar solo las nuevas
keywords_to_process = [kw for kw in keywords if kw not in processed_keywords]
print(f"Keywords a procesar: {keywords_to_process}")

# Configuración del navegador con webdriver-manager y modo incógnito
options = Options()
options.add_argument("--incognito")
options.add_argument("--lang=es")
options.add_argument("--disable-notifications")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL de la página a visitar
url = "https://www.fao.org/faoterm/es/"

# Abrir la página
driver.get(url)

# Esperar a que la barra de búsqueda esté presente
time.sleep(5)  # Espera fija de 5 segundos

# Lista para almacenar los resultados
results = []
columns = ["Término", "Idioma", "Materia", "Colección", "Keyword"]

# Función para extraer la tabla
def extract_table_data(keyword):
    global columns
    # Esperar a que la tabla esté presente
    time.sleep(5)  # Espera fija de 5 segundos

    # Verificar si la tabla está vacía
    try:
        empty_table = driver.find_element(By.CLASS_NAME, "dataTables_empty")
        if empty_table:
            # Si la tabla está vacía, agregar una fila con 'NA' y la keyword
            results.append(['NA', 'NA', 'NA', 'NA', keyword])
            print(f"Tabla vacía para keyword: {keyword}")
            return
    except:
        pass
    
    table = driver.find_element(By.ID, "searchResultTable")

    # Extraer los datos de la tabla
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if cols:
            data = [col.text for col in cols]
            data.append(keyword)
            results.append(data)
    print(f"Datos extraídos para keyword: {keyword}")

try:
    # Iterar sobre cada keyword
    for keyword in keywords_to_process:
        # Borrar la barra de búsqueda usando JavaScript antes de ingresar el nuevo keyword
        search_box = driver.find_element(By.ID, "searchBox")
        driver.execute_script("arguments[0].value = '';", search_box)
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        # Esperar a que el botón de búsqueda esté presente y hacer clic
        time.sleep(5)  # Espera fija de 5 segundos
        search_button = driver.find_element(By.ID, "mainSearchButton")
        search_button.click()

        # Esperar a que el dropdown de filas esté presente y seleccionar 100 filas
        time.sleep(5)  # Espera fija de 5 segundos
        rows_dropdown = driver.find_element(By.NAME, "searchResultTable_length")
        rows_dropdown.send_keys("100")

        # Esperar a que se carguen los resultados y extraer los datos de la tabla
        extract_table_data(keyword)

        # Cargar más resultados si el botón está presente
        while True:
            try:
                load_more_button = driver.find_element(By.ID, "loadMoreResults")
                load_more_button.click()
                time.sleep(5)  # Esperar un poco para que se carguen más resultados
                extract_table_data(keyword)
            except:
                break

        # Navegar por la paginación si está presente
        while True:
            try:
                next_button = driver.find_element(By.ID, "searchResultTable_next")
                if "disabled" in next_button.get_attribute("class"):
                    break
                next_button.click()
                time.sleep(5)  # Esperar un poco para que se carguen más resultados
                extract_table_data(keyword)
            except:
                break

        # Guardar los resultados después de procesar cada keyword
        save_results()
        results = []  # Limpiar la lista de resultados para la siguiente keyword

except Exception as e:
    print(f"Error inesperado: {e}")
finally:
    # Cerrar el navegador y guardar los resultados
    driver.quit()
    save_results()
