from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.uix.screenmanager import Screen

class Inicio(Screen):
    '''
    Esta clase define la pantalla de inicio de la aplicación, donde se puede navegar por las opciones
    de inicio de sesión.
    '''

    def __init__(self, conexion, **kwargs):
        super().__init__(**kwargs)
        self.conexion = conexion        # Conexión de la base de datos

        # Imagen del logo de la aplicación
        self.logo = Image(
            source='recursos/autonomelogo.png',
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        self.add_widget(self.logo)

        # Botón de entrada mediante el reconocimiento facial
        self.login_btn = Button(
            text='Entrar',
            size_hint=(0.6, 0.06),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size = '25sp',
            font_name='recursos/font.ttf'
        )
        self.login_btn.bind(on_press=self.cambiar_a_reconocimientosesion)       # Si lo presionamos, nos cambia a la pantalla de reconocimiento
        self.add_widget(self.login_btn)

        # Botón de acceso manual
        self.manual_btn = Button(
            text='Acceso Manual',
            size_hint=(0.5, 0.06),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='25sp',
            font_name='recursos/font.ttf'
        )
        self.manual_btn.bind(on_press=self.cambiar_a_accesomanual)      # Si lo presionamos, nos cambia a la pantalla de inicio de sesion manual
        self.add_widget(self.manual_btn)

        # Añadimos el separador a la pantalla
        divider = Divider(size_hint=(0.8, None),
                          height=20,
                          pos_hint={"center_x": 0.5, "center_y": 0.57}
                          )
        self.add_widget(divider)

        # Botón para ir a crear una cuenta
        self.crear_cuenta_btn = Button(
            text='Crear cuenta',
            size_hint=(0.4, 0.05),
            pos_hint={'center_x': 0.5, 'center_y': 0.20},
            background_color=(0.3, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            font_size='25sp',
            font_name='recursos/font.ttf'
        )
        self.crear_cuenta_btn.bind(on_press=self.cambiar_a_crear_cuenta)
        self.add_widget(self.crear_cuenta_btn)

# ----------------------------------------------------------------------------------------------------------------------#

    def cambiar_a_crear_cuenta(self, instance):     # Metodo para ir a la pantalla de crear cuenta usando el screenmanager
        self.manager.current = 'crearcuenta'

# ----------------------------------------------------------------------------------------------------------------------#

    def cambiar_a_accesomanual(self, instance):     # Metodo para ir a la pantalla de acceso manual usando el screenmanager
        self.manager.current = 'accesomanual'

#----------------------------------------------------------------------------------------------------------------------#

    def cambiar_a_reconocimientosesion(self, instance):     # Metodo para ir a la pantalla de reconocimiento usando el screenmanager
        self.manager.current = 'reconocimientosesion'

#----------------------------------------------------------------------------------------------------------------------#

class Divider(Widget):
    '''
    Widget que dibuja un dividor, con dos lineas y un circulo en medio.
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:

            # Línea a la izquierda
            Color(0.8, 0.8, 0.8, 1)  # Gris claro
            self.line_left = Line(width=1)

            # Línea a la derecha
            self.line_right = Line(width=1)

            # Círculo en el centro
            Color(0.5, 0.5, 0.5, 1)  # Gris más oscuro
            self.circle = Line(width=1)

        # Lanza el dibujo y lo actualiza por si se cambia la posición o el tamaño
        self.bind(pos=self.actualizar_graf, size=self.actualizar_graf)

#----------------------------------------------------------------------------------------------------------------------#

    def actualizar_graf(self, *args):
        '''
        Este metodo calcula la posición de las líneas y el circulo para que se adapten al widget
        '''

        center_x, center_y = self.center        # Posición en vertical
        left_x = self.x     # Posicion en x inicial, en la esquina izquierda
        right_x = self.right        #Posición en x final, en la esquina derecha
        circle_radius = 5       # Radio del círculo

        # DIbujamos las líneas y se definen los puntos tanto para la linea izquierda como la linea derecha
        self.line_left.points = [left_x, center_y, center_x - circle_radius - 10, center_y]      # Hacemos esa cuenta para ajustarlo y dejar un margen de 4 pixeles entre el circulo y las lineas
        self.line_right.points = [center_x + circle_radius + 10, center_y, right_x, center_y]       # Lo mismo para el otro lado

        # DIbujo del circulo: como kivy dibuja los circulos desde la esquina superior de la izq, del contenedor que le definimos, se lo restamos para centrarlo
        self.circle.ellipse = (center_x - circle_radius, center_y - circle_radius, circle_radius * 2, circle_radius * 2)

#----------------------------------------------------------------------------------------------------------------------#


