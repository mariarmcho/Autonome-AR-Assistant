import cv2
import numpy as np

class Arauco():
    '''
    ESta clase tiene la funcionalidad relacionada con la deteccion de los marcadores de aruco y además
    el diseño y dibujo de las instrucciones en realidad aumentada sobre las imagenes de la camara.
    He dispuesto la información de las lavadoras en esta clase ya que me suponía un ahorro de tiempo en cuanto
    a la utilización de la base de datos que se lo he podido dar a otras funcionalidades más importantes para esta asignatura.
    '''
    def __init__(self, app, conexion, **kwargs):
        super().__init__(**kwargs)
        self.conexion = conexion        # Conexion a la base de datos
        self.app = app         # Inicializacion de la aplicación
        self.id_marcador = -1       # Inicialización de los ids de los marcadores
        self.TAM = 0.026        # Tamaño del marcador

        self.diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)     # Diccionario que contiene los patrones de los marcadores
        self.detector = cv2.aruco.ArucoDetector(self.diccionario)       # Inicializacion del detector de los marcadores del diccionario

        # Aquí está toda la informacion relevante de las lavadoras, los pasos y lo que tendria que dibujar con el tamaño adecuado
        self.INSTRUCCIONES = {
            1: [    #Lavadora 1
                {
                    "info": "Ajusta la rueda a la versión ECO",
                    "acciones": [
                        {
                            "tipo": "circulo",
                            "offset": (0.12, 0.048),
                            "radio": 0.1,
                            "color": (200, 0, 0)
                        }
                    ]
                },
                {   # paso2
                    "info": "Introducimos el detergente en la ranura de la izquierda y el suavizante a la derecha",
                    "acciones": [
                        {
                            "tipo": "flecha",
                            "inicio": (0,0.08),
                            "fin": (0, 0.05),
                            "color": (0, 250, 0),
                            "grosor": 3
                        }
                    ]
                },
                {  # paso 3
                    "info": "Pulsamos el botón de inicio",
                    "acciones": [
                        {
                            "tipo": "circulo",
                            "offset": (0.205, 0.038),
                            "radio": 0.1,
                            "color": (0, 0, 255)
                        }
                    ]
                },
                {  # paso 4
                    "info": "Instrucciones completadas",
                }
            ],
            0: [    #Lavadora 2
                {  # paso 1
                    "info": "Ajustamos la rueda a la versión ECO",
                    "acciones": [
                        {
                            "tipo": "circulo",
                            "offset": (-0.102, 0.055),
                            "radio": 0.1,
                            "color": (255, 0, 0)
                        }
                    ]
                },
                {  # paso 2
                    "info": "Introducimos el detergente en la ranura de la izquierda y el suavizante a la derecha",
                    "acciones": [
                        {
                            "tipo": "flecha",
                            "inicio": (-0.212,0.067),
                            "fin": (-0.212, 0.097),
                            "color": (0, 250, 0),
                            "grosor": 3
                        }
                    ]
                },
                {  # paso 3
                    "info": "Pulsamos el botón de inicio",
                    "acciones": [
                        {
                            "tipo": "circulo",
                            "offset": (0, 0.047),
                            "radio": 0.1,
                            "color": (0, 0, 255)
                        }
                    ]
                },
                {  # paso 4
                    "info": "Instrucciones completadas",
                }
            ],
            2: [  # Lavadora 3
                {  # paso 1
                    "info": "Ajustamos la rueda a la versión ECO",
                    "acciones": [
                        {
                            "tipo": "circulo",
                            "offset": (-0.056, -0.014),
                            "radio": 0.1,
                            "color": (255, 0, 0)
                        }
                    ]
                },
                {  # paso 2
                    "info": "Introducimos el detergente en la ranura de la izquierda y el suavizante a la derecha",
                    "acciones": [
                        {
                            "tipo": "flecha",
                            "inicio": (-0.24, -0.09),
                            "fin": (-0.24, -0.06),
                            "color": (0, 250, 0),
                            "grosor": 3
                        }
                    ]
                },
                {  # paso  3
                    "info": "Pulsamos el botón de temperatura a la deseada",
                    "acciones": [
                        {
                            "tipo": "circulo",
                            "offset": (-0.16, -0.053),
                            "radio": 0.1,
                            "color": (0, 0, 255)
                        }
                    ]
                },
                {  # paso 4
                    "info": "Pulsamos el botón de inicio",
                    "acciones": [
                        {
                            "tipo": "circulo",
                            "offset": (-0.037, -0.005),
                            "radio": 0.1,
                            "color": (255, 255, 0)
                        }
                    ]
                },
                {  # paso 5
                    "info": "Instrucciones completadas",
                }
            ],
            3: [  # Lavadora 4
                {  # paso 1
                    "info": "Ajustamos la rueda a la versión ECO",
                    "acciones": [
                        {
                            "tipo": "circulo",
                            "offset": (0.003, 0.03),
                            "radio": 0.1,
                            "color": (255, 0, 0)
                        }
                    ]
                },
                {  # paso 2
                    "info": "Introducimos el detergente en la ranura de la izquierda y el suavizante a la derecha",
                    "acciones": [
                        {
                            "tipo": "flecha",
                            "inicio": (-0.255, -0.02),
                            "fin": (-0.255, 0.01),
                            "color": (0, 250, 0),
                            "grosor": 3
                        }
                    ]
                },
                {  # paso 3
                    "info": "Pulsamos el botón de temperatura a la deseada",
                    "acciones": [
                        {
                            "tipo": "circulo",
                            "offset": (-0.155, 0.035),
                            "radio": 0.1,
                            "color": (0, 0, 255)
                        }
                    ]
                },
                {  # paso 4
                    "info": "Pulsamos el botón de inicio",
                    "acciones": [
                        {
                            "tipo": "circulo",
                            "offset": (-0.097, 0.035),
                            "radio": 0.1,
                            "color": (255, 255, 0)
                        }
                    ]
                },
                {  # paso 5
                    "info": "Instrucciones completadas",
                }
            ],
            4: [  # Lavadora 5
                {  # paso 1
                    "info": "Ajustamos la rueda a la versión ECO",
                    "acciones": [
                        {
                            "tipo": "circulo",
                            "offset": (0.048, 0.062),
                            "radio": 0.1,
                            "color": (255, 0, 0)
                        }
                    ]
                },
                {  # paso 2
                    "info": "Pulsamos el botón de temperatura a la deseada",
                    "acciones": [
                        {
                            "tipo": "circulo",
                            "offset": (-0.092, 0.047),
                            "radio": 0.1,
                            "color": (0, 255, 0)
                        }
                    ]
                },
                {  # paso 3
                    "info": "Introducimos el detergente en la ranura de la izquierda y el suavizante a la derecha",
                    "acciones": [
                        {
                            "tipo": "flecha",
                            "inicio": (-0.15, 0),
                            "fin": (-0.12, 0),
                            "color": (0, 0, 255),
                            "grosor": 3
                        }
                    ]
                },
                {  # paso 4
                    "info": "Ajustamos el tiempo deseado pulsando el botón",
                    "acciones": [
                        {
                            "tipo": "circulo",
                            "offset": (-0.04, 0.047),
                            "radio": 0.1,
                            "color": (255, 0, 255)
                        }
                    ]
                },
                {  # paso 5
                    "info": "Pulsamos el botón de inicio",
                    "acciones": [
                        {
                            "tipo": "circulo",
                            "offset": (0.018, 0.047),
                            "radio": 0.1,
                            "color": (0, 255, 255)
                        }
                    ]
                },
                {  # paso 6
                    "info": "Instrucciones completadas",
                }
            ]
        }

        self.paso_actual = {}   # Guarda el paso actual por id de marcador
        self.ultimas_poses = {}  # Guarda la última posición de la realidad aumentada en dibujo en ese momento

        # Iniciamos todo lo relativo a la camara
        try:
            import camara
            self.cameraMatrix = camara.cameraMatrix     # se guarda la matriz de calibracion de la camara del modulo camara ( se usa para traformar los puntos 3d en coordenadas 2d)
            self.distCoeffs = camara.distCoeffs     # Se guarda el vector de coeficientes de distorsion, los que corrigen las deformaciones optimas que puedan surgir por la camara
        except ImportError:     # si no se puede tomar las cosas del modulo de la camara por algun error se usan estos parametros por defecto
            h, w = 480, 640
            self.cameraMatrix = np.array([[1000, 0, w / 2],
                                          [0, 1000, h / 2],
                                          [0, 0, 1]])
            self.distCoeffs = np.zeros((5, 1))

# ----------------------------------------------------------------------------------------------------------------------#

    def procesar_frame(self, frame):
        '''
        Este metodo detecta llos marcadores aruco en el frme actual, calcula la posicion y la orientacion de este
        y dibuja las instrucciones si está el marcador reconocido
        '''

        bboxs, ids, rechazados = self.detector.detectMarkers(frame)     # utilizamos el detector de aruco para detectar los marcadores en el frame actual
        encontrado = False

        if ids is not None:     # Si el marcador que hay en pantalla coincide con alguno que contenga el diccionario
            ids_detectados = set()      # almacena los ids de los marcadores detectadoe en el frame

            for i in range(len(bboxs)):     # iteramos sobre los marcadores
                self.id_marcador = int(ids[i][0])       # se extrae el identificador dle marcador actual
                ids_detectados.add(self.id_marcador)        # añadimos el id al conjunto de marcadores detectados en el frame
                encontrado = True       # si hemos encontrado alguno, se pone valido
                imagePoints = bboxs[i][0]       # se obtienen las coordenadas en 2d de las esquinas del marcador
                objectPoints = self.origen()        # obtenemos el origen del marcador

                # solvePnP estima la orientacion y la posicion en el espacio del objeto que vamos a dibujar, por eso usamos rvec (como esta orientado el marcador) y tvec (donde esta el marcador)
                ret, rvec, tvec = cv2.solvePnP(objectPoints, imagePoints, self.cameraMatrix, self.distCoeffs)

                # Se verifica que rvec y tvec no tengan valores nan (es decir, que no hayan fallado
                if not np.isnan(rvec).any() and not np.isnan(tvec).any():
                    self.ultimas_poses[self.id_marcador] = (rvec, tvec)     # si es valido, guardamos la posicion
                    self.dibujar_instrucciones(frame, self.id_marcador, rvec, tvec)     # llamamos al metodo que dibuja las instrucciones en ra

        return frame

# ----------------------------------------------------------------------------------------------------------------------#

    def dibujar_instrucciones(self, frame, id_marcador, rvec, tvec):
        '''
        Este metodo dibuja las instrucciones sobre el frame actual del video
        '''

        paso = self.paso_actual.get(id_marcador, 0)     # obtiene el paso actual del marcador detectado
        pasos = self.INSTRUCCIONES.get(id_marcador, [])     # recupera la lista de instrucciones para el marcador desde el diccionario que hemos hecho

        if paso < len(pasos):       # comprueba que el paso actual escita dentro de la lista de pasos posibles
            acciones = pasos[paso].get("acciones", [])      # extrae la lista de acciones del paso actual

            # se calcula la distancia al marcador
            distancia = tvec[2][0] if isinstance(tvec, np.ndarray) else 0.5  # profundidad Z
            escala = max(0.1, min(1.0 / distancia, 2.0))  # evita valores extremos

            # itera sobre todas las acciones que se tiene que hacer en el paso actual
            for instruccion in acciones:
                if instruccion["tipo"] == "circulo":        # para las acciones de tipo circulo
                    offset = instruccion["offset"]      # desplazamiento del circulo respecto el marcador
                    punto_3d = np.array([[offset[0], offset[1], 0.0]], dtype=np.float32)        # define la posicion dle circulo en coordenadas 3d
                    punto_2d, _ = cv2.projectPoints(punto_3d, rvec, tvec, self.cameraMatrix, self.distCoeffs)       # define la posicion del circulo en coordenadas 2d
                    centro = tuple(np.int32(punto_2d[0][0]))        # convierte el punto a coordenadas con pixeles
                    radio_base = instruccion["radio"] * 100     # se calcula el radio del circulo
                    radio = int(radio_base * escala)        # ajusta el radio con la escala segun la distancia al marcador
                    color = instruccion["color"]        # obtenemos el color del circulo
                    cv2.circle(frame, centro, radio, color, 2)      # dibuja el circulo en el frame en la posicion dicha, con el radio y el color y un grosor de 2 px

                elif instruccion["tipo"] == "flecha":       # para las acciones de tipo flecha
                    inicio = instruccion["inicio"]      # obtenemos las coordenadas de inicio y de fin de la flecha en el marcador
                    fin = instruccion["fin"]
                    color = instruccion["color"]     # obtenemos el color de la flecha
                    grosor_base = instruccion["grosor"]     # obtenemos el grosor de la flecha
                    grosor = max(1, int(grosor_base * escala))          # ajusta el grosor en funcion de la distancia

                    puntos_3d = np.array([[inicio[0], inicio[1], 0.0], [fin[0], fin[1], 0.0]], dtype=np.float32)        # definimos los puntos en 3d
                    puntos_2d, _ = cv2.projectPoints(puntos_3d, rvec, tvec, self.cameraMatrix, self.distCoeffs)     # y en 2d
                    p1 = tuple(np.int32(puntos_2d[0][0]))       # se convierten los puntos proyectados para dibujarlos
                    p2 = tuple(np.int32(puntos_2d[1][0]))
                    cv2.arrowedLine(frame, p1, p2, color, grosor)       # se dibuja la flecha desde p1 hasta p2 con el color y grosor que se indica

# ----------------------------------------------------------------------------------------------------------------------#

    def origen(self):
        '''
        Este metodo se usa para calcular la posicion y la orientacion del marcador en el espacio, devolviendo las coordenadas de las esquinas
        '''

        TAM = self.TAM      # se obtiene el tamaño que le hayamos dicho
        return np.array([
            [-TAM / 2, TAM / 2, 0.0],
            [TAM / 2, TAM / 2, 0.0],
            [TAM / 2, -TAM / 2, 0.0],
            [-TAM / 2, -TAM / 2, 0.0]       # esto construye un array con las 4 esquinas del marcador en 3d, para tomarlo de origen de coordenadas para dibujar los elementos
        ])

# ----------------------------------------------------------------------------------------------------------------------#

    def obtener_info_paso_actual(self):
        '''
        Este metodo se usa para obtener la informacion del paso que nos encontremos
        '''

        if self.id_marcador != -1:      # si ha detectado un marcador, se busca la instruccion
            pasos = self.INSTRUCCIONES.get(self.id_marcador, [])
            paso_actual = self.paso_actual.get(self.id_marcador, 0)

            if paso_actual < len(pasos):        # si el paso actual aun esta dentor de los pasos posibles
                paso = pasos[paso_actual]       # accede al contenido del paso actual
                # Si es un diccionario con campo 'info', lo devolvemos
                if isinstance(paso, dict) and "info" in paso:
                    return paso["info"]
                else:
                    return f"Paso {paso_actual + 1}"
            else:
                return "Instrucciones completadas"      # si el numero del paso actual suepra el numero de pasos disponibles, las instrucciones han finalizado
        elif self.id_marcador == -2:
            return "Instrucciones completadas"
        else:
            return "Pasos a seguir"

# ----------------------------------------------------------------------------------------------------------------------#

    def avanzar_paso(self):
        '''
        Este metodo avanza al siguiente paso cuando se da al boton para ello
        '''

        if self.id_marcador in self.INSTRUCCIONES:      # nos aseguramos de que el marcador tenga instrucciones
            total_pasos = len(self.INSTRUCCIONES[self.id_marcador])         # se calcula el numero total de pasos
            paso_actual = self.paso_actual.get(self.id_marcador, 0)     # obtenemos el paso actual del marcador, si no tiene valor asumimos que esta en el 0
            if paso_actual + 1 < total_pasos:       # si todavia quedan pasos por mostras (no estamos en el ultimo)
                self.paso_actual[self.id_marcador] = paso_actual + 1        #actualizamos el paso, añadiendole uno
            else:
                self.id_marcador = -2       # si se ha llegado al final, lo ponemos a -2, que indica que se han acabado las instrucciones

# ----------------------------------------------------------------------------------------------------------------------#

    def obtener_id(self):
        # Devuelve el id del marcador actual
        return self.id_marcador

# ----------------------------------------------------------------------------------------------------------------------#

    def retroceder_paso(self):
        '''
        Este metodo retrocede al paso anterior de las instrucciones que tenga el marcador actual
        '''

        if self.id_marcador in self.INSTRUCCIONES:      #verificamos que el marcador tenga instrucciones
            paso_actual = self.paso_actual.get(self.id_marcador, 0)     #se obtiene el paso actual
            if paso_actual > 0:     #si el paso actual no es el primero, se puede retroceder
                self.paso_actual[self.id_marcador] = paso_actual - 1        # disminuye el numero del paso
            else:
                self.paso_actual[self.id_marcador] = 0  # Ya esta en el primer paso

# ----------------------------------------------------------------------------------------------------------------------#
