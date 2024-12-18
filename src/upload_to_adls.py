from azure.storage.filedatalake import DataLakeServiceClient
import os
from config import Config
from datetime import datetime

def upload_to_adls():
    """
    Upload files to Azure Data Lake Storage Gen2 using environment variables
    Files will be overwritten if they already exist
    """
    try:
        # Validate environment variables
        Config.validate_config()
        
        # Create a service client
        service_client = DataLakeServiceClient(
            account_url=Config.ADLS_URL,
            credential=Config.STORAGE_ACCESS_KEY
        )
        
        # Get file system client
        file_system_client = service_client.get_file_system_client(
            file_system=Config.CONTAINER_NAME
        )
        
        # Track upload statistics
        upload_stats = {
            'new_files': 0,
            'overwritten_files': 0,
            'failed_files': 0
        }
        
        # Upload each CSV file in the directory
        for filename in os.listdir(Config.LOCAL_CSV_PATH):
            if filename.endswith('.csv'):
                try:
                    # Create full paths
                    local_file_path = os.path.join(Config.LOCAL_CSV_PATH, filename)
                    
                    # Get file client
                    file_client = file_system_client.get_file_client(filename)
                    
                    # Check if file exists
                    file_exists = True
                    try:
                        file_client.get_file_properties()
                    except:
                        file_exists = False
                    
                    # Upload file with overwrite
                    with open(local_file_path, 'rb') as file:
                        file_client.upload_data(file, overwrite=True)
                    
                    # Update statistics
                    if file_exists:
                        upload_stats['overwritten_files'] += 1
                        print(f"Successfully overwritten {filename}")
                    else:
                        upload_stats['new_files'] += 1
                        print(f"Successfully uploaded new file {filename}")
                    
                except Exception as e:
                    upload_stats['failed_files'] += 1
                    print(f"Failed to upload {filename}: {str(e)}")
        
        # Print summary
        print("\nUpload Summary:")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"New files uploaded: {upload_stats['new_files']}")
        print(f"Files overwritten: {upload_stats['overwritten_files']}")
        print(f"Failed uploads: {upload_stats['failed_files']}")
                
    except Exception as e:
        print(f"Error in upload process: {str(e)}")

if __name__ == "__main__":
    upload_to_adls()