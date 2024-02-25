import pandas as pd
from data_ingestion import create_db_engine, query_data, read_from_web_CSV
import logging

### START FUNCTION

class FieldDataProcessor:

    def __init__(self, config_params, logging_level="INFO"):  # Make sure to add this line, passing in config_params to the class 
        self.db_path = config_params['db_path']
        self.sql_query = config_params['sql_query']
        self.columns_to_rename = config_params['columns_to_rename']
        self.values_to_rename = config_params['values_to_rename']
        self.weather_map_data = config_params['weather_mapping_csv']

        # Add the rest of your class code here
        self.initialize_logging(logging_level)

        # We create empty objects to store the DataFrame and engine in
        self.df = None
        self.engine = None
        
    # This method enables logging in the class.
    def initialize_logging(self, logging_level):
        """
        Sets up logging for this instance of FieldDataProcessor.
        """
        logger_name = __name__ + ".FieldDataProcessor"
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False  # Prevents log messages from being propagated to the root logger

        # Set logging level
        if logging_level.upper() == "DEBUG":
            log_level = logging.DEBUG
        elif logging_level.upper() == "INFO":
            log_level = logging.INFO
        elif logging_level.upper() == "NONE":  # Option to disable logging
            self.logger.disabled = True
            return
        else:
            log_level = logging.INFO  # Default to INFO

        self.logger.setLevel(log_level)

        # Only add handler if not already added to avoid duplicate messages
        if not self.logger.handlers:
            ch = logging.StreamHandler()  # Create console handler
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)