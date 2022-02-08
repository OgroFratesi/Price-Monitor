from modificaciones import crear_dic
import pandas as pd
import time
from selenium import webdriver
import timeit
from selenium.webdriver.common.keys import Keys
import warnings
warnings.filterwarnings('ignore')


def scrapper_vea():

    print('/-------------------------------------------------------/')
    print('Comenzamos a scrappear VEA..')


    start_time = timeit.default_timer()

    # Save the chromedriver path
    path = 'C:/Users/Usuario/chromedriver'
    driver = webdriver.Chrome(path)

    start_time = timeit.default_timer()

    dic_marcas, PRODUCTOS = crear_dic('vea')


    # Now we need to be sure that the location is in Capital Federal
    driver.get('https://www.veadigital.com.ar/')
    time.sleep(5)
    driver.set_window_size(600, 800)
    time.sleep(4)
    try:
        driver.find_element_by_xpath('//*[@id="onesignal-slidedown-cancel-button"]').click()
    except:
        con = 0
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[2]/div[1]/div/div/div[2]/section/div/div[2]/div/div/div[2]/a/span').click()
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[13]/div[1]/div/div[2]/div[1]/a[2]/div[2]/p').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="provincia"]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="provincia"]/option[8]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="tienda"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="tienda"]/option[3]').click()
    time.sleep(4)
    driver.find_element_by_xpath('/html/body/div[13]/div[1]/div/div[2]/div[1]/header/form/button').click()
    time.sleep(4)
    driver.maximize_window()
    time.sleep(4)


    # Now that we are located in Capital Federal, the scraping begin
    lista_productos = []

    for PRODUCTO in PRODUCTOS:


        driver.get(f'https://www.vea.com.ar/{PRODUCTO}?_q={PRODUCTO}&map=ft')
        time.sleep(4)
        try:
            s = driver.find_element_by_xpath('//*[@id="gallery-layout-container"]')
            lista_productos.append(s.text)
            time.sleep(2)
        except:
            print(f'{PRODUCTO} Sin Stock')

    driver.quit()


    ITEMS = []
    pre_items = []
    for item in range(len(lista_productos)):
        p = lista_productos[item].split('\n')
        for e in range(len(p)):
            if p[e] != 'Agregar' and p[e] != 'Sin Stock':
                if 'Ver Producto' in p[e]:
                    pass
                else:
                    pre_items.append(p[e])
            elif p[e] == 'Sin Stock':
                pre_items = []
            else:
                ITEMS.append(pre_items)
                pre_items = []


    MARCA, PRE_PRECIO, PRE_PROMO = [], [], []
    for item in ITEMS:
        MARCA.append(item[1])
        if ('%' in item[2]) or ('x' in item[2]):
            PRE_PRECIO.append(item[4])
            PRE_PROMO.append(item[2])
        else:
            PRE_PRECIO.append(item[2])
            PRE_PROMO.append('1')

    PRECIO = []
    for e in range(len(PRE_PRECIO)):
        if '$' in PRE_PRECIO[e]:
            precio = PRE_PRECIO[e].split('$')[1].replace('.', '').replace(',', '.')
            PRECIO.append(precio)
        else:
            PRECIO.append('0')


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

    PACK = []
    for e in MARCA:
        if 'pack' in e.lower():
            if 'hoppy lager' in e.lower():
                if '10' in e:
                    PACK.append(10)
                else:
                    PACK.append(1)
            else:
                PACK.append(6)
        elif '6' in e:
            if 'awafrut' in e.lower(): PACK.append(1)
            elif 'paso de los' in e.lower(): PACK.append(1)
            elif 'glaciar' in e.lower(): PACK.append(1)
            elif 'nestl' in e.lower(): PACK.append(1)
            elif 'blasfemia' in e: PACK.append(1)
            elif 'corona' in e.lower(): PACK.append(1)
            else: PACK.append(6)
        else:
            PACK.append(1)

    PROMO = []
    for e in PRE_PROMO:
        if '2do al 50' in e: PROMO.append(0.75)
        elif '2do al 80' in e: PROMO.append(0.6)
        elif '3x2' in e: PROMO.append(2/3)
        elif '6x4' in e: PROMO.append(2/3)
        elif '2x1' in e: PROMO.append(0.5)
        elif '25%' in e: PROMO.append(0.75)
        elif '20%' in e: PROMO.append(0.75)
        elif 'oferta' in e.lower():
            try:
                g = e.split()[1].split('$')[1]
                if len(g) > 3:
                    PROMO.append(int(g[:-2]))
                else:
                    PROMO.append(int(g))
            except:
                PROMO.append(1)
        else:
            PROMO.append(1)

    TAMAÑO = []
    for tamaño in MARCA:   
        if '1.5' in tamaño: TAMAÑO.append('1500')
        elif '2.25' in tamaño: TAMAÑO.append('2250')
        elif '1.75' in tamaño: TAMAÑO.append('1750')
        elif '1.25' in tamaño: TAMAÑO.append('1250')
        elif '1,5' in tamaño: TAMAÑO.append('1500')
        elif '750' in tamaño: TAMAÑO.append('750')
        elif '2,25' in tamaño: TAMAÑO.append('2250')
        elif '2.5' in tamaño: TAMAÑO.append('2500')
        elif '1,75' in tamaño: TAMAÑO.append('1750')
        elif '269' in tamaño: TAMAÑO.append('269')
        elif '354' in tamaño: TAMAÑO.append('354')
        elif '730' in tamaño: TAMAÑO.append('730')
        elif '473' in tamaño: TAMAÑO.append('473')
        elif '354' in tamaño: TAMAÑO.append('354')
        elif 'hoppy lager' in tamaño:
            if '10' in tamaño: TAMAÑO.append('269')
            else: TAMAÑO.append('other')
        elif '500' in tamaño: TAMAÑO.append('500')
        elif '250' in tamaño: TAMAÑO.append('250')
        elif '330' in tamaño: TAMAÑO.append('330')
        elif '710' in tamaño: TAMAÑO.append('710')
        elif '730' in tamaño: TAMAÑO.append('730')
        elif '500' in tamaño: TAMAÑO.append('500')
        elif '2' in tamaño: TAMAÑO.append('2000')
        elif '1' in tamaño: TAMAÑO.append('1000')
        elif '6.3' in tamaño: TAMAÑO.append('6.3')
        elif '6,3' in tamaño: TAMAÑO.append('6.3')
        else: TAMAÑO.append('other')


    df = pd.DataFrame()
    df['marca'] = nombre
    df['subtipo'] = subtipo
    df['tamaño'] = TAMAÑO
    df['precio'] = PRECIO
    df['promo'] = PROMO
    df['precio_final'] = 0
    for i in range(df.shape[0]):
        if df.loc[i, 'promo'] > 5:
            df.loc[i, 'precio_final'] = df.loc[i, 'promo']
        else:
            df.loc[i, 'precio_final'] = round(float(df.loc[i, 'precio']) * df.loc[i, 'promo'])
    df['pack'] = PACK
    df['precio_final'] = round(df.precio_final / df.pack,2)

    df.to_csv('scrappeado/vea_resultados.csv')

    elapsed = timeit.default_timer() - start_time
    print('Tiempo de ejecucion disco: ' + str(round((elapsed/60),2)) + ' Minutos')