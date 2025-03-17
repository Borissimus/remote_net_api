# File Management API

## Overview

Repository: [remote_net_api](git@github.com:Borissimus/remote_net_api.git)

This is a simple Flask-based file management API that allows users to list, read, write, and delete files within a specified directory. The API uses Basic Authentication (username & password) for security.

## Installation

### 1. Clone the repository

```bash
mkdir project_api && cd project_api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the API

Start the API server with the following command:

```bash
python3 api.py --base_dir /path/to/project --host 0.0.0.0 --port 5000 --user admin --password secret123
```

Replace `/path/to/project` with the actual directory you want to manage.

## API Endpoints

### **1. List Files**

Get a list of files and directories inside a folder.

```bash
curl -u admin:secret123 "http://YOUR_PUBLIC_IP:5000/list"
```

#### **List a specific subdirectory:**

```bash
curl -u admin:secret123 "http://YOUR_PUBLIC_IP:5000/list?dir=subdir"
```

### **2. Read a File**

Retrieve the contents of a file.

```bash
curl -u admin:secret123 "http://YOUR_PUBLIC_IP:5000/read?file=subdir/file.txt"
```

### **3. Write a File**

Create or overwrite a file with new content.

```bash
curl -X POST http://YOUR_PUBLIC_IP:5000/write \
     -u admin:secret123 \
     -H "Content-Type: application/json" \
     -d '{"file": "subdir/file.txt", "content": "Hello, subdir!"}'
```

### **4. Delete a File**

Remove a file or an empty directory.

```bash
curl -X DELETE -u admin:secret123 "http://YOUR_PUBLIC_IP:5000/delete?file=subdir/file.txt"
```

## Running as a Background Service

To run the API in the background:

```bash
nohup python3 api.py --base_dir /path/to/project --host 0.0.0.0 --port 5000 --user admin --password secret123 > api.log 2>&1 &
```

## Running Tests

To test the API automatically, use the provided test script:

1. Make the script executable:
   ```bash
   chmod +x test_api.sh
   ```
2. Run the test script:
   ```bash
   ./test_api.sh
   ```

This script will:
- Create a temporary directory for testing.
- Start the API in the background.
- Create, read, and delete test files via API calls.
- Stop the API and clean up all test data.

To run the API in the background:

```bash
nohup python3 api.py --base_dir /path/to/project --host 0.0.0.0 --port 5000 --user admin --password secret123 > api.log 2>&1 &
```

## Security Considerations

- Always use a **strong password**.
- Consider using HTTPS instead of HTTP.
- Restrict API access to trusted IPs using a firewall.

## License

This project is licensed under the MIT License.

