import uuid

    
def process_data(data, cursor_customer, cursor_runtime):
    owner_id = data.ownerId
    
    cursor_customer.execute("SELECT * FROM PRV_CUSTOMER WHERE OWNER_ID = %s", (owner_id,))
    existing_row = cursor_customer.fetchone()

    if existing_row:
        update_customer_query = """
            UPDATE PRV_CUSTOMER
            SET CUSTOMER_NAME = %s, CUSTOMER_TYPE = %s, PROJECT = %s, LOB = %s, ENVIRONMENT = %s,
                ACTIVE = %s, UPDATED_BY = 'bala', UPDATED_DATE = NOW()
            WHERE OWNER_ID = %s
        """
        cursor_customer.execute(update_customer_query, (
            data.customerName, data.customerType, data.project, data.lineOfBusiness,
            data.environmentType, data.active, data.ownerId
        ))

        update_runtime_query = """
            UPDATE PRV_CUSTOMER_RUNTIME
            SET ENVIRONMENT = %s, TXN_DB_ENABLED = %s, UIUX_ENABLED = %s, WORKFLOW_ENABLED = %s,
                RATING_ENABLED = %s, REPORTING_DB_ENABLED = %s, UPDATED_BY = 'bala', UPDATED_DATE = NOW()
            WHERE PRV_CUSTOMER_ID = %s
        """
        cursor_runtime.execute(update_runtime_query, (
            data.environmentType, data.txnDbEnabled, data.uiuxEnabled,
            data.workflowEnabled, data.ratingEnabled, data.reportingDbEnabled, data.ownerId
        ))
    else:
        insert_customer_query = """
            INSERT INTO PRV_CUSTOMER (PRV_CUSTOMER_ID, OWNER_ID, CUSTOMER_NAME, CUSTOMER_TYPE, PROJECT, LOB, ENVIRONMENT
            , ACTIVE, CREATED_BY, CREATED_DATE)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        cursor_customer.execute(insert_customer_query, (
            data.ownerId, data.ownerId, data.customerName, data.customerType, data.project,
            data.lineOfBusiness, data.environmentType, data.active, 'Sritharan'
        ))

        insert_runtime_query = """
            INSERT INTO PRV_CUSTOMER_RUNTIME (PRV_CUSTOMER_RUNTIME_ID, PRV_CUSTOMER_ID, ENVIRONMENT, TXN_DB_ENABLED, 
            UIUX_ENABLED, WORKFLOW_ENABLED, RATING_ENABLED, REPORTING_DB_ENABLED, CREATED_BY, CREATED_DATE)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        cursor_runtime.execute(insert_runtime_query, (
            str(uuid.uuid4()), data.ownerId, data.environmentType, data.txnDbEnabled, data.uiuxEnabled,
            data.workflowEnabled, data.ratingEnabled, data.reportingDbEnabled, 'Sritharan'
        ))
