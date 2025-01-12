import requests
import json

def send_to_linebot(id, message, send_to_group=False):
    """
    Send a message to a LINE user or group.

    Parameters:
    id (str): The user ID or group ID.
    message (str): The message to send.
    send_to_group (bool): Whether to send the message to a group. Default is False.
    """
    # URL of the Flask application running on another machine
    url = "https://ethical-patient-gazelle.ngrok-free.app/send_message"

    # Data to be sent in the POST request
    data = {
        "group_id" if send_to_group else "user_id": id,
        "message": message
    }

    # Headers for the POST request
    headers = {
        "Content-Type": "application/json"
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Print the response
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")