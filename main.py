from scrappeado.disco import scrapper_disco
from modificaciones import *
from scrappeado.coto import scrapper_coto
from scrappeado.walmart import scrapper_walmart
from datetime import datetime, timedelta
from scrappeado.vea import scrapper_vea
import pandas as pd

scrapper_coto()

scrapper_disco()

# scrapper_vea()

scrapper_walmart()



# Creamos la tabla de modificaciones
supermercados = ['coto', 'disco', 'vea', 'walmart']

concatenar_precios()

# for super in supermercados:
#      crear_modificaciones(super)


# concatenar_modificaciones()

