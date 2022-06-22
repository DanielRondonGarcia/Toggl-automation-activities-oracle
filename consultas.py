import cx_Oracle
import config

connection = None
v = None
def conectar():
    try:
        global cur
        connection = cx_Oracle.connect(
            config.username,
            config.password,
            config.dsn,
            encoding=config.encoding)

        # imprime la version de la base de datos
        print(connection.version)
        cur = connection.cursor()
        return cur

    except cx_Oracle.Error as error:
        print(error)

def finalizar():
    # release the connection
    if connection:
        connection.close()
        

def forma_uno():
    conectar()
    try:
        cur.execute("SELECT * FROM bases_objetos where rownum < 11")
        for BASE, TIPO, NOMBRE, ESQUEMA, LAST_DDL_TIME, FECHA_SISTEMA  in cur:
            print("Department number: ", BASE)
            print("Department name: ", TIPO)
            print("Department name: ", NOMBRE)
            print("Department name: ", ESQUEMA)
            print("Department name: ", LAST_DDL_TIME)
            print("Department name: ", FECHA_SISTEMA)

    except cx_Oracle.Error as error:
        print(error)
    finalizar()


def forma_dos():
    conectar()
    try:
        cur.execute("SELECT NUMERO_REQUERIMIENTO, TIPO, DESCRIPCION, FECHA, HORAS, USER_SISTEMA, FECHA_SISTEMA, ETAPA, ESTADO_DESDE, ESTADO_HASTA, RESPONSABLE_DESDE, RESPONSABLE_HASTA FROM sgi.req_actividades WHERE numero_requerimiento = 76871 AND ROWNUM < 11 ORDER BY fecha DESC")
        res = cur.fetchall()
        print(res)
    except cx_Oracle.Error as error:
        print(error)
    finalizar()

forma_dos()