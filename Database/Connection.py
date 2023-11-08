
# from jproperties import Properties
from mysql.connector import pooling
from ReadConfigs.readConfigs import readConfigFromFile
from Logger.logging import logger

log = logger(__name__)
config = readConfigFromFile()
# print(config.sections())
# print(config.items("Logging"))

def createsysdbConnectionPooling():
    try:
        configs = {
            "pool_size": config.get('sysconfigDB', 'pool_size'),
            "db_host": config.get('sysconfigDB', 'db_host'),
            "db_port": config.get('sysconfigDB', 'db_port'),
            "db_user": config.get('sysconfigDB', 'db_user'),
            "db_cred": config.get('sysconfigDB', 'db_cred'),
            "dbname": config.get('sysconfigDB', 'dbname')
        }
        sysdb_pooling_object = pooling.MySQLConnectionPool(pool_name="sysconfigdbV3",
                                                        pool_size=int(configs["pool_size"]),
                                                        pool_reset_session=True,
                                                        host=configs["db_host"],
                                                        port=int(configs["db_port"]),
                                                        user=configs["db_user"],
                                                        password=configs["db_cred"],
                                                        database=configs["dbname"],
                                                        auth_plugin='mysql_native_password',
                                                        ssl_disabled=True,
                                                        buffered=True)
        return sysdb_pooling_object
    except Exception as exception:
        log.error(exception)
        raise exception("Error while getting createsysdbConnectionPooling")
    

def createProvisioningDbPooling():
    try:
        configs = {
            "pool_size": config.get('provisioningDB', 'pool_size'),
            "db_host": config.get('provisioningDB', 'db_host'),
            "db_port": config.get('provisioningDB', 'db_port'),
            "db_user": config.get('provisioningDB', 'db_user'),
            "db_cred": config.get('provisioningDB', 'db_cred'),
            "dbname": config.get('provisioningDB', 'dbname')
        }
        ProvisioningDb_pooling_object = pooling.MySQLConnectionPool(pool_name="ProvisioningDbPool",
                                                        pool_size=int(configs["pool_size"]),
                                                        pool_reset_session=True,
                                                        host=configs["db_host"],
                                                        port=int(configs["db_port"]),
                                                        user=configs["db_user"],
                                                        password=configs["db_cred"],
                                                        database=configs["dbname"],
                                                        auth_plugin='mysql_native_password',
                                                        ssl_disabled=True,
                                                        buffered=True)
        return ProvisioningDb_pooling_object
    except Exception as exception:
        log.error("Error while getting createProvisioningDbConnectionPooling")
        log.error(exception)
        raise exception("Error while getting createProvisioningDbConnectionPooling")
    
    