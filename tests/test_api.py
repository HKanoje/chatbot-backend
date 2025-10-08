# test_api.py
"""
Simple script to test your API endpoints
Run after starting the server
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_info():
    """Test info endpoint"""
    print("Testing info endpoint...")
    response = requests.get(f"{BASE_URL}/info")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_chat():
    """Test chat endpoint"""
    print("Testing chat endpoint...")
    payload = {
        "message": "Hello, how are you?"
    }
    response = requests.post(f"{BASE_URL}/api/v1/chat", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_stats():
    """Test stats endpoint"""
    print("Testing stats endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_upload():
    """Test file upload (you need a test file)"""
    print("Testing upload endpoint...")
    # Create a simple test text file
    test_file_path = "test_document.txt"
    with open(test_file_path, "w") as f:
        f.write("This is a test document for the RAG chatbot. It contains some sample text to test document processing.")
    
    with open(test_file_path, "rb") as f:
        files = {"file": ("test_document.txt", f, "text/plain")}
        response = requests.post(f"{BASE_URL}/api/v1/upload", files=files)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("=" * 50)
    print("API Testing Script")
    print("=" * 50 + "\n")
    
    try:
        test_health()
        test_info()
        test_stats()
        test_chat()
        # test_upload()  # Uncomment to test file upload
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to API. Make sure the server is running!")
    except Exception as e:
        print(f"ERROR: {e}")