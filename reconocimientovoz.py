import speech_recognition as sr # Usaremos la pyaudio para abrir el microfono

class ReconocimientoVoz:
    '''
    Esta clase utiliza el microfono, captura el audio cuando hablamos y luego lo intenta reconocer mediante Sphinx
    '''

    def __init__(self):
        # Creamos un reconocedor de voz, lo que hace es que convertira el audio en texto
        self.r = sr.Recognizer()
        self.texto = ""     # Variables donde guardaremos el texto que se ha reconocido

        # abrimos el microfono como entrada de audio
        with sr.Microphone() as source:
            # Ajustamos el recognizer al ruido ambiental para mejorar la precision
            self.r.adjust_for_ambient_noise(source)

            # Se muestra en la terminal el nivel del ruido detectado
            nivel_ruido = self.r.energy_threshold
            print("Nivel de ruido ambiental calibrado:", nivel_ruido)

            # Indicamos al usuario que puede hablar por la terminal (esto lo uso sobre todo para las pruebas)
            print("¡Di algo!")

            # Escuchamos lo que dice durante solo 10 segundos
            self.audio = self.r.listen(source, phrase_time_limit=10)

# ----------------------------------------------------------------------------------------------------------------------#

    def reconocerpalabras(self):
        '''
        Esta funcion intenta reconocer lo que se ha dicho mediante Sphinx y devolverá el texto que reconoce
        '''

        try:
            # COnvierte el audio en texto
            self.texto = self.r.recognize_sphinx(self.audio)
            print("Sphinx piensa que dijiste: " + self.texto)
        except sr.UnknownValueError:        # Este error ocurre si el motor no entiende lo que decimos
            print("Sphinx no pudo entender el audio")
        except sr.RequestError as e:        # Este error ocurre si Phinx no está bien instalado o hay algun fallo
            print("Error al solicitar resultados de Sphinx; {0}".format(e))
        return self.texto

# ----------------------------------------------------------------------------------------------------------------------#


'''
Comento esta parte por que es lo mejor para usar pero no me funcionaba bien por que no me tomaba bien la 
conexion a Google Speech Recognition, aunque haya depurado e intentado solucionarlo, me funcionaba mejor con 
Sphinx.

    def reconocerpalabras(self):
        try:
            self.texto = self.r.recognize_google(self.audio, language='es-ES')
            print("Google Speech Recognition cree que dijiste:", self.texto)
        except sr.UnknownValueError as e:
            print("Google Speech Recognition no pudo entender el audio")
            print("Detalle:", repr(e))
        except sr.RequestError as e:
            print("No se pudieron solicitar resultados del servicio de Google Speech Recognition")
            print("Detalle:", repr(e))
        except Exception as e:
            print("Ocurrió una excepción inesperada:")
            print("Tipo:", type(e))
            print("Detalle:", repr(e))
        return self.texto

'''