import pandas as pd
import numpy as np
import time
import warnings
warnings.filterwarnings('ignore')

def crear_modificaciones(market):
    
    tabla = pd.read_csv('mapeo_productos.csv',encoding='utf-8')
    tabla = tabla[['sku', 'marca', 'tamaño', 'subtipo', 'pack']]
    tabla.fillna('', inplace=True)
    tabla.subtipo = tabla.subtipo.apply(lambda x: str(x))
    tabla = tabla.fillna('')
    tabla.subtipo = tabla.subtipo.replace('nan', '')

    df = pd.read_csv(f'scrappeado/{market}_resultados.csv', index_col=0)
    df.rename(columns={'precio_final': market}, inplace=True)

    columnas = ['marca', 'subtipo', 'tamaño', 'pack']
    tabla = tabla.merge(df, on=columnas, how='left')
    tabla[['sku', 'marca', 'subtipo', 'tamaño', 'pack', market]]
    

 
    porc = (tabla[tabla[market] > 0].shape[0] / tabla.shape[0])
    print(f'Porcentaje de productos {market}: ' + str(round(porc,2)) + '%')

    tabla.to_csv('quilmes_precios.csv')
    # Bajo la lista de precios que se usaron el día anterior
    tabla_ayer = pd.read_excel('quilmes_precios.xlsx', usecols = 'C,D,E,F,L,M,N,O,P,Q,R')
    # Tomo solo los precios de coto
    precio_ayer = tabla_ayer[market].values

    # Las agrego al df para ver que productos modificaron sus precios.
    tabla['precio_ayer'] = precio_ayer
    tabla['diferencia'] = (tabla[market] - tabla.precio_ayer) / tabla.precio_ayer * 100
    tabla['modificar'] = tabla['diferencia'].apply(lambda x: 'Si' if abs(x) > 4 else 'No')

    modificados = tabla[tabla.modificar == 'Si']
    modificados['precio_hoy'] = modificados[market]
    modificados = modificados[['marca', 'subtipo', 'tamaño','pack', 'precio_ayer', 'precio_hoy']]
    time.sleep(1)
    # Guardamos en un CSV
    modificados.to_csv(f'modificaciones/modificacion_{market}.csv')
    print(f'{market} nuevos precios guardado.')


def concatenar_modificaciones():

    supermercados = ['disco', 'vea', 'coto', 'walmart']
    mkt_to_concat = []
    for super in supermercados:
        mkt = pd.read_csv(f'modificaciones/modificacion_{super}.csv', index_col=0)
        mkt['SMK'] = super
        mkt_to_concat.append(mkt)

    df = pd.concat(mkt_to_concat)
    df.to_excel('MODIFICACIONES.xlsx')
    print('Tabla modificaciones LISTA')



def crear_dic(market):
    
    excel = pd.read_csv('mapeo_productos.csv', index_col=0,encoding='utf-8')

    excel.sort_values('marca',ascending=False, inplace=True)
    excel.fillna('', inplace=True)

    dic_marcas = {}
    for marca, marca_market in zip(excel.marca, excel[f'{market}_marca']):
        dic_subtipo = {}
        df_marca = excel[excel.marca == marca].sort_values(f'{market}_subtipo', ascending=False)
        for subtipo, subtipo_market in zip(df_marca.subtipo, df_marca[f'{market}_subtipo']):
            dic_subtipo[subtipo_market] = subtipo
        dic_marcas[marca_market] = {'marca':marca, 'subtipo': dic_subtipo}

    PRODUCTOS = [x for x in excel.marca.unique()]

    return dic_marcas, PRODUCTOS

def concatenar_precios():
    
    tabla = pd.read_csv('mapeo_productos.csv',converters={'tamaño':str},encoding='utf-8')
    tabla = tabla[['sku', 'marca', 'tamaño', 'subtipo', 'pack']]
    tabla.fillna('', inplace=True)
    tabla.subtipo = tabla.subtipo.apply(lambda x: str(x))
    tabla = tabla.fillna('')
    tabla.subtipo = tabla.subtipo.replace('nan', '')
    

    supermercados = ['disco', 'coto', 'vea', 'walmart']

    for market in supermercados:

        df = pd.read_csv(f'scrappeado/{market}_resultados.csv',encoding='utf-8',converters={'tamaño':str}, index_col=0)
        df.rename(columns={'precio_final': market}, inplace=True)
        df = df[['marca', 'subtipo', 'tamaño', 'pack', market]]
        df = df.fillna('')
        columnas = ['marca', 'subtipo', 'tamaño', 'pack']
        df.sort_values(market, inplace=True)
        df.drop_duplicates(subset=columnas, keep='first', inplace=True)
        tabla = tabla.merge(df, on=columnas, how='left')
        
    print('Precios concatenados!')
    tabla.to_csv('quilmes_precios.csv', encoding='utf-8')