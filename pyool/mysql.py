import mysql.connector 
import pandas as pd 
import os 
import time 
import csv 



# Defining MySQL specific class to work with 

class MySQLConnector: 

    def connect(self, db_name, host, port, user, password): 
        self.connection = mysql.connector.connect(
                                                    database = db_name,
                                                    host = host,
                                                    port = port,
                                                    user = user,
                                                    passwd = password
                                                    )

    
    def read_sql(self, file_path):
        with open(file_path, "r", encoding = "utf-8") as file:
            query  = file.read()

        return query 
    

    def extract_header(self, csv_file_path): 
        with open(csv_file_path, "r", newline = "") as file:
            reader = csv.reader(file)
            header = ",".join(next(reader))

        return header 


    def run_query(self, query, return_data = False):
        cur = self.connection.cursor()
        print("Start querying .....")
        cur.execute(query)

        if return_data == True:
            column_names = cur.column_names
            data = cur.fetchall()

            df = pd.DataFrame(data, columns = column_names) 
            print("Data is returned")
            return df 

        else: 
            print("Query is executed") 
            return True 

        cur.close() 

    def disconnect(self):
        self.connection.close() 
