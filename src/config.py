from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuration class to handle environment variables
class Config:
    STORAGE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
    STORAGE_ACCESS_KEY = os.getenv('AZURE_STORAGE_ACCESS_KEY')
    CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME')
    LOCAL_CSV_PATH = os.getenv('LOCAL_CSV_PATH')
    ADLS_URL = f"https://{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net"

    @staticmethod
    def validate_config():
        required_vars = [
            'STORAGE_ACCOUNT_NAME',
            'STORAGE_ACCESS_KEY',
            'CONTAINER_NAME',
            'LOCAL_CSV_PATH'
        ]
        
        missing_vars = [var for var in required_vars 
                       if getattr(Config, var) is None]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {missing_vars}")