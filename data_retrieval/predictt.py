import requests
import json

def main():
    x = requests.get("https://www.predictit.org/api/marketdata/all/")
    j = json.loads(x.text)
    print(j["markets"][0])


if __name__ == "__main__":
    main()