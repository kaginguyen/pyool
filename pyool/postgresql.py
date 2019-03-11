import psycopg2 
import pandas as pd 
import csv 
import os 
import time 


# Defining PostgreSQL Database specific Class to work with

class PostgreSQLConnector: 
    def connect(self, db_name, host, port, user, password):
        self.connection  = psycopg2.connect(dbname = db_name
                                            , host = host
                                            , port = port
                                            , user = user
                                            , password = password) 


    def disconnect(self):
        self.connection.close() 


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
        cur.execute(query) 

        if return_data == True: 
            data = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            df = pd.DataFrame(data, columns = column_names) 
            print("Data is returned")
            return df 

        else: 
            self.connection.commit()
            print("Query is executed")  
            return True 

        cur.close() 
        

    def truncate(self, table):
        cur = self.connection.cursor()
        cur.execute("TRUNCATE TABLE %s" % (table)) 


    def uploadCsv(self, filepath, table, fields, truncate = False, remove_file = False):
        if truncate == True: 
            self.truncate(table)
            print("Table truncated. Start uploading...")

        cur = self.connection.cursor()

        attemps = 0

        while attemps < 3:
            try: 
                with open(filepath, 'r', encoding='utf-8') as f:
                    sql = "COPY %s(%s) FROM STDIN WITH ( DELIMITER ',', FORMAT CSV, HEADER, ENCODING 'UTF8', FORCE_NULL(%s))" % (table, fields, fields) 
                    cur.copy_expert(sql, f) 
                    self.connection.commit()

            except Exception as e:
                attemps += 1
                print("Retrying... %s. Why: %s" % (attemps, e))
                time.sleep(5)
            else:
                break  

        if remove_file == True:
            os.remove(filepath) 
        
        return True 