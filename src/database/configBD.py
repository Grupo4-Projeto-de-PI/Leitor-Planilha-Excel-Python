from mysql.connector import connect, Error
import os
from dotenv import load_dotenv

# Arquivo de conexão com o banco de dados 
# Aqui tem função de Select e Insert no banco de dados

load_dotenv()

config = {
    "user": os.getenv("USER_LOGIN"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
    "database": os.getenv("DATABASE")
}

def insert(query):
    mydb = None
    try:
        mydb = connect(**config)
        if mydb.is_connected():
            
            mycursor = mydb.cursor()
            sql_query = query
            mycursor.execute(sql_query)
            mydb.commit()
            return mycursor.rowcount 
            
    except Error as e:
        print("Erro ao conectar com o MySQL", e)
    finally:
        if mydb and mydb.is_connected():
            mycursor.close()
            mydb.close()
            
def select(query):
    mydb = None
    try:
        mydb = connect(**config)
        if mydb.is_connected():
            
            mycursor = mydb.cursor()
            sql_query = query
            mycursor.execute(sql_query)
                    
            #Aqui será gravado os resultados encontrado no banco retorna uma lista de tuplas
            resultado = mycursor.fetchall() 
            return resultado

                
    except Error as e:
        print("Erro ao conectar com o MySQL", e)
    finally:
        if mydb and mydb.is_connected():
            mycursor.close()
            mydb.close()