from modificaciones import crear_dic
import pandas as pd
import time
from selenium import webdriver
import timeit
from selenium.webdriver.common.keys import Keys
import warnings
warnings.filterwarnings('ignore')

def scrapper_disco():

    print('/-------------------------------------------------------/')
    print('Comenzamos a scrappear DISCO..')

    start_time = timeit.default_timer()

    dic_marcas, LISTA_PRODUCTOS = crear_dic('disco')

    # Tomamos el path donde tenemos guardado el chromedriver
    path = 'C:/Users/Usuario/chromedriver'
    driver = webdriver.Chrome(path)

    # Entramos a la pagina de Disco
    driver.get('https://www.disco.com.ar/')
    time.sleep(8)

    # Si nos figura el cartelito de suscripcion, lo cancelamos.
    try:
        driver.find_element_by_xpath('//*[@id="onesignal-slidedown-cancel-button"]').click()
    except:
        pass
    time.sleep(3)

 # Achicamos la pantalla
    driver.set_window_size(600, 800)
    time.sleep(3)
    # ----------- Cambiamos a ubicacion Palermo ----------------- # 
    driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[3]/div[1]/div/div/div[2]/section/div/div[2]/div/div/div[2]/a/span').click()
    time.sleep(3)
    driver.find_element_by_xpath('/html/body/div[12]/div[1]/div/div[2]/div[1]/a[2]/div[2]/p').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="provincia"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="provincia"]/option[2]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="tienda"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="tienda"]/option[2]').click()
    time.sleep(4)
    driver.find_element_by_xpath('/html/body/div[12]/div[1]/div/div[2]/div[1]/header/form/button').click()
    time.sleep(5)

    # "No queremos suscribirnos"
 # "No queremos suscribirnos"
    try:
        driver.find_element_by_xpath('//*[@id="onesignal-slidedown-cancel-button"]').click()
    except:
        pass

    # --------------------- Buscamos la lupita y pasamos lista de productos ------------------ # 
    time.sleep(5)
    try:
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[3]/div[1]/div/div/div[1]/section/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div/p').click()
        time.sleep(2)                 
    except:
        pass
    try:
        driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[3]/div[1]/div/div/div[1]/section/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div/p').click()
        time.sleep(2)
    except:
        pass
    time.sleep(3)
    try:
        driver.find_element_by_xpath('/html/body/div[10]/div/div[2]/div/div/div[3]/div/div/div/div/div[2]/div/div[1]/div/div').click()
    except:
        pass
    try:
        driver.find_element_by_xpath('/html/body/div[8]/div/div[2]/div/div/div[3]/div/div/div/div/div[2]/div/div[1]/div/div/p').click()
    except:
        pass

    time.sleep(5)                
    buscador = driver.find_element_by_xpath('/html/body/div[14]/div/div[2]/section/div/article/div/input')

    # Loopeamos por la lista de productos para ir mandando de a uno
    for productos in LISTA_PRODUCTOS:
        buscador.send_keys(productos)
        buscador.send_keys(Keys.ENTER)
        time.sleep(2)

    # Buscamos los productos
    try:                                   
        driver.find_element_by_class_name('searchByList__btn-search searchByList__btn-search--active').click()
    except:
        pass

    try:                                   
        driver.find_element_by_xpath('/html/body/div[15]/div/div[2]/section/div/div[2]/a').click()
    except:
        driver.find_element_by_xpath('/html/body/div[14]/div/div[2]/section/div/div[2]/a').click()

    time.sleep(3)
    # Volvemos a poner la pantalla asi aparecen la mayor cantidad de productos sin scrollear
    driver.set_window_size(1050, 660)
    # ------------------------------------------------------------ # 

    # --------------------------------------------------------- #
    time.sleep(3)
    # Refresheamos por las dudas
    driver.refresh()
    time.sleep(5)

    # Loopeamos devuelta por resultado de cada productos y traemos todos los que nos aparecen
    PRODUCTOS=[]
    for numero in range(1, len(LISTA_PRODUCTOS)+1):
        time.sleep(1)
        try:                               
            driver.find_element_by_xpath(f'/html/body/div[2]/div/div[1]/div/div[8]/div/div/section/div/a[{numero}]').click()
        except:
            pass
        try:
            driver.find_element_by_xpath(f'/html/body/div[4]/div/div[1]/div/div[8]/div/div/section/div/a[{numero}]').click()
        except:
            pass
        time.sleep(1)   
        n_products = 1
        try:                                           
            products_n = driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[8]/div/div/section/section/div[2]/div/div[2]/section/div/div[1]/div/div/div/div/div[2]/div/div/div')
            n_products = int(products_n.text.split('\n')[0].split(' ')[0])
        except:
            pass
        try:                                           
            products_n = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[8]/div/div/section/section/div[2]/div/div[2]/section/div/div[1]/div/div/div/div/div[2]/div/div/div/span')
            n_products = int(products_n.text.split('\n')[0].split(' ')[0])
        except:
            pass

        print(f'Cantidad productos para {LISTA_PRODUCTOS[numero-1]}: {n_products}')
        driver.execute_script("window.scrollBy(0,1300)")
        time.sleep(2)

    # Si hay varios productos nos fijamos si tenemos que "mostrar mas"
        if n_products > 10:
            try:
                driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div/div[8]/div/div/section/section/div[2]/div/div[3]/section/div/div/div/div/div[2]/div/div[3]/div/div/div/div/div/button/div').click()
                print('Mostrando mas productos..')
                time.sleep(2)
            except:
                pass
            try:
                driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[8]/div/div/section/section/div[2]/div/div[3]/section/div/div/div/div/div[2]/div/div[3]/div/div/div/div/div/button/div').click()
                print('Mostrando mas productos..')
                time.sleep(2)
            except:
                pass


        time.sleep(1)
        try:
            body = driver.find_element_by_xpath('//*[@id="gallery-layout-container"]')
            t = body.text
        except:
            print('ERROR')
            continue

        text = t.split('\n')

        if len(text) < 1:
            continue

        # i = 0
        # n_productos = []
        # while 'comparar' not in text[i].lower():
        #     text.pop(0)


        # Limpiamos un poco los datos para separarlos por producto
        info_productos = []
        info1 = []
        for e in text:
            if 'stock' in e.lower():
                info1 = []
            elif e != 'Agregar':
                info1.append(e)
            else:
                info1.pop(0)
                info_productos.append(info1)
                info1 = []
        PRODUCTOS += info_productos
        print(f'Cantidad productos DESCARGADOS para {LISTA_PRODUCTOS[numero-1]}: {len(info_productos)}')
        time.sleep(1)

        driver.execute_script("window.scrollTo(0, 0);")


    driver.quit()


    MARCA, PRECIO, DESCUENTO = [], [], []

    for e in range(len(PRODUCTOS)):
        p = PRODUCTOS[e]
        MARCA.append(p[0])
        if  '$' in p[1]:
            PRECIO.append(p[1])
            DESCUENTO.append(1)
        elif '2do al 50' in p[1]: 
            DESCUENTO.append(0.75)
            PRECIO.append(p[3])
        elif '2do al 80' in p[1]: 
            DESCUENTO.append(0.6)
            PRECIO.append(p[3])
        elif '3x2' in p[1]: 
            DESCUENTO.append(2/3)
            PRECIO.append(p[3])
        elif '6x4' in p[1]: 
            DESCUENTO.append(2/3)
            PRECIO.append(p[3])
        elif '6x3' in p[1]: 
            DESCUENTO.append(0.5)
            PRECIO.append(p[3])
        elif '4x2' in p[1]: 
            DESCUENTO.append(0.5)
            PRECIO.append(p[3])
        elif '2x1' in p[1]: 
            DESCUENTO.append(0.5)
            PRECIO.append(p[3])
        elif '25%' in p[1]: 
            DESCUENTO.append(0.75)
            PRECIO.append(p[3])
        elif '20%' in p[1]: 
            DESCUENTO.append(0.8)
            PRECIO.append(p[3])
        elif '30%' in p[1]: 
            DESCUENTO.append(0.7)
            PRECIO.append(p[3])
        elif '40%' in p[1]: 
            DESCUENTO.append(0.6)
            PRECIO.append(p[3])
        else:
            PRECIO.append('0')
            DESCUENTO.append(1)


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

    PRECIO_FINAL = []
    for e in PRECIO:
        if '$' in e:
            P = e.split('$')[1]
            pre = P.split(',')[0]
            PRECIO_FINAL.append(pre.replace('.', ''))
        else:
            PRECIO_FINAL.append(0)

    # Guardamos el descuento si es que lo hay
    # DESCUENTO = []
    # for e in DESC:
    #     if '2do al 50' in e: DESCUENTO.append(0.75)
    #     elif '2do al 80' in e: DESCUENTO.append(0.6)
    #     elif '3x2' in e: DESCUENTO.append(2/3)
    #     elif '6x4' in e: DESCUENTO.append(2/3)
    #     elif '6x3' in e: DESCUENTO.append(0.5)
    #     elif '4x2' in e: DESCUENTO.append(0.5)
    #     elif '2x1' in e: DESCUENTO.append(0.5)
    #     elif '25%' in e: DESCUENTO.append(0.75)
    #     elif '20%' in e: DESCUENTO.append(0.8)
    #     elif '30%' in e: DESCUENTO.append(0.7)
    #     elif '40%' in e: DESCUENTO.append(0.6)
    #     else: DESCUENTO.append(1)


    # Buscamos si el producto es un pack
    PACK = []
    for e in MARCA:
        e = e.lower()
        if 'hoppy' in e:
            if 'pack' in e:
                PACK.append(10)
            elif '10' in e:
                PACK.append(10)
            else:
                PACK.append(1)
        elif 'corona' in e and ' 10' in e:
            PACK.append(10)
        elif 'pack' in e:
            PACK.append(6)
        elif '6' in e:
            if 'paso de los' in e:
                PACK.append(1)
            elif 'awafrut' in e:
                PACK.append(1)
            elif 'corona' in e:
                PACK.append(1)
            elif 'blasfemia' in e:
                PACK.append(1)
            elif 'glaciar' in e:
                PACK.append(1)
            elif 'nestlé' in e:
                PACK.append(1)
            else:
                PACK.append(6)
        else:
            PACK.append(1)

    # Guardamos el tamaño de cada producto
    TAMAÑO = []
    for e in MARCA:
        e = e.lower()
        if '1.5' in e: TAMAÑO.append('1500')
        elif '2.25' in e: TAMAÑO.append('2250')
        elif '2.5' in e: TAMAÑO.append('2500')
        elif '750' in e: TAMAÑO.append('750')
        elif '269' in e: TAMAÑO.append('269')
        elif '2,5' in e: TAMAÑO.append('2500')
        elif '1.25' in e: TAMAÑO.append('1250')
        elif '1,25' in e: TAMAÑO.append('1250')
        elif '250' in e: TAMAÑO.append('250')
        elif '730' in e: TAMAÑO.append('730')
        elif '1650' in e: TAMAÑO.append('1650')
        elif '473' in e: TAMAÑO.append('473')
        elif '710' in e: TAMAÑO.append('710')
        elif '330' in e: TAMAÑO.append('330')
        elif '1.25' in e: TAMAÑO.append('1250')
        elif '1.75' in e: TAMAÑO.append('1750')
        elif '1.65' in e: TAMAÑO.append('1650')
        elif '1,5' in e: TAMAÑO.append('1500')
        elif '2,25' in e: TAMAÑO.append('2250')
        elif '269' in e: TAMAÑO.append('269')
        elif '1,75' in e: TAMAÑO.append('1750')
        elif '354' in e: TAMAÑO.append('354')
        elif '500' in e: TAMAÑO.append('500')
        elif '2' in e: TAMAÑO.append('2000')
        elif '1' in e: TAMAÑO.append('1000')
        elif '6.3' in e: TAMAÑO.append('6.3')
        elif '6,3' in e: TAMAÑO.append('6.3')
        else: TAMAÑO.append('other')

    # Creamos el DF con los valores que tenemos hasta el momento
    df = pd.DataFrame()
    df['marca'] = nombre
    df['subtipo'] = subtipo
    df['tamaño'] = TAMAÑO
    df['precio'] = PRECIO_FINAL
    # df.precio = df.precio.apply(lambda x: float(x)/100 if float(x) > 5000 else x)
    df['promo'] = DESCUENTO
    df['precio_promo'] = df.precio.astype(float) * df.promo.astype(float)
    df['pack'] = PACK
    df['precio_final'] = round(df.precio_promo / df.pack,2)

    df.to_csv('scrappeado/disco_resultados.csv')

    elapsed = timeit.default_timer() - start_time
    print('Tiempo de ejecucion disco: ' + str(round((elapsed/60),2)) + ' Minutos')

