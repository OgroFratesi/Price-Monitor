
import pandas as pd
import time
from selenium import webdriver
import timeit
import warnings

from modificaciones import crear_dic
warnings.filterwarnings('ignore')

def scrapper_coto():
    print('/-------------------------------------------------------/')
    print('Comenzamos a scrappear COTO..')
    start_time = timeit.default_timer()

    dic_marcas, PRODUCTOS = crear_dic('coto')

    # El PATH donde se encuentra el CHROMEDRIVER
    path = 'C:/Users/Usuario/chromedriver'

    driver = webdriver.Chrome(path)

    # Entramos a la pagina de COTO
    driver.get('https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-bebidas-bebidas-sin-alcohol-aguas/_/N-17xtqou')
    time.sleep(3)

    ITEMS=[]
    MARCA=[]
    PRECIO=[]

    for producto in PRODUCTOS:
        # Obtenemos el path del buscador para ir enviando nuestros productos uno a uno
        buscador = driver.find_element_by_xpath('//*[@id="atg_store_searchInput"]')
        buscador.send_keys(producto)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="atg_store_searchSubmit"]').submit()
        time.sleep(2)

            
        try:
            items = driver.find_element_by_id('products')
            pagina = items.text
            pagina = pagina.split('AGREGAR')
            # Metemos en una lista el texto que figura de cada producto que aparece
            lista_productos=[]
            for e in range(len(pagina)):
                prod = pagina[e].split('\n')
                prod = [string for string in prod if string != '']
                lista_productos.append(prod)
            ITEMS.append(lista_productos[0])
            
            # Buscamos la descripcion total del producto
            DESCRIPCION = driver.find_elements_by_class_name('descrip_full')
            for d in DESCRIPCION:
                MARCA.append(d.get_attribute("textContent"))
            time.sleep(2)
        except:
            print(f'Producto sin stock: {producto}')
            pass

    # Cerramos la pagina
    driver.quit()



    def look_in_dic(dic, item):
    
        for key in dic.keys():
            if key in item.lower():
                return dic[key]

    nombre, subtipo = [], []
    for e in range(len(MARCA)):
        for key in dic_marcas.keys():
            if key in MARCA[e].lower():
                clean_text = ' '.join(MARCA[e].split())
                nombre.append(dic_marcas[key]['marca'])
                dic = dic_marcas[key]['subtipo']
                subtipo.append(look_in_dic(dic, clean_text))
                break
        if len(nombre) != (e+1):
            nombre.append('none')
        if len(subtipo) != (e+1):
            subtipo.append('none')

    # Limpiamos el texto dentro del item para obtener el precio final del producto. Insertado en 'PRECIO'
    # Son 4 pasos para terminar con el precio final, y si tiene descuento, el mismo aplicado.
    texto = []
    for i in range(len(ITEMS)):
        texto += ITEMS[i]

    PRE_PRECIO = []
    for e in range(len(texto)):
        if 'ver planes de' in texto[e].lower():
            if 'interés' not in texto[e-1]:
                PRE_PRECIO.append(texto[e-1])
        elif 'para comprar este producto' in texto[e].lower():
            PRE_PRECIO.append(texto[e-1])
        elif 'cuotas sin interés' in texto[e].lower():
            PRE_PRECIO.append(texto[e-1])
        elif 'por el momento' in texto[e].lower():
            PRE_PRECIO.append(texto[e-1])

    PRECIOS = []
    for e in PRE_PRECIO:
        if 'c/u' in e:
            PRECIOS.append(e[:-3].split('$')[1])
        elif '$' in e:
            PRECIOS.append(e.split('$')[1])
        else:
            PRECIOS.append('0')
    PRECIO = []
    for e in PRECIOS:
        PRECIO.append(e.replace(',', '.'))


    # Ahora manualmente creamos una lista con todos los tamaños para luego mapear con nuestra tabla.

    tamaños = []
    for e in MARCA:   
        if '1.5' in e: tamaños.append('1500')
        elif '1500' in e: tamaños.append('1500')
        elif 'limoneto' in e:
            if '1500' in e: tamaños.append('1500')
            elif '2250' in e: tamaños.append('2250')
            else: tamaños.append('500')
        elif '2.25' in e: tamaños.append('2250')
        elif '1.25' in e: tamaños.append('1250')
        elif '1,25' in e: tamaños.append('1250')
        elif '1.65' in e: tamaños.append('1650')
        elif '250' in e: tamaños.append('250')
        elif '269' in e: tamaños.append('269')
        elif '730' in e: tamaños.append('730')
        elif '473' in e: tamaños.append('473')
        elif '710' in e: tamaños.append('710')
        elif '330' in e: tamaños.append('330')
        elif '1.75' in e: tamaños.append('1750')
        elif 'one' in e: tamaños.append('1000')
        elif '1,5' in e: tamaños.append('1500')
        elif '750' in e: tamaños.append('750')
        elif '2,25' in e: tamaños.append('2250')
        elif '1,75' in e: tamaños.append('1750')
        elif '354' in e: tamaños.append('354')
        elif '500' in e: tamaños.append('500')
        elif 'glaciar' in e:
            if '50..' in e: tamaños.append('500')
            elif 'Bi' in e: tamaños.append('6.3')
            elif '2' in e: tamaños.append('2000')
        elif '2' in e: tamaños.append('2000')
        elif '1' in e: tamaños.append('1000')
        elif '6.3' in e: tamaños.append('6.3')
        elif '6,3' in e: tamaños.append('6.3')
        elif '3' in e: tamaños.append('3000')
        else:
            tamaños.append('other')


    # Armamos el dataframe con los datos ya limpios
    df = pd.DataFrame()
    df['marca'] = nombre
    df['subtipo'] = subtipo
    df['tamaño'] = tamaños
    df['precio'] = PRECIO


    # Ahora deberiamos chequear qué productos estan en packss
    PACK = []
    for e in MARCA:
        if '6 unidades' in e.lower():
            PACK.append(6)
        elif '4 unidades' in e.lower():
            PACK.append(4)
        elif '10 unidades' in e.lower():
            PACK.append(10)
        elif 'pak' in e.lower():
            PACK.append(6)
        elif 'PACK' in e.lower():
            if '269' in e:
                PACK.append(10)
            elif '6' in e:
                PACK.append(6)
            elif '4' in e:
                PACK.append(4)
            else:
                print(e)
        elif '6' in e:
            if '269' in e:
                PACK.append(1)
            elif 'agua' in e.lower():
                PACK.append(1)
            else:
                PACK.append(6)
        else:
            PACK.append(1)
            
    df['pack'] = PACK

    # Modificamos el punto para que no haya confusiones 
    nuevo_precio = []
    for e in PRECIO:
        if len(e) > 6:
            n = e[:-3]
            n = n.replace('.', '')
            nuevo_precio.append(n)
        else:
            nuevo_precio.append(e)

    # Ponemos el precio del producto y si es un pack ponemos el precio individual
    df['precio'] = nuevo_precio
    df['precio_final'] =round(df['precio'].astype(float) / df.pack,2)

    df.to_csv('scrappeado/coto_resultados.csv')

