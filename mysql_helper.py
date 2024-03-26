import mysql.connector
from mysql.connector import Error
from config import os, logging

class MySQLHelper():
    def __init__(self):
        # Database connection details
        self.db_name = "defi-perf-monitoring"
        self.host_name = os.environ.get('MYSQL_HOST_NAME')
        self.user_name = os.environ.get('MYSQL_USER_NAME')
        self.user_password = os.environ.get('MYSQL_PASSWORD')

        self.create_db_if_not_exists()

        # Connect to the database
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=self.host_name,
                user=self.user_name,
                passwd=self.user_password,
                database=self.db_name
            )
            logging.info("Connection to MySQL DB successful")
        except Error as e:
            logging.error(f"The error '{e}' occurred")
        
        self.cursor = self.connection.cursor()

    def create_db_if_not_exists(self):
        try:
            # Connect to the MySQL server
            connection = mysql.connector.connect(
                host=self.host_name,
                user=self.user_name,
                passwd=self.user_password
            )
            
            if connection.is_connected():
                cursor = connection.cursor()
                # Check if the database exists
                cursor.execute(f"SHOW DATABASES LIKE '{self.db_name}';")
                result = cursor.fetchone()
                if result:
                    logging.info(f"Database '{self.db_name}' already exists.")
                else:
                    # Create the database if it does not exist
                    cursor.execute(f"CREATE DATABASE `{self.db_name}`;")
                    logging.info(f"Database '{self.db_name}' created successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            # Close the connection
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            logging.info("Query executed successfully")
        except Error as e:
            logging.error(f"The error '{e}' occurred")


    def create_if_not_exists(self, sql_without_semi_colon):
        insert_query = f"""
            {sql_without_semi_colon}
            ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id);
            """
        self.execute_query(insert_query)
        row_id = self.cursor.lastrowid
        return row_id

    def get_single_value_from_query(self, query):
        self.cursor.execute(query)
        try:
            return self.cursor.fetchall()[0][0]
        except:
            logging.error("Could not find the single value from the following query:")
            logging.error(query)

    def get_app_network_id(self, network, app):
        logging.info(f"Getting the 'app_network_id' for {network} - {app}")
        get_app_network_id_query = f"""
            SELECT `app_network`.`id`
            FROM `app_network`
            LEFT JOIN `network` ON `app_network`.`network_id` = `network`.`id`
            LEFT JOIN `app` ON `app_network`.`app_id` = `app`.`id`
            WHERE network.name = '{network}'
            AND app.name = '{app}'
        """
        app_network_id = self.get_single_value_from_query(get_app_network_id_query)
        return app_network_id

    def preprocess_list(self, li):
        preprocessed_li = [
            str(l) if isinstance(l, int) else f"'{l}'" 
            for l in li
        ]
        return preprocessed_li

    def insert_in_table(self, table_name, names, values):
        query = f"""
            INSERT INTO {table_name} ({', '.join(names)})
            VALUES ({', '.join(self.preprocess_list(values))})
            """
        line_id = self.create_if_not_exists(query)
        return line_id
    

    def insert_pool(self, pool_data, pool_token_data, network, app):
        app_network_id = self.get_app_network_id(network, app)
        
        # Create the pool
        pool_id = self.insert_in_table(
                'pool', 
                ['name', 'address', 'app_network_id'],
                [pool_data['name'], pool_data['address'], app_network_id],
            )

        # For each token, if not already created, create it
        for pool_token in pool_token_data:
            # Create the token (unique on address)
            token_id = self.insert_in_table(
                'token', 
                ['address', 'symbol'],
                [pool_token['address'], pool_token['symbol']],
            )

            # Create the pool_token
            pool_token_id = self.insert_in_table(
                'pool_token', 
                ['pool_id', 'token_id'],
                [pool_id, token_id],
            )
    

    def insert_position(self, owner_address, position_data, network, app):
        app_network_id = self.get_app_network_id(network, app)
        # Get pool_id
        # In theory the pool already exists (might be some edge cases where the pool is created between the beginning and the end of the script, need to handle those)
        pool_id_query = f"""
            SELECT id 
            FROM pool
            WHERE app_network_id = {app_network_id}
            AND address = '{position_data['pool_address']}';
        """
        pool_id = self.get_single_value_from_query(pool_id_query)

        position_id = self.insert_in_table(
            "`position`", 
            ['owner_address', 'pool_id', 'nft_id'],
            [owner_address, pool_id, position_data['nft_id']],
        )

        # Create the balance_history
        self.insert_in_table(
            'position_balance_history', 
            ['position_id', 'balance'],
            [position_id, position_data['balance']]
        )

        for token_address in position_data['token_balances']:
            # Get pool's tokens
            pool_tokens_query = f"""
                SELECT token_id 
                FROM pool_token
                LEFT JOIN token ON pool_token.token_id = token.id
                WHERE pool_id = {pool_id}
                AND token.address = '{token_address}';
            """
            token_id = self.get_single_value_from_query(pool_tokens_query)

            # Create the position_token
            self.insert_in_table(
                'position_token', 
                ['position_id', 'token_id'],
                [position_id, token_id],
            )

            # Create the position_token_history
            self.insert_in_table(
                'position_token_history', 
                ['position_id', 'token_id', 'token_balance'],
                [position_id, token_id, position_data['token_balances'][token_address]],
            )