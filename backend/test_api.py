#!/usr/bin/env python3

import requests
import json

# Test the cancel plan functionality
def test_cancel_plan():
    url = "http://localhost:5001/user/cancel-plan"
    data = {"user_id": 2}
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

# Test getting plans
def test_get_plans():
    url = "http://localhost:5001/user/plans"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing API endpoints...")
    test_get_plans()
    print("\n" + "="*50 + "\n")
    test_cancel_plan()
