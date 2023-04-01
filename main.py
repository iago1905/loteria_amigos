import json
import datetime
import requests
from bs4 import BeautifulSoup


year = 2023



def sorteos(i):
    global fechas
    fechas = []
    today = datetime.date.today()  # Obtiene la fecha actual
    date = datetime.date(year, 1, 1)
    
    if (i == 0):
        #PRIMITIVA
        while date <= today:  # Verifica si la fecha actual ha sido alcanzadaS
            if date.weekday() == 0 or date.weekday() == 3 or date.weekday() == 5:
                fechas.append(date.strftime("%Y-%m-%d"))
            date += datetime.timedelta(days=1)
    else:
        #EUROMILLONES
        while date <= today:  # Verifica si la fecha actual ha sido alcanzada
            if date.weekday() == 1 or date.weekday() == 4:
                fechas.append(date.strftime("%Y-%m-%d"))
            date += datetime.timedelta(days=1)      

def premios(fechas,i):
    global dia, premio
    dia = []
    premio = []
    if (i == 0):
        #PRIMITIVA
        for i in fechas:
            response = requests.get(f"https://www.primitivacomprobar.es/primitiva-jueves.php?del-dia={i}&n1=4&n2=17&n3=23&n4=28&n5=37&n6=11&nr=7#comprobador")
            html_text = response.text

            soup = BeautifulSoup(html_text, "html.parser")

            span_tag = soup.find('span', {'class': 'text-premio'})

            if (span_tag != None):
                # print(f"Dia : {i} - " + span_tag.text)
                dia.append(i),premio.append(span_tag.text)
    else:
        #EUROMILLONES
        for i in fechas:
            response = requests.get(f"https://www.comprobareuromillones.com/euromillones-martes.php?del-dia={i}&n1=4&n2=17&n3=23&n4=28&n5=37&e1=7&e2=11&bt=comprobar#comprobador")
            html_text = response.text

            soup = BeautifulSoup(html_text, "html.parser")

            span_tag = soup.find('span', {'class': 'text-premio'})

            if (span_tag != None):
                # print(f"Dia : {i} - " + span_tag.text)
                dia.append(i),premio.append(span_tag.text)




def guardar(dia,premio,i):
    datos = []
    
    if i == 0:
        # Carga los datos existentes del archivo JSON si es que existe
        try:
            with open('resultado.json', 'r') as infile:
                resultado = json.load(infile)
        except FileNotFoundError:
            resultado = {}

        # Agrega los nuevos datos de la Primitiva
        for i in range(len(dia)):
            dato = {"fecha": dia[i], "premio": premio[i]}
            datos.append(dato)

        if "Primitiva" in resultado:
            resultado["Primitiva"] += datos
        else:
            resultado["Primitiva"] = datos

        # Guarda los datos actualizados en el archivo JSON
        with open('resultado.json', 'w') as outfile:
            json.dump(resultado, outfile, indent=4)

    elif i == 1:
        # Carga los datos existentes del archivo JSON si es que existe
        try:
            with open('resultado.json', 'r') as infile:
                resultado = json.load(infile)
        except FileNotFoundError:
            resultado = {}

        # Agrega los nuevos datos de Euromillones
        for i in range(len(dia)):
            dato = {"fecha": dia[i], "premio": premio[i]}
            datos.append(dato)

        if "Euromillon" in resultado:
            resultado["Euromillon"] += datos
        else:
            resultado["Euromillon"] = datos

        # Guarda los datos actualizados en el archivo JSON
        with open('resultado.json', 'w') as outfile:
            json.dump(resultado, outfile, indent=4)


if __name__ == "__main__":
    #PRIMITIVA
    sorteos(0)
    premios(fechas,0)
    guardar(dia,premio,0)


    #EUROMILLONES
    sorteos(1)
    premios(fechas,1)
    guardar(dia,premio,1)
    