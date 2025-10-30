"""Test script for the FastAPI application."""
import requests
import json

API_URL = "http://127.0.0.1:8000/chat"

def run_test(description: str, user_input: str, expected_intent: str):
    """Helper function to run a single test case."""
    print(f"--- Running Test: {description} ---")
    try:
        payload = {"user_input": user_input, "conversation_history": []}
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        print(f"User Input: {user_input}")
        print(f"Agent Response: {data.get('response')}")
        print(f"Detected Intent: {data.get('intent')}")
        print(f"Citations: {data.get('citations')}")
        print(f"Should Escalate: {data.get('should_escalate')}")

        assert data.get("intent") == expected_intent, f"Intent mismatch! Expected {expected_intent}, got {data.get('intent')}"
        
        if expected_intent == "telecom_support":
            assert isinstance(data.get("citations"), list), "Citations should be a list"

        print(f"--- Test Passed ---\n")
        return True
    except (requests.exceptions.RequestException, AssertionError) as e:
        print(f"!!! Test Failed: {e} !!!\n")
        return False

def main():
    """Main function to run all test cases."""
    print("Starting API tests...")
    
    # Test cases
    tests = [
        {
            "description": "Telecom Support Intent - Billing Question",
            "user_input": "Why is my bill so high this month?",
            "expected_intent": "telecom_support"
        },
        {
            "description": "Telecom Support Intent - Technical Issue",
            "user_input": "My internet is not working.",
            "expected_intent": "telecom_support"
        },
        {
            "description": "Task Automation Intent - Flight Booking",
            "user_input": "I need to book a flight to New York.",
            "expected_intent": "task_automation"
        },
        {
            "description": "General Intent - Greeting",
            "user_input": "Hello, how are you?",
            "expected_intent": "general"
        },
        {
            "description": "Telecom Support Intent - Escalation",
            "user_input": "I want a refund now, this is unacceptable!",
            "expected_intent": "telecom_support"
        }
    ]

    results = [run_test(**test) for test in tests]

    if all(results):
        print("All tests passed successfully!")
    else:
        print(f"{results.count(False)}/{len(results)} tests failed.")

if __name__ == "__main__":
    main()
