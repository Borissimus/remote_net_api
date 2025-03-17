#!/bin/bash

# Configuration
API_URL="http://127.0.0.1:5000"
USER="admin"
PASSWORD="secret123"
TEST_DIR="/tmp/test_api_dir"
LOG_FILE="api_test.log"

# Clear logs
> $LOG_FILE

echo "===== STARTING API TESTING =====" | tee -a $LOG_FILE

# 1. Create test directory
echo "Creating test directory: $TEST_DIR" | tee -a $LOG_FILE
mkdir -p "$TEST_DIR"

# 2. Start API in background
echo "Starting API in background..." | tee -a $LOG_FILE
python3 api.py --base_dir "$TEST_DIR" --host 127.0.0.1 --port 5000 --user $USER --password $PASSWORD > /dev/null 2>&1 &
API_PID=$!
sleep 2  # Wait for API to start

# 3. Create files via API
echo "Creating files via API..." | tee -a $LOG_FILE
curl -X POST "$API_URL/write" \
     -u $USER:$PASSWORD \
     -H "Content-Type: application/json" \
     -d '{"file": "folder1/file1.txt", "content": "Hello, World!"}' | tee -a $LOG_FILE

curl -X POST "$API_URL/write" \
     -u $USER:$PASSWORD \
     -H "Content-Type: application/json" \
     -d '{"file": "folder2/file2.txt", "content": "Another test file"}' | tee -a $LOG_FILE

# 4. Check file existence
echo "Checking file existence..." | tee -a $LOG_FILE
curl -u $USER:$PASSWORD "$API_URL/list?dir=folder1" | tee -a $LOG_FILE
curl -u $USER:$PASSWORD "$API_URL/list?dir=folder2" | tee -a $LOG_FILE

# 5. Read test files
echo "Reading test files..." | tee -a $LOG_FILE
curl -u $USER:$PASSWORD "$API_URL/read?file=folder1/file1.txt" | tee -a $LOG_FILE
curl -u $USER:$PASSWORD "$API_URL/read?file=folder2/file2.txt" | tee -a $LOG_FILE

# 6. Delete test files via API
echo "Deleting test files..." | tee -a $LOG_FILE
curl -X DELETE -u $USER:$PASSWORD "$API_URL/delete?file=folder1/file1.txt" | tee -a $LOG_FILE
curl -X DELETE -u $USER:$PASSWORD "$API_URL/delete?file=folder2/file2.txt" | tee -a $LOG_FILE

# 7. Delete directories
echo "Deleting directories..." | tee -a $LOG_FILE
curl -X DELETE -u $USER:$PASSWORD "$API_URL/delete?file=folder1" | tee -a $LOG_FILE
curl -X DELETE -u $USER:$PASSWORD "$API_URL/delete?file=folder2" | tee -a $LOG_FILE

# 8. Stop API
echo "Stopping API..." | tee -a $LOG_FILE
kill $API_PID

# 9. Remove test directory
echo "Removing test directory: $TEST_DIR" | tee -a $LOG_FILE
rm -rf "$TEST_DIR"

echo "===== API TESTING COMPLETED =====" | tee -a $LOG_FILE
