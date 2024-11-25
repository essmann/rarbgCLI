import requests

# Function to add a magnet link to qBittorrent
def add_magnet_to_qbittorrent(magnet_link, qbt_url="http://localhost:8080", username="admin", password="essmann"):
    # Create a session to maintain the login
    session = requests.Session()

    # Log in to qBittorrent Web API
    login_payload = {'username': username, 'password': password}
    login_response = session.post(f"{qbt_url}/api/v2/auth/login", data=login_payload)

    if login_response.status_code == 200:
        print("Logged in successfully.")
        
        # Add the magnet link
        add_magnet_payload = {'urls': magnet_link}
        add_magnet_response = session.post(f"{qbt_url}/api/v2/torrents/add", data=add_magnet_payload)

        if add_magnet_response.status_code == 200:
            print("Magnet link added successfully.")
        else:
            print("Failed to add magnet link.")
    else:
        print("Failed to log in.")