from kivy.app import App
from inicio import Inicio
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from basededatos import conectar
from kivy.uix.screenmanager import ScreenManager
from crearcuenta import CrearCuenta
from camaraapp import CamaraApp
from accesomanual import AccesoManual
from reconocimientosesion import ReconocimientoSesion

class AutonoMe(App):
    '''
    Clase principal de AutonoMe, la cuál usaré las especificaciones de Kivy.
    Se define la construcción de la interfaz principal, se inicializa la base de datos
    y la navegación entre las diferentes pantallas.
    '''
    def build(self):
        # Creamos el layout base
        self.root_layout = FloatLayout()

        # COnfiguramos el tamaño y el color predeterminado de la interfaz
        Window.size = (1850, 1250)
        Window.clearcolor = (1, 1, 1, 1)

        # Creamos la conexión a la base de datos
        self.conexion = conectar()

        # Creamos el administrador de pantallas
        sm = ScreenManager()
        # Añadimos todas las pantallas que va a tener la aplicación asigandole un nombre
        sm.add_widget(Inicio(self.conexion, name='inicio'))
        sm.add_widget(CrearCuenta(self.conexion, name='crearcuenta'))
        sm.add_widget(CamaraApp(self.conexion, name='camaraapp'))
        sm.add_widget(AccesoManual(self.conexion, name='accesomanual'))
        sm.add_widget(ReconocimientoSesion(self.conexion, name='reconocimientosesion'))

        # Devolvemos el screen manager como la raíz de la aplicación para que inicie
        return sm


if __name__ == '__main__':
    AutonoMe().run()
