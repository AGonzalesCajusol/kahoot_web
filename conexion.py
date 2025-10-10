import pymysql

def conectarbd():
    try:
        return pymysql.connect(
            host='preguntas-calculadoramateriales.e.aivencloud.com',
            user='avnadmin',
            password='AVNS_LFRg88CLhVu59pB2C0e',
            db='cuestionario',
            port=10416,
            cursorclass=pymysql.cursors.DictCursor
        )
    
    except pymysql.Error as error:
        return False
    
