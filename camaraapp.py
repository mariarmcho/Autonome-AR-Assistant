from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from arauco import Arauco
from threading import Thread
from reconocimientovoz import ReconocimientoVoz

class CamaraApp(Screen):
    '''
    La clase camaraapp es el eje principal pues es la pantalla donde se van a mostrar toda la realidad aumentada, además
    de dar todas las funcionalidades de los botones
    '''

    def __init__(self, conexion, **kwargs):
        super().__init__(**kwargs)      # constructor
        self.frame_actual = None        # Variable para guardar el último fotograma de la camara
        self.conexion = conexion        # Conexion a la base de datos
        self.arauco = Arauco(self, self.conexion)       # instancia para poder usar los metodos de la clase Arauco

        # Logo de la aplicación
        self.logo = Image(
            source='recursos/autonomelogo.png',
            size_hint=(0.2, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )
        self.add_widget(self.logo)

        # Layout que sirve para poner el texto de las instrucciones que aparecerán en pantalla
        self.layout = BoxLayout(orientation='vertical',
                           spacing=10,
                           size_hint=(None, None),
                           size=(500, 175),
                           pos_hint={'center_x': 0.5, 'center_y': 0.23})

        # Botón para avanzar paso
        self.siguiente_paso = Button(
            text= "Siguiente paso",
            size_hint=(0.2, 0.05),
            pos_hint={'center_x': 0.6, 'center_y': 0.17},
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='25sp',
            font_name='recursos/font.ttf'
        )
        self.add_widget(self.siguiente_paso)
        self.siguiente_paso.bind(on_press=self.boton_siguiente_paso)

        # Botón para retroceder paso
        self.anterior_paso = Button(
            text= "Paso anterior",
            size_hint=(0.2, 0.05),
            pos_hint={'center_x': 0.4, 'center_y': 0.17},
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='25sp',
            font_name='recursos/font.ttf'
        )
        self.add_widget(self.anterior_paso)
        self.anterior_paso.bind(on_press=self.boton_retroceder_paso)

        # Botón para salir de la aplicacion
        self.salir = Button(
            text='Salir',
            size_hint=(0.4, 0.05),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='25sp',
            font_name='recursos/font.ttf'
        )
        self.add_widget(self.salir)
        self.salir.bind(on_press=self.click_salir)

        # Muestra la informacion del paso actual en el que estemos
        self.label = Label(text=str(self.arauco.obtener_info_paso_actual()),
                              color=(0.5, 0.7, 1, 1),
                              font_size='25sp',
                              font_name='recursos/negrita.ttf',
                              pos_hint={'center_x': 0.5, 'center_y': 0.23} )
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)

        # Botón que activa el micro y el reconocimiento de voz
        self.boton_voz = Button(background_normal='recursos/microfono.png',
                                   size_hint=(None, None),
                                   size=(150, 150),
                                   pos_hint={'center_x': 0.85, 'center_y': 0.5},
                                   opacity=1)
        self.boton_voz.bind(on_press=self.obteneraccion)
        self.add_widget(self.boton_voz)

# ----------------------------------------------------------------------------------------------------------------------#

    def camara(self):
        if getattr(self, 'webcam', None) is not None and self.webcam.isOpened():
            self.webcam.release()

            # Crear widget solo una vez
        if not hasattr(self, 'image'):
            self.image = Image(size = (850, 650),
                                size_hint=(None, None),
                                pos_hint={'center_x': 0.5, 'center_y': 0.55})
            self.add_widget(self.image)

        self.webcam = cv2.VideoCapture(0)

        if not self.webcam.isOpened():
            self.label.text = "No se pudo abrir la cámara."
            return

        Clock.schedule_interval(self.update, 1.0 / 30.0)

# ----------------------------------------------------------------------------------------------------------------------#

    def update(self, dt):
        ret, frame = self.webcam.read()
        self.frame_actual = frame
        if ret:
            # Convertir el frame de BGR (OpenCV) a RGB (Kivy)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Voltear la imagen horizontalmente (modo espejo)
            frame = cv2.flip(frame, 1)

           # Voltear la imagen verticalmente
            frame = cv2.flip(frame, 0)  # 0 indica que se voltea verticalmente

            if hasattr(self, 'arauco'):
                frame = self.arauco.procesar_frame(frame)

             # Escalamos el frame al tamaño del widget
            target_width, target_height = self.image.size
            frame = cv2.resize(frame, (int(target_width), int(target_height)))

            buf = frame.tobytes()

            # Crear una textura a partir del frame
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

            # Asignar la textura al widget Image
            self.image.texture = texture
            #actualizacion de los pasos
            self.label.text = str(self.arauco.obtener_info_paso_actual())

# ----------------------------------------------------------------------------------------------------------------------#

    def on_enter(self):
        # Llama al metodo para activar la camara
        self.camara()

# ----------------------------------------------------------------------------------------------------------------------#

    def get_frame_actual(self):
        # Obtiene la variable que contiene el frame actual
        return self.frame_actual

# ----------------------------------------------------------------------------------------------------------------------#

    def click_salir(self, instance):
        # Cierra la aplicacion
        exit()

# ----------------------------------------------------------------------------------------------------------------------#

    def boton_siguiente_paso(self, instance):
        # Llama a la funcion de la clase arauco que hace que avance de paso
        self.arauco.avanzar_paso()

# ----------------------------------------------------------------------------------------------------------------------#

    def boton_retroceder_paso(self, instance):
        # Llama a la funcion de la clase arauco que hace que retroceda un paso
        self.arauco.retroceder_paso()

# ----------------------------------------------------------------------------------------------------------------------#

    def obteneraccion(self, instance):
        # Esat funcion ejecuta un hilo para no bloquear la interfaz y que se puedan usar el micro y la camara a la vez
        hebra1 = Thread(target=self.hebra)
        hebra1.start()      # Lanza la hebra

# ----------------------------------------------------------------------------------------------------------------------#

    def daltonismo(self, dt):
        # Solo cambia el color del label, sin borrar ni añadir widgets de nuevo
        self.label.color = (1, 0, 0, 1)  # Rojo

# ----------------------------------------------------------------------------------------------------------------------#

    def hebra(self):
        # Esta funcion hace la comparacion entre lo que reconoce el micro y el "diccionario de acciones que tenemos"

        recvoz = ReconocimientoVoz()
        palabras = recvoz.reconocerpalabras()           # Reconoce una palabra

        # Aquí ejecuta diferentes comandos según la palabra que reconozca
        if palabras == "next" or palabras == "continue" or palabras == "next step":
            Clock.schedule_once(lambda dt: self.arauco.avanzar_paso())
        elif palabras == "previous" or palabras == "back":
            Clock.schedule_once(lambda dt: self.arauco.retroceder_paso())
        elif palabras == "red" or palabras == "change":
            Clock.schedule_once(self.daltonismo)

# ----------------------------------------------------------------------------------------------------------------------#

