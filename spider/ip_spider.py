import requests
import lxml


def main():
    url = 'http://www.xicidaili.com/nn/1'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497.81 Safari/537.36'
    header = {'User-Agent': user_agent}
    requests.get(url=url, headers=header).content()


if __name__ == '__main__':
    main()