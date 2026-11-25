
import requests

url = "https://himalayas.app/jobs/api?limit=5"

response = requests.get(url, timeout=20)

print("Status Code:", response.status_code)

data = response.json()

print("\nData Type:", type(data))

if isinstance(data, dict):
    print("\nAvailable Keys:", data.keys())

    for key, value in data.items():
        if isinstance(value, list):
            print("\nJob List Found:", key)
            print("Number of jobs:", len(value))

            if value:
                print("\nFirst Job:")
                print(value[0])
            break

elif isinstance(data, list):
    print("\nNumber of jobs:", len(data))

    if data:
        print("\nFirst Job:")
        print(data[0])
