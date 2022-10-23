import requests                       # Importamos las paqueterias que usaremos 
import matplotlib.pyplot as plt
from PIL import Image
from urllib.request import urlopen
import json
import os
import errno

try:                          # Intentamos crear un archivo con el nombre pokedex
    os.mkdir('pokedex')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
name_pokemon = ""              # Creamos una variable donde se guardará el nombre del pokémon

while True :    # Ingresamos a un ciclo perpetuo
    while True:
        name_pokemon = input("Ingrese el nombre de algún pokémon\nO pulse enter para terminar el programa: ") # Le pedimos al usuario el nombre de un pokémon y la guardamos en una variable
        if name_pokemon == "" :  # Si el nombre del pokémon esta vacio terminamos el programa
            exit()
        url_inicial = f"https://pokeapi.co/api/v2/pokemon/{name_pokemon}"  # definimos una variable con el link de la pokeapi y el nombre del pokémon, todo esto en una cadena formateada

        try:                     # Usamos try para hacer una peticion get 
            respuesta = requests.get(url_inicial)
        except :   # Si llega a ocurrir algun error por falta de conexión le imprimimos lo siguiente y se termina el programa
            print("Ha ocurrido un error, intentalo más tarde")
            exit()
        
        if respuesta.status_code == 404 :  # Si el estatus code es de 404 imprimimos lo siguiente
            print("Ese pokemon no existe o no pudo ser encontrado! \nIntente mas tarde o ingrese otro valor")
            continue
        elif respuesta.status_code == 200 :  # Si todo esta bien rompemos el ciclo
            break
        else :   # Y si hay otro estatus distinto imprimimos lo sigueinte y termina el programa
            print("Ha ocurrido un error, intentelo más tarde")
            exit()
    try:  # Usamos try para intentar obtener todos los siguientes datos
        datos = respuesta.json()  # a la respuesta la hacemos un json y la guardamos en una variable
        name_pokemon = datos["name"]
        url_img = datos["sprites"]["front_default"]
        peso = datos["weight"]
        tamaño = datos["height"]
        movimientos = datos["moves"]
        habilidades = datos["abilities"]
        types = datos["types"]
        lista_movimientos = [] # Creamos las siguientes listas para que se almacenen cada una de las habilidades, movimientos y tipos
        lista_habilidades = [] 
        lista_tipos = []

    except :  # Si algo llegará a falla imprimiria lo siguiente y terminamos el programa
        print("Ha ocurrido algun error en los datos del pokemon :(")
        exit()  
    def calcular_movimientos(namePokemon, mov):
        """ Función para calcular todos los movimientos del pokémon, la cual pide como parametros el nombre del pokemon y los movimientos"""
        print(f"Movimientos de: {namePokemon}")
        for i in range(int(len(mov))) : # En este ciclo recorre la longitud de los movimientos, buscando el valor "move" y "name" y lo guardamos en la variable movimiento, para despues añadirlo a la lista previamente definida
            movimiento = mov[i]["move"]["name"] 
            lista_movimientos.append(movimiento)
            print(f"El movimiento {i + 1} es : {movimiento}") # Imprimimos todos los movimientos
    
    def calcular_habilidades(namePokemon, hab) :
        """Funcion para calcular todas las habilidades, recibe como parametros el nombre y las habilidades"""
        print(f"Habilidades de: {namePokemon} ")
        for i in range(int(len(hab))) :# En este ciclo recorre la longitud de las habilidades, buscando el valor "ability" y "name" y lo guardamos en la variable habilidad, para despues añadirlo a la lista previamente definida
            habilidad = habilidades[i]["ability"]["name"]
            lista_habilidades.append(habilidad)
            print(f"La habilidad {i + 1} es: {habilidad}") # Imprimimos todos los movimientos
    
    def calcular_tipos(tipos) :
        """Funcion para calcular los tipos, recibe como parametros los tipos"""
        print("Tipos:")
        for i in range(int(len(tipos))) : # En est ciclo al igual que en las anteriores recorre la longitud de los tipos, buscando "type" y "name", porteriormente lo guarda en una variable
            tipo = tipos[i]["type"]["name"]
            lista_tipos.append(tipo)  # Añade el valor de esa variable a una lista
            print(tipo) # Imprimimos los tipos


    # Creamos un sencillo menú de opciones
    option = input(""" OPCCIONES  
    1) Visualizar datos en pantalla y posteriormente guardarlos en un archivo json
    2) Terminar
    O pulse cualquier otra tecla para buscar algun otro pokémon
        :""")
    if option == "1" :
        # Mostramos en pantalla todos los datos del pokémon
        print(f"""{name_pokemon.capitalize()}
Pesa: {peso}
Mide: {tamaño}""")
        calcular_movimientos(name_pokemon, movimientos)
        calcular_habilidades(name_pokemon, habilidades)
        calcular_tipos(types)
        try :  # Intentamos abrir la imagen del pokemon si es que tiene
            img = Image.open(urlopen(url_img))
        except : # Si no tiene se imprime lo siguiente
            print("No se encontró la imagen del pokémon :(")
        plt.title(name_pokemon)
        imgplot = plt.imshow(img)
        plt.show()
        dic_datos = { # Se crea un diccionario para guardar los datos del pokémon
            "Nombre Pokemon" : name_pokemon,
            "Url_Imagen" : url_img,
            "Peso" : peso, 
            "Tamanio" : tamaño, 
            "Movimientos" : lista_movimientos,
            "Habilidades" : lista_habilidades, 
            "Tipos" : lista_tipos 
        }
        with open("pokedex/datos_pokemon.json", "a") as json1:  # Creamos en la carpeta previamente creada un archivo json usando la paqueteria json y abriendolo en modo append
            json.dump(dic_datos, json1) # y le pasamos como parametro el alias del archivo y el contenido, que en este caso seria el diccionario de datos
            json1.write("\n\n")
    elif option == "2" : # SI elije la opcionn 2 rompemos el ciclo perpetuo y se termina el programa
        break
    else :  # Y si ingresa otro valor continuamos con la ejecucion 
        continue