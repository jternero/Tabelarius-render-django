# utils/functions.py

import os
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# Opciones del navegador Chrome para ejecutar sin GUI (headless)
def get_chrome_driver(download_folder):
    chrome_options = Options()
    chrome_options.binary_location = os.getenv("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    service = Service(os.getenv("CHROMEDRIVER_BIN"))

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "download.extensions_to_open": ""
    })
    
    return driver


# Seleccionar certificado (ajusta según necesidades)
def seleccionar_certificado(driver, ruta_xml):
    print("🔹 Accediendo a FACe para remitir factura...")
    driver.get('https://face.gob.es/es/facturas/remitir-factura')

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "factura_email"))
    )

    driver.find_element(By.ID, 'factura_factura').send_keys(ruta_xml)

    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "firma_submit2"))
    )
    driver.find_element(By.ID, 'firma_submit2').click()
    time.sleep(2)    


# Enviar facturas con PDF
def enviar_facturas_con_pdf(driver, files_pdf, files_xml, main_folder, email):
    print(f"📤 Enviando {len(files_xml)} facturas con PDF...")

    for xml_file, pdf_file in zip(files_xml, files_pdf):
        ruta_xml = os.path.join(main_folder, xml_file)
        ruta_pdf = os.path.join(main_folder, pdf_file)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "factura_email")))
        driver.find_element(By.ID, 'factura_email').send_keys(email)
        driver.find_element(By.ID, 'factura_factura').send_keys(ruta_xml)
        driver.find_element(By.ID, 'factura_anexos').send_keys(ruta_pdf)
        
        time.sleep(2)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'factura[Enviar]')))
        driver.find_element(By.NAME, 'factura[Enviar]').click()
        
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@ng-click, 'confirmar')]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@ng-click='toRemitir()']"))).click()



# Enviar facturas sin PDF
def enviar_facturas_sin_pdf(driver, files_xml, main_folder, email):
    print(f"📤 Enviando {len(files_xml)} facturas sin PDF...")

    for xml_file in files_xml:
        ruta_xml = os.path.join(main_folder, xml_file)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "factura_email")))
        driver.find_element(By.ID, 'factura_email').send_keys(email)
        driver.find_element(By.ID, 'factura_factura').send_keys(ruta_xml)


        driver.find_element(By.NAME, 'factura[Enviar]').click()
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//button[contains(@ng-click, 'confirmar')]"))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@ng-click='toRemitir()']"))).click()



# Función principal para Django
def remitir_en_FACE(main_folder, email):
    print(f"📂 Procesando archivos en {main_folder} para remitir en FACe...")

    files_xml = [f for f in os.listdir(main_folder) if f.endswith('.xml') or f.endswith('.xsig')]
    files_pdf = [f for f in os.listdir(main_folder) if f.endswith('.pdf')]

    driver = get_chrome_driver(main_folder)

    try:
        seleccionar_certificado(driver, os.path.join(main_folder, files_xml[0]))

        if files_pdf and len(files_pdf) == len(files_xml):
            enviar_facturas_con_pdf(driver, sorted(files_pdf), sorted(files_xml), main_folder, email)
        elif not files_pdf:
            enviar_facturas_sin_pdf(driver, sorted(files_xml), main_folder, email)
        else:
            raise Exception('❌ La cantidad de archivos XML y PDF no coincide.')

    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        driver.quit()
        print("🔴 Selenium cerrado.")

    return "✅ Proceso de remisión finalizado."
