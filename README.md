# Azure Data Lake Storage CSV Uploader

This project provides a secure way to upload CSV files to Azure Data Lake Storage Gen2.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix/MacOS
# or
venv\Scripts\activate     # Windows
```

2. Install dependencies::
```bash
pip install -r requirements.txt
```

3. Create a .env file in the project root and add your Azure credentials:

For uploading to a specific directory:
```bash
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account_name
AZURE_STORAGE_ACCESS_KEY=your_access_key
AZURE_CONTAINER_NAME=your_container_name
AZURE_DIRECTORY_PATH=your_directory_name
LOCAL_CSV_PATH=path/to/your/csv/files
```

For uploading to root container, either:
- Remove the AZURE_DIRECTORY_PATH line, or
- Set it to empty:

```bash
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account_name
AZURE_STORAGE_ACCESS_KEY=your_access_key
AZURE_CONTAINER_NAME=your_container_name
AZURE_DIRECTORY_PATH=
LOCAL_CSV_PATH=path/to/your/csv/files
```

## Usage

Run the script from the src directory:
```bash
python upload_to_adls.py
```

The script will:

- Upload all CSV files from the specified local path
- Overwrite existing files if they exist
- Provide upload statistics including new files and overwrites
- Show detailed logs of the upload process

## Upload Behavior

Root Container Upload

- Files will be uploaded directly to the container root
- Example path: https://your_storage_name.blob.core.windows.net/your_container_name/file.csv

Directory Upload

- Files will be uploaded to the specified directory within the container
- Example path: https://your_storage_name.blob.core.windows.net/your_container_name/your_directory_name/file.csv

## Security Notes

- Never commit the .env file to version control
- Regularly rotate your Azure access keys
- Consider using Azure Key Vault for production environments

## License
This project is licensed under the MIT License - see the LICENSE file for details