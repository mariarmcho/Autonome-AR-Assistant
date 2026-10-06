from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import face_recognition as fr
import numpy as np
import pickle

class CrearCuenta(Screen):
    '''
    Esta es la pantalla para poder crear una cuenta.
    '''
    def __init__(self, conexion, **kwargs):
        super().__init__(**kwargs)

        self.conexion = conexion        # Conexión a la base de datos
        self.webcam = None      # Inicialización de la cámara


        # Logo de la aplicación
        self.logo = Image(
            source='recursos/autonomelogo.png',
            size_hint=(0.3, 0.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.85}
        )
        self.add_widget(self.logo)

        # Layout para los campos de entrada
        layout = BoxLayout(orientation='vertical',
                           spacing=10,
                           size_hint=(None, None),
                           size=(500, 200),
                           pos_hint={'center_x': 0.5, 'center_y': 0.65})

        # Título de la página
        self.label = Label(text='CREACION DE CUENTAS',
                              color=(0.5, 0.7, 1, 1),
                              font_size='25sp',
                              font_name='recursos/negrita.ttf',
                              pos_hint={'center_x': 0.5, 'center_y': 0.63} )

        # Entrada de texto del nombre de usuario
        self.nombre_usuario = TextInput(hint_text="Introduce un nombre de usuario",
                                        font_size=25,
                                        font_name='recursos/font.ttf',
                                        size=(400, 50),
                                        multiline=False)

        # Entrada de texto de la contraseña
        self.contrasenia = TextInput(hint_text="Introduce una contraseña",
                                     font_size=25,
                                     font_name='recursos/font.ttf',
                                     size=(400, 50),
                                     password=True,
                                     multiline=False)

        # Entrada de texto del email
        self.email = TextInput(hint_text="Introduce tu email",
                                     font_size=25,
                                     font_name='recursos/font.ttf',
                                     size=(400, 50),
                                     multiline=False)

        # Añadimos todo al layout
        layout.add_widget(self.label)
        layout.add_widget(self.nombre_usuario)
        layout.add_widget(self.contrasenia)
        layout.add_widget(self.email)
        self.add_widget(layout)

        # Botón para crear la cuenta
        self.crear_cuenta_btn = Button(
            text='Crea tu cuenta ahora',
            size_hint=(0.4, 0.05),
            pos_hint={'center_x': 0.5, 'center_y': 0.17},
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='25sp',
            font_name='recursos/font.ttf'
        )
        self.crear_cuenta_btn.bind(on_press=self.crear_cuenta)
        self.add_widget(self.crear_cuenta_btn)

        # Botón para volver a la pantalla de inicio
        self.volver_atras = Button(
            text='Volver atrás',
            size_hint=(0.4, 0.05),
            pos_hint={'center_x': 0.5, 'center_y': 0.1},
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='25sp',
            font_name='recursos/font.ttf'
        )
        self.add_widget(self.volver_atras)
        self.volver_atras.bind(on_press=self.cambiar_a_inicio)

        # Botón para activar la cámara
        self.boton_camara = Button(background_normal='recursos/camara.png',
                                   size_hint=(None, None),
                                   size=(64, 64),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                   opacity=1)
        self.boton_camara.bind(on_press=self.abrir_camara)
        self.add_widget(self.boton_camara)

        # Botón para capturar la imagen de la cámara
        self.boton_capturar = Button(
            text='Capturar cara',
            size_hint=(0.3, 0.05),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            background_color=(0.1, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            font_size='25sp',
            font_name='recursos/font.ttf'
        )
        self.boton_capturar.bind(on_press=self.capturar_cara)
        self.add_widget(self.boton_capturar)

# ----------------------------------------------------------------------------------------------------------------------#

    def abrir_camara(self, instance):
        '''
        Esta funcion llama al metodo que abre la camara
        '''

        self.camara()

# ----------------------------------------------------------------------------------------------------------------------#

    def cambiar_a_inicio(self, instance):
        '''
        Esta función limpia los campos y luego cambia a la pantalla de inicio
        '''

        self.nombre_usuario.text = ''
        self.email.text = ''
        self.contrasenia.text = ''
        if(self.webcam != None):
            self.webcam.release()       # Libera la camara
            self.remove_widget(self.image)      # Quitamos el widget de la camara
        Clock.unschedule(self.update)       # Detiene la actualizacion de los frames
        self.manager.current = 'inicio'     # Cambia la pantalla

# ----------------------------------------------------------------------------------------------------------------------#

    def cambiar_a_camaraapp(self, instance):
        '''
        Cambia a la pantalla dando acceso a la aplicación si se ha creado la cuenta correctamente
        '''

        self.webcam.release()
        Clock.unschedule(self.update)
        self.manager.current = 'camaraapp'

# ----------------------------------------------------------------------------------------------------------------------#

    def crear_cuenta(self, instance):
        '''
        Crea la cuenta si no hay errores guardando toda la informacion del perfil en la base de datos
        '''

        if not self.capturado:
            self.label.text = "Cara no capturada correctamente."
            return
        if self.comprobar_cuenta(instance):
            if self.nombre_usuario.text.strip() != "" and self.contrasenia.text.strip() != "" and self.email.text.strip() != "":
                # Serializa el encoding de la cara (guarda todos los datos de la imagen)
                codigo_cara = pickle.dumps(self.codigo_cara)
                # Inserta el usuario
                with self.conexion.cursor() as cursor:
                    cursor.execute("""
                                INSERT INTO USUARIOS (nom_user, password, email, user_face)
                                VALUES (:nombre, :contraseña, :email, :face)
                            """, {
                        'nombre': self.nombre_usuario.text,
                        'contraseña': self.contrasenia.text,
                        'email': self.email.text,
                        'face': codigo_cara
                    })
                    self.conexion.commit()      # GUardamos los cambios en la base de datos
                    self.manager.current = 'camaraapp'     #Cambiamos de pantalla
            else:
                self.label.text = "Rellene todos los campos"

# ----------------------------------------------------------------------------------------------------------------------#

    def comprobar_cuenta(self, instance):
        '''
        Esta funcion verifica si el usuario o el email ya se han usado
        '''

        if self.nombre_usuario.text.strip() != "" and self.contrasenia.text.strip() != "" and self.email.text.strip() != "":
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM USUARIOS WHERE nom_user = :nombre_user OR email = :email", {
                    'nombre_user': self.nombre_usuario.text,
                    'email': self.email.text
                })
                usuario = cursor.fetchone()         # Esto obtiene la primera final de resultado (por si hay o si no hay coincidencias)
                if usuario:
                    self.label.text = 'El usuario o el email ya han sido utilizados.'
                    return False
                else:
                    return True
        else:
            self.label.text = 'Por favor, rellene todos los campos.'
            return False

# ----------------------------------------------------------------------------------------------------------------------#

    def capturar_cara(self, instance):
        '''
        Captura la imagen de la cara a traves de la camara
        '''

        if not hasattr(self, 'webcam') or not self.webcam.isOpened():
            self.label.text = "Cámara no disponible."
            return
        ret, frame = self.webcam.read()     # Lee un frame de la webcam
        self.cara = frame
        cara_rgb = cv2.cvtColor(self.cara, cv2.COLOR_BGR2RGB)       # Lo convierte a rgb
        ubicaciones = fr.face_locations(cara_rgb)       # busca las caras

        if ubicaciones:
            self.capturado = True
            self.codigo_cara = fr.face_encodings(cara_rgb, known_face_locations=ubicaciones)[0]
            self.buscar_cara()  # Busca después de capturar
        else:
            self.label.text = "Cara no reconocida."
            Clock.schedule_once(lambda dt: self.borrar_mensaje(), 3)

# ----------------------------------------------------------------------------------------------------------------------#

    def buscar_cara(self):
        '''
        Verifica si el vector que guarda la cara ya existe (es decir que ya esta esa cara registrada)
        '''

        vector_caras = []

        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT USER_FACE FROM USUARIOS")
                caras = cursor.fetchall()       # Trae todas las caras guardadas
                print("marca")
                for cara in caras:
                    encoding = pickle.loads(cara[0].read())     #Deserializa el vector de la cara
                    vector_caras.append(encoding)

                resultado = fr.compare_faces(vector_caras, self.codigo_cara)        # Lo compara con cada vector que tiene

                # Verificamos si hay alguna coincidencia
                if np.any(resultado):
                    self.capturado = True
                    self.webcam.release()
                    self.label.text = "Cara ya registrada."

        except Exception as e:
            print(e)
            Clock.schedule_once(lambda dt: self.borrar_mensaje(), 3)

        return False  # Si no se encontró ninguna coincidencia

# ----------------------------------------------------------------------------------------------------------------------#

    def on_enter(self):
        '''
        Este método inicializa las variables cuando se entra a esta pantalla
        '''

        self.capturado = False
        self.codigo_cara = None
        self.cara = None

# ----------------------------------------------------------------------------------------------------------------------#

    def borrar_mensaje(self):
        '''
        Borra el texto del label
        '''

        self.label.text = ""

# ----------------------------------------------------------------------------------------------------------------------#

    def camara(self):
        '''
        Activa la camara y lo muestra en la pantalla
        '''

        if getattr(self, 'webcam', None) is not None and self.webcam.isOpened():
            self.webcam.release()

        self.image = Image(size_hint=(0.25, 0.25),
                           pos_hint={'center_x': 0.5, 'center_y': 0.43})
        self.add_widget(self.image)

        self.webcam = cv2.VideoCapture(0)       # abre la camara

        if not self.webcam.isOpened():
            self.label.text = "No se pudo abrir la cámara."
            return

        Clock.schedule_interval(self.update, 1.0 / 30.0)        # actualiza los frame a 30 fps

# ----------------------------------------------------------------------------------------------------------------------#

    def update(self, dt):
        '''
        Refresca los frame de la camara para poder mostrarlo en vivo
        '''

        if self.capturado == False:
            ret, frame = self.webcam.read()
            if ret:
                # convierte el frame de BGR (opencv) a RGB (kivy)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Pone el modo espejo
                frame = cv2.flip(frame, 1)

                # Gira la imagen horizontalmente
                frame = cv2.flip(frame, 0)  # 0 indica que se gira verticalmente
                buf = frame.tobytes()

                # Crear una textura a partir del frame
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
                texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

                # Asignar la textura al widget image
                self.image.texture = texture

# ----------------------------------------------------------------------------------------------------------------------#