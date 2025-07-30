from src.network.httpClient import HttpClient

if __name__ == "__main__":
    import sys

    url = sys.argv[1]

    client = HttpClient(max_redirects=5)
    response = client.get(url)

    if response:
        print(response.html_content)
