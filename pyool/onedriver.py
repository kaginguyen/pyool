from .logger_setting import logger 
from O365 import Account, MSGraphProtocol, oauth_authentication_flow


class OneDriver():

    def self_authenticate(self, client_id, client_secret):
        try: 
            oauth_authentication_flow(client_id, client_secret, scopes = ['onedrive'])
            return True 
        except Exception as e: 
            logger.error(e)  
            raise RuntimeError("Cannot query to OneDrive due to: {}".format(e)) 



    def connect(self, client_id, client_secret, user):
        credentials = (client_id, client_secret)

        try: 
            account = Account(credentials, main_resource = user)
            return account  
        except Exception as e: 
            logger.error(e)  
            raise RuntimeError("Cannot query to OneDrive due to: {}".format(e)) 



    def locate_root_folder(self, account): 
        root_folder = account.storage().get_default_drive().get_root_folder()
        return root_folder 

    
    
    def upload(self, folder, file_path_list):
        items = []
        
        try: 
            for file_path in file_path_list:
                item_object = folder.upload_file(item = file_path)
                items.append(item_object)
            return items 

        except Exception as e: 
            logger.error(e)  
            raise RuntimeError("Cannot query to OneDrive due to: {}".format(e)) 



