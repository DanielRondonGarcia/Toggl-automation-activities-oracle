from asyncio.windows_events import NULL
from pprint import pprint
import cx_Oracle
import config

connection = None
maxHoras = 9
v = None
def conectar():
    try:
        global cur, connection
        connection = cx_Oracle.connect(
            config.username,
            config.password,
            config.dsn,
            encoding=config.encoding)

        # imprime la version de la base de datos
        print(connection.version)
        cur = connection.cursor()
        return cur, connection

    except cx_Oracle.Error as error:
        print(error)

def finalizar():
    # release the connection
    if connection:
        connection.close()

def getHours():
    try:
        command = """SELECT sum(horas)
                    FROM sgi.req_actividades 
                    WHERE user_sistema = 'DRONDON' AND
                    TRUNC(fecha) = TRUNC(sysdate)
                    ORDER BY fecha DESC"""
        cur.execute(command)
        resHours = cur.fetchall()
        return resHours
    except cx_Oracle.Error as error:
        print(error)

def activarRoles():
    try:
        command = """DECLARE comando VARCHAR2(32767);
        vl_schema parametros.valor%TYPE := NVL(PK_ACTSIS.F_Leer_Parametro('SAC_SCHEMA'),'SAC');
        PROCEDURE P_Alterar_Sesion_NumCharacters IS
        db_nls nls_database_parameters.value%type;
        ses_nls nls_session_parameters.value%type;
        BEGIN
        SELECT VALUE
        INTO db_nls
        FROM nls_database_parameters
        WHERE parameter='NLS_NUMERIC_CHARACTERS';
        SELECT VALUE
        INTO ses_nls
        FROM nls_session_parameters
        WHERE parameter='NLS_NUMERIC_CHARACTERS';
        IF db_nls <> ses_nls THEN
        EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_NUMERIC_CHARACTERS = '''|| db_nls||'''';
        END IF;
        COMMIT;
        END P_Alterar_Sesion_NumCharacters;
        BEGIN
        SELECT PK_ACTSIS.F_Activar_Roles(DECODE(PK_ACTSIS.F_Leer_Parametro('EMP_SIGLA'),'EDEQ','EDEQACTSIS2001'
        ,'ACTSIS19932006'),USER)
        INTO comando
        FROM dual;
        EXECUTE IMMEDIATE comando;
        --
        P_Alterar_Sesion_NumCharacters;
        --
        DBMS_OUTPUT.PUT_LINE('Activó roles correctamente');
        --
        PK_ACTSIS.P_Set_Current_Schema(vl_schema);
        --
        DBMS_OUTPUT.PUT_LINE('Esquema: '||vl_schema);
        END;"""
        cur.execute(command)
    except cx_Oracle.Error as error:
        print(error)


def inserInto(data):
    try:
        conectar()
        resHours = getHours()
        for id in resHours:
            Hours = id[0]
        if Hours is None: # The variable is none
            Hours = 0
        print("Ya se han registrado un total de: "+str(Hours)+" Horas")
        if Hours < 9:
            activarRoles()
            for row in data['entradas']:
                consulta = ""            
                consulta = 'INSERT INTO sgi.req_actividades (NUMERO_REQUERIMIENTO, TIPO, DESCRIPCION, FECHA, HORAS, USER_SISTEMA, FECHA_SISTEMA, ETAPA, ESTADO_DESDE, ESTADO_HASTA, RESPONSABLE_DESDE, RESPONSABLE_HASTA) VALUES ('+row['rq']+', '+row['act']+', '+"'"+row['description']+"'"+', sysdate, '+str(row['diff'])+', SYS_CONTEXT ('+"'USERENV'"+', '+"'SESSION_USER'"+'), sysdate, '+row['etapa']+', '+"'T'"+', '+"'T'"+', SYS_CONTEXT ('+"'USERENV'"+', '+"'SESSION_USER'"+'), SYS_CONTEXT ('+"'USERENV'"+', '+"'SESSION_USER'"+'))'
                print("====================================================================================================================================")
                print(consulta)
                print("====================================================================================================================================\n")
                cur.execute(consulta) 
            """ connection.rollback() """
            connection.commit()
            print("Se han registrado las actividades correctamente")
            finalizar()
            return True
    except  cx_Oracle.Error as error:
        print(error)
        print("Se ha presentado un error al registrar las actividades")
        finalizar()        
