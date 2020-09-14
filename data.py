
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import math
import time as time
import numpy as np
import pandas as pd
import yfinance as yf
from os import listdir, path
from os.path import isfile, join
from datetime import datetime

#from main import precios

pd.set_option('display.max_rows', None)                   # sin limite de renglones maximos
pd.set_option('display.max_columns', None)                # sin limite de columnas maximas
pd.set_option('display.width', None)                      # sin limite el ancho del display
pd.set_option('display.expand_frame_repr', False)         # visualizar todas las columnas

# -------------------------------------------------------------------------------------------- PASO 1.1  -- #
# -- Obtener la lista de los archivos a leer

# obtener la ruta absoluta de la carpeta donde estan los archivos
abspath = path.abspath('files/NAFTRAC_holdings')
# obtener una lista de todos los archivos en la carpeta (quitandole la extension de archivo)
# no tener archivos abiertos al mismo tiempo que correr la siguiente linea, error por ".~loc.archivo"
archivos = [f[8:-4] for f in listdir(abspath) if isfile(join(abspath, f))]
archivos = sorted(archivos, key=lambda t: datetime.strptime(t[8:], '%d%m%y'))
# --------------------------------------------------------------------------------------------- PASO 1.2 -- #
# -- Leer todos los archivos y guardarlos en un diccionario

# crear un diccionario para almacenar todos los datos
data_archivos = {}

for i in archivos:
    # leer archivos despues de los primeros dos renglones
    data = pd.read_csv('files/NAFTRAC_holdings/' + i + '.csv', skiprows=2, header=None)
    # renombrar las columnas con lo que tiene el 1er renglon
    data.columns = list(data.iloc[0, :])
    # quitar columnas que no sean nan
    data = data.loc[:, pd.notnull(data.columns)]
    # resetear el indice
    data = data.iloc[1:-1].reset_index(drop=True, inplace=False)
    # quitar las comas en la columna de precios
    data['Precio'] = [i.replace(',', '') for i in data['Precio']]
    # quitar el asterisco de columna ticker
    data['Ticker'] = [i.replace('*', '') for i in data['Ticker']]
    # hacer conversiones de tipos de columnas a numerico
    convert_dict = {'Ticker': str, 'Nombre': str, 'Peso (%)': float, 'Precio': float}
    data = data.astype(convert_dict)
    # convertir a decimal la columna de peso (%)
    data['Peso (%)'] = data['Peso (%)']/100
    # guardar en diccionario
    data_archivos[i] = data
return data_archivos


# --------------------------------------------------------------------------------------------- PASO 1.3 -- #
# -- Construir el vector de fechas a partir del vector de nombres de archivos

# estas serviran como etiquetas en dataframe y para yfinance
t_fechas = [i.strftime('%d-%m-%Y') for i in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]

# lista con fechas ordenadas (para usarse como indexadores de archivos)
i_fechas = [j.strftime('%d%m%y') for j in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]



# Desgloce ----------------------------------------------------------------------------------------------
# Fecha en la que se busca hacer el match de precios
match = 0
precios.index.to_list()[match]

# Precios necesarios para la posicion metodo 1
#m1 = np.array(precios.iloc[match,[i in pos_datos['Ticker'].to_list() for i in precios.columns.to_list()]])
m2 = [precios.iloc[match,precios.columns.to_list().index(i)] for i in pos_datos['Ticker']]

#pos_datos['Precio_m1'] = m1
pos_datos['Precio_m2'] = m2




