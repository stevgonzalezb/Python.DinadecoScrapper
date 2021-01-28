import requests
import configparser
import os
from bs4 import BeautifulSoup
import pandas as pd

config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "config.ini")
config = configparser.ConfigParser()
config.read(config_path)

BASE_URL = config['config']['base_url']
USER_AGENT = config['config']['user_agent']
CSV_PATH = config['config']['csv_path']
SEPARATOR = config['config']['separator']

def set_personeria(row):
    if row['Estado'] == 'Activa':
        return 'http://dinadecodevcopia.addax.cc/zf_ConsultaPublica/Index/personeria/DAODnaVAsociacion_numero_registro/' + row['Número Registro']


def get_html(number):
    url = BASE_URL + number
    headers = {"User-Agent": USER_AGENT}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

def process_data():
    datasets = []
    for x in range(1, 2):
        print('Procesando página ' + str(x))
        data = get_html(str(x))
        table = data.find(id='the_table')

        if x == 1:
            headings = [th.get_text() for th in table.find("tr").find_all("th")]

        for row in table.find_all("tr")[1:]:
            datasets.append([td.get_text().strip().replace('\n\n\n\n\n\n\nSaving...', '') for td in row.find_all("td")])
        print('Termina página ' + str(x))

    df = pd.DataFrame(datasets, columns = headings)
    return df

df = process_data()
df['Personería'] = df.apply(set_personeria, axis = 1)
df.to_csv(CSV_PATH, sep=SEPARATOR, index=False, encoding='utf-8-sig')