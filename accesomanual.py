from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

class AccesoManual(Screen):
    '''
    Esta clase define la pantalla de acceso manual de la aplicación.
    Va a permitir ingresar al usuario mediante su nombre de usuario y contraseña que se ha
    creado previamente.
    '''
    def __init__(self, conexion, **kwargs):
        super().__init__(**kwargs)
        self.conexion = conexion        # Conexión a la base de datos

        # Imagen del logo de la aplicación
        self.logo = Image(
            source='recursos/autonomelogo.png',
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        self.add_widget(self.logo)

        # Creamos un leyout para poder añadir elementos a la interfaz
        self.layout2 = BoxLayout(orientation='vertical',
                                 spacing=10,
                                 size_hint=(None, None),
                                 size=(500, 100),
                                 pos_hint={'center_x': 0.5, 'center_y': 0.28})

        # Este label sirve para poder poner el estado de la creación de cuentas
        self.label3 = Label(text='',
                            color=(1, 0, 0, 1),
                            font_size='25sp',
                            font_name='recursos/negrita.ttf',
                            pos_hint={'center_x': 0.5, 'center_y': 0.28})
        self.layout2.add_widget(self.label3)
        self.add_widget(self.layout2)

        # Layout principal para los elementos del formulario de registro
        layout = BoxLayout(orientation='vertical',
                           spacing=10,
                           size_hint=(None, None),
                           size=(500, 175),
                           pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # Título de la pantalla
        self.label = Label(text='INICIO DE SESIÓN',
                           color=(0.5, 0.7, 1, 1),
                           font_size='25sp',
                           font_name='recursos/negrita.ttf',
                           pos_hint={'center_x': 0.5, 'center_y': 0.63})

        # Campo de entrada para el nombre de usuario
        self.nombre_usuario = TextInput(hint_text="Introduce tu nombre de usuario",
                                        font_size=25,
                                        font_name='recursos/font.ttf',
                                        size=(400, 50),
                                        multiline=False)

        # Campo de entrada para la contraseña
        self.contrasenia = TextInput(hint_text="Introduce tu contraseña",
                                     font_size=25,
                                     font_name='recursos/font.ttf',
                                     size=(400, 50),
                                     password=True,
                                     multiline=False)

        # Añadimos los elementos al layout
        layout.add_widget(self.label)
        layout.add_widget(self.nombre_usuario)
        layout.add_widget(self.contrasenia)
        self.add_widget(layout)

        # Botón para iniciar sesión
        self.crear_cuenta_btn = Button(
            text='Inicia Sesión',
            size_hint=(0.4, 0.05),
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='25sp',
            font_name='recursos/font.ttf'
        )
        self.add_widget(self.crear_cuenta_btn)
        self.crear_cuenta_btn.bind(on_press=self.comprobar_cuenta)

        # Botón para volver atrás en la pantalla de inicio
        self.volver_atras = Button(
            text='Volver atrás',
            size_hint=(0.4, 0.05),
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='25sp',
            font_name='recursos/font.ttf'
        )
        self.add_widget(self.volver_atras)
        self.volver_atras.bind(on_press=self.cambiar_a_inicio)

# ----------------------------------------------------------------------------------------------------------------------#

    def cambiar_a_inicio(self, instance):
        '''
        Este metodo vuelve de nuevo a la pantalla de inicio limpiando los campos de entrada
        '''

        self.label3.text = ''
        self.nombre_usuario.text = ''
        self.contrasenia.text = ''
        self.manager.current = 'inicio'

# ----------------------------------------------------------------------------------------------------------------------#

    def cambiar_a_camaraapp(self, instance):
        '''
        Este metodo da acceso a la interfaz de la funcionalidad de la aplicacion si el inicio de sesión
        fue correcto.
        '''

        self.manager.current = 'camaraapp'

# ----------------------------------------------------------------------------------------------------------------------#

    def comprobar_cuenta(self, instance):
        '''
        Este metodo comprueba si el nombre de usuario y la contraseña que han puesot en los campos están registrados
        en la base de datos, si lo están, cambia a la pantalla principal y si no muestra un mensaje de error.
        '''

        if self.nombre_usuario.text.strip() != "" and self.contrasenia.text.strip() != "":
            with self.conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM USUARIOS WHERE nom_user = :nombre_user AND password = :contrasenia", {'nombre_user':self.nombre_usuario.text, 'contrasenia':self.contrasenia.text})
                usuario = cursor.fetchone()
                if usuario:
                    self.cambiar_a_camaraapp(instance)

                else:
                    self.label3.text = 'El usuario o la contraseña no coinciden.'
        else:
            self.label3.text = 'Por favor, rellene todos los campos.'

#----------------------------------------------------------------------------------------------------------------------#
