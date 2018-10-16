import requests
import time
import telnetlib
from lxml import etree


'''
高匿 nn 透明nt https wn http 'wt'
'''


class IpSpider(object):

    def __init__(self, ip_type='nn', agreement='HTTP'):
        '''
        :param ip_type: 高匿:nn 透明:nt https:wn http:wt Default:nn
        :param agreement: HTTP/HTTPS
        :param agreement: if continuous failure count > fail_count break
        '''
        self.ip_type = ip_type
        self.agreement = agreement
        self.fail_count = 0

    def get_ip(self):
        self.run()

    def run(self):
        start_url = 'http://www.xicidaili.com/%s/' % self.ip_type
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/69.0.3497.81 Chrome/69.0.3497.81 Safari/537.36'
        header = {'User-Agent': user_agent}
        start_html = requests.get(url=start_url, headers=header).text
        ip_iter = self.html_to_data(start_html)
        yield ip_iter
        page = 1
        while True:
            page += 1
            next_url = start_url + '%s' % page
            html = requests.get(url=next_url, headers=header).text
            ip_iter = self.html_to_data(html)
            yield ip_iter

    def html_to_data(self, body):
        html = etree.HTML(body)
        tr_list = html.xpath('//tr')
        items = []
        for tr in tr_list[1:]:
            item = {}
            td = tr.xpath('.//td')
            item['国家'] = td[0].xpath('img/@alt')
            item['IP地址'] = td[1].xpath('text()')
            item['端口'] = td[2].xpath('text()')
            item['服务器地址'] = td[3].xpath('a/text()')
            item['是否匿名'] = td[4].xpath('text()')
            item['类型'] = td[5].xpath('text()')
            if item['类型'] != 'HTTP':
                pass
            item['速度'] = td[6].xpath('div/@title')
            item['连接时间'] = td[7].xpath('div/@title')
            item['存活时间'] = td[8].xpath('text()')
            item['验证时间'] = td[9].xpath('text()')
            for k, y in item.items():
                item[k] = y[0] if y else None
            print(item['IP地址'], item['端口'])
            if self.is_available(item['IP地址'], item['端口']):
                items.append(item)
                print('true ip')
            else:
                print('useless ip')

        print(items)
        return items

    def is_available(self, ip, port):
        if self.fail_count > 50:
            raise Exception('all useless ip')
        try:
            telnetlib.Telnet(ip, port, timeout=2)
            self.fail_count = 0
            return True
        except Exception as e:
            self.fail_count += 1
            return False


def main():
    ip_spider = IpSpider(ip_type='wt')
    result = ip_spider.run()
    for _ in range(5):
        print(result.__next__())
        print('------------')
        time.sleep(10)


if __name__ == '__main__':
    main()
