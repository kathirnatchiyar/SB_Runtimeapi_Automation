from Database.Connection import createProvisioningDbPooling
from datetime import datetime
from fastapi.responses import JSONResponse
from Logger.logging import logger

log = logger(__name__)

def getStatusCall(data): 
    log.debug("inside the getStatusCall")
    # Initializing default Values for response
    transactionDB_Status = "NA"
    masterdevDb_Name = "NA"
    masterdevDb_CreatedBy = "NA"
    masterdevDb_CreatedDate = "NA"
    masterdevDb_UpdatedBy = "NA"
    masterdevDb_UpdatedDate = "NA"
    masterdevDb_Datasource = "NA"
    mastertestDb_Name = "NA"
    mastertestDb_CreatedBy = "NA"
    mastertestDb_CreatedDate = "NA"
    mastertestDb_UpdatedBy = "NA"
    mastertestDb_UpdatedDate = "NA"
    mastertestDb_Datasource = "NA"
    masterliveDb_Name = "NA"
    masterliveDb_CreatedBy = "NA"
    masterliveDb_CreatedDate = "NA"
    masterliveDb_UpdatedBy = "NA"
    masterliveDb_UpdatedDate = "NA"
    masterliveDb_Datasource = "NA"
    slavedevDb_Name = "NA"
    slavedevDb_CreatedBy = "NA"
    slavedevDb_CreatedDate = "NA"
    slavedevDb_UpdatedBy = "NA"
    slavedevDb_UpdatedDate = "NA"
    slavedevDb_Datasource = "NA"
    slavetestDb_Name = "NA"
    slavetestDb_CreatedBy = "NA"
    slavetestDb_CreatedDate = "NA"
    slavetestDb_UpdatedBy = "NA"
    slavetestDb_UpdatedDate = "NA"
    slavetestDb_Datasource = "NA"
    slaveliveDb_Name = "NA"
    slaveliveDb_CreatedBy = "NA"
    slaveliveDb_CreatedDate = "NA"
    slaveliveDb_UpdatedBy = "NA"
    slaveliveDb_UpdatedDate = "NA"
    slaveliveDb_Datasource = "NA"
    reportdevDb_Name = "NA"
    reportdevDb_CreatedBy = "NA"
    reportdevDb_CreatedDate = "NA"
    reportdevDb_UpdatedBy = "NA"
    reportdevDb_UpdatedDate = "NA"
    reportdevDb_Datasource = "NA"
    reporttestDb_Name = "NA"
    reporttestDb_CreatedBy = "NA"
    reporttestDb_CreatedDate = "NA"
    reporttestDb_UpdatedBy = "NA"
    reporttestDb_UpdatedDate = "NA"
    reporttestDb_Datasource = "NA"
    reportliveDb_Name = "NA"
    reportliveDb_CreatedBy = "NA"
    reportliveDb_CreatedDate = "NA"
    reportliveDb_UpdatedBy = "NA"
    reportliveDb_UpdatedDate = "NA"
    reportliveDb_Datasource = "NA"
    uiux_Status = "NA"
    uiuxDev_CreatedBy = "NA"
    uiuxDev_CreatedDate = "NA"
    uiuxDev_UpdatedBy = "NA"
    uiuxDev_UpdatedDate = "NA"
    uiuxDev_endPointURL = "NA"
    uiuxTest_CreatedBy = "NA"
    uiuxTest_CreatedDate = "NA"
    uiuxTest_UpdatedBy = "NA"
    uiuxTest_UpdatedDate = "NA"
    uiuxTest_endPointURL = "NA"
    uiuxLive_CreatedBy = "NA"
    uiuxLive_CreatedDate = "NA"
    uiuxLive_UpdatedBy = "NA"
    uiuxLive_UpdatedDate = "NA"
    uiuxLive_endPointURL = "NA"
    uiux_gitUrl_resourceUrl = "NA"
    workflow_Status = "NA"
    workflow_CreatedDate = "NA"
    workflow_UpdatedDate = "NA"
    workflow_CreatedBy = "NA"
    workflow_UpdatedBy = "NA"
    workflow_serverGroupName = "NA"
    workflow_endPointURL = "NA"
    workflow_gitUrl_sourcecodeUrl = "NA"
    rating_Status = "NA"
    rating_CreatedDate = "NA"
    rating_UpdatedDate = "NA"
    rating_CreatedBy = "NA"
    rating_UpdatedBy = "NA"
    rating_endPointURL = "NA"
    rating_gitUrl_sourcecodeUrl = "NA"
    formsGitUrl = "NA"
    dbVersionGiturl = "NA"
    jenkinsUrl_dmlsqlextractor = "NA"
    jenkinsUrl_ddlsqlextractor = "NA"
    jenkinsUrl_customerpipeline = "NA"
    jenkinsUrl_Adoptionpipeline ="NA"
    jenkinsUrl_bpmnrestartedpipeline = "NA"
    message="NA"
    retCode=200
    
        
    ownerId=data["ownerId"]
    customerName=data["customerName"]
    customerType=data["customerType"]
    lineOfBusiness=data["lineOfBusiness"]
    environmentType=data["environmentType"]
    sbLoginUser=data["sbLoginUser"]
    
    # Getting DB pool from createProvisioningDbPooling
    try:    
        ProvisioningDbPoolingObject = createProvisioningDbPooling()
        ProvisioningDbConnection = ProvisioningDbPoolingObject.get_connection()
        PrvDBcursor = ProvisioningDbConnection.cursor()
        
        try:
            # Gathering RUNTIME Status, etc
            logCustomerRuntimeQuery = """SELECT lcr.RUNTIME, lcr.STATUS etc
            FROM PRV_CUSTOMER as pc 
            JOIN PRV_CUSTOMER_RUNTIME as pcr ON pc.PRV_CUSTOMER_ID = pcr.PRV_CUSTOMER_ID
            JOIN LOG_CUSTOMER_RUNTIME as lcr ON pcr.PRV_CUSTOMER_RUNTIME_ID = lcr.PRV_CUSTOMER_RUNTIME_ID
            WHERE pc.OWNER_ID = %s AND pc.CUSTOMER_NAME = %s AND pc.CUSTOMER_TYPE = %s AND pc.LOB = %s AND pc.ENVIRONMENT = %s"""

            PrvDBcursor.execute(logCustomerRuntimeQuery,(ownerId,customerName,customerType,lineOfBusiness,environmentType))
            
            logCustomerRuntimeQueryOut = PrvDBcursor.fetchall()
            log.debug(logCustomerRuntimeQueryOut)
            if logCustomerRuntimeQueryOut:
                for queryOut in logCustomerRuntimeQueryOut:
                    if queryOut[0] == 'TXN_DB':
                        transactionDB_Status = queryOut[1]
                    elif queryOut[0] == 'UIUX':
                        uiux_Status = queryOut[1]
                    elif queryOut[0] == 'RATING':
                        rating_Status = queryOut[1]
                    elif queryOut[0] == 'WORKFLOW':
                        workflow_Status = queryOut[1]
                    else:
                        log.error("Unknow runtime name found is : ", queryOut[0])
            else:
                errormsg = "Couldn't find any RUNTIME tasks in LOG_CUSTOMER_RUNTIME table for OwnerId: {}, customerName: {}, customerType: {},  lineofBusiness: {}, environmentType: {} ".format(ownerID, customerName, customerType, lineofBusiness, environmentType )
                log.error(errormsg)
                message = errormsg
                retCode = 400
                                
            # Gathering DB details like DB Name, CreatedBy, UpdatedBy, CreatedDate, UpdatedDate etc
            
            prvCustomerDbRuntimeQuery = """SELECT pcdr.DB_TYPE, pcdr.MODE, pcdr.DB_NAME, pcdr.CREATED_BY, pcdr.UPDATED_BY, pcdr.CREATED_DATE, pcdr.UPDATED_DATE, pcdr.DATASOURCE_NAME
            FROM PRV_CUSTOMER as pc 
            JOIN PRV_CUSTOMER_RUNTIME as pcr ON pc.PRV_CUSTOMER_ID = pcr.PRV_CUSTOMER_ID
            JOIN PRV_CUSTOMER_DB_RUNTIME as pcdr ON pcr.PRV_CUSTOMER_RUNTIME_ID = pcdr.PRV_CUSTOMER_RUNTIME_ID
            WHERE pc.OWNER_ID = %s AND pc.CUSTOMER_NAME = %s AND pc.CUSTOMER_TYPE = %s AND pc.LOB = %s AND pc.ENVIRONMENT = %s"""

            PrvDBcursor.execute(prvCustomerDbRuntimeQuery,(ownerId,customerName,customerType,lineOfBusiness,environmentType))
            
            prvCustomerDbRuntimeQueryOut = PrvDBcursor.fetchall()
            
            if prvCustomerDbRuntimeQueryOut:
                for queryOut in prvCustomerDbRuntimeQueryOut:
                    if queryOut[0] == 'Transaction_Master' and (queryOut[1] == 'DEV'):
                        masterdevDb_Name = queryOut[2]
                        masterdevDb_CreatedBy = queryOut[3]
                        masterdevDb_UpdatedBy = queryOut[4]
                        masterdevDb_CreatedDate = queryOut[5].isoformat()
                        masterdevDb_UpdatedDate = queryOut[6].isoformat()
                        masterdevDb_Datasource = queryOut[7]
                    elif queryOut[0] == 'Transaction_Master' and (queryOut[1] == 'TEST'):
                        mastertestDb_Name = queryOut[2]
                        mastertestDb_CreatedBy = queryOut[3]
                        mastertestDb_UpdatedBy = queryOut[4]
                        mastertestDb_CreatedDate = queryOut[5].isoformat()
                        mastertestDb_UpdatedDate = queryOut[6].isoformat()
                        mastertestDb_Datasource = queryOut[7]
                    elif queryOut[0] == 'Transaction_Master' and (queryOut[1] == 'LIVE'):
                        masterliveDb_Name = queryOut[2]
                        masterliveDb_CreatedBy = queryOut[3]
                        masterliveDb_UpdatedBy = queryOut[4]
                        masterliveDb_CreatedDate = queryOut[5].isoformat()
                        masterliveDb_UpdatedDate = queryOut[6].isoformat()
                        masterliveDb_Datasource = queryOut[7]
                        # log.debug("transactionDB_dbName : ", transactionDB_dbName)
                    elif queryOut[0] == 'Transaction_Slave' and (queryOut[1] == 'DEV'):
                        slavedevDb_Name = queryOut[2]
                        slavedevDb_CreatedBy = queryOut[3]
                        slavedevDb_UpdatedBy = queryOut[4]
                        slavedevDb_CreatedDate = queryOut[5].isoformat()
                        slavedevDb_UpdatedDate = queryOut[6].isoformat()
                        slavedevDb_Datasource = queryOut[7]
                    elif queryOut[0] == 'Transaction_Slave' and (queryOut[1] == 'TEST'):
                        slavetestDb_Name = queryOut[2]
                        slavetestDb_CreatedBy = queryOut[3]
                        slavetestDb_UpdatedBy = queryOut[4]
                        slavetestDb_CreatedDate = queryOut[5].isoformat()
                        slavetestDb_UpdatedDate = queryOut[6].isoformat()
                        slavetestDb_Datasource = queryOut[7]
                    elif queryOut[0] == 'Transaction_Slave' and (queryOut[1] == 'LIVE'):
                        slaveliveDb_Name = queryOut[2]
                        slaveliveDb_CreatedBy = queryOut[3]
                        slaveliveDb_UpdatedBy = queryOut[4]
                        slaveliveDb_CreatedDate = queryOut[5].isoformat()
                        slaveliveDb_UpdatedDate = queryOut[6].isoformat()
                        slaveliveDb_Datasource = queryOut[7]
                        # log.debug("transactionDB_dbName : ", transactionDB_dbName)
                    elif queryOut[0] == 'Transaction_Report' and (queryOut[1] == 'DEV'):
                        reportdevDb_Name = queryOut[2]
                        reportdevDb_CreatedBy = queryOut[3]
                        reportdevDb_UpdatedBy = queryOut[4]
                        reportdevDb_CreatedDate = queryOut[5].isoformat()
                        reportdevDb_UpdatedDate = queryOut[6].isoformat()
                        reportdevDb_Datasource = queryOut[7]
                    elif queryOut[0] == 'Transaction_Report' and (queryOut[1] == 'TEST'):
                        reporttestDb_Name = queryOut[2]
                        reporttestDb_CreatedBy = queryOut[3]
                        reporttestDb_UpdatedBy = queryOut[4]
                        reporttestDb_CreatedDate = queryOut[5].isoformat()
                        reporttestDb_UpdatedDate = queryOut[6].isoformat()
                        reporttestDb_Datasource = queryOut[7]
                    elif queryOut[0] == 'Transaction_Report' and (queryOut[1] == 'LIVE'):
                        reportliveDb_Name = queryOut[2]
                        reportliveDb_CreatedBy = queryOut[3]
                        reportliveDb_UpdatedBy = queryOut[4]
                        reportliveDb_CreatedDate = queryOut[5].isoformat()
                        reportliveDb_UpdatedDate = queryOut[6].isoformat()
                        reportliveDb_Datasource = queryOut[7]
                        # log.debug("transactionDB_slaveDbName : ", transactionDB_slaveDbName)      
            else:
                errormsg = "Couldn't find DB details PRV_CUSTOMER_DB_RUNTIME table for ownerId: {}, customerName: {}, customerType: {},  lineOfBusiness: {}, environmentType: {} ".format(ownerId, customerName, customerType, lineOfBusiness, environmentType )
                log.error(errormsg)
                # message = errormsg
                # retCode = 400
            
            # Gathering UIUX details like UIUX URL, CreatedBy, UpdatedBy, CreatedDate, UpdatedDate etc
            
            prvCustomerUiuxRuntimeQuery = """SELECT pcur.MODE, pcur.UIUX_URL, pcur.CREATED_BY, pcur.UPDATED_BY, pcur.CREATED_DATE, pcur.UPDATED_DATE
            FROM PRV_CUSTOMER as pc 
            JOIN PRV_CUSTOMER_RUNTIME as pcr ON pc.PRV_CUSTOMER_ID = pcr.PRV_CUSTOMER_ID
            JOIN PRV_CUSTOMER_UIUX_RUNTIME as pcur ON pcr.PRV_CUSTOMER_RUNTIME_ID = pcur.PRV_CUSTOMER_RUNTIME_ID
            WHERE pc.OWNER_ID = %s AND pc.CUSTOMER_NAME = %s AND pc.CUSTOMER_TYPE = %s AND pc.LOB = %s AND pc.ENVIRONMENT = %s"""

            PrvDBcursor.execute(prvCustomerUiuxRuntimeQuery,(ownerId,customerName,customerType,lineOfBusiness,environmentType))
            
            prvCustomerUiuxRuntimeQueryOut = PrvDBcursor.fetchall()
            
            if prvCustomerUiuxRuntimeQueryOut:
                for queryOut in prvCustomerUiuxRuntimeQueryOut:
                    if queryOut[0] == 'DEV':
                        uiuxDev_endPointURL = queryOut[1]
                        uiuxDev_CreatedBy = queryOut[2]
                        uiuxDev_UpdatedBy = queryOut[3]
                        uiuxDev_CreatedDate = queryOut[4].isoformat()
                        uiuxDev_UpdatedDate = queryOut[5].isoformat()
                    elif queryOut[0] == 'TEST':
                        uiuxTest_endPointURL = queryOut[1]
                        uiuxTest_CreatedBy = queryOut[2]
                        uiuxTest_UpdatedBy = queryOut[3]
                        uiuxTest_CreatedDate = queryOut[4].isoformat()
                        uiuxTest_UpdatedDate = queryOut[5].isoformat()
                    elif queryOut[0] == 'LIVE':
                        uiuxLive_endPointURL = queryOut[1]
                        uiuxLive_CreatedBy = queryOut[2]
                        uiuxLive_UpdatedBy = queryOut[3]
                        uiuxLive_CreatedDate = queryOut[4].isoformat()
                        uiuxLive_UpdatedDate = queryOut[5].isoformat()          
            else:
                errormsg = "Couldn't find UIUX RUNTIME details PRV_CUSTOMER_UIUX_RUNTIME table for ownerId: {}, customerName: {}, customerType: {},  lineOfBusiness: {}, environmentType: {} ".format(ownerId, customerName, customerType, lineOfBusiness, environmentType )
                log.info(errormsg)
                # message = errormsg
                # retCode = 400
           
            # Gathering RATING details like RATING URL, CreatedBy, UpdatedBy, CreatedDate, UpdatedDate etc
            
            prvCustomerRatingRuntimeQuery = """SELECT pcrr.MODE, pcrr.RATING_URL, pcrr.CREATED_BY, pcrr.UPDATED_BY, pcrr.CREATED_DATE, pcrr.UPDATED_DATE
            FROM PRV_CUSTOMER as pc 
            JOIN PRV_CUSTOMER_RUNTIME as pcr ON pc.PRV_CUSTOMER_ID = pcr.PRV_CUSTOMER_ID
            JOIN PRV_CUSTOMER_RATING_RUNTIME as pcrr ON pcr.PRV_CUSTOMER_RUNTIME_ID = pcrr.PRV_CUSTOMER_RUNTIME_ID
            WHERE pc.OWNER_ID = %s AND pc.CUSTOMER_NAME = %s AND pc.CUSTOMER_TYPE = %s AND pc.LOB = %s AND pc.ENVIRONMENT = %s"""

            PrvDBcursor.execute(prvCustomerRatingRuntimeQuery,(ownerId,customerName,customerType,lineOfBusiness,environmentType))
            
            prvCustomerRatingRuntimeQueryOut = PrvDBcursor.fetchall()
            
            if prvCustomerRatingRuntimeQueryOut:
                for queryOut in prvCustomerRatingRuntimeQueryOut:
                    if queryOut[0] == 'DEV':
                        rating_endPointURL = queryOut[1]
                        rating_CreatedBy = queryOut[2]
                        rating_UpdatedBy = queryOut[3]
                        rating_CreatedDate = queryOut[4].isoformat()
                        rating_UpdatedDate = queryOut[5].isoformat()
                    elif queryOut[0] == 'TEST':
                        rating_endPointURL = queryOut[1]
                        rating_CreatedBy = queryOut[2]
                        rating_UpdatedBy = queryOut[3]
                        rating_CreatedDate = queryOut[4].isoformat()
                        rating_UpdatedDate = queryOut[5].isoformat()
                    elif queryOut[0] == 'LIVE':
                        rating_endPointURL = queryOut[1]
                        rating_CreatedBy = queryOut[2]
                        rating_UpdatedBy = queryOut[3]
                        rating_CreatedDate = queryOut[4].isoformat()
                        rating_UpdatedDate = queryOut[5].isoformat()
                    else:
                        errormsg = "Couldn't find RATING RUNTIME details PRV_CUSTOMER_RATING_RUNTIME table for ownerId: {}, customerName: {}, customerType: {},  lineOfBusiness: {}, environmentType: {} ".format(ownerId, customerName, customerType, lineOfBusiness, environmentType )
                        log.info(errormsg)
                        # message = errormsg
                        # retCode = 400
            else:
                errormsg = "Couldn't find RATING RUNTIME details PRV_CUSTOMER_RATING_RUNTIME table for ownerId: {}, customerName: {}, customerType: {},  lineOfBusiness: {}, environmentType: {} ".format(ownerId, customerName, customerType, lineOfBusiness, environmentType )
                log.info(errormsg)
                # message = errormsg
                # retCode = 400

            # Gathering WORKFLOW details like WORKFLOW URL, CreatedBy, UpdatedBy, CreatedDate, UpdatedDate etc
            
            prvCustomerWFRuntimeQuery = """SELECT pcwr.MODE, pcwr.SERVER_GROUP_NAME, pcwr.WORKFLOW_URL, pcwr.CREATED_BY, pcwr.UPDATED_BY, pcwr.CREATED_DATE, pcwr.UPDATED_DATE
            FROM PRV_CUSTOMER as pc 
            JOIN PRV_CUSTOMER_RUNTIME as pcr ON pc.PRV_CUSTOMER_ID = pcr.PRV_CUSTOMER_ID
            JOIN PRV_CUSTOMER_WORKFLOW_RUNTIME as pcwr ON pcr.PRV_CUSTOMER_RUNTIME_ID = pcwr.PRV_CUSTOMER_RUNTIME_ID
            WHERE pc.OWNER_ID = %s AND pc.CUSTOMER_NAME = %s AND pc.CUSTOMER_TYPE = %s AND pc.LOB = %s AND pc.ENVIRONMENT = %s"""

            PrvDBcursor.execute(prvCustomerWFRuntimeQuery,(ownerId,customerName,customerType,lineOfBusiness,environmentType))
            
            prvCustomerWFRuntimeQueryOut = PrvDBcursor.fetchall()
            
            if prvCustomerWFRuntimeQueryOut:
                for queryOut in prvCustomerWFRuntimeQueryOut:
                    if queryOut[0] == 'DEV':
                        workflow_serverGroupName = queryOut[1]
                        workflow_endPointURL = queryOut[2]
                        workflow_CreatedBy = queryOut[3]
                        workflow_UpdatedBy = queryOut[4]
                        workflow_CreatedDate = queryOut[5].isoformat()
                        workflow_UpdatedDate = queryOut[6].isoformat()
                    elif queryOut[0] == 'TEST':
                        workflow_serverGroupName = queryOut[1]
                        workflow_endPointURL = queryOut[2]
                        workflow_CreatedBy = queryOut[3]
                        workflow_UpdatedBy = queryOut[4]
                        workflow_CreatedDate = queryOut[5].isoformat()
                        workflow_UpdatedDate = queryOut[6].isoformat()
                    elif queryOut[0] == 'LIVE':
                        workflow_serverGroupName = queryOut[1]
                        workflow_endPointURL = queryOut[2]
                        workflow_CreatedBy = queryOut[3]
                        workflow_UpdatedBy = queryOut[4]
                        workflow_CreatedDate = queryOut[5].isoformat()
                        workflow_UpdatedDate = queryOut[6].isoformat()
                    else:
                        errormsg = "Couldn't find WORKFLOW RUNTIME details PRV_CUSTOMER_WORFLOW_RUNTIME table for ownerId: {}, customerName: {}, customerType: {},  lineOfBusiness: {}, environmentType: {} ".format(ownerId, customerName, customerType, lineOfBusiness, environmentType )
                        log.info(errormsg)
                        # message = errormsg
                        # retCode = 400
            else:
                errormsg = "Couldn't find WORKFLOW RUNTIME details PRV_CUSTOMER_WORFLOW_RUNTIME table for ownerId: {}, customerName: {}, customerType: {},  lineOfBusiness: {}, environmentType: {} ".format(ownerId, customerName, customerType, lineOfBusiness, environmentType )
                log.info(errormsg)
                # message = errormsg
                # retCode = 400
    
            # Gathering Customer Jenkins details like Jenkins URL, etc.
            
            prvCustomerJenkinsPipelineQuery = """SELECT pcjp.JOB_TYPE, pcjp.JENKINS_URL
            FROM PRV_CUSTOMER as pc 
            JOIN PRV_CUSTOMER_JENKINS_PIPELINE as pcjp ON pc.PRV_CUSTOMER_ID = pcjp.PRV_CUSTOMER_ID
            WHERE pc.OWNER_ID = %s AND pc.CUSTOMER_NAME = %s AND pc.CUSTOMER_TYPE = %s AND pc.LOB = %s AND pc.ENVIRONMENT = %s"""

            PrvDBcursor.execute(prvCustomerJenkinsPipelineQuery,(ownerId,customerName,customerType,lineOfBusiness,environmentType))
            
            prvCustomerJenkinsPipelineQueryOut = PrvDBcursor.fetchall()
            
            log.debug(prvCustomerJenkinsPipelineQueryOut)
            if prvCustomerJenkinsPipelineQueryOut:
                for queryOut in prvCustomerJenkinsPipelineQueryOut:
                    if queryOut[0] == 'CUSTOMERPIPELINE':
                        jenkinsUrl_customerpipeline = queryOut[1]
                    elif queryOut[0] == 'ADOPTIONPIPELINE':
                        jenkinsUrl_Adoptionpipeline = queryOut[1]
                    elif queryOut[0] == 'DMLSQLEXTRACTOR':
                        jenkinsUrl_dmlsqlextractor = queryOut[1]
                    elif queryOut[0] == 'DDLSQLEXTRACTOR':
                        jenkinsUrl_ddlsqlextractor = queryOut[1]
                    elif queryOut[0] == 'BPMNRESTARTER':
                        jenkinsUrl_bpmnrestartedpipeline = queryOut[1]
            else:
                errormsg = "Couldn't find CUSTOMER JENKINS details PRV_CUSTOMER_JENKINS_PIPELINE table for ownerId: {}, customerName: {}, customerType: {},  lineOfBusiness: {}, environmentType: {} ".format(ownerId, customerName, customerType, lineOfBusiness, environmentType )
                log.info(errormsg)
                # message = errormsg
                # retCode = 400
                
            # Gathering Customer REPO URL details like REPO URL, etc
            
            prvCustomerrepourlQuery = """SELECT pcru.MODULE, pcru.GIT_REPO_TYPE, pcru.GIT_URL
                        FROM PRV_CUSTOMER as pc 
                        JOIN PRV_CUSTOMER_REPO_URL as pcru ON pc.PRV_CUSTOMER_ID = pcru.PRV_CUSTOMER_ID
                        WHERE pc.OWNER_ID = %s AND pc.CUSTOMER_NAME = %s AND pc.CUSTOMER_TYPE = %s AND pc.LOB = %s AND pc.ENVIRONMENT = %s"""

            PrvDBcursor.execute(prvCustomerrepourlQuery,(ownerId,customerName,customerType,lineOfBusiness,environmentType))
                        
            prvCustomerrepourlQueryOut = PrvDBcursor.fetchall()
            
            if prvCustomerrepourlQueryOut:
                for queryOut in prvCustomerrepourlQueryOut:
                    if (queryOut[0] == 'DB_VERSION') and (queryOut[1] == 'CONFIG'):
                        dbVersionGiturl = queryOut[2]
                    elif (queryOut[0] == 'RUNTIME_LOGO') and (queryOut[1] == 'CONFIG'):
                        uiux_gitUrl_resourceUrl = queryOut[2]
                    elif (queryOut[0] == 'WORKFLOW') and (queryOut[1] == 'CONFIG'):
                        workflow_gitUrl_sourcecodeUrl = queryOut[2]
                    elif (queryOut[0] == 'RATING') and (queryOut[1] == 'CONFIG'):
                        rating_gitUrl_sourcecodeUrl = queryOut[2]
                    elif (queryOut[0] == 'FORMS') and (queryOut[1] == 'CONFIG'):
                        formsGitUrl = queryOut[2]
                    # else:
                    #     log.error("Unknow runtime name found is : ", queryOut[0])
                else:
                    errormsg = "Couldn't find any CUSTOMER REPO details in PRV_CUSTOMER_REPO_URL table for ownerId: {}, customerName: {}, customerType: {},  lineOfBusiness: {}, environmentType: {} ".format(ownerId, customerName, customerType, lineOfBusiness, environmentType )
                    log.error(errormsg)
                    # message = errormsg
                    # retCode = 400    
           
        except Exception as e:
            errormsg = "Exception found in collecting the RUNTIME status information for ownerId: {}, customerName: {}, customerType: {},  lineOfBusiness: {}, environmentType: {} ".format(ownerId, customerName, customerType, lineOfBusiness, environmentType)
            log.error(errormsg)
            log.error(e)
            message = errormsg
            retCode = 500
        
        finally:
            log.info("Closing DB cursor...")
            PrvDBcursor.close()
            
    except Exception as e:
        log.error("Exception found in getting createProvisioningDbPooling ")
        log.error(e)
        message = "Error in getting DB connection pool. Internal server error"
        retCode = 500

            
    resp_json = {  
        "ownerId": ownerId,
        "customerName": customerName,
        "customerType": customerType,
        "lineOfBusiness": lineOfBusiness,
        "environmentType": environmentType,
		"sbLoginUser": sbLoginUser,
        "message": message,
        "transactionDb": {
            "status": transactionDB_Status,
            "master": {
                "dev": {
                    "dbName": masterdevDb_Name,
                    "createdBy": masterdevDb_CreatedBy,
                    "createdDate": masterdevDb_CreatedDate,
                    "updatedBy": masterdevDb_UpdatedBy,
                    "updatedDate": masterdevDb_UpdatedDate,
                    "datasource": masterdevDb_Datasource
                },
                "test": {
                    "dbName": mastertestDb_Name,
                    "createdBy": mastertestDb_CreatedBy,
                    "createdDate": mastertestDb_CreatedDate,
                    "updatedBy": mastertestDb_UpdatedBy,
                    "updatedDate": mastertestDb_UpdatedDate,
                    "datasource": mastertestDb_Datasource
                },
                "live": {
                    "dbName": masterliveDb_Name,
                    "createdBy": masterliveDb_CreatedBy,
                    "createdDate": masterliveDb_CreatedDate,
                    "updatedBy": masterliveDb_UpdatedBy,
                    "updatedDate": masterliveDb_UpdatedDate,
                    "datasource": masterliveDb_Datasource
                }
            },
            "slave": {
                "dev": {
                    "dbName": slavedevDb_Name,
                    "createdBy": slavedevDb_CreatedBy,
                    "createdDate": slavedevDb_CreatedDate,
                    "updatedBy": slavedevDb_UpdatedBy,
                    "updatedDate": slavedevDb_UpdatedDate,
                    "datasource": slavedevDb_Datasource
                },
                "test": {
                    "dbName": slavetestDb_Name,
                    "createdBy": slavetestDb_CreatedBy,
                    "createdDate": slavetestDb_CreatedDate,
                    "updatedBy": slavetestDb_UpdatedBy,
                    "updatedDate": slavetestDb_UpdatedDate,
                    "datasource": slavetestDb_Datasource
                },
                "live": {
                    "dbName": slaveliveDb_Name,
                    "createdBy": slaveliveDb_CreatedBy,
                    "createdDate": slaveliveDb_CreatedDate,
                    "updatedBy": slaveliveDb_UpdatedBy,
                    "updatedDate": slaveliveDb_UpdatedDate,
                    "datasource": slaveliveDb_Datasource
                }
            },
            "report": {
                "dev": {
                    "dbName": reportdevDb_Name,
                    "createdBy": reportdevDb_CreatedBy,
                    "createdDate": reportdevDb_CreatedDate,
                    "updatedBy": reportdevDb_UpdatedBy,
                    "updatedDate": reportdevDb_UpdatedDate,
                    "datasource": reportdevDb_Datasource
                },
                "test": {
                    "dbName": reporttestDb_Name,
                    "createdBy": reporttestDb_CreatedBy,
                    "createdDate": reporttestDb_CreatedDate,
                    "updatedBy": reporttestDb_UpdatedBy,
                    "updatedDate": reporttestDb_UpdatedDate,
                    "datasource": reporttestDb_Datasource
                },
                "live": {
                    "dbName": reportliveDb_Name,
                    "createdBy": reportliveDb_CreatedBy,
                    "createdDate": reportliveDb_CreatedDate,
                    "updatedBy": reportliveDb_UpdatedBy,
                    "updatedDate": reportliveDb_UpdatedDate,
                    "datasource": reportliveDb_Datasource
                }
            }
        }, 
        "uiux": {
            "status": uiux_Status,
            "url": {
                "dev": {
                    "createdBy": uiuxDev_CreatedBy,
                    "createdDate": uiuxDev_CreatedDate,
                    "updatedBy": uiuxDev_UpdatedBy,
                    "updatedDate": uiuxDev_UpdatedDate,
                    "endpointUrl": uiuxDev_endPointURL
                    },
                "test": {
                    "createdBy": uiuxTest_CreatedBy,
                    "createdDate": uiuxTest_CreatedDate,
                    "updatedBy": uiuxTest_UpdatedBy,
                    "updatedDate": uiuxTest_UpdatedDate,
                    "endpointUrl": uiuxTest_endPointURL
                },
                "live": {
                    "createdBy": uiuxLive_CreatedBy,
                    "createdDate": uiuxLive_CreatedDate,
                    "updatedBy": uiuxLive_UpdatedBy,
                    "updatedDate": uiuxLive_UpdatedDate,
                    "endpointUrl": uiuxLive_endPointURL
                }
            },
            "gitUrl": {
                "resourceGitUrl": uiux_gitUrl_resourceUrl
                }
        },
        "workflow": {
            "status": workflow_Status,
            "createdBy": workflow_CreatedBy,
            "createdDate": workflow_CreatedDate,
            "updatedBy": workflow_UpdatedBy,
            "updatedDate": workflow_UpdatedDate,
            "serverGroupName": workflow_serverGroupName,
            "endpointUrl": workflow_endPointURL,
            "gitUrl": {
                "sourcecodeUrl": workflow_gitUrl_sourcecodeUrl
            }
        },
        "rating": {
            "status": rating_Status,
            "createdBy": rating_CreatedBy,
            "createdDate": rating_CreatedDate,
            "updatedBy": rating_UpdatedBy,
            "updatedDate": rating_UpdatedDate,
            "endpointUrl": rating_endPointURL,
            "gitUrl": {
                "sourcecodeUrl": rating_gitUrl_sourcecodeUrl
            }
        },        
        "formsGitUrl": formsGitUrl,
        "dbVersionGiturl": dbVersionGiturl,
        "jenkinsUrl": {
            "dmlSqlExtractor": jenkinsUrl_dmlsqlextractor,
            "ddlSqlExtractor": jenkinsUrl_ddlsqlextractor,
            "customerPipeline": jenkinsUrl_customerpipeline,
            "adoptionPipeline": jenkinsUrl_Adoptionpipeline,
            "bpmnRestartedPipeline": jenkinsUrl_bpmnrestartedpipeline
        }
    }

    if message == "NA":
        return JSONResponse(status_code=200, content=resp_json)
    else:
        return JSONResponse(status_code=retCode, content=resp_json)
    
