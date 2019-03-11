import csv 
from datetime import datetime
from odps import ODPS 
import time 
import uuid 
import os 


# Defining ODPS specific class to work with 

class OdpsConnector: 

    def connect(self, accessId, accessKey, project, endPoint, tunnelEndPoint):
        self.connection = ODPS(
            access_id = accessId
            , secret_access_key = accessKey
            , project = project
            , endpoint = endPoint 
            ,tunnel_endpoint = tunnelEndPoint
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


    def run_query(self, query, return_data = False, retry_time = 3, buffering = 5):  
        
        attempt = 1

        while attempt <= retry_time:
            try:
                print("Querying.....")

                with self.connection.execute_sql(query, None, 1, hints = {"odps.sql.submit.mode" : "script"}).open_reader() as reader:
                    print("Query is finished")
                    if return_data == True: 
                        return reader.to_pandas()  
                    else: 
                        return reader 
            except Exception as e:
                attempt += 1
                error = "Attempt {}, error {}. Retrying ....."
                error = error.format(attempt, e) 
                print(error) 
                time.sleep(buffering) 
                continue  
        
        raise RuntimeError("Cannot query to ODPS due to: %s" % error) 


    def dump_to_csv(self, query, storage_path, filename = None, buffering = 5): 
        if not filename:
            filename = str(uuid.uuid4())

        filename = filename + ".csv"

        filepath = os.path.join(storage_path, filename)

        attemps = 0 

        while attemps < 3 :
            try: 
                reader = self.run_query(query)
                print("... Done dumping to csv file %s" % filename)
                with open(filepath, "w", encoding ="utf-8") as file:
                    writer = csv.writer(file, delimiter = ",", quoting = csv.QUOTE_NONNUMERIC
                                        , lineterminator = "\n")
                    
                    writer.writerow(reader._schema.names)

                    for record in reader: 
                        writer.writerow(record[0:])
                
                return filepath

            except Exception as e:
                attemps += 1
                print("Retrying... %s. Why: %s" % (attemps, e))
                time.sleep(buffering)
            else:
                break 











