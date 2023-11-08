import os
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ReadConfigs.readConfigs import readConfigFromFile

script_statuses = {}

config = readConfigFromFile()


def execute_script(script_name, ownerId, customerName, prv_customer_runtime_id, customerType, data):
    def run_script():
        try:
            # Add a print statement to indicate that the script is executing
            print("Script execution has been initiated.")
            run_TXN_DB_ENABLED(ownerId, customerName, prv_customer_runtime_id, data)
            run_UIUX_ENABLED(customerName, customerType, ownerId, prv_customer_runtime_id, data)
            run_WORKFLOW_ENABLED(customerName, customerType, ownerId, prv_customer_runtime_id, data)
            #run_RATING_ENABLED(prv_customer_runtime_id, ownerId, customerName, data)
            #run_REPORTING_DB_ENABLED(prv_customer_runtime_id, ownerId, customerName, data)
            print("All the requested services scripts has been executed.")
            # 1800 seconds = 30 minutes
        except subprocess.CalledProcessError as e:
            send_error_email(script_name, str(e))
        except subprocess.TimeoutExpired:
            send_error_email(script_name, "Script execution timed out after 30 minutes")
        # Update the script status to indicate that it has finished executing
        script_statuses[script_name] = "Completed"

    # Set the script status to "Running" before starting execution
    script_statuses[script_name] = "Running"
    run_script()


def send_error_email(script_name, error_message):
    sender_email = 'balakumaran_m@solartis.com'  # Replace with your email
    sender_password = 'qfrdqdbsljvrsslw'  # Replace with your email password
    receiver_email = 'sritharan_j@solartis.com'  # Replace with recipient's email

    subject = f"Error occurred while executing {script_name}"
    body = f"Error message: {error_message}"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print(f"Error email sent for {script_name}")
    except Exception as e:
        print(f"Failed to send error email for {script_name}: {str(e)}")


def run_TXN_DB_ENABLED(ownerId, customerName, prv_customer_runtime_id, data):
    #SCRIPTPATH = r"/opt/SB_Runtimeapi_Automation_Beta/Runtime_Scripts/transactiondb.sh"
    #SCRIPTPATH = r"/opt/config_env/Create_Transaction_Database_API/Create_Transaction_Database_API.sh"
    SCRIPTPATH = config.get('RuntimeScript', 'transactiondb')
    command_line = [SCRIPTPATH, customerName, ownerId, data.reportingDbEnabled,  prv_customer_runtime_id]
    if data.txnDbEnabled.lower() == 'yes':
        # Construct the command line arguments

        # Execute the shell script with the constructed command line
        result = subprocess.run(command_line, check=True)

        # Handle the result as needed
        if result.returncode != 0:
            send_error_email('Create_Transaction_Database_API.sh',
                             f'Script exited with non-zero return code: {result.returncode}')
        else:
            print("Create_Transaction_Database_API.sh executed")


def run_UIUX_ENABLED(customerName, customerType, ownerId, prv_customer_runtime_id, data):
    #SCRIPTPATH = r"/opt/SB_Runtimeapi_Automation_Beta/Runtime_Scripts/uiux.sh"
    #SCRIPTPATH = r"/opt/config_env/Create_UIUX_Runtime_API/Create_UIUX_Runtime_API.sh"
    SCRIPTPATH = config.get('RuntimeScript', 'uiux')
    command_line = [SCRIPTPATH, customerName, customerType, ownerId, prv_customer_runtime_id]
    if data.uiuxEnabled.lower() == 'yes':
        # Construct the command line arguments

        # Execute the shell script with the constructed command line
        result = subprocess.run(command_line, check=True)

        # Handle the result as needed
        if result.returncode != 0:
            send_error_email('Create_UIUX_Runtime_API.sh',
                             f'Script exited with non-zero return code: {result.returncode}')
        else:
            print("Create_UIUX_Runtime_API.sh executed")


def run_WORKFLOW_ENABLED(customerName, customerType, ownerId, prv_customer_runtime_id, data):
    #SCRIPTPATH = r"/opt/SB_Runtimeapi_Automation_Beta/Runtime_Scripts/wf.sh"
    #SCRIPTPATH = r"/opt/config_env/Create_Workflow_Microservice_Runtime_API/Create_Workflow_Microservice_Runtime_API.sh"
    SCRIPTPATH = SCRIPTPATH = config.get('RuntimeScript', 'workflow')
    command_line = [SCRIPTPATH, customerName, customerType, ownerId, prv_customer_runtime_id]
    if data.workflowEnabled.lower() == 'yes':
        # Construct the command line arguments

        # Execute the shell script with the constructed command line
        result = subprocess.run(command_line, check=True)

        # Handle the result as needed
        if result.returncode != 0:
            send_error_email('Create_WORKFLOW_Runtime_API.sh',
                             f'Script exited with non-zero return code: {result.returncode}')
        else:
            print("Create_WORKFLOW_Runtime_API.sh executed")


def run_RATING_ENABLED(customerName, customerType, ownerId, prv_customer_runtime_id, data):
    SCRIPTPATH = r"/opt/config_env/Create_Rating_Microservice_Runtime_API/Create_Rating_Microservice_Runtime_API.sh"
    command_line = [SCRIPTPATH, customerName, customerType, ownerId, prv_customer_runtime_id]
    if data.ratingEnabled.lower() == 'yes':
        # Construct the command line arguments

        # Execute the shell script with the constructed command line
        result = subprocess.run(command_line, check=True)

        # Handle the result as needed
        if result.returncode != 0:
            send_error_email('Create_RATING_Runtime_API.sh',
                             f'Script exited with non-zero return code: {result.returncode}')
        else:
            print("Create_RATING_Runtime_API.sh executed")


def run_REPORTING_DB_ENABLED(prv_customer_runtime_id, ownerId, customerName, data):
    SCRIPTPATH = r"/opt/config_env/Create_Transaction_Database_API/Create_Transaction_Database_API.sh"
   # print(f"print value {OWNER_ID}, {CUSTOMER_NAME}, {prv_customer_runtime_id}, {data.REPORTING_DB_ENABLED}")
    command_line = [SCRIPTPATH, customerName, ownerId, data.reportingDbEnabled, prv_customer_runtime_id]
    if data.reportingDbEnabled.lower() == 'yes':
        # Construct the command line arguments

        # Execute the shell script with the constructed command line
        result = subprocess.run(command_line, check=True)

        # Handle the result as needed
        if result.returncode != 0:
            send_error_email('Create_REPORTINGDB_Runtime_API.sh',
                             f'Script exited with non-zero return code: {result.returncode}')
        else:
            print("Create_REPORTINGDB_Runtime_API.sh executed")
