import requests
import os
import dotenv
import argparse
dotenv.load_dotenv()
TOKEN = os.getenv('TOKEN')


def check_link(url):
    header = {"Authorization": f"Bearer {TOKEN}"}
    req = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{url}', headers=header)
    return req.ok


def get_short_url(long_url):
    header = {"Authorization": f"Bearer {TOKEN}"}
    body = {"long_url": long_url}
    post_req = requests.post("https://api-ssl.bitly.com/v4/bitlinks", headers=header, json=body)
    if not post_req.ok:
        return None
    else:
        response = post_req.json()
        bitlink = response['link'].split("//")
        return bitlink[1]


def get_amount_click(short_url):
    header = {"Authorization": f"Bearer {TOKEN}"}
    params = {"unit": "day", "units": -1}
    req = requests.get(f"https://api-ssl.bitly.com/v4/bitlinks/{short_url}/clicks/summary",
                            json=params, headers=header)
    if req.ok:
        amount = req.json()['total_clicks']
        return amount
    else:
        return None


def main():
    parser = argparse.ArgumentParser(description="USAGE: python script.py your_url")
    parser.add_argument("url", help="Ссылка на сокращение/Подсчет количества кликов")
    args = parser.parse_args()
    if check_link(args.url):
      info = get_amount_click(args.url)
    else:
      info = get_short_url(args.url)
    print(info)


if __name__ == "__main__":
    main()
