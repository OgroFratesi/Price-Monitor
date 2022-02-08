import pandas as pd
from tqdm import tqdm 
import time
from selenium import webdriver
import timeit

def scrapper_walmart():

    print('/-------------------------------------------------------/')
    print('Comenzamos a scrappear WALMART..')

    start_time = timeit.default_timer()

    path = 'C:/Users/Usuario/chromedriver'

    driver = webdriver.Chrome(path)


    PRODUCTOS = ['Eco de los Andes', 'Glaciar', 'agua Nestle', 'Awafrut',
            'cerveza Andes', 'Brahma', 'Budweiser', 'cerveza Corona', 'cerveza Patagonia',
        'Quilmes', 'Stella Artois', '7up', 'h2o', 'Paso De Los Toros',
        'Pepsi', 'redbull', 'gatorade', 'mirinda',
            'novecento', 'salentein', 'portillo', 'blasfemia', 'callia', 'robino', 'capriccio']


    SUCURSAL = ['15', '17']

    ITEMS = []

    for num in SUCURSAL:
        
        driver.get('https://www.walmart.com.ar/buscar?text=pepsi&sc={}'.format(num)) 
        
        for producto in PRODUCTOS:
    
        
            
            time.sleep(4)
            buscador = driver.find_element_by_xpath('//*[@id="header-root"]/div/div/div[1]/div/div/div[1]/div/div[1]/div/input')
            # Borramos lo que ya esta escrito
            buscador.clear()
            # Escribimos el nuevo producto
            buscador.send_keys(producto)
            time.sleep(7)

            try:
                # Si el producto existe, lo seleccionamos para buscarlo.
                driver.find_element_by_xpath('//*[@id="header-root"]/div/div/div[1]/div/div/div[1]/div/div[3]/div/div[2]/div[2]/a').click()
                time.sleep(4)
                
                s = driver.find_element_by_class_name('search-results')
                ARTICULOS = s.text
                ARTICULOS = ARTICULOS.split('AGREGAR')

                texto_limpio=[]
                for e in range(len(ARTICULOS)):
                    limpio = ARTICULOS[e].split('\n')
                    limpio = [string for string in limpio if string != '']
                    texto_limpio.append(limpio)

                # Borramos de la lista lo que no son articulos
                texto_limpio = texto_limpio[0][9:]
    #             texto_limpio = texto_limpio[9:]

                # Separamos la info de cada articulo en una lista
                info_articulo=[]
                info_final=[]
                for e in texto_limpio:
                    if e != 'Agregar':
                        info_articulo.append(e)
                    else:
                        info_final.append(info_articulo)
                        info_articulo = []
                # Agregamos la info de todos los articulos a la lista de items
                for e in info_final:
                    ITEMS.append(e)
            except:
                print(f'ERROR:{producto}')
                pass
            
    driver.quit()

    DESCUENTO = []
    for e in ITEMS:
        des = []
        for i in e:
            if '3x2' in i:
                des = 2/3
                break
            elif '2da al 60%' in i:
                des = 0.7
                break
            elif '2da al 50%' in i:
                des = 0.75
                break
            elif '2x1' in i:
                des = 0.5
                break
            elif '4x3' in i:
                des = 0.75
                break
            else:
                des = 1
        DESCUENTO.append(des)
        
    PRECIO = []
    NOMBRE = []
    for e in ITEMS:
        NOMBRE.append(e[-1])
        pre_precio = []
        for i in e:
            if '$' in i and 'x' not in i:
                if '.' in i:
                    pre_precio.append(float(i.split('$')[1].replace('.','').replace(',', '.')))
                else:
                    pre_precio.append(float(i.split('$')[1].replace(',', '.')))
        PRECIO.append(min(pre_precio))
        
    TAMAÑO = []
    for e in NOMBRE:   
        if '1.5' in e: TAMAÑO.append('1500')
        elif '2.25' in e:TAMAÑO.append('2250')
        elif '2.5' in e:TAMAÑO.append('2500')
        elif '220' in e:TAMAÑO.append('220')
        elif '1.75' in e:TAMAÑO.append('1750')
        elif '1,5' in e:TAMAÑO.append('1500')
        elif '2,25' in e:TAMAÑO.append('2250')
        elif '1,75' in e:TAMAÑO.append('1750')
        elif '1.75' in e:TAMAÑO.append('1750')
        elif '269' in e:TAMAÑO.append('269')
        elif '250' in e:TAMAÑO.append('250')
        elif '750' in e:TAMAÑO.append('750')
        elif '354' in e:TAMAÑO.append('354')
        elif '473' in e:TAMAÑO.append('473')
        elif '710' in e:TAMAÑO.append('710')
        elif '730' in e:TAMAÑO.append('730')
        elif '330' in e:TAMAÑO.append('330')
        elif '1,25' in e:TAMAÑO.append('1250')
        elif '1.25' in e:TAMAÑO.append('1250')
        elif '354' in e:TAMAÑO.append('354')
        elif '500' in e:TAMAÑO.append('500')
        elif '2' in e:TAMAÑO.append('2000')
        elif '1' in e:TAMAÑO.append('1000')
        elif '6.3' in e:TAMAÑO.append('6.3')
        elif '6,3' in e:TAMAÑO.append('6.3')
        elif '3' in e:TAMAÑO.append('3000')
        else:TAMAÑO.append('other')
            
        
    PACK = []
    for e in NOMBRE:
        e = e.lower()
        if 'six' in e:
            PACK.append(6)
        elif 'pack' in e:
            if '10' in e and 'corona' in e:
                PACK.append(10)
            elif '10' in e and 'patag' in e:
                PACK.append(10)
            elif '6' in e:
                PACK.append(6)
            else:
                PACK.append(1)
        elif 'hoppy lager' in e:
            if '269' in e:
                PACK.append(1)
            else:
                PACK.append(1)
        elif '6' in e:
            if 'agua' in e:
                PACK.append(1)
            elif 'corona' in e:
                PACK.append(1)
            elif 'paso de' in e:
                PACK.append(1)
            else:
                PACK.append(6)
        else:
            PACK.append(1)
        
        
    marca = []
    subtipo = []

    for e in NOMBRE:
        e = e.lower()
        if 'novecento' in e:
            marca.append('Novecento')
            if 'raices' in e:
                if 'malbec' in e:
                    subtipo.append('Raices Malbec')
                elif 'sauvignon' in e:
                    subtipo.append('Raices Cabernet Sauvignon')
                elif 'chardonnay' in e:
                    subtipo.append('Raices Chardonnay')
                elif 'chardonay' in e:
                    subtipo.append('Raices Chardonnay')
                else:
                    subtipo.append('Other')
            elif 'malbec' in e:
                subtipo.append('Tinto Malbec')
            elif 'sauvignon' in e:
                subtipo.append('Tinto Cabernet Sauvignon')
            elif 'chardonnay' in e:
                subtipo.append('Blanco Chardonnay')
            elif 'brut' in e:
                subtipo.append('Espumante Extra Brut')
            elif 'extra dulce' in e:
                subtipo.append('Espumante Extra Dulce')
            else:
                subtipo.append('Other')
        elif 'capriccio' in e:
            marca.append('Capriccio Dolceza')
            if 'blanco' in e:
                subtipo.append('Blanco')
            elif 'dulce' in e:
                subtipo.append('Blanco')
            else:
                subtipo.append('other')
        elif 'blasfemia' in e:
            marca.append('Blasfemia')
            if 'chenin' in e:
                subtipo.append('Blanco Chenin')
            elif 'rosado' in e:
                subtipo.append('Rosado')
            elif 'tinto' in e:
                subtipo.append('Tinto')
            else:
                subtipo.append('Other')
        elif 'callia' in e:
            marca.append('Callia')
            if 'alta' in e:
                if 'malbec' in e:
                    if 'syrah' in e:
                        subtipo.append('other')
                    else:
                        subtipo.append('Alta Malbec')
                elif 'sauvignon' in e:
                    subtipo.append('Alta Cabernet Sauvignon')
                elif 'chardon' in e:
                    subtipo.append('Alta Chardonnay')
                else:
                    subtipo.append('Other')
            else:
                subtipo.append('other')
        elif 'portillo' in e:
            marca.append('Portillo')
            if 'malbec' in e:
                if 'rosado' in e:
                    subtipo.append('other')
                else:
                    subtipo.append('Tinto Malbec')
            elif 'sauvignon' in e:
                if 'blan' in e:
                    subtipo.append('Blanco')
                else:
                    subtipo.append('Tinto Cabernet Sauvignon')
            elif 'chardonnay' in e:
                subtipo.append('Blanco Chardonnay')
            else:
                subtipo.append('Other')
        elif 'salentein' in e:
            marca.append('Salentein')
            if 'e/b' in e:
                subtipo.append('Espumante Extra Brut')
            elif 'chardon reserve' in e:
                subtipo.append('Chardonnay Reserva')
            else:
                subtipo.append('other')
        elif 'robino' in e:
            marca.append('Dante Robino')
            if 'malbec' in e:
                subtipo.append('Malbec')
            elif 'sauvignon' in e:
                subtipo.append('Cabernet Sauvignon')
            elif 'chardonnay' in e:
                subtipo.append('Chardonnay')
            elif 'chardonay' in e:
                subtipo.append('Chardonnay')
            else:
                subtipo.append('other')
        elif 'con gas' in e:
            subtipo.append('Con Gas')
            if 'andes' in e:
                marca.append('Eco de los Andes')
            else:
                marca.append('Other')
        elif 'sin gas' in e:
            subtipo.append('Sin Gas')
            if 'nestle' in e:
                marca.append('Nestle')
            elif 'glaciar' in e:
                marca.append('Glaciar')
            elif 'andes' in e:
                marca.append('Eco de los Andes')
            else:
                marca.append('Other')
        elif 'awafrut' in e:
            marca.append('Awafrut')
            if 'manzana' in e:
                subtipo.append('Manzana')
            elif 'durazno' in e:
                subtipo.append('Durazno')
            elif 'Pomelo' in e:
                subtipo.append('Pomelo')
            else:
                subtipo.append('Other')
        elif 'glaciar' in e:
            marca.append('Glaciar')
            if 'limonada' in e:
                subtipo.append('Limonada')
            elif 'manzana' in e:
                subtipo.append('Manzana')
            else:
                subtipo.append('Sin Gas')
        elif 'nestle' in e:
                marca.append('Nestle')
                subtipo.append('Sin Gas')
        elif 'h2' in e:
            marca.append('h2o')
            if 'limoneto' in e:
                subtipo.append('Limoneto')
            elif 'citrus' in e:
                subtipo.append('Citrus')
            else:
                subtipo.append('Other')
        elif 'seven up' in e:
            marca.append('7up')
            if 'sin azucar' in e:
                subtipo.append('Sin Azúcar')
            else:
                subtipo.append('Normal')
        elif '7up' in e:
            marca.append('7up')
            if 'sin azucar' in e:
                subtipo.append('Sin Azúcar')
            else:
                subtipo.append('Normal')
        elif 'paso de los toros' in e:
            marca.append('Paso De Los Toros')
            if 'pomelo' in e:
                if 'light' in e:
                    subtipo.append('Light')
                else:
                    subtipo.append('Pomelo')
            else:
                subtipo.append('Tónica')
        elif 'pepsi' in e:
            marca.append('Pepsi')
            if 'black' in e:
                subtipo.append('Black')
            elif 'light' in e:
                subtipo.append('Light')
            else:
                subtipo.append('Pet')
        elif 'h2oh!' in e:
            marca.append('H2OH!')
            subtipo.append('H2OH!')
        elif 'stella artois' in e:
            marca.append('Stella Artois')
            subtipo.append('')
        elif 'andes' in e:
            marca.append('Andes')
            if 'ipa' in e:
                subtipo.append('Ipa')
            elif 'rubia' in e:
                subtipo.append('Rubia')
            elif 'negra' in e:
                subtipo.append('Negra')
            elif 'roja' in e:
                subtipo.append('Roja')
            else:
                subtipo.append('Other')
        elif 'brahma' in e:
            marca.append('Brahma')
            subtipo.append('Clásica')
        elif 'corona' in e:
            marca.append('Corona')
            subtipo.append('')
        elif 'patagonia' in e:
            marca.append('Patagonia')
            if 'bohemian' in e:
                subtipo.append('Bohemian Pilsener')
            elif 'amber' in e:
                subtipo.append('Amber Lager')
            elif 'hoppy' in e:
                subtipo.append('Hoppy Lager')
            elif '24 7' in e:
                subtipo.append('24.7')
            elif 'weisse' in e:
                subtipo.append('Weisse')
            else:
                subtipo.append('Other')
        elif 'budweiser' in e:
            marca.append('Budweiser')
            subtipo.append('')
        elif 'quilmes' in e:
            marca.append('Quilmes')
            if 'clasica' in e:
                subtipo.append('Clásica')
            elif '1890' in e:
                subtipo.append('1890')
            elif 'stout' in e:
                subtipo.append('Stout')
            elif 'red' in e:
                subtipo.append('Red Lager')
            elif 'bock' in e:
                subtipo.append('Bock')
            else:
                subtipo.append('Other')
        elif 'heineken' in e:
            marca.append('Heineken')
            subtipo.append('')
        elif 'imperial' in e:
            marca.append('Imperial')
            if 'rubie' in e:
                subtipo.append('Rubia')
            elif 'rubia' in e:
                subtipo.append('Rubia')
            else:
                subtipo.append('Other')
        elif 'schneider' in e:
                marca.append('Schneider')
                subtipo.append('')
        elif 'gatorade' in e:
            marca.append('Gatorade')
            if 'manzana' in e:
                subtipo.append('Manzana')
            elif 'naranja' in e:
                subtipo.append('Naranja')
            elif 'cool' in e:
                subtipo.append('Cool Blue')
            elif 'frutas' in e:
                subtipo.append('Frutas Tropi')
            else:
                subtipo.append('Normal')
        elif 'red bull' in e:
            marca.append('Red Bull')
            if 'sugar free' in e:
                subtipo.append('Sin Azucar')
            else:
                subtipo.append('Normal')
        else:
            marca.append('other')
            subtipo.append('other')
    



    df = pd.DataFrame(marca, columns=['marca'])
    df['subtipo'] = subtipo
    df['tamaño'] = TAMAÑO
    df['precio'] = PRECIO
    df['pack'] = PACK
    df['descuento'] = DESCUENTO
    df.descuento = df.descuento.apply(lambda x: round(x,2))
    df['precio_final'] = round((df.precio * df.descuento)/df.pack,1)

    df.to_csv('scrappeado/walmart_resultados.csv')

    
    elapsed = timeit.default_timer() - start_time
    print('Tiempo de ejecucion Walmart: ' + str(round((elapsed/60),2)) + ' Minutos')