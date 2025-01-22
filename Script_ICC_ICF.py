from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from google.cloud import bigquery
import pandas as pd
import os
import time
import datetime

# Configurações gerais
DOWNLOAD_DIR = r"C:\Users\Desktop\Documents\Teste_Arquivo"
CHROMEDRIVER_PATH = r"C:\Users\Desktop\Documents\chromedriver-win64\chromedriver.exe"
GOOGLE_CREDENTIALS = r"C:\Users\Desktop\Downloads\SA-andersonlf21.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS

def wait_for_download(directory, timeout=30):
    """Espera até que um novo arquivo seja baixado no diretório."""
    initial_files = set(os.listdir(directory))
    for _ in range(timeout):
        time.sleep(1)
        new_files = set(os.listdir(directory)) - initial_files
        if new_files:
            return new_files.pop()
    raise TimeoutError("O download não foi concluído a tempo.")

def delete_existing_files():
    """Deleta arquivos antigos do diretório."""
    files_to_delete = ["icc.xlsx", "icf.xlsx"]
    for file_name in files_to_delete:
        file_path = os.path.join(DOWNLOAD_DIR, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)

def download_files():
    """Faz o download dos arquivos ICC e ICF."""
    delete_existing_files()

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": DOWNLOAD_DIR}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
    try:
        wait = WebDriverWait(driver, 10)

        # Download do ICC
        driver.get("https://www.fecomercio.com.br/pesquisas/indice/icc")
        icc_download = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main']/div[1]/div[1]/div[5]/a")))
        icc_download.click()
        downloaded_icc = wait_for_download(DOWNLOAD_DIR)
        os.rename(os.path.join(DOWNLOAD_DIR, downloaded_icc), os.path.join(DOWNLOAD_DIR, "icc.xlsx"))

        # Download do ICF
        driver.get("https://www.fecomercio.com.br/pesquisas/indice/icf")
        icf_download = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='main']/div[1]/div[1]/div[5]/a")))
        icf_download.click()
        downloaded_icf = wait_for_download(DOWNLOAD_DIR)
        os.rename(os.path.join(DOWNLOAD_DIR, downloaded_icf), os.path.join(DOWNLOAD_DIR, "icf.xlsx"))

    finally:
        driver.quit()

def process_icc_data(file_path, sheet_name):
    """Processa os dados do arquivo ICC para adequar ao formato icc_raw."""
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=1)

    # Atualizar lista de colunas
    column_names = [
        "mes", "icc", "icc_ate_10_sm", "icc_mais_de_10_sm", "icc_homens", 
        "icc_mulheres", "icc_ate_35_anos", "icc_mais_de_35_anos", 
        "icea", "icea_ate_10_sm", "icea_mais_de_10_sm", "icea_homens", 
        "icea_mulheres", "icea_ate_35_anos", "icea_mais_de_35_anos", 
        "iec", "iec_ate_10_sm", "iec_mais_de_10_sm", "iec_homens", 
        "iec_mulheres", "iec_ate_35_anos", "iec_mais_de_35_anos"
    ]

    if len(df.columns) != len(column_names):
        raise ValueError(f"Erro: Número de colunas no arquivo ({len(df.columns)}) não corresponde ao esperado ({len(column_names)}).")

    # Renomear colunas
    df.columns = column_names

    # Adicionar timestamp
    df["load_timestamp"] = datetime.datetime.now()

    # Converter colunas numéricas para float
    numeric_columns = column_names[1:]  # Exclui a coluna "mes"
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="coerce")

    return df

def process_icf_data(file_path, sheet_name):
    """Processa os dados do arquivo ICF para adequar ao formato icf_raw."""
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=1)

    # Atualizar lista de colunas
    column_names = [
        "mes", "icf", "icf_ate_10_sm", "icf_mais_de_10_sm", "emprego_atual", 
        "emprego_atual_ate_10_sm", "emprego_atual_mais_de_10_sm", "perspectiva_profissional", 
        "perspectiva_profissional_ate_10_sm", "perspectiva_profissional_mais_de_10_sm", 
        "renda_atual", "renda_atual_ate_10_sm", "renda_atual_mais_de_10_sm", 
        "acesso_credito", "acesso_credito_ate_10_sm", "acesso_credito_mais_de_10_sm", 
        "nivel_consumo_atual", "nivel_consumo_atual_ate_10_sm", "nivel_consumo_atual_mais_de_10_sm", 
        "perspectiva_consumo", "perspectiva_consumo_ate_10_sm", "perspectiva_consumo_mais_de_10_sm", 
        "momento_duraveis", "momento_duraveis_ate_10_sm", "momento_duraveis_mais_de_10_sm"
    ]

    if len(df.columns) != len(column_names):
        raise ValueError(f"Erro: Número de colunas no arquivo ({len(df.columns)}) não corresponde ao esperado ({len(column_names)}).")

    # Renomear colunas
    df.columns = column_names

    # Adicionar timestamp
    df["load_timestamp"] = datetime.datetime.now()

    # Converter colunas numéricas para float
    numeric_columns = column_names[1:]  # Exclui a coluna "mes"
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="coerce")

    return df

def transform_and_upload_to_bigquery(file_path, table_id, sheet_name, process_function):
    """Transforma e carrega os dados no BigQuery."""
    print(f"Processando o arquivo {file_path} na aba {sheet_name}...")

    df_transformed = process_function(file_path, sheet_name)

    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE)

    job = client.load_table_from_dataframe(df_transformed, table_id, job_config=job_config)
    job.result()

    print(f"Dados carregados com sucesso na tabela {table_id}.")

def main():
    """Fluxo principal do script."""
    # Fazer download dos arquivos
    download_files()

    # Caminhos dos arquivos baixados
    icc_path = os.path.join(DOWNLOAD_DIR, "icc.xlsx")
    icf_path = os.path.join(DOWNLOAD_DIR, "icf.xlsx")

    # Tabelas do BigQuery
    icc_table = "ps-eng-dados-ds3x.andersonlf21.icc_raw"
    icf_table = "ps-eng-dados-ds3x.andersonlf21.icf_raw"

    # Processar e carregar dados do ICC
    transform_and_upload_to_bigquery(icc_path, icc_table, sheet_name="SÉRIE", process_function=process_icc_data)

    # Processar e carregar dados do ICF
    transform_and_upload_to_bigquery(icf_path, icf_table, sheet_name="Série Histórica", process_function=process_icf_data)

if __name__ == "__main__":
    main()
