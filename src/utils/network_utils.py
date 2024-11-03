import requests

class NetworkUtils:
    @staticmethod
    def get_json_response(url: str) -> dict:
        """Make a GET request and return the JSON response."""
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    @staticmethod
    def post_json_request(url: str, data: dict) -> dict:
        """Make a POST request with JSON data and return the JSON response."""
 response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

# Example usage
if __name__ == "__main__":
    url = "https://example.com/api/data"
    data = {"key": "value"}

    response = NetworkUtils.get_json_response(url)
    print(f"GET Response: {response}")

    response = NetworkUtils.post_json_request(url, data)
    print(f"POST Response: {response}")
