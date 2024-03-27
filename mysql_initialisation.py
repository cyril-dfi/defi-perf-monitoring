from mysql_helper import *

MySQLHelper = MySQLHelper()

logging.info("Creating 'network' MySQL table")
create_table_query = """
CREATE TABLE IF NOT EXISTS network (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB
"""
MySQLHelper.execute_query(create_table_query)


logging.info("Creating 'app' MySQL table")
create_table_query = """
CREATE TABLE IF NOT EXISTS app (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB
"""
MySQLHelper.execute_query(create_table_query)


logging.info("Creating 'app_network' MySQL table")
create_table_query = """
CREATE TABLE IF NOT EXISTS app_network (
  id INT AUTO_INCREMENT PRIMARY KEY,
  app_id INT NOT NULL,
  network_id INT NOT NULL,
  position_contract_address VARCHAR(100) UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (app_id) REFERENCES app(id),
  FOREIGN KEY (network_id) REFERENCES network(id),
  UNIQUE (app_id, network_id) 
) ENGINE=InnoDB
"""
MySQLHelper.execute_query(create_table_query)


logging.info("Initialising maverick on ethereum")
supported_apps_and_networks = {
    'maverick': [
        {'network': 'ethereum', 'position_contract_address': '0x4A3e49f77a2A5b60682a2D6B8899C7c5211EB646'},
        {'network': 'bnb', 'position_contract_address': '0x23Aeaf001E5DF9d7410EE6C6916f502b7aC8e9D0'},
        {'network': 'zksync', 'position_contract_address': '0xFd54762D435A490405DDa0fBc92b7168934e8525'},
        {'network': 'base', 'position_contract_address': '0x0d8127A01bdb311378Ed32F5b81690DD917dBa35'},
    ]
}

for app in supported_apps_and_networks:
    app_id = MySQLHelper.insert_in_table(
          'app', 
          ['name'],
          [app],
      )

    for network in supported_apps_and_networks[app]:
        network_id = MySQLHelper.insert_in_table(
          'network', 
          ['name'],
          [network['network']],
        )

        MySQLHelper.insert_in_table(
          'app_network', 
          ['app_id', 'network_id', 'position_contract_address'],
          [app_id, network_id, network['position_contract_address']],
        )


logging.info("Creating 'pool' MySQL table")
create_table_query = """
CREATE TABLE IF NOT EXISTS pool (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  address VARCHAR(100) NOT NULL UNIQUE,
  app_network_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (app_network_id) REFERENCES app_network(id)
) ENGINE=InnoDB
"""
MySQLHelper.execute_query(create_table_query)


logging.info("Creating 'token' MySQL table")
create_table_query = """
CREATE TABLE IF NOT EXISTS token (
  id INT AUTO_INCREMENT PRIMARY KEY,
  address VARCHAR(100) NOT NULL UNIQUE,
  symbol VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB
"""
MySQLHelper.execute_query(create_table_query)


logging.info("Creating 'token_price_history' MySQL table")
create_table_query = """
CREATE TABLE IF NOT EXISTS token_price_history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  token_id INT NOT NULL,
  price DECIMAL(10,10),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (token_id) REFERENCES token(id)
) ENGINE=InnoDB
"""
MySQLHelper.execute_query(create_table_query)


logging.info("Creating 'pool_token' MySQL table")
create_table_query = """
CREATE TABLE IF NOT EXISTS pool_token (
  id INT AUTO_INCREMENT PRIMARY KEY,
  pool_id INT NOT NULL,
  token_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (token_id) REFERENCES token(id),
  FOREIGN KEY (pool_id) REFERENCES pool(id),
  UNIQUE (pool_id, token_id)
) ENGINE=InnoDB
"""
MySQLHelper.execute_query(create_table_query)


logging.info("Creating 'position' MySQL table")
create_table_query = """
CREATE TABLE IF NOT EXISTS position (
  id INT AUTO_INCREMENT PRIMARY KEY,
  owner_address VARCHAR(100) NOT NULL,
  pool_id INT NOT NULL,
  nft_id INT,
  initial_balance DECIMAL(20,10),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (pool_id) REFERENCES pool(id),
  UNIQUE (owner_address, pool_id) -- For now, we don't handle the case when on user has multiple positions on the same pool
) ENGINE=InnoDB
"""
MySQLHelper.execute_query(create_table_query)


logging.info("Creating 'position_token' MySQL table")
create_table_query = """
CREATE TABLE IF NOT EXISTS position_token (
  id INT AUTO_INCREMENT PRIMARY KEY,
  position_id INT NOT NULL,
  token_id INT NOT NULL,
  token_initial_balance DECIMAL(20,10),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (position_id) REFERENCES `position`(id),
  FOREIGN KEY (token_id) REFERENCES token(id),
  UNIQUE (position_id, token_id)
) ENGINE=InnoDB
"""
MySQLHelper.execute_query(create_table_query)


logging.info("Creating 'position_token_history' MySQL table")
create_table_query = """
CREATE TABLE IF NOT EXISTS position_token_history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  position_id INT NOT NULL,
  token_id INT NOT NULL,
  token_balance DECIMAL(20,10),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (position_id) REFERENCES `position`(id),
  FOREIGN KEY (token_id) REFERENCES token(id)
) ENGINE=InnoDB
"""
MySQLHelper.execute_query(create_table_query)


logging.info("Creating 'position_balance_history' MySQL table")
create_table_query = """
CREATE TABLE IF NOT EXISTS position_balance_history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  position_id INT NOT NULL,
  balance DECIMAL(20,10),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (position_id) REFERENCES `position`(id)
) ENGINE=InnoDB
"""
MySQLHelper.execute_query(create_table_query)
