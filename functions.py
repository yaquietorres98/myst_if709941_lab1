
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
import datetime
import glob
import pandas as pd
import numpy as np



def f_fechas(p_archivos):
    # Estas serviran como etiquetas en dataframe y para yfinance
    t_fechas = [i.strftime('%d-%m-%Y') for i in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]

    # lista con fechas ordenadas (para usarse como indexadores de archivos)
    i_fechas = [j.strftime('%d%m%y') for j in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]

    # Final data to return
    r_f_fechas = {'i_fechas': i_fechas, 't_fechas': t_fechas}

    return r_f_fechas
# --------------------------------------------------------------------------------------------- PASO 1.4 -- #
# -----------------------------------------------------------------
# -- Construir el vector de tickers utilizables en yahoo finance

def f_ticker(p_archivos, p_data_archivos):


    tickers = []
    for i in p_archivos:
        # i = archivos[0]
        l_tickers = list(p_data_archivos[i]['Ticker'])
        [tickers.append(i + '.MX') for i in l_tickers]
    global_tickers = np.unique(tickers).tolist()


    # Ajustes de nombre de tickers
    global_tickers = [i.replace('GFREGIOO.MX', 'RA.MX') for i in global_tickers]
    global_tickers = [i.replace('MEXCHEM.MX', 'ORBIA.MX') for i in global_tickers]
    global_tickers = [i.replace('LIVEPOLC.1.MX', 'LIVEPOLC-1.MX') for i in global_tickers]

    # eliminar entradas de efectivo: MXN, USD, y tickers con problemas de precios: KOFL, BSMXB
    [global_tickers.remove(i) for i in ['MXN.MX', 'USD.MX', 'KOFL.MX', 'KOFUBL.MX', 'BSMXB.MX']]

return global_tickers

# --------------------------------------------------------------------------------------------- PASO 1.5 -- #
# -- Descargar y acomodar todos los precios historicos

def f_precios(p_archivos):
    # para contar tiempo que se tarda
    inicio = time.time()

    # Descarga masiva de precios de yahoo finance
    data = yf.download(global_tickers, start="2017-08-21", end="2020-08-21", actions=False,
                       group_by="close", interval='1d', auto_adjust=True, prepost=False, threads=True)

    # Tiempo que se tarda
    print('se tardo', round(time.time() - inicio, 2), 'segundos')

    data_close = pd.DataFrame({i: ['Close'] for i in global_tickers})
    ic_fechas = sorted(list(set(data_close.index.astype(str).tolist()) & set(i_fechas)))
    # Localizar todos los precios
    precios = data_close.iloc[[int(np.where(data_close.index.astype(str) == i)[0]) for i in ic_fechas]]
    # Ordenar columnas lexicograficamente
    precios = precios.reindex(sorted(precios.columns), axis=1)

    return precios
# --------------------------------------------------------------------------------------------- PASO 1.6 -- #
# -- Obtener posiciones historicas

# nota, pasar en todos los meses las posiciones en KOFL.MXN y BSMXB.MX a CASH en MXN

# tomar solo las fechas de interes
# tomar solo las columnas de interes
# transponer matriz para tener x: fechas, y: precios
# multiplicar matriz de precios por matriz de pesos
# hacer suma de cada columna para obtener valor de mercado de la posicion

# capital inicial
k = 1000000
# comisiones por transaccion
c = 0.00125
# vector de comisiones historicas
comisiones = []

#Obtener posicion inicial
# los % para KOFL, KOFUBL, BSMX, USD asignarlos a CASH (eliminados)
c_activos = ['KOFL', 'KOFUBL', 'BSMX', 'MX', 'USD']
# Diccionario para resultado final
inv_pasiva = {'timestamp':['30-01-2018'],'capital':[k]}

#Falta revisar que sea el archivo del primer mes
pos_datos = data_archivos[archivos[0]].copy().sort_values('Ticker')[['Ticker','Nombre', 'Peso (%)']]

# Extraer la lista de activos a eliminar
i_activos = list(pos_datos[pos_datos['Ticker'].isin(c_activos)].index)
# Eliminar los activos del dataframe
pos_datos.drop(i_activos, inplace=True)

# Resetear el index
pos_datos.reset_index(inplace=True, drop=True)

#Agregar.MX para empatar precios
pos_datos['Ticker'] = pos_datos['Ticker'] + '.MX'

#Corregir tickers en datos
pos_datos['Ticker'] = pos_datos['Ticker'].replace('LIVEPOLC.1.MX','LIVEPOLC-1.MX')
pos_datos['Ticker'] = pos_datos['Ticker'].replace('MEXCHEM.MX','ORBIA.MX')
pos_datos['Ticker'] = pos_datos['Ticker'].replace('GFREGIOO.MX', 'RA.MX')
#pos_datos['Ticker'] = pos_datos['Ticker'].replace('KOFL.MX', 'CASH')
#pos_datos['Ticker'] = pos_datos['Ticker'].replace('BSMXB.MX', 'CASH')
#pos_datos['Ticker'] = pos_datos['Ticker'].replace('MXN,MX', 'CASH')

#-----------------------------------------------------------------------------

#i_activos = list(pos_datos[pos_datos['Ticker'].isin])
#pos_datos['Precio'] = (np.array([precios.iloc[0, precios.columns.to_list().index(i)] for i in pos_datos['Ticker']]))
#pos_datos['Precio'] = np.array(precios.iloc[0,[i in pos_datos['Ticker'].to_list() for i in precios.columns.to_list()]])

# Capital destinado por accion = proporcion de capital - comisiones por la posicion
pos_datos['Capital'] = pos_datos['Peso(%)']*k - pos_datos['Peso(%)']*k*c

#-- Cantidad de titulos por accion
pos_datos['Titulos'] = pos_datos['Capital']//pos_datos['Precio']

#-- Valor de la postura por accion
pos_datos['Postura'] = pos_datos['Titulos']*pos_datos['Precio']

#-- Comision pagada
pos_datos['Comision'] = pos_datos['Postura']*c
pos_comision = pos_datos['Comision'].sum()

#Efectivo libre en la postura
pos_cash = k - pos_datos['Postura'].sum() - pos_comision['Comision'].sum()
pos_cash=np.round(pos_cash)
#Valor de la postura
pos_value = pos_datos['Postura'].sum

#for i in range (len(i_fechas)):
 #   i_fechas.append()

#Actualizar lista de valores de cada llave en el diccionario
df_pasiva['timestamp'].append(fechas['t_fechas'][0])
df_pasiva['capital'].append(pos_value + pos_cash)


#---------------------------------------------------------
#-- Evolucion de la postura (Inversion pasiva)

#for arch in range(1,len(archivos)):...
















