
#Importing necessary libraries 
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.authorization.models import RoleAssignmentCreateParameters
from azure.identity import *
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobClient,BlobServiceClient
from azure.storage.queue import QueueClient,QueueMessage, QueueServiceClient
from azure.data.tables import TableServiceClient
import random
import ast
import uuid
import jwt
import time
#start code
def create_storage_account_and_container():
    #Checking the availability of the storage group name
    var= False
    while var != True:
        Base_name = f'{'floatingnimbus'}{random.randint(1,100)}'
        result = storage_client.storage_accounts.check_name_availability({'name':Base_name})
        var = result.name_available

    #Creating storage group
    poller = storage_client.storage_accounts.begin_create(
        resource_group_name = resource_group, account_name = Base_name , 
        parameters = { 'location': 'eastus', 'kind': 'StorageV2' , 'sku' : {'name' : 'Standard_LRS'}
                    }
    )

    poller_Results = poller.result()
    storage_account =  poller_Results.name

    #Creating Container
    
    containter = storage_client.blob_containers.create(
    resource_group_name = resource_group,
    account_name = storage_account,
    container_name = container_name,
    blob_container = {"metadata": {
            "category": "documents",
            "owner": "floating nimbus limited"}
                    }
    )
    
    return storage_account

def role_assignment(storage_account):
    new_guid_1 = uuid.uuid4()
    guid_str_1 = str(new_guid_1)
    new_guid_2 = uuid.uuid4()
    guid_str_2 = str(new_guid_2)
    new_guid_3 = uuid.uuid4()
    guid_str_3 = str(new_guid_3)
    credential = DefaultAzureCredential()
    
    authorization_client = AuthorizationManagementClient(credential, subscription_id)
    
    scope = f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Storage/storageAccounts/{storage_account}"

    #principle_id is the object_id
    role_assignment_params = RoleAssignmentCreateParameters(
        principal_id = '95fc57ec-1f99-4957-9a20-c59593b896bb' ,
        role_definition_id="/subscriptions/{subscription_id}/providers/Microsoft.Authorization/roleDefinitions/b7e6dc6d-f1e8-4753-8033-0f276bb0955b",
        scope=scope
    )
    role_assignment_params_2 = RoleAssignmentCreateParameters(
        principal_id = '95fc57ec-1f99-4957-9a20-c59593b896bb' ,
        role_definition_id="/subscriptions/{subscription_id}/providers/Microsoft.Authorization/roleDefinitions/974c5e8b-45b9-4653-ba55-5f855dd0fb88",
        scope=scope
    )
    role_assignment_params_3 = RoleAssignmentCreateParameters(
        principal_id = '95fc57ec-1f99-4957-9a20-c59593b896bb' ,
        role_definition_id="/subscriptions/{subscription_id}/providers/Microsoft.Authorization/roleDefinitions/0a9a7e1f-b9d0-4cc4-a60d-0319b160aaa3",
        scope=scope
    )

    # Create the role assignment
    role_assignment_1 = authorization_client.role_assignments.create(scope=scope, role_assignment_name = guid_str_1, parameters=role_assignment_params)
    role_assignment_2 = authorization_client.role_assignments.create(scope=scope, role_assignment_name = guid_str_2, parameters=role_assignment_params_2)
    role_assignment_3 = authorization_client.role_assignments.create(scope=scope, role_assignment_name = guid_str_3, parameters=role_assignment_params_3)
    
def upload_blob(storage_account):
    print("Upload any Document")
    path = input("Path for Document: ")
    account_url = "https://"+storage_account+".blob.core.windows.net/"
    
    #Extracting username
    token_bytes = credential.get_token(account_url).token
    decoded_token = jwt.decode(token_bytes, options={"verify_signature": False})
    user_name = decoded_token.get("name")
    
    #Generating a unique naming convention for document, as per the user
    var = True
    while var!= False:
        document_name = f'{user_name}{"-document-"}{random.randint(1,1000)}'
        
        #Setting up blob service client 
        blob_service_client = BlobServiceClient(account_url, credential = DefaultAzureCredential())
        blob_client = blob_service_client.get_blob_client(container = container_name, blob = document_name)
        if blob_client.exists() == False:
            with open(path, "rb") as data:
                blob_client.upload_blob(data)
            var = False    
            print (f'{"Document with convention "}{document_name}{" successfully created"}')
    blob_properties = blob_client.get_blob_properties()
    dt = blob_properties.creation_time
    date_time_string = dt.strftime("%Y-%m-%d %H:%M:%S")
    dict = {"name" : user_name , "time" : date_time_string,"url":f"{blob_service_client.url}{container_name}/{document_name}"} 
    return (dict)

def queue_upload(storage_account,credential):
    #Queue client setup
   
    queue_client= QueueClient(
        account_url= "https://"+storage_account+".queue.core.windows.net/", 
        queue_name = 'floating-queue' ,credential= credential )
    #Create a Queue
    queue_client.create_queue()
    #Enqueue
    enqueue = "yes"
    while enqueue != "no":
        blob_data = upload_blob(storage_account)
        queue_client.send_message(blob_data)
        enqueue = input("Upload another file?")
    
def dequeue(storage_account,credential,connection_string):
    #Get messsage off the queue
    table_client  = TableServiceClient.from_connection_string(conn_str=connection_string)
    table = table_client.create_table(table_name = "Nimbustable01")
    queue_client= QueueClient(
            account_url= "https://"+storage_account+".queue.core.windows.net/", 
            queue_name = 'floating-queue' ,credential= credential )
    while queue_client.get_queue_properties().approximate_message_count != 0:
        message = queue_client.receive_message()
        if message != None: 
            job_processor(message,connection_string,table)
            queue_client.delete_message(message)
        time.sleep(10)
    queue_client.delete_queue()

def job_processor(message,connection_string,table):
    string_data = message['content']
    # Initialize the TableServiceClient with the connection string
    table_client  = TableServiceClient.from_connection_string(conn_str=connection_string)
    data = ast.literal_eval(string_data)
    table_entity=table.create_entity(
    entity= {'PartitionKey':data['name'],
             'RowKey':data['time'],
             'Blob_URL':data['url']
            }
    )

    

if __name__ == "__main__":
    #Setting up storage management client
    
    subscription_id = '4fc7f2dc-e142-4948-8d0f-a8a6c7d9c167'
    resource_group = 'test-resource'
    container_name = 'nimbus-blob-container'
    
    credential = AzureCliCredential()
    storage_client = StorageManagementClient(credential,subscription_id)
    #Create a storage account for Organisation floatonnimbus
    storage_account = create_storage_account_and_container()
    role_assignment(storage_account)
    connection = input("enter key")
    connection_string = input("enter string")
    queue_upload(storage_account,connection)
    dequeue(storage_account,connection,connection_string)
    
  
    
  