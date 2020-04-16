source_estado = "http://www.seade.gov.br/wp-content/uploads/2020/04/Dados-covid-19-estado.csv"
source_municipios = "http://www.seade.gov.br/wp-content/uploads/2020/04/Dados-covid-19-municipios.csv"

import pandas as pd
import numpy as np
import requests
import io

#pd.read_csv(source) # Falha por causa de algum certificado, verificar
# Enquanto isso workaround:
# requests.get(source, verify=False)

#
# Municípios
#
data = requests.get(source_municipios, verify=False)
f = io.StringIO(data.content.decode('iso8859-1'))
df = pd.read_csv(f, sep=';')

df.columns = ['MUNICÍPIO', 'CONFIRMADO', 'MORTES', 'LETALIDADE', 'COD. IBGE', 'LATITUDE', 'LONGITUDE', 'N/A', 'N/A']
del df['N/A']
df = df[pd.notnull(df['MUNICÍPIO'])]
df.to_csv('br-sp.csv', index=False)


#
#  Timeseries
#
data = requests.get(source_estado, verify=False)
f = io.StringIO(data.content.decode('iso8859-1'))
df = pd.read_csv(f, sep=';')
del df['Unnamed: 5']
del df['Unnamed: 6']
df.columns = ['DATA', 'CONFIRMADOS', 'CONFIRMADOS NO DIA', 'MORTES', 'LETALIDADE']
df = df[pd.notnull(df['DATA'])]

month = {
    'jan': 1,
    'fev': 2,
    'mar': 3,
    'abr': 4,
    'mai': 5,
    'jun': 6,
    'jul': 7,
    'ago': 8,
    'set': 9,
    'out': 10,
    'nov': 11,
    'dez': 12,
}

df['DATA'] = pd.to_datetime(df['DATA'].str.split(' ').map(lambda x: "{}-{}-{}".format(2020, month[x[1]], x[0])))
df['LETALIDADE'] = pd.to_numeric(df['LETALIDADE'].str.strip("%").str.replace(',', '.'))
df.to_csv('br-sp-timeseries.csv', index=False)
