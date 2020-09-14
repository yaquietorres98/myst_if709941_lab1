
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: main.py : python script with the main functionality                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
from data import archivos
import functions as fn
import data as dt


# data.py
# --------------------------------------
# Obtener la lista de los archivos a leer

archivos = dt.archivos


#----------------------------------------------
# -- Leer todos los archivos y guardarlos en un diccionario

data_archivos = dt.data_archivos

# functions.py
#----------------------------------------------
# -- Construir el vector de fechas a partir del vector de nombres de archivos

fechas = fn.f_fechas(p_archivos=archivos)

# Mostrar las primeras 5 fechas (con formato 1)
print(fechas['i_fechas'][0:4])

# Mostrar las primeras 5 fechas (con formato 1)
print(fechas['t_fechas'][0:4])

# functions.py
#-------------------------------------------------------
# -- Construir el vector de tickers utilizables en yahoo finance

global_tickers = fn.t_tickers(p_archivos=archivos,p_data_archivos=data_archivos)

# Mostrar los tickers globales (5)
print(global_tickers[0:4])

# funtions.py
#-------------------------------------------------------------------
# -- Descargar y acomodar todos los precios historicos

precios = fn.f_obtener_precios(p_tickers=global_tickers, p_fechas=fechas['i_fechas'])
precios = precios['precios']

# Mostrar los primeros precios





























