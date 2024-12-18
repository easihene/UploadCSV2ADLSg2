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
```bash
AZURE_STORAGE_ACCOUNT_NAME=your_storage_account_name
AZURE_STORAGE_ACCESS_KEY=your_access_key
AZURE_CONTAINER_NAME=your_container_name
LOCAL_CSV_PATH=path/to/your/csv/files
```

## Usage

Run the script from the src directory:
```bash
python upload_to_adls.py
```

## Security Notes

- Never commit the .env file to version control
- Regularly rotate your Azure access keys
- Consider using Azure Key Vault for production environments

