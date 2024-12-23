from azure.storage.filedatalake import DataLakeServiceClient
import os
from config import Config
from datetime import datetime

def get_destination_path(filename: str) -> str:
    """
    Construct the destination path based on whether a directory is specified
    """
    if Config.DIRECTORY_PATH.strip():
        return f"{Config.DIRECTORY_PATH}/{filename}"
    return filename

def upload_to_adls():
    """
    Upload files to Azure Data Lake Storage Gen2 using environment variables
    Files will be uploaded to root container or specified directory
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
        
        # Create directory if specified and doesn't exist
        if Config.DIRECTORY_PATH.strip():
            try:
                directory_client = file_system_client.get_directory_client(Config.DIRECTORY_PATH)
                
                print(f"Using directory: {Config.DIRECTORY_PATH}")
            except Exception as e:
                print(f"Warning: Directory creation check failed: {str(e)}")
        else:
            print("No directory specified. Uploading to container root.")
        
        # Upload each CSV file in the directory
        for filename in os.listdir(Config.LOCAL_CSV_PATH):
            if filename.endswith('.csv'):
                try:
                    # Create full paths
                    local_file_path = os.path.join(Config.LOCAL_CSV_PATH, filename)
                    destination_path = get_destination_path(filename)
                    
                    # Get file client
                    file_client = file_system_client.get_file_client(destination_path)
                    
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
                        print(f"Successfully overwritten {destination_path}")
                    else:
                        upload_stats['new_files'] += 1
                        print(f"Successfully uploaded new file {destination_path}")
                    
                except Exception as e:
                    upload_stats['failed_files'] += 1
                    print(f"Failed to upload {filename}: {str(e)}")
        
        # Print summary
        print("\nUpload Summary:")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Target container: {Config.CONTAINER_NAME}")
        if Config.DIRECTORY_PATH.strip():
            print(f"Target directory: {Config.DIRECTORY_PATH}")
        else:
            print("Target directory: <root>")
        print(f"New files uploaded: {upload_stats['new_files']}")
        print(f"Files overwritten: {upload_stats['overwritten_files']}")
        print(f"Failed uploads: {upload_stats['failed_files']}")
                
    except Exception as e:
        print(f"Error in upload process: {str(e)}")

if __name__ == "__main__":
    upload_to_adls()