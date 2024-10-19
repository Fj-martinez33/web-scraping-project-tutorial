#Librerias

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import sqlite3

#Proporcionamos una URL

URL = "https://ycharts.com/companies/TSLA/revenues"

def DataSeeker(get_url):
    driver = webdriver.Chrome()
    driver.get(get_url)

    #Obtenemos el HTML
    raw_data = driver.find_elements(By.TAG_NAME, "tr")

    #Filtramos los datos que nos interesan

    data = []
    for i in raw_data:
        data.append(i.text)
        if ("General Motors Co" in str(i.text)):
            data.remove(i.text)
    
            break
    #Limpiamos la data
    for e in data:
        data.remove(e)
        if ("Date Value" in str(e)):
            data.remove(e)


    #Cerramos conexion
    driver.quit()
    return data

def SplitData(data):
    
    #Separamos los valores que queremos ingresar al DataFrame
    split_date = []
    date = []
    revenue = []
    for i in range(len(data)):
        revenue.append (data[i].split(" ")[-1])
        split_date.append(data[i].split(" ")[:3])
        date.append(" ".join(split_date[i]))
    return date, revenue

def TransformDataSet(col1, col2):
    #Creamos el Data Set
    dataset = pd.DataFrame(zip(col1, col2), columns=["Date","Revenue"])

    #Eliminamos las dos primeras filas innecesarias.
    dataset = dataset.drop(index=[0,1,2,3]).reset_index(drop = True)
    return dataset

def SaveIntoDB(dataset):
    # Nos conectamos a la base de datos

    con = sqlite3.connect("tesla.db")

    dataset.to_sql(name=("tesla_quaterly_revenue"), con = con, if_exists="replace", index=False)

    con.commit()
    
    return f"Database is uploaded."

#Ejecutamos las funciones

date, revenue = SplitData(DataSeeker(URL))

SaveIntoDB(TransformDataSet(date, revenue))
