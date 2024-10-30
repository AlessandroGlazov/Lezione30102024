import os
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
import re
from datetime import datetime

logging.basicConfig(level=logging.INFO)

chrome_driver_path = r"C:\Users\pigro\OneDrive\Desktop\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)
options = Options()
options.add_experimental_option("detach", True)

logging.info("Avvio del driver di Chrome")
driver = Chrome(service=service, options=options)

logging.info("Navigazione verso la pagina di destinazione")
driver.get("https://www.albopretorionline.it/campania/alboente.aspx")
time.sleep(2)

def clicca_bottone_ambiente(driver):
    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'btCerca'))
        )
        logging.info("Bottone trovato")
        driver.execute_script("arguments[0].click();", button)
        logging.info("Bottone cliccato con successo.")
    except NoSuchElementException:
        logging.error("Bottone non è stato trovato.")
    except Exception as e:
        logging.error(f"Errore imprevisto: {str(e)}")

def scarica_file_da_link(link, directory=r"C:\Users\pigro\OneDrive\Desktop\Lezione30102024\pdf_files"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    logging.info(f"Scaricamento del file da {link}")
    nome_file = re.sub(r'[\\/*?:"<>|]', "", link.split("/")[-1] + '.pdf')
    nome_file = os.path.join(directory, nome_file)
    try:
        response = requests.get(link)
        response.raise_for_status()
        with open(nome_file, "wb") as file:
            file.write(response.content)
        logging.info(f"File scaricato correttamente: {nome_file}")
    except Exception as e:
        logging.error(f"Errore durante il download di {link}: {str(e)}")

def trova_e_scarica_tutti_i_pdf(driver, directory=r"C:\Users\pigro\OneDrive\Desktop\Lezione30102024\pdf_files"):
    logging.info("Ricerca dei link PDF sulla pagina")
    try:
        links = driver.find_elements(By.TAG_NAME, "a")
        logging.info(f"Numero di elementi 'a' trovati: {len(links)}")
        pdf_trovati = False
        for link in links:
            href = link.get_attribute("href")
            if href and 'download.aspx' in href:
                full_url = "https://www.albopretorionline.it/campania/" + href if href.startswith('download.aspx') else href
                logging.info(f"Trovato link PDF: {full_url}")
                scarica_file_da_link(full_url, directory)
                logging.info(f"File PDF scaricato: {full_url}")
                pdf_trovati = True
        if not pdf_trovati:
            logging.warning("Nessun file PDF trovato sulla pagina.")
    except Exception as e:
        logging.error(f"Errore durante la ricerca dei link PDF: {str(e)}")

clicca_bottone_ambiente(driver)
logging.info("Attendi di 2 secondi per il caricamento dei risultati")
time.sleep(2)
trova_e_scarica_tutti_i_pdf(driver)
logging.info("Chiusura di Chrome")

data_scraping = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
logging.info(f"Data dello scraping: {data_scraping}")

driver.quit()
