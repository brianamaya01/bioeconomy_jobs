import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import signal
import sys

# Variables globales
data = []

# Función para manejar la interrupción Ctrl+C y guardar los datos
def signal_handler(sig, frame):
    print("Interrupción recibida, guardando datos...")
    save_data()
    sys.exit(0)

# Función para guardar los datos en un CSV
def save_data():
    df = pd.DataFrame(data, columns=['word', 'word_link'])
    df.to_csv('raw_data/thesaurus/vocabularios_spines.csv', index=False)
    print("Datos guardados en vocabularios_spines.csv")

# Conectar la señal de interrupción a la función de guardado
signal.signal(signal.SIGINT, signal_handler)

# Configuración del Chromedriver usando webdriver-manager
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--lang=es")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def scrape_page():
    words = driver.find_elements(By.CSS_SELECTOR, 'div#listaLetras li a')
    for word in words:
        word_text = word.text
        word_link = word.get_attribute('href')
        data.append({'word': word_text, 'word_link': word_link})
        save_data()  # Guardar datos después de agregar cada palabra

# Función principal
def main():
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base_url = 'http://vocabularios.caicyt.gov.ar/spines/index.php?letra='

    for letter in letters:
        url = base_url + letter
        driver.get(url)
        time.sleep(2)  # Esperar a que la página cargue

        while True:
            scrape_page()
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'a.next-off')
                next_button.click()
                time.sleep(2)  # Esperar a que la nueva página cargue
            except:
                break  # Si no se encuentra el botón de siguiente, salir del bucle

    save_data()
    driver.quit()

if __name__ == "__main__":
    main()
