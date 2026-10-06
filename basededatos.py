import oracledb

# Parámetros de conexion a la base de datos de la ugr
dsn = oracledb.makedsn("oracle0.ugr.es", "1521", service_name="PRACTBD")
user = "x5932341"
password = "x5932341"

def conectar():
    '''
    Este metodo es el que establece la conexión con la base de datos de Oracle.
    '''

    try:
        connection = oracledb.connect(user=user, password=password, dsn=dsn)
        print("Conectado a Oracle")
        return connection
    except oracledb.DatabaseError as e:
        print("Error de conexión:", e)
        return None