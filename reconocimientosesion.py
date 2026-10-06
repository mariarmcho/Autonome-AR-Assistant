from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import face_recognition as fr
import numpy as np
import pickle

class ReconocimientoSesion(Screen):
    '''
    Esta clase gestiona la pantalla del reconocimiento facial para el inicio de sesion
    '''

    def __init__(self, conexion, **kwargs):
        super().__init__(**kwargs)      # constructor de la clase
        self.conexion = conexion        # Creamos la conexion a la base de datos

        # Logo de la aplicación
        self.logo = Image(
            source='recursos/autonomelogo.png',
            size_hint=(0.4, 0.4),
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        self.add_widget(self.logo)

        # Botón para volver a la pantalla de inicio
        self.volver_atras = Button(
            text='Volver atrás',
            size_hint=(0.4, 0.05),
            pos_hint={'center_x': 0.5, 'center_y': 0.20},
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='25sp',
            font_name='recursos/font.ttf'
        )
        self.add_widget(self.volver_atras)
        self.volver_atras.bind(on_press=self.cambiar_a_inicio)

        # Este layout lo usamos para mostrar mensajes de error o de informacion
        self.layout2 = BoxLayout(orientation='vertical',
                                 spacing=10,
                                 size_hint=(None, None),
                                 size=(500, 100),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.31})
        self.label = Label(text='',     # label vacio para poder poner luego cosas segun ocurran
                            color=(1, 0, 0, 1),
                            font_size='25sp',
                            font_name='recursos/negrita.ttf',
                            pos_hint={'center_x': 0.5, 'center_y': 0.1})
        self.layout2.add_widget(self.label)
        self.add_widget(self.layout2)

        # Botón para capturar la cara desde la camara
        self.boton_capturar = Button(
            text='Capturar cara',
            size_hint=(0.4, 0.05),
            pos_hint={'center_x': 0.5, 'center_y': 0.14},
            background_color=(0.1, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size='25sp',
            font_name='recursos/font.ttf'
        )
        self.boton_capturar.bind(on_press=self.capturar_cara)
        self.add_widget(self.boton_capturar)

# ----------------------------------------------------------------------------------------------------------------------#

    def camara(self):
        '''
        Este metodo abre la camara para poder hacer el reconocimiento facial
        '''

        # En primer lugar, liberamos la camara si ya se esta usando
        if getattr(self, 'webcam', None) is not None and self.webcam.isOpened():
            self.webcam.release()

        # Creamos el widget si no existe
        if not hasattr(self, 'image'):
            self.image = Image(size_hint=(0.6, 0.6),
                               pos_hint={'center_x': 0.5, 'center_y': 0.45})
            self.add_widget(self.image)

        # Inicia la camara
        self.webcam = cv2.VideoCapture(0)

        # Si no se abre correctamente, muestra error
        if not self.webcam.isOpened():
            self.label.text = "No se pudo abrir la cámara."
            return

        # Programa el metodo update para actuar a 30fps
        Clock.schedule_interval(self.update, 1.0 / 30.0)

# ----------------------------------------------------------------------------------------------------------------------#

    def update(self, dt):
        '''
        Actualiza la camara para poder mantener la imagen a tiempo real
        '''

        if self.capturado == False:
            ret, frame = self.webcam.read()     # Lee un frame de la camara
            if ret:
                # convierte el framde e opencv a kivy
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # pone el modo espejo
                frame = cv2.flip(frame, 1)

                # Voltear la imagen verticalmente
                frame = cv2.flip(frame, 0)  # 0 indica que se voltea verticalmente
                buf = frame.tobytes()

                # Crear una textura a partir del frame
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
                texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

                # Asignar la textura al widget Image
                self.image.texture = texture

# ----------------------------------------------------------------------------------------------------------------------#

    def cambiar_a_inicio(self, instance):
        '''
        Este metodo cambia de la pantalla actual a la pantalla de inicio
        '''

        self.webcam.release()       # Libera la camara
        Clock.unschedule(self.update)       # detiene las actualizaciones de los frame
        self.manager.current = 'inicio'     # Cambia la pantalla

# ----------------------------------------------------------------------------------------------------------------------#

    def capturar_cara(self, instance):
        '''
        Metodo que captura la cara cuando la reconoce en los frame
        '''

        # Verifica que la camara etse disponible
        if not hasattr(self, 'webcam') or not self.webcam.isOpened():
            self.label.text = "Cámara no disponible."
            return
        ret, frame = self.webcam.read()
        self.cara = frame       # GUarda la imagen

        cara_rgb = cv2.cvtColor(self.cara, cv2.COLOR_BGR2RGB)
        ubicaciones = fr.face_locations(cara_rgb)       # Detecta la cara

        if ubicaciones:
            self.capturado = True
            self.codigo_cara = fr.face_encodings(cara_rgb, known_face_locations=ubicaciones)[0]
            self.buscar_cara()  # Busca la cara en la base de datos
        else:
            self.label.text = "Cara no reconocida."
            Clock.schedule_once(lambda dt: self.borrar_mensaje(), 3)

# ----------------------------------------------------------------------------------------------------------------------#

    def buscar_cara(self):
        '''
        Esta funcion busca la cara que hemos capturado antes en la base de datos para ver si coincide o no
        '''

        vector_caras = []

        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT USER_FACE FROM USUARIOS")        # COnsulta las caras que tenemos en la base de datos
                caras = cursor.fetchall()       # Las guarda todas en el vector
                print(caras[0])

                for cara in caras:
                    encoding = pickle.loads(cara[0].read())
                    vector_caras.append(encoding)

                resultado = fr.compare_faces(vector_caras, self.codigo_cara)    # Compara als caras que ha guardado en el vector con la que hemos comparado

                # SI alguna coincide
                if np.any(resultado):
                    self.webcam.release()
                    Clock.unschedule(self.update)
                    self.manager.current = 'camaraapp'      # Cambia la pantalla dando acceso a la aplicación
                else:
                    self.label.text = "Cara no reconocida en la base de datos."
                    Clock.schedule_once(lambda dt: self.borrar_mensaje(), 3)
        except Exception as e:
            self.label.text = "Cara no reconocida en la base de datos."
            Clock.schedule_once(lambda dt: self.borrar_mensaje(), 3)
        return False  # Si no se encontró ninguna coincidencia

# ----------------------------------------------------------------------------------------------------------------------#

    def on_enter(self):
        '''
        Metodo que se ejecuta cuando se entra en esta interfaz, para inicializar las variables
        '''

        self.capturado = False
        self.codigo_cara = None
        self.cara = None
        self.camara()       # Enciende la camara

# ----------------------------------------------------------------------------------------------------------------------#

    def borrar_mensaje(self):
        '''
        Borra el mensaje que hay en el label
        '''

        self.label.text = ""

# ----------------------------------------------------------------------------------------------------------------------#

    def cambiar_a_camaraapp(self, instance):
        '''
        Metodo que cambia la pantalla cuando hemos iniciado sesion correctamente
        '''

        self.webcam.release()       # Libera la camara
        Clock.unschedule(self.update)       # Detiene la actualizacion de frames
        self.manager.current = 'camaraapp'      # Cambia la pantalla

# ----------------------------------------------------------------------------------------------------------------------#
