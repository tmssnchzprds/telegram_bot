###################################################
### FUNCIONES #####################################
###################################################

def opera(consulta):
    respuesta = ""
    data = container.calc_intent(consulta) # preguntamos por el intent identificado
    #en data.name está el nombre del intent identificado
    #en data.conf está la confianza o seguridad de haber acertado
    #en data.matches están los entities encontrados
    respuesta = "Lo siento no te entiendo. Pídemelo de otro modo"
    if data.conf > 0.5: # si estás seguro al 50% o más
        if data.name == "pedir.autor": # aquí se pone el nombre del intent
            respuesta = infoAutor()
        elif data.name == "pedir.aleatorio":
            respuesta = pedirAleatorio(data)
        elif data.name == "llamar":
            respuesta = llamar(data)
        elif data.name == "establecer.temperatura":
            respuesta = cambiarTemperatura(data)
        elif data.name == "pedir.ruta":
            respuesta = obtenerRuta(data)
        elif data.name == "mostrar.mapa":
            respuesta = obtenerMapa(data)
    else:
        respuesta = openai.ChatCompletion.create(model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": consulta}
        ]).choices[0].message.content
    return respuesta

### FUNCION PARA DEVOLVER UN NUMERO ALEATORIO ###
'''
Matches: 
    from (para establecer el número aleatorio mínimo a generar)
    to   (para establecer el número aleatorio máximo a generar)
'''
def pedirAleatorio(data):
    desde = 0
    hasta = 100
    if data.matches.__contains__('from'):
        desde = int(data.matches["from"])
    if data.matches.__contains__('to'):
        hasta = int(data.matches["to"])
    aleatorio = random.randint(desde,hasta)
    return ("Un aleatorio desde " + str(desde) + " hasta " + str(hasta) + " podría ser el " + str(aleatorio))

def llamar(data):
    respuesta = "llamando"
    if data.matches.__contains__('phone'):
        respuesta += " al " + data.matches["phone"]
    return respuesta

### FUNCION PARA SUBIR O BAJAR LA TEMPERATURA ###
'''
Matches: 
    accion_subir*   (para indicar si queremos subir la temperatura)
    accion_bajar*   (para indicar si queremos bajar la temperatura)
    grados         (para establecer los grados a subir o bajar)
'''
def cambiarTemperatura(data):
    respuesta = 'De acuerdo. '
    if data.matches.__contains__('accion_subir'):
        respuesta += 'Subiendo la temperatura '
    if data.matches.__contains__('accion_bajar'):
        respuesta += 'Bajando la temperatura '
    if data.matches.__contains__('grados'):
        respuesta += data.matches['grados'] + ' ºC'
    return respuesta

### FUNCION PARA PEDIR LA RUTA GPS ###
'''
Matches: 
    origen     (para indicar el inicio de la ruta)
    destino**  (para indicar el final de la ruta)
'''
def obtenerRuta(data):
    origen = ''
    destino = ''
    respuesta = 'Esta es la ruta para ir'
    if data.matches.__contains__('origen'):
        origen = data.matches['origen'].replace(' ', '%20')
        respuesta += ' desde ' + origen
    if data.matches.__contains__('destino'):
        destino = data.matches['destino'].replace(' ', '%20')
        respuesta += ' hasta ' + destino
    respuesta += ':\n'
    respuesta += 'https://www.google.com/maps/dir/?api=1&origin='+origen+'&destination='+destino
    return respuesta

### FUNCION PARA MOSTRAR EL MAPA ###
'''
Matches: 
    ciudad**   (para indicar la ciudad)
    provincia  (para indicar la provincia)
'''
def obtenerMapa(data):
    respuesta = 'Esta es la ubicación:\n'
    if data.matches.__contains__('ciudad'):
        respuesta += 'https://www.google.com/maps/place/'+data.matches['ciudad'].replace(' ', '%20')
        if data.matches.__contains__('provincia'):
            respuesta +=  ',+'+data.matches['provincia'].replace(' ', '%20')
    return respuesta

def infoAutor():
    respuestas = ['Mi autor es Daniel Gallego... o no...',
                   'Podría decirse que me he creado a mi mismo',
                     'Si te lo dijera tendría que matarte...',
                       'Dice la leyenda que me crearon en el CPR de Cáceres']
    aleatorio = random.randint(0, len(respuestas)-1)
    return respuestas[aleatorio]
