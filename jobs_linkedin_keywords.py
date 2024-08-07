from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.by import By
#import pandas as pd
#import time
#import urllib.parse
#from datetime import datetime
#
## Configuración del Chromedriver
#chromedriver_path = r"C:/Users/brian.amaya/Documents/2.Proyectos/Bedex/chromedriver-win64/chromedriver-win64/chromedriver.exe"
#chrome_options = Options()
#chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--lang=es")
#chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--start-maximized")
#
## Función para obtener los datos de una oferta de trabajo
#def get_job_details(driver, keyword):
#    job_details = {}
#    job_details['keyword'] = keyword
#
#    def get_text_or_na(by, value):
#        try:
#            element = driver.find_element(by, value)
#            return element.text if element else 'NA'
#        except Exception as e:
#            print(f"Error al obtener texto para {value}: {e}")
#            return 'NA'
#
#    # Intentar cerrar el popup si aparece
#    try:
#        close_button = driver.find_element(By.CSS_SELECTOR, "button.cta-modal__dismiss-btn")
#        close_button.click()
#        time.sleep(2)  # Esperar un momento para que el popup se cierre
#    except Exception as e:
#        print(f"No se encontró el botón para cerrar el popup: {e}")
#
#    job_details['job_title'] = get_text_or_na(By.CLASS_NAME, "top-card-layout__title")
#    job_details['company'] = get_text_or_na(By.CLASS_NAME, "topcard__flavor")
#    job_details['company_link'] = get_text_or_na(By.CSS_SELECTOR, "span.topcard__flavor a")
#    job_details['location_job'] = get_text_or_na(By.CSS_SELECTOR, "span.topcard__flavor--bullet")
#    job_details['time_ago_job'] = get_text_or_na(By.CLASS_NAME, "posted-time-ago__text")
#    job_details['applicants'] = get_text_or_na(By.CSS_SELECTOR, "span.num-applicants__caption")
#    job_details['description_job'] = get_text_or_na(By.CLASS_NAME, "show-more-less-html__markup")
#    job_details['vacancy_url'] = 'NA'
#
#    # Obtener la URL de la vacante
#    try:
#        vacancy_url_code = driver.find_element(By.ID, "applyUrl")
#        job_details['vacancy_url'] = vacancy_url_code.get_attribute("innerHTML").split('"')[1]
#    except Exception as e:
#        print(f"Error al obtener la URL de la vacante: {e}")
#
#    # Inicializar campos de criterios
#    job_details['seniority_level'] = 'NA'
#    job_details['employment_type'] = 'NA'
#    job_details['job_function'] = 'NA'
#    job_details['industries'] = 'NA'
#
#    try:
#        criteria_elements = driver.find_elements(By.CSS_SELECTOR, "ul.description__job-criteria-list li.description__job-criteria-item")
#        criteria_texts = [element.find_element(By.CLASS_NAME, "description__job-criteria-text").text for element in criteria_elements]
#        
#        if len(criteria_texts) >= 4:
#            job_details['seniority_level'] = criteria_texts[0]
#            job_details['employment_type'] = criteria_texts[1]
#            job_details['job_function'] = criteria_texts[2]
#            job_details['industries'] = criteria_texts[3]
#        else:
#            print(f"Se encontraron menos de 4 criterios: {criteria_texts}")
#    except Exception as e:
#        print(f"Error al obtener elementos de criterio: {e}")
#
#    return job_details
#
## Función para extraer el currentJobId de la URL
#def get_current_jobid(url):
#    parsed_url = urllib.parse.urlparse(url)
#    query_params = urllib.parse.parse_qs(parsed_url.query)
#    current_jobid = query_params.get('currentJobId', [None])[0]
#    return current_jobid
#
## Función para guardar datos en CSV
#def save_to_csv(job_list, filename='job_details.csv'):
#    df = pd.DataFrame(job_list)
#    df['FetchDate'] = datetime.now().strftime('%Y-%m-%d')
#    try:
#        existing_df = pd.read_csv(filename)
#        df = pd.concat([existing_df, df], ignore_index=True)
#    except FileNotFoundError:
#        pass
#    # Eliminar duplicados basados en current_jobid
#    df.drop_duplicates(subset=['current_jobid'], inplace=True)
#    df.to_csv(filename, index=False)
#
## Inicializar el navegador
#service = Service(chromedriver_path)
#driver = webdriver.Chrome(service=service, options=chrome_options)
#
## Palabras clave dinámicas
#keywords = ["Alkaloids","Precision Farming", "Agriculture"]
#
#for keyword in keywords:
#    # URL inicial dinámica
#    base_url = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location=Colombia"
#    driver.get(base_url)
#    time.sleep(5)  # Esperar a que cargue la página
#
#    # Verificar si existe la clase "core-section-container my-3 no-results"
#    try:
#        no_results_element = driver.find_element(By.CSS_SELECTOR, "section.core-section-container.my-3.no-results")
#        print(f"No hay resultados para la búsqueda '{keyword}'. Pasando a la siguiente palabra clave.")
#        continue
#    except:
#        pass
#
#    # Obtener el total de trabajos disponibles
#    try:
#        total_jobs_element = driver.find_element(By.CLASS_NAME, "results-context-header__job-count")
#        total_jobs = int(total_jobs_element.text.replace(',', ''))
#    except Exception as e:
#        print(f"No se pudo obtener el total de trabajos para '{keyword}'. Pasando a la siguiente palabra clave.")
#        continue
#
#    # Realizar scroll y hacer clic en el botón 'Mostrar más' hasta encontrar el div final
#    while True:
#        try:
#            # Realizar un scroll hasta el final de la página
#            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#            time.sleep(3)
#
#            # Verificar si se ha encontrado el div final
#            try:
#                final_div = driver.find_element(By.CSS_SELECTOR, "div.inline-notification.text-color-signal-positive")
#                if "Has visto todos los empleos para esta búsqueda" in final_div.text:
#                    print("Se ha alcanzado el final de la lista de trabajos.")
#                    break
#            except:
#                pass
#
#            # Intentar encontrar y hacer clic en el botón 'Mostrar más'
#            try:
#                show_more_button = driver.find_element(By.CSS_SELECTOR, "button.infinite-scroller__show-more-button--visible")
#                show_more_button.click()
#                time.sleep(3)
#            except:
#                pass
#
#        except Exception as e:
#            print(f"Error durante el scroll y la búsqueda del botón: {e}")
#            break
#
#    # Volver al inicio de la página
#    driver.execute_script("window.scrollTo(0, 0);")
#    time.sleep(3)
#
#    # Lista para almacenar los detalles de cada oferta de trabajo
#    all_jobs = []
#
#    # Variable para rastrear los data-entity-urn procesados
#    processed_job_ids = set()
#
#    error_count = 0
#
#    try:
#        while len(processed_job_ids) < total_jobs:
#            job_elements = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")
#
#            if not job_elements:
#                break
#
#            for job_element in job_elements:
#                try:
#                    data_entity_urn = job_element.find_element(By.CSS_SELECTOR, "div.base-card").get_attribute("data-entity-urn")
#                    
#                    if data_entity_urn not in processed_job_ids:
#                        processed_job_ids.add(data_entity_urn)
#                        job_element.click()
#                        time.sleep(3)  # Esperar a que cargue el contenido de la oferta de trabajo
#
#                        # Obtener la URL actual y extraer el currentJobId
#                        current_url = driver.current_url
#                        current_jobid = get_current_jobid(current_url)
#
#                        # Obtener los detalles de la oferta de trabajo
#                        job_details = get_job_details(driver, keyword)
#                        job_details['current_jobid'] = current_jobid
#
#                        # Añadir los detalles a la lista
#                        all_jobs.append(job_details)
#
#                        # Guardar los detalles de los trabajos en un CSV
#                        save_to_csv(all_jobs)
#
#                        # Reiniciar contador de errores después de un éxito
#                        error_count = 0
#                except Exception as e:
#                    print(f"Se produjo un error al procesar un elemento: {e}")
#                    error_count += 1
#                    if error_count >= 3:
#                        print("Se han producido 3 errores consecutivos, pasando a la siguiente palabra clave.")
#                        break
#                    continue
#
#            if error_count >= 3:
#                break
#
#            # Si no se encuentran más elementos, salir del bucle
#            if len(job_elements) == 0:
#                break
#
#    except Exception as e:
#        print(f"Se produjo un error general: {e}")
#        save_to_csv(all_jobs)
#
#    finally:
#        # Guardar los detalles de los trabajos en un CSV al finalizar
#        save_to_csv(all_jobs)
#
## Cerrar el navegador
#driver.quit()
#print("Ejecución finalizada. Revisa el navegador para más detalles.")


#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.by import By
#import pandas as pd
#import random
#import time
#import urllib.parse
#from datetime import datetime
#
## Configuración del Chromedriver
#chromedriver_path = r"C:/Users/brian.amaya/Documents/2.Proyectos/Bedex/chromedriver-win64/chromedriver-win64/chromedriver.exe"
#chrome_options = Options()
#chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--lang=es")
#chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--start-maximized")
#
## Función para obtener los datos de una oferta de trabajo
#def get_job_details(driver, keyword):
#    job_details = {}
#    job_details['keyword'] = keyword
#
#    def get_text_or_na(by, value):
#        try:
#            element = driver.find_element(by, value)
#            return element.text if element else 'NA'
#        except Exception as e:
#            print(f"Error al obtener texto para {value}: {e}")
#            return 'NA'
#
#    # Intentar cerrar el popup si aparece
#    try:
#        close_button = driver.find_element(By.CSS_SELECTOR, "button.cta-modal__dismiss-btn")
#        close_button.click()
#        time.sleep(2)  # Esperar un momento para que el popup se cierre
#    except Exception as e:
#        print(f"No se encontró el botón para cerrar el popup: {e}")
#
#    job_details['job_title'] = get_text_or_na(By.CLASS_NAME, "top-card-layout__title")
#    job_details['company'] = get_text_or_na(By.CLASS_NAME, "topcard__flavor")
#    job_details['company_link'] = get_text_or_na(By.CSS_SELECTOR, "span.topcard__flavor a")
#    job_details['location_job'] = get_text_or_na(By.CSS_SELECTOR, "span.topcard__flavor--bullet")
#    job_details['time_ago_job'] = get_text_or_na(By.CLASS_NAME, "posted-time-ago__text")
#    job_details['applicants'] = get_text_or_na(By.CSS_SELECTOR, "span.num-applicants__caption")
#    job_details['description_job'] = get_text_or_na(By.CLASS_NAME, "show-more-less-html__markup")
#    job_details['vacancy_url'] = 'NA'
#
#    # Obtener la URL de la vacante
#    try:
#        vacancy_url_code = driver.find_element(By.ID, "applyUrl")
#        job_details['vacancy_url'] = vacancy_url_code.get_attribute("innerHTML").split('"')[1]
#    except Exception as e:
#        print(f"Error al obtener la URL de la vacante: {e}")
#
#    # Inicializar campos de criterios
#    job_details['seniority_level'] = 'NA'
#    job_details['employment_type'] = 'NA'
#    job_details['job_function'] = 'NA'
#    job_details['industries'] = 'NA'
#
#    try:
#        criteria_elements = driver.find_elements(By.CSS_SELECTOR, "ul.description__job-criteria-list li.description__job-criteria-item")
#        criteria_texts = [element.find_element(By.CLASS_NAME, "description__job-criteria-text").text for element in criteria_elements]
#        
#        if len(criteria_texts) >= 4:
#            job_details['seniority_level'] = criteria_texts[0]
#            job_details['employment_type'] = criteria_texts[1]
#            job_details['job_function'] = criteria_texts[2]
#            job_details['industries'] = criteria_texts[3]
#        else:
#            print(f"Se encontraron menos de 4 criterios: {criteria_texts}")
#    except Exception as e:
#        print(f"Error al obtener elementos de criterio: {e}")
#
#    return job_details
#
## Función para extraer el currentJobId de la URL
#def get_current_jobid(url):
#    parsed_url = urllib.parse.urlparse(url)
#    query_params = urllib.parse.parse_qs(parsed_url.query)
#    current_jobid = query_params.get('currentJobId', [None])[0]
#    return current_jobid
#
## Función para guardar datos en CSV
#def save_to_csv(job_list, filename='raw_data/jobs/job_details.csv'):
#    df = pd.DataFrame(job_list)
#    df['FetchDate'] = datetime.now().strftime('%Y-%m-%d')
#    try:
#        existing_df = pd.read_csv(filename)
#        df = pd.concat([existing_df, df], ignore_index=True)
#    except FileNotFoundError:
#        pass
#    # Eliminar duplicados basados en current_jobid
#    df.drop_duplicates(subset=['current_jobid'], inplace=True)
#    df.to_csv(filename, index=False)
#
## Cargar palabras clave desde el CSV
#keywords_df = pd.read_csv('raw_data/jobs/keywords_jobs.csv')
#keywords = keywords_df['keywords'].tolist()
#
## Inicializar el navegador
#service = Service(chromedriver_path)
#driver = webdriver.Chrome(service=service, options=chrome_options)
#
## Lista para almacenar el estado de cada palabra clave
#keyword_status_list = []
#
#for keyword in keywords:
#    # URL inicial dinámica
#    base_url = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location=Colombia"
#    driver.get(base_url)
#    time.sleep(random.randint(6, 10))  # Esperar a que cargue la página
#
#    # Verificar si existe la clase "core-section-container my-3 no-results"
#    try:
#        no_results_element = driver.find_element(By.CSS_SELECTOR, "section.core-section-container.my-3.no-results")
#        print(f"No hay resultados para la búsqueda '{keyword}'. Pasando a la siguiente palabra clave.")
#        keyword_status_list.append({'keyword': keyword, 'status_keyword': 0})
#        continue
#    except:
#        keyword_status_list.append({'keyword': keyword, 'status_keyword': 1})
#        pass
#
#    # Obtener el total de trabajos disponibles
#    try:
#        total_jobs_element = driver.find_element(By.CLASS_NAME, "results-context-header__job-count")
#        total_jobs = int(total_jobs_element.text.replace(',', ''))
#    except Exception as e:
#        print(f"No se pudo obtener el total de trabajos para '{keyword}'. Pasando a la siguiente palabra clave.")
#        continue
#
#    # Realizar scroll y hacer clic en el botón 'Mostrar más' hasta encontrar el div final
#    while True:
#        try:
#            # Realizar un scroll hasta el final de la página
#            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#            time.sleep(3)
#
#            # Verificar si se ha encontrado el div final
#            try:
#                final_div = driver.find_element(By.CSS_SELECTOR, "div.inline-notification.text-color-signal-positive")
#                if "Has visto todos los empleos para esta búsqueda" in final_div.text:
#                    print("Se ha alcanzado el final de la lista de trabajos.")
#                    break
#            except:
#                pass
#
#            # Intentar encontrar y hacer clic en el botón 'Mostrar más'
#            try:
#                show_more_button = driver.find_element(By.CSS_SELECTOR, "button.infinite-scroller__show-more-button--visible")
#                show_more_button.click()
#                time.sleep(3)
#            except:
#                pass
#
#        except Exception as e:
#            print(f"Error durante el scroll y la búsqueda del botón: {e}")
#            break
#
#    # Volver al inicio de la página
#    driver.execute_script("window.scrollTo(0, 0);")
#    time.sleep(3)
#
#    # Lista para almacenar los detalles de cada oferta de trabajo
#    all_jobs = []
#
#    # Variable para rastrear los data-entity-urn procesados
#    processed_job_ids = set()
#
#    error_count = 0
#
#    try:
#        while len(processed_job_ids) < total_jobs:
#            job_elements = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")
#
#            if not job_elements:
#                break
#
#            for job_element in job_elements:
#                try:
#                    data_entity_urn = job_element.find_element(By.CSS_SELECTOR, "div.base-card").get_attribute("data-entity-urn")
#                    
#                    if data_entity_urn not in processed_job_ids:
#                        processed_job_ids.add(data_entity_urn)
#                        job_element.click()
#                        time.sleep(3)  # Esperar a que cargue el contenido de la oferta de trabajo
#
#                        # Obtener la URL actual y extraer el currentJobId
#                        current_url = driver.current_url
#                        current_jobid = get_current_jobid(current_url)
#
#                        # Obtener los detalles de la oferta de trabajo
#                        job_details = get_job_details(driver, keyword)
#                        job_details['current_jobid'] = current_jobid
#
#                        # Añadir los detalles a la lista
#                        all_jobs.append(job_details)
#
#                        # Guardar los detalles de los trabajos en un CSV
#                        save_to_csv(all_jobs)
#
#                        # Reiniciar contador de errores después de un éxito
#                        error_count = 0
#                except Exception as e:
#                    print(f"Se produjo un error al procesar un elemento: {e}")
#                    error_count += 1
#                    if error_count >= 3:
#                        print("Se han producido 3 errores consecutivos, pasando a la siguiente palabra clave.")
#                        break
#                    continue
#
#            if error_count >= 3:
#                break
#
#            # Si no se encuentran más elementos, salir del bucle
#            if len(job_elements) == 0:
#                break
#
#    except Exception as e:
#        print(f"Se produjo un error general: {e}")
#        save_to_csv(all_jobs)
#
#    finally:
#        # Guardar los detalles de los trabajos en un CSV al finalizar
#        save_to_csv(all_jobs)
#
## Guardar el estado de cada palabra clave en un CSV
#status_df = pd.DataFrame(keyword_status_list)
#status_df.to_csv('raw_data/jobs/keyword_status.csv', index=False)
#
## Cerrar el navegador
#driver.quit()
#print("Ejecución finalizada. Revisa el navegador para más detalles.")


# https://www.linkedin.com/jobs/search?keywords=An%C3%A1lisis%2BDe%2BAdn&location=Colombia&geoId=100876405&trk=public_jobs_jobs-search-bar_search-submit&currentJobId=3923635460&position=2&pageNum=0

#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.by import By
#import pandas as pd
#import random
#import time
#import urllib.parse
#import os
#from datetime import datetime
#
## Configuración del Chromedriver
#chromedriver_path = r"C:/Users/brian.amaya/Documents/2.Proyectos/Bedex/chromedriver-win64/chromedriver-win64/chromedriver.exe"
#chrome_options = Options()
#chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--lang=es")
#chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--start-maximized")
#
## Función para obtener los datos de una oferta de trabajo
#def get_job_details(driver, keyword):
#    job_details = {}
#    job_details['keyword'] = keyword
#
#    def get_text_or_na(by, value):
#        try:
#            element = driver.find_element(by, value)
#            return element.text if element else 'NA'
#        except Exception as e:
#            print(f"Error al obtener texto para {value}: {e}")
#            return 'NA'
#
#    ## Intentar cerrar el popup si aparece
#    #try:
#    #    close_button = driver.find_element(By.CSS_SELECTOR, "button.cta-modal__dismiss-btn")
#    #    close_button.click()
#    #    time.sleep(2)  # Esperar un momento para que el popup se cierre
#    #except Exception as e:
#    #    print(f"No se encontró el botón para cerrar el popup: {e}")
#
#    job_details['job_title'] = get_text_or_na(By.CLASS_NAME, "top-card-layout__title")
#    job_details['company'] = get_text_or_na(By.CLASS_NAME, "topcard__flavor")
#    job_details['company_link'] = get_text_or_na(By.CSS_SELECTOR, "span.topcard__flavor a")
#    job_details['location_job'] = get_text_or_na(By.CSS_SELECTOR, "span.topcard__flavor--bullet")
#    job_details['time_ago_job'] = get_text_or_na(By.CLASS_NAME, "posted-time-ago__text")
#    job_details['applicants'] = get_text_or_na(By.CSS_SELECTOR, "span.num-applicants__caption")
#    
#    # Obtener descripción completa incluyendo elementos dentro de ul y li
#    try:
#        description_element = driver.find_element(By.CLASS_NAME, "show-more-less-html__markup")
#        description_job = description_element.get_attribute('innerHTML')
#        job_details['description_job'] = description_job
#    except Exception as e:
#        print(f"Error al obtener la descripción del trabajo: {e}")
#        job_details['description_job'] = 'NA'
#    
#    job_details['vacancy_url'] = 'NA'
#
#    # Obtener la URL de la vacante
#    try:
#        vacancy_url_code = driver.find_element(By.ID, "applyUrl")
#        job_details['vacancy_url'] = vacancy_url_code.get_attribute("innerHTML").split('"')[1]
#    except Exception as e:
#        print(f"Error al obtener la URL de la vacante: {e}")
#
#    # Inicializar campos de criterios
#    job_details['seniority_level'] = 'NA'
#    job_details['employment_type'] = 'NA'
#    job_details['job_function'] = 'NA'
#    job_details['industries'] = 'NA'
#
#    try:
#        criteria_elements = driver.find_elements(By.CSS_SELECTOR, "ul.description__job-criteria-list li.description__job-criteria-item")
#        criteria_texts = [element.find_element(By.CLASS_NAME, "description__job-criteria-text").text for element in criteria_elements]
#        
#        if len(criteria_texts) >= 4:
#            job_details['seniority_level'] = criteria_texts[0]
#            job_details['employment_type'] = criteria_texts[1]
#            job_details['job_function'] = criteria_texts[2]
#            job_details['industries'] = criteria_texts[3]
#        else:
#            print(f"Se encontraron menos de 4 criterios: {criteria_texts}")
#    except Exception as e:
#        print(f"Error al obtener elementos de criterio: {e}")
#
#    return job_details
#
## Función para extraer el currentJobId de la URL
#def get_current_jobid(url):
#    parsed_url = urllib.parse.urlparse(url)
#    query_params = urllib.parse.parse_qs(parsed_url.query)
#    current_jobid = query_params.get('currentJobId', [None])[0]
#    return current_jobid
#
## Función para guardar datos en CSV
#def save_to_csv(job_list, filename='raw_data/jobs/job_details.csv'):
#    df = pd.DataFrame(job_list)
#    df['FetchDate'] = datetime.now().strftime('%Y-%m-%d')
#    try:
#        existing_df = pd.read_csv(filename)
#        df = pd.concat([existing_df, df], ignore_index=True)
#    except FileNotFoundError:
#        pass
#    # Eliminar duplicados basados en current_jobid
#    df.drop_duplicates(subset=['current_jobid'], inplace=True)
#    df.to_csv(filename, index=False)
#
## Leer el estado de keywords
#def read_keyword_status(keyword_status_file):
#    if not os.path.exists(keyword_status_file):
#        return {}
#    return pd.read_csv(keyword_status_file).set_index('keyword')['count'].to_dict()
#
## Guardar el estado de keywords
#def save_keyword_status(keyword_status_file, keyword_status):
#    status_df = pd.DataFrame(list(keyword_status.items()), columns=['keyword', 'count'])
#    status_df.to_csv(keyword_status_file, index=False)
#
#keyword_status_file = 'raw_data/jobs/keyword_status.csv'
#keyword_status = read_keyword_status(keyword_status_file)
#
## Cargar palabras clave desde el CSV
#keywords_df = pd.read_csv('raw_data/jobs/keywords_jobs.csv')
#keywords = keywords_df['keywords'].tolist()
#
## Excluir las keywords ya procesadas
#keywords_to_process = [kw for kw in keywords if kw not in keyword_status]
#
## Inicializar el navegador
#service = Service(chromedriver_path)
#driver = webdriver.Chrome(service=service, options=chrome_options)
#
## Lista para almacenar el estado de cada palabra clave
#keyword_status_list = []
#
#for keyword in keywords_to_process:
#    # URL inicial dinámica
#    base_url = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location=Colombia"
#    driver.get(base_url)
#    time.sleep(random.randint(6, 10))  # Esperar a que cargue la página
#
#    # Verificar si existe la clase "core-section-container my-3 no-results"
#    try:
#        no_results_element = driver.find_element(By.CSS_SELECTOR, "section.core-section-container.my-3.no-results")
#        print(f"No hay resultados para la búsqueda '{keyword}'. Pasando a la siguiente palabra clave.")
#        keyword_status[keyword] = 0
#        save_keyword_status(keyword_status_file, keyword_status)
#        continue
#    except:
#        keyword_status[keyword] = 1
#        pass
#
#    # Obtener el total de trabajos disponibles
#    try:
#        total_jobs_element = driver.find_element(By.CLASS_NAME, "results-context-header__job-count")
#        total_jobs = int(total_jobs_element.text.replace(',', ''))
#        keyword_status[keyword] = total_jobs
#    except Exception as e:
#        print(f"No se pudo obtener el total de trabajos para '{keyword}'. Pasando a la siguiente palabra clave.")
#        continue
#
#    # Guardar el estado actualizado inmediatamente
#    save_keyword_status(keyword_status_file, keyword_status)
#
#    # Realizar scroll y hacer clic en el botón 'Mostrar más' hasta encontrar el div final
#    while True:
#        try:
#            # Realizar un scroll hasta el final de la página
#            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#            time.sleep(3)
#
#            # Verificar si se ha encontrado el div final
#            try:
#                final_div = driver.find_element(By.CSS_SELECTOR, "div.inline-notification.text-color-signal-positive")
#                if "Has visto todos los empleos para esta búsqueda" in final_div.text:
#                    print("Se ha alcanzado el final de la lista de trabajos.")
#                    break
#            except:
#                pass
#
#            # Intentar encontrar y hacer clic en el botón 'Mostrar más'
#            try:
#                show_more_button = driver.find_element(By.CSS_SELECTOR, "button.infinite-scroller__show-more-button--visible")
#                show_more_button.click()
#                time.sleep(3)
#            except:
#                pass
#
#        except Exception as e:
#            print(f"Error durante el scroll y la búsqueda del botón: {e}")
#            break
#
#    # Volver al inicio de la página
#    driver.execute_script("window.scrollTo(0, 0);")
#    time.sleep(3)
#
#    # Lista para almacenar los detalles de cada oferta de trabajo
#    all_jobs = []
#
#    # Variable para rastrear los data-entity-urn procesados
#    processed_job_ids = set()
#
#    error_count = 0
#
#    try:
#        while len(processed_job_ids) < total_jobs:
#            job_elements = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")
#
#            if not job_elements:
#                break
#
#            for job_element in job_elements:
#                try:
#                    data_entity_urn = job_element.find_element(By.CSS_SELECTOR, "div.base-card").get_attribute("data-entity-urn")
#                    
#                    if data_entity_urn not in processed_job_ids:
#                        processed_job_ids.add(data_entity_urn)
#                        job_element.click()
#                        time.sleep(3)  # Esperar a que cargue el contenido de la oferta de trabajo
#
#                        # Obtener la URL actual y extraer el currentJobId
#                        current_url = driver.current_url
#                        current_jobid = get_current_jobid(current_url)
#
#                        # Obtener los detalles de la oferta de trabajo
#                        job_details = get_job_details(driver, keyword)
#                        job_details['current_jobid'] = current_jobid
#
#                        # Añadir los detalles a la lista
#                        all_jobs.append(job_details)
#
#                        # Guardar los detalles de los trabajos en un CSV
#                        save_to_csv(all_jobs)
#
#                        # Reiniciar contador de errores después de un éxito
#                        error_count = 0
#                except Exception as e:
#                    print(f"Se produjo un error al procesar un elemento: {e}")
#                    error_count += 1
#                    if error_count >= 3:
#                        print("Se han producido 3 errores consecutivos, pasando a la siguiente palabra clave.")
#                        break
#                    continue
#
#            if error_count >= 3:
#                break
#
#            # Si no se encuentran más elementos, salir del bucle
#            if len(job_elements) == 0:
#                break
#
#    except Exception as e:
#        print(f"Se produjo un error general: {e}")
#        save_to_csv(all_jobs)
#
#    finally:
#        # Guardar los detalles de los trabajos en un CSV al finalizar
#        save_to_csv(all_jobs)
#
## Guardar el estado de cada palabra clave en un CSV
#save_keyword_status(keyword_status_file, keyword_status)
#
## Cerrar el navegador
#driver.quit()
#print("Ejecución finalizada. Revisa el navegador para más detalles.")
#

##
#import undetected_chromedriver as uc
#from selenium.webdriver.common.by import By
#import pandas as pd
#import random
#import time
#import urllib.parse
#import os
#from datetime import datetime
#from webdriver_manager.chrome import ChromeDriverManager
#
## Configuración del Chromedriver
#
#
##chromedriver_path = r"C:/Users/brian.amaya/Documents/2.Proyectos/Bedex/chromedriver-win64/chromedriver-win64/chromedriver.exe"
#chrome_options = uc.ChromeOptions()
#chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--lang=es")
#chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--start-maximized")
#
## Función para obtener los datos de una oferta de trabajo
#def get_job_details(driver, keyword):
#    job_details = {}
#    job_details['keyword'] = keyword
#
#    def get_text_or_na(by, value):
#        try:
#            element = driver.find_element(by, value)
#            return element.text if element else 'NA'
#        except Exception as e:
#            print(f"Error al obtener texto para {value}: {e}")
#            return 'NA'
#
#    job_details['job_title'] = get_text_or_na(By.CLASS_NAME, "top-card-layout__title")
#    job_details['company'] = get_text_or_na(By.CLASS_NAME, "topcard__flavor")
#    job_details['company_link'] = get_text_or_na(By.CSS_SELECTOR, "span.topcard__flavor a")
#    job_details['location_job'] = get_text_or_na(By.CSS_SELECTOR, "span.topcard__flavor--bullet")
#    job_details['time_ago_job'] = get_text_or_na(By.CLASS_NAME, "posted-time-ago__text")
#    job_details['applicants'] = get_text_or_na(By.CSS_SELECTOR, "span.num-applicants__caption")
#    
#    # Obtener descripción completa incluyendo elementos dentro de ul y li
#    try:
#        description_element = driver.find_element(By.CLASS_NAME, "show-more-less-html__markup")
#        description_job = description_element.get_attribute('innerHTML')
#        job_details['description_job'] = description_job
#    except Exception as e:
#        print(f"Error al obtener la descripción del trabajo: {e}")
#        job_details['description_job'] = 'NA'
#    
#    job_details['vacancy_url'] = 'NA'
#
#    # Obtener la URL de la vacante
#    try:
#        vacancy_url_code = driver.find_element(By.ID, "applyUrl")
#        job_details['vacancy_url'] = vacancy_url_code.get_attribute("innerHTML").split('"')[1]
#    except Exception as e:
#        print(f"Error al obtener la URL de la vacante: {e}")
#
#    # Inicializar campos de criterios
#    job_details['seniority_level'] = 'NA'
#    job_details['employment_type'] = 'NA'
#    job_details['job_function'] = 'NA'
#    job_details['industries'] = 'NA'
#
#    try:
#        criteria_elements = driver.find_elements(By.CSS_SELECTOR, "ul.description__job-criteria-list li.description__job-criteria-item")
#        criteria_texts = [element.find_element(By.CLASS_NAME, "description__job-criteria-text").text for element in criteria_elements]
#        
#        if len(criteria_texts) >= 4:
#            job_details['seniority_level'] = criteria_texts[0]
#            job_details['employment_type'] = criteria_texts[1]
#            job_details['job_function'] = criteria_texts[2]
#            job_details['industries'] = criteria_texts[3]
#        else:
#            print(f"Se encontraron menos de 4 criterios: {criteria_texts}")
#    except Exception as e:
#        print(f"Error al obtener elementos de criterio: {e}")
#
#    return job_details
#
## Función para extraer el currentJobId de la URL
#def get_current_jobid(url):
#    parsed_url = urllib.parse.urlparse(url)
#    query_params = urllib.parse.parse_qs(parsed_url.query)
#    current_jobid = query_params.get('currentJobId', [None])[0]
#    return current_jobid
#
## Función para guardar datos en CSV
#def save_to_csv(job_list, filename='raw_data/jobs/job_details.csv'):
#    df = pd.DataFrame(job_list)
#    df['FetchDate'] = datetime.now().strftime('%Y-%m-%d')
#    try:
#        existing_df = pd.read_csv(filename)
#        df = pd.concat([existing_df, df], ignore_index=True)
#    except FileNotFoundError:
#        pass
#    # Eliminar duplicados basados en current_jobid
#    df.drop_duplicates(subset=['current_jobid'], inplace=True)
#    df.to_csv(filename, index=False)
#
## Leer el estado de keywords
#def read_keyword_status(keyword_status_file):
#    if not os.path.exists(keyword_status_file):
#        return {}
#    return pd.read_csv(keyword_status_file).set_index('keyword')['count'].to_dict()
#
## Guardar el estado de keywords
#def save_keyword_status(keyword_status_file, keyword_status):
#    status_df = pd.DataFrame(list(keyword_status.items()), columns=['keyword', 'count'])
#    status_df.to_csv(keyword_status_file, index=False)
#
#keyword_status_file = 'raw_data/jobs/keyword_status.csv'
#keyword_status = read_keyword_status(keyword_status_file)
#
## Cargar palabras clave desde el CSV
#keywords_df = pd.read_csv('raw_data/jobs/keywords_jobs.csv')
#keywords = keywords_df['keywords'].tolist()
#
## Excluir las keywords ya procesadas
#keywords_to_process = [kw for kw in keywords if kw not in keyword_status]
#
## Inicializar el navegador
#driver = uc.Chrome(options=chrome_options, driver_executable_path=ChromeDriverManager().install())
#
## Lista para almacenar el estado de cada palabra clave
#keyword_status_list = []
#
#for keyword in keywords_to_process:
#    # URL inicial dinámica
#    base_url = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location=Colombia"
#    driver.get(base_url)
#    time.sleep(random.randint(6, 10))  # Esperar a que cargue la página
#
#    # Verificar si existe la clase "core-section-container my-3 no-results"
#    try:
#        no_results_element = driver.find_element(By.CSS_SELECTOR, "section.core-section-container.my-3.no-results")
#        print(f"No hay resultados para la búsqueda '{keyword}'. Pasando a la siguiente palabra clave.")
#        keyword_status[keyword] = 0
#        save_keyword_status(keyword_status_file, keyword_status)
#        continue
#    except:
#        keyword_status[keyword] = 1
#        pass
#
#    # Obtener el total de trabajos disponibles
#    try:
#        total_jobs_element = driver.find_element(By.CLASS_NAME, "results-context-header__job-count")
#        total_jobs = int(total_jobs_element.text.replace(',', ''))
#        keyword_status[keyword] = total_jobs
#    except Exception as e:
#        print(f"No se pudo obtener el total de trabajos para '{keyword}'. Pasando a la siguiente palabra clave.")
#        continue
#
#    # Guardar el estado actualizado inmediatamente
#    save_keyword_status(keyword_status_file, keyword_status)
#
#    # Realizar scroll y hacer clic en el botón 'Mostrar más' hasta encontrar el div final
#    while True:
#        try:
#            # Realizar un scroll hasta el final de la página
#            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#            time.sleep(3)
#
#            # Verificar si se ha encontrado el div final
#            try:
#                final_div = driver.find_element(By.CSS_SELECTOR, "div.inline-notification.text-color-signal-positive")
#                if "Has visto todos los empleos para esta búsqueda" in final_div.text:
#                    print("Se ha alcanzado el final de la lista de trabajos.")
#                    break
#            except:
#                pass
#
#            # Intentar encontrar y hacer clic en el botón 'Mostrar más'
#            try:
#                show_more_button = driver.find_element(By.CSS_SELECTOR, "button.infinite-scroller__show-more-button--visible")
#                show_more_button.click()
#                time.sleep(3)
#            except:
#                pass
#
#        except Exception as e:
#            print(f"Error durante el scroll y la búsqueda del botón: {e}")
#            break
#
#    # Volver al inicio de la página
#    driver.execute_script("window.scrollTo(0, 0);")
#    time.sleep(3)
#
#    # Lista para almacenar los detalles de cada oferta de trabajo
#    all_jobs = []
#
#    # Variable para rastrear los data-entity-urn procesados
#    processed_job_ids = set()
#
#    error_count = 0
#
#    try:
#        while len(processed_job_ids) < total_jobs:
#            job_elements = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")
#
#            if not job_elements:
#                break
#
#            for job_element in job_elements:
#                try:
#                    data_entity_urn = job_element.find_element(By.CSS_SELECTOR, "div.base-card").get_attribute("data-entity-urn")
#                    
#                    if data_entity_urn not in processed_job_ids:
#                        processed_job_ids.add(data_entity_urn)
#                        job_element.click()
#                        time.sleep(3)  # Esperar a que cargue el contenido de la oferta de trabajo
#
#                        # Obtener la URL actual y extraer el currentJobId
#                        current_url = driver.current_url
#                        current_jobid = get_current_jobid(current_url)
#
#                        # Obtener los detalles de la oferta de trabajo
#                        job_details = get_job_details(driver, keyword)
#                        job_details['current_jobid'] = current_jobid
#
#                        # Añadir los detalles a la lista
#                        all_jobs.append(job_details)
#
#                        # Guardar los detalles de los trabajos en un CSV
#                        save_to_csv(all_jobs)
#
#                        # Reiniciar contador de errores después de un éxito
#                        error_count = 0
#                except Exception as e:
#                    print(f"Se produjo un error al procesar un elemento: {e}")
#                    error_count += 1
#                    if error_count >= 3:
#                        print("Se han producido 3 errores consecutivos, pasando a la siguiente palabra clave.")
#                        break
#                    continue
#
#            if error_count >= 3:
#                break
#
#            # Si no se encuentran más elementos, salir del bucle
#            if len(job_elements) == 0:
#                break
#
#    except Exception as e:
#        print(f"Se produjo un error general: {e}")
#        save_to_csv(all_jobs)
#
#    finally:
#        # Guardar los detalles de los trabajos en un CSV al finalizar
#        save_to_csv(all_jobs)
#
## Guardar el estado de cada palabra clave en un CSV
#save_keyword_status(keyword_status_file, keyword_status)
#
## Cerrar el navegador
#driver.quit()
#print("Ejecución finalizada. Revisa el navegador para más detalles.")
#
#
#
#from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.common.by import By
#import pandas as pd
#import random
#import time
#import urllib.parse
#import os
#from datetime import datetime
#import undetected_chromedriver as uc
#from webdriver_manager.chrome import ChromeDriverManager
#
## Configuración del Chromedriver
#chrome_options = uc.ChromeOptions()
#chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--lang=es")
#chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--start-maximized")
#
## Función para obtener los datos de una oferta de trabajo
#def get_job_details(driver, keyword):
#    job_details = {}
#    job_details['keyword'] = keyword
#
#    def get_text_or_na(by, value):
#        try:
#            element = driver.find_element(by, value)
#            return element.text if element else 'NA'
#        except Exception as e:
#            print(f"Error al obtener texto para {value}: {e}")
#            return 'NA'
#
#    job_details['job_title'] = get_text_or_na(By.CLASS_NAME, "top-card-layout__title")
#    job_details['company'] = get_text_or_na(By.CLASS_NAME, "topcard__flavor")
#    job_details['company_link'] = get_text_or_na(By.CSS_SELECTOR, "span.topcard__flavor a")
#    job_details['location_job'] = get_text_or_na(By.CSS_SELECTOR, "span.topcard__flavor--bullet")
#    job_details['time_ago_job'] = get_text_or_na(By.CLASS_NAME, "posted-time-ago__text")
#    job_details['applicants'] = get_text_or_na(By.CSS_SELECTOR, "span.num-applicants__caption")
#    
#    try:
#        description_element = driver.find_element(By.CLASS_NAME, "show-more-less-html__markup")
#        description_job = description_element.get_attribute('innerHTML')
#        job_details['description_job'] = description_job
#    except Exception as e:
#        print(f"Error al obtener la descripción del trabajo: {e}")
#        job_details['description_job'] = 'NA'
#    
#    job_details['vacancy_url'] = 'NA'
#
#    try:
#        vacancy_url_code = driver.find_element(By.ID, "applyUrl")
#        job_details['vacancy_url'] = vacancy_url_code.get_attribute("innerHTML").split('"')[1]
#    except Exception as e:
#        print(f"Error al obtener la URL de la vacante: {e}")
#
#    job_details['seniority_level'] = 'NA'
#    job_details['employment_type'] = 'NA'
#    job_details['job_function'] = 'NA'
#    job_details['industries'] = 'NA'
#
#    try:
#        criteria_elements = driver.find_elements(By.CSS_SELECTOR, "ul.description__job-criteria-list li.description__job-criteria-item")
#        criteria_texts = [element.find_element(By.CLASS_NAME, "description__job-criteria-text").text for element in criteria_elements]
#        
#        if len(criteria_texts) >= 4:
#            job_details['seniority_level'] = criteria_texts[0]
#            job_details['employment_type'] = criteria_texts[1]
#            job_details['job_function'] = criteria_texts[2]
#            job_details['industries'] = criteria_texts[3]
#        else:
#            print(f"Se encontraron menos de 4 criterios: {criteria_texts}")
#    except Exception as e:
#        print(f"Error al obtener elementos de criterio: {e}")
#
#    return job_details
#
#def get_current_jobid(url):
#    parsed_url = urllib.parse.urlparse(url)
#    query_params = urllib.parse.parse_qs(parsed_url.query)
#    current_jobid = query_params.get('currentJobId', [None])[0]
#    return current_jobid
#
#def save_to_csv(job_list, filename='raw_data/jobs/job_details.csv'):
#    df = pd.DataFrame(job_list)
#    df['FetchDate'] = datetime.now().strftime('%Y-%m-%d')
#    try:
#        existing_df = pd.read_csv(filename)
#        df = pd.concat([existing_df, df], ignore_index=True)
#    except FileNotFoundError:
#        pass
#    df.drop_duplicates(subset=['current_jobid'], inplace=True)
#    df.to_csv(filename, index=False)
#
#def read_keyword_status(keyword_status_file):
#    if not os.path.exists(keyword_status_file):
#        return {}
#    return pd.read_csv(keyword_status_file).set_index('keyword')['count'].to_dict()
#
#def save_keyword_status(keyword_status_file, keyword_status):
#    status_df = pd.DataFrame(list(keyword_status.items()), columns=['keyword', 'count'])
#    status_df.to_csv(keyword_status_file, index=False)
#
#keyword_status_file = 'raw_data/jobs/keyword_status.csv'
#keyword_status = read_keyword_status(keyword_status_file)
#
#keywords_df = pd.read_csv('raw_data/jobs/keywords_jobs.csv')
#keywords = keywords_df['keywords'].tolist()
#
#keywords_to_process = [kw for kw in keywords if kw not in keyword_status]
#
#service = Service(ChromeDriverManager().install())
#driver = uc.Chrome(service=service, options=chrome_options)
#
#try:
#    for keyword in keywords_to_process:
#        base_url = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location=Colombia"
#        driver.get(base_url)
#        time.sleep(random.randint(6, 10))
#
#        try:
#            no_results_element = driver.find_element(By.CSS_SELECTOR, "section.core-section-container.my-3.no-results")
#            print(f"No hay resultados para la búsqueda '{keyword}'. Pasando a la siguiente palabra clave.")
#            keyword_status[keyword] = 0
#            save_keyword_status(keyword_status_file, keyword_status)
#            continue
#        except:
#            keyword_status[keyword] = 1
#            pass
#
#        try:
#            total_jobs_element = driver.find_element(By.CLASS_NAME, "results-context-header__job-count")
#            total_jobs = int(total_jobs_element.text.replace(',', ''))
#            keyword_status[keyword] = total_jobs
#        except Exception as e:
#            print(f"No se pudo obtener el total de trabajos para '{keyword}'. Pasando a la siguiente palabra clave.")
#            continue
#
#        save_keyword_status(keyword_status_file, keyword_status)
#
#        while True:
#            try:
#                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#                time.sleep(3)
#
#                try:
#                    final_div = driver.find_element(By.CSS_SELECTOR, "div.inline-notification.text-color-signal-positive")
#                    if "Has visto todos los empleos para esta búsqueda" in final_div.text:
#                        print("Se ha alcanzado el final de la lista de trabajos.")
#                        break
#                except:
#                    pass
#
#                try:
#                    show_more_button = driver.find_element(By.CSS_SELECTOR, "button.infinite-scroller__show-more-button--visible")
#                    show_more_button.click()
#                    time.sleep(3)
#                except:
#                    pass
#
#            except Exception as e:
#                print(f"Error durante el scroll y la búsqueda del botón: {e}")
#                break
#
#        driver.execute_script("window.scrollTo(0, 0);")
#        time.sleep(3)
#
#        all_jobs = []
#
#        processed_job_ids = set()
#
#        error_count = 0
#
#        try:
#            while len(processed_job_ids) < total_jobs:
#                job_elements = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")
#
#                if not job_elements:
#                    break
#
#                for job_element in job_elements:
#                    try:
#                        data_entity_urn = job_element.find_element(By.CSS_SELECTOR, "div.base-card").get_attribute("data-entity-urn")
#                        
#                        if data_entity_urn not in processed_job_ids:
#                            processed_job_ids.add(data_entity_urn)
#                            job_element.click()
#                            time.sleep(3)
#
#                            current_url = driver.current_url
#                            current_jobid = get_current_jobid(current_url)
#
#                            job_details = get_job_details(driver, keyword)
#                            job_details['current_jobid'] = current_jobid
#
#                            all_jobs.append(job_details)
#
#                            save_to_csv(all_jobs)
#
#                            error_count = 0
#                    except Exception as e:
#                        print(f"Se produjo un error al procesar un elemento: {e}")
#                        error_count += 1
#                        if error_count >= 3:
#                            print("Se han producido 3 errores consecutivos, pasando a la siguiente palabra clave.")
#                            break
#                        continue
#
#                if error_count >= 3:
#                    break
#
#                if len(job_elements) == 0:
#                    break
#
#        except Exception as e:
#            print(f"Se produjo un error general: {e}")
#            save_to_csv(all_jobs)
#
#        finally:
#            save_to_csv(all_jobs)
#
#finally:
#    driver.quit()
#    print("Ejecución finalizada. Revisa el navegador para más detalles.")
#

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import random
import time
import urllib.parse
import os
from datetime import datetime

# Configuración del Chromedriver usando webdriver-manager
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--lang=es")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--start-maximized")

# Inicializar el navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Función para obtener los datos de una oferta de trabajo
def get_job_details(driver, keyword):
    job_details = {}
    job_details['keyword'] = keyword

    def get_text_or_na(by, value):
        try:
            element = driver.find_element(by, value)
            return element.text if element else 'NA'
        except Exception as e:
            print(f"Error al obtener texto para {value}: {e}")
            return 'NA'

    job_details['job_title'] = get_text_or_na(By.CLASS_NAME, "top-card-layout__title")
    job_details['company'] = get_text_or_na(By.CLASS_NAME, "topcard__flavor")
    job_details['company_link'] = get_text_or_na(By.CSS_SELECTOR, "span.topcard__flavor a")
    job_details['location_job'] = get_text_or_na(By.CSS_SELECTOR, "span.topcard__flavor--bullet")
    job_details['time_ago_job'] = get_text_or_na(By.CLASS_NAME, "posted-time-ago__text")
    job_details['applicants'] = get_text_or_na(By.CSS_SELECTOR, "span.num-applicants__caption")
    
    # Obtener descripción completa incluyendo elementos dentro de ul y li
    try:
        description_element = driver.find_element(By.CLASS_NAME, "show-more-less-html__markup")
        description_job = description_element.get_attribute('innerHTML')
        job_details['description_job'] = description_job
    except Exception as e:
        print(f"Error al obtener la descripción del trabajo: {e}")
        job_details['description_job'] = 'NA'
    
    job_details['vacancy_url'] = 'NA'

    # Obtener la URL de la vacante
    try:
        vacancy_url_code = driver.find_element(By.ID, "applyUrl")
        job_details['vacancy_url'] = vacancy_url_code.get_attribute("innerHTML").split('"')[1]
    except Exception as e:
        print(f"Error al obtener la URL de la vacante: {e}")

    # Inicializar campos de criterios
    job_details['seniority_level'] = 'NA'
    job_details['employment_type'] = 'NA'
    job_details['job_function'] = 'NA'
    job_details['industries'] = 'NA'

    try:
        criteria_elements = driver.find_elements(By.CSS_SELECTOR, "ul.description__job-criteria-list li.description__job-criteria-item")
        criteria_texts = [element.find_element(By.CLASS_NAME, "description__job-criteria-text").text for element in criteria_elements]
        
        if len(criteria_texts) >= 4:
            job_details['seniority_level'] = criteria_texts[0]
            job_details['employment_type'] = criteria_texts[1]
            job_details['job_function'] = criteria_texts[2]
            job_details['industries'] = criteria_texts[3]
        else:
            print(f"Se encontraron menos de 4 criterios: {criteria_texts}")
    except Exception as e:
        print(f"Error al obtener elementos de criterio: {e}")

    return job_details

# Función para extraer el currentJobId de la URL
def get_current_jobid(url):
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    current_jobid = query_params.get('currentJobId', [None])[0]
    return current_jobid

# Función para guardar datos en CSV
def save_to_csv(job_list, filename='raw_data/jobs/job_details.csv'):
    df = pd.DataFrame(job_list)
    df['FetchDate'] = datetime.now().strftime('%Y-%m-%d')
    try:
        existing_df = pd.read_csv(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    # Eliminar duplicados basados en current_jobid
    df.drop_duplicates(subset=['current_jobid'], inplace=True)
    df.to_csv(filename, index=False)

# Leer el estado de keywords
def read_keyword_status(keyword_status_file):
    if not os.path.exists(keyword_status_file):
        return {}
    return pd.read_csv(keyword_status_file).set_index('keyword')['count'].to_dict()

# Guardar el estado de keywords
def save_keyword_status(keyword_status_file, keyword_status):
    status_df = pd.DataFrame(list(keyword_status.items()), columns=['keyword', 'count'])
    status_df.to_csv(keyword_status_file, index=False)

keyword_status_file = 'raw_data/jobs/keyword_status.csv'
keyword_status = read_keyword_status(keyword_status_file)

# Cargar palabras clave desde el CSV
keywords_df = pd.read_csv('raw_data/jobs/keywords_jobs.csv')
keywords = keywords_df['keywords'].tolist()

# Excluir las keywords ya procesadas
keywords_to_process = [kw for kw in keywords if kw not in keyword_status]

# Lista para almacenar el estado de cada palabra clave
keyword_status_list = []

for keyword in keywords_to_process:
    # URL inicial dinámica
    base_url = f"https://www.linkedin.com/jobs/search?keywords={keyword}&location=Colombia"
    driver.get(base_url)
    time.sleep(random.randint(6, 10))  # Esperar a que cargue la página

    # Verificar si existe la clase "core-section-container my-3 no-results"
    try:
        no_results_element = driver.find_element(By.CSS_SELECTOR, "section.core-section-container.my-3.no-results")
        print(f"No hay resultados para la búsqueda '{keyword}'. Pasando a la siguiente palabra clave.")
        keyword_status[keyword] = 0
        save_keyword_status(keyword_status_file, keyword_status)
        continue
    except:
        keyword_status[keyword] = 1
        pass

    # Obtener el total de trabajos disponibles
    try:
        total_jobs_element = driver.find_element(By.CLASS_NAME, "results-context-header__job-count")
        total_jobs = int(total_jobs_element.text.replace(',', ''))
        keyword_status[keyword] = total_jobs
    except Exception as e:
        print(f"No se pudo obtener el total de trabajos para '{keyword}'. Pasando a la siguiente palabra clave.")
        continue

    # Guardar el estado actualizado inmediatamente
    save_keyword_status(keyword_status_file, keyword_status)

    # Realizar scroll y hacer clic en el botón 'Mostrar más' hasta encontrar el div final
    while True:
        try:
            # Realizar un scroll hasta el final de la página
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            # Verificar si se ha encontrado el div final
            try:
                final_div = driver.find_element(By.CSS_SELECTOR, "div.inline-notification.text-color-signal-positive")
                if "Has visto todos los empleos para esta búsqueda" in final_div.text:
                    print("Se ha alcanzado el final de la lista de trabajos.")
                    break
            except:
                pass

            # Intentar encontrar y hacer clic en el botón 'Mostrar más'
            try:
                show_more_button = driver.find_element(By.CSS_SELECTOR, "button.infinite-scroller__show-more-button--visible")
                show_more_button.click()
                time.sleep(3)
            except:
                pass

        except Exception as e:
            print(f"Error durante el scroll y la búsqueda del botón: {e}")
            break

    # Volver al inicio de la página
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(3)

    # Lista para almacenar los detalles de cada oferta de trabajo
    all_jobs = []

    # Variable para rastrear los data-entity-urn procesados
    processed_job_ids = set()

    error_count = 0

    try:
        while len(processed_job_ids) < total_jobs:
            job_elements = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")

            if not job_elements:
                break

            for job_element in job_elements:
                try:
                    data_entity_urn = job_element.find_element(By.CSS_SELECTOR, "div.base-card").get_attribute("data-entity-urn")
                    
                    if data_entity_urn not in processed_job_ids:
                        processed_job_ids.add(data_entity_urn)
                        job_element.click()
                        time.sleep(3)  # Esperar a que cargue el contenido de la oferta de trabajo

                        # Obtener la URL actual y extraer el currentJobId
                        current_url = driver.current_url
                        current_jobid = get_current_jobid(current_url)

                        # Obtener los detalles de la oferta de trabajo
                        job_details = get_job_details(driver, keyword)
                        job_details['current_jobid'] = current_jobid

                        # Añadir los detalles a la lista
                        all_jobs.append(job_details)

                        # Guardar los detalles de los trabajos en un CSV
                        save_to_csv(all_jobs)

                        # Reiniciar contador de errores después de un éxito
                        error_count = 0
                except Exception as e:
                    print(f"Se produjo un error al procesar un elemento: {e}")
                    error_count += 1
                    if error_count >= 3:
                        print("Se han producido 3 errores consecutivos, pasando a la siguiente palabra clave.")
                        break
                    continue

            if error_count >= 3:
                break

            # Si no se encuentran más elementos, salir del bucle
            if len(job_elements) == 0:
                break

    except Exception as e:
        print(f"Se produjo un error general: {e}")
        save_to_csv(all_jobs)

    finally:
        # Guardar los detalles de los trabajos en un CSV al finalizar
        save_to_csv(all_jobs)

# Guardar el estado de cada palabra clave en un CSV
save_keyword_status(keyword_status_file, keyword_status)

# Cerrar el navegador
driver.quit()
print("Ejecución finalizada. Revisa el navegador para más detalles.")

