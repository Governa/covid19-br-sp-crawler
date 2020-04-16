source_estado = "http://www.seade.gov.br/wp-content/uploads/2020/04/Dados-covid-19-estado.csv"
source_municipios = "http://www.seade.gov.br/wp-content/uploads/2020/04/Dados-covid-19-municipios.csv"

import pandas as pd
import numpy as np
import requests
import io

#pd.read_csv(source) # Falha por causa de algum certificado, verificar
# Enquanto isso workaround:
data = requests.get(source_municipios, verify=False)
f = io.StringIO(data.content.decode('iso8859-1'))
df = pd.read_csv(f, sep=';')

df.columns = ['MUNICÍPIO', 'CONFIRMADO', 'MORTES', 'LETALIDADE', 'COD. IBGE', 'LATITUDE', 'LONGITUDE', 'N/A', 'N/A']
del df['N/A']
df = df[pd.notnull(df['MUNICÍPIO'])]
df.to_csv('br-sp.csv', index=False)
