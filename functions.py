
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























    # Estas serviran como etiquetas en dataframe y para yfinance
    t_fechas = [i.strftime('%d-%m-%Y') for i in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]

    # lista con fechas ordenadas (para usarse como indexadores de archivos)
    i_fechas = [j.strftime('%d%m%y') for j in sorted([pd.to_datetime(i[8:]).date() for i in archivos])]

    # Final data to return
    r_f_fechas = {'i_fechas': i_fechas, 't_fechas': t_fechas}

    return r_f_fechas

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















