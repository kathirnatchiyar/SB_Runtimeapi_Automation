#import uvicorn
import threading
# from SolartisConfig import db_connection
# from SolartisConfig import logger
from Solartismultiscript import execute_script, script_statuses
from SolartisFunction import process_data
from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
import os
from fastapi.responses import JSONResponse
import traceback
from datetime import datetime
from GetStatus.getStatus import getStatusCall
from Database.Connection import createProvisioningDbPooling
from Logger.logging import logger

log = logger(__name__)

app = FastAPI()


class CustomerData(BaseModel):
    ownerId: str
    project: str
    customerName: str
    customerType: str
    lineOfBusiness: str
    environmentType: str
    sbLoginUser: str
    active: str
    txnDbEnabled: str
    uiuxEnabled: str
    workflowEnabled: str
    ratingEnabled: str
    reportingDbEnabled: str


######API Key Authentication####
VALID_API_KEY = 'abcdefghijkl250899'

def authenticate_api_key(api_key):
    return api_key == VALID_API_KEY
    
@app.post('/createruntime')
async def insert_data_route(
    api_key: str = Header(None),
    data: CustomerData = None
):
    if not authenticate_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid authentication")

    required_fields = ["txnDbEnabled", "uiuxEnabled", "workflowEnabled", "ratingEnabled", "reportingDbEnabled"]
    if all(data.model_dump().get(field, "") == "No" for field in required_fields):
        response_data = {
            "request_data": data.model_dump(),
            "status": "Error",
            "message": "All required fields are set to 'No'. Data cannot be inserted."
        }
        return response_data

    missing_inputs = [key for key, value in data.model_dump().items() if not value]
    if missing_inputs:
        response_data = {
            "request_data": data.model_dump(),
            "status": "Input Missing",
            "message": "Input fields are missing.",
            "missing_inputs": missing_inputs
        }
        return response_data
      
    try:
        ProvisioningDbPoolingObject = createProvisioningDbPooling()
        ProvisioningDbConnection = ProvisioningDbPoolingObject.get_connection()   
        cursor_customer = ProvisioningDbConnection.cursor()
        cursor_runtime = ProvisioningDbConnection.cursor()
        cursor_customer.execute("SELECT * FROM PRV_CUSTOMER WHERE OWNER_ID = %s", (data.ownerId,))
        existing_row = cursor_customer.fetchone()

        if existing_row:
            response_data = {
                "request_data": data.model_dump(),
                "status": "Error",
                "message": f"Customer with owner ID {data.ownerId} already exists."
            }
            return response_data

        process_data(data, cursor_customer, cursor_runtime)
        ProvisioningDbConnection.commit()
        log.info(f"Data inserted into the database for OWNER_ID: {data.ownerId}")

        # Fetch the PRV_CUSTOMER_RUNTIME_ID after process_data is executed
        cursor_runtime.execute("SELECT PRV_CUSTOMER_RUNTIME_ID FROM PRV_CUSTOMER_RUNTIME WHERE PRV_CUSTOMER_ID = %s",
                               (data.ownerId,))
        prv_customer_runtime_id = cursor_runtime.fetchone()[0]
        print(f"the value is {prv_customer_runtime_id}")
        script_name = 'your_script.py'

        thread = threading.Thread(target=execute_script,
                                  args=(script_name, data.ownerId, data.customerName, prv_customer_runtime_id,
                                        data.customerType, data))
        thread.start()

        script_statuses[data.ownerId] = "InProgress"
        log.info(f"Data insertion and script execution initiated for OWNER_ID: {data.ownerId}")

        response_data = {
            "request_data": data.model_dump(),
            "status": "In progress",
            "message": "Data inserted and script execution initiated."
        }

        return response_data

    finally:
        cursor_customer.close()
        cursor_runtime.close()


@app.post('/updateruntime')
async def update_data_route(
    api_key: str = Header(None),
    data: CustomerData = None
):
    if not authenticate_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid authentication")
        
    try:
        ProvisioningDbPoolingObject = createProvisioningDbPooling()
        ProvisioningDbConnection = ProvisioningDbPoolingObject.get_connection() 
        cursor_customer = ProvisioningDbConnection.cursor()
        cursor_runtime = ProvisioningDbConnection.cursor()
        cursor_customer.execute("SELECT * FROM PRV_CUSTOMER WHERE PRV_CUSTOMER_ID = %s", (data.ownerId,))
        existing_row = cursor_customer.fetchone()

        if not existing_row:
            response_data = {
                "request_data": data.model_dump(),
                "status": "Error",
                "message": f"OWNERID {data.ownerId} does not exist."
            }
            return response_data

# Check if all the required fields are "No"
        required_fields = ["txnDbEnabled", "uiuxEnabled", "workflowEnabled", "ratingEnabled",
                           "reportingDbEnabled"]
        if all(data.model_dump().get(field, "") == "No" for field in required_fields):
            response_data = {
                "request_data": data.model_dump(),
                "status": "Error",
                "message": "All required fields are set to 'No'. Data cannot be updated."
            }
            return response_data

        missing_inputs = [key for key, value in data.model_dump().items() if not value]

        if missing_inputs:
            response_data = {
                "request_data": data.model_dump(),
                "status": "Input Missing",
                "message": "Input fields are missing.",
                "missing_inputs": missing_inputs
            }
            return response_data

        # Create a dictionary to map field names to database column names
        field_to_column_mapping = {
            "TXN_DB_ENABLED": "TXN_DB_ENABLED",
            "UIUX_ENABLED": "UIUX_ENABLED",
            "WORKFLOW_ENABLED": "WORKFLOW_ENABLED",
            "RATING_ENABLED": "RATING_ENABLED",
            "REPORTING_DB_ENABLED": "REPORTING_DB_ENABLED",
        }

        # Update only the fields with "Yes" values in the database
        for field, db_column in field_to_column_mapping.items():
            if data.model_dump().get(field, "") == "Yes":
                update_query = f"""
                    UPDATE PRV_CUSTOMER_RUNTIME
                    SET {db_column} = 'Yes', UPDATED_BY = 'bala', UPDATED_DATE = NOW()
                    WHERE PRV_CUSTOMER_ID = %s
                """
                cursor_runtime.execute(update_query, (data.ownerId,))

        ProvisioningDbConnection.commit()
        log.info(f"Data inserted into the database for OWNER_ID: {data.ownerId}")
        cursor_runtime.execute("SELECT PRV_CUSTOMER_RUNTIME_ID FROM PRV_CUSTOMER_RUNTIME WHERE PRV_CUSTOMER_ID = %s",
                               (data.ownerId,))
        prv_customer_runtime_id = cursor_runtime.fetchone()[0]
        print(f"the value is     {prv_customer_runtime_id}")
        script_name = 'your_script.py'

        thread = threading.Thread(target=execute_script,
                                  args=(script_name, data.ownerId, data.customerName, prv_customer_runtime_id,
                                        data.customerType, data))
        thread.start()

        script_statuses[data.ownerId] = "InProgress"
        log.info(f"Data insertion and script execution initiated for OWNER_ID: {data.ownerId}")

        response_data = {
            "request_data": data.model_dump(),
            "status": "Success",
            "message": f"Data updated and script execution initiated",
        }

        return response_data

    finally:
        cursor_customer.close()
        cursor_runtime.close()


@app.post('/getstatus')

def getstatus( request : Request, data: dict = None, api_key: str = Header(None) ):
    rheaders = request.headers

    if not authenticate_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid authentication")
    
    # Verifying the input data 
    RequiredInputs = [ "ownerId", "customerName", "customerType", "lineOfBusiness", "environmentType", "sbLoginUser" ]
    errormsg=""
    for key in RequiredInputs:
        if ( key not in data ) or ( data[key] == ''):
            errormsg = "{} is invalid or not provided in input. check and try again".format(key)
            print(errormsg)
            message = errormsg
            break
    if errormsg != "":   
        resp_json =  {
                    "message": errormsg
        }
        return JSONResponse(status_code=400, content=resp_json)
    
    
    # Calling getStatusCall with inputData
    resp_json = getStatusCall(data)
    return resp_json

if __name__ == "__main__":
   uvicorn.run(app, host="127.0.0.1", port=5006)
