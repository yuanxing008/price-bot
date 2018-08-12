#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018年8月12日03:43:54
# @Author  : Joker
# @QQ      : 450156750
# @github  : https://github.com/yuanxing008/price-bot

import urllib
import urllib.parse
import urllib.request
import requests
from colorama import init, Fore, Back, Style
from prettytable import PrettyTable

# API 请求地址
btcfuture_MARKET_URL = "https://www.bitfuture.cc/ajax/public"
cryptopia_MARKET_URL = "https://www.cryptopia.co.nz/api"

#'Timestamp': '2017-06-02T06:13:49'

def http_get_request(url, add_to_headers=None):
	headers = {
		"Content-type": "application/x-www-form-urlencoded",
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
	}
	if add_to_headers:
		headers.update(add_to_headers)
	response = requests.get(url, headers=headers, timeout=10)
	try:
		if response.status_code == 200:
			return response.json()
		else:
			return
	except BaseException as e:
		print("httpGet failed, detail is:%s,%s" %(response.text,e))
		return

init(autoreset=False)
class Colored(object):
    def red(self, s):
        return Fore.LIGHTRED_EX + s + Fore.RESET
    def green(self, s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET
    def yellow(self, s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET
    def white(self,s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET
    def blue(self,s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET

def npw():
	btcfuture_urls = btcfuture_MARKET_URL+'/trade/symbol/usdt_npw'
	cryptopia_urls = cryptopia_MARKET_URL+'/GetMarket/NPW_BTC'
	try:
		print("=====比特未来=====")
		btcfuture_res = http_get_request(btcfuture_urls)
		orders = btcfuture_res['Orders']
		table = PrettyTable(["时间", "方向", "成交价(USDT)", "成交价(CNY)", "数量"])  
		table.align["时间"] = "1"
		table.padding_width = 1
		color = Colored()
		for i in range(0, len(orders)):
			orders_time = orders[i][0]
			orders_price = orders[i][1]
			orders_amount = orders[i][2]
			orders_type = orders[i][3]
			if(orders_type) == 'sell':
				orders_type = color.green('卖出')
			else:
				orders_type = color.red('买入')
			table.add_row([orders_time, orders_type, orders_price, float(orders_price) * 6.8, orders_amount])
			pass
		print(table)

		#C网信息获取
		print("=====Cryptopia=====")
		cryptopia_res = http_get_request(cryptopia_urls)
		cryptopia_data= cryptopia_res['Data']
		cryptopia_last_price = cryptopia_data['LastPrice']
		cryptopia_cny = float(cryptopia_data['LastPrice']) * 6300 * 6.8
		print("|      BTC      |    CNY       |")
		print("|%s     |%s    |" %(cryptopia_last_price, cryptopia_cny))

	except BaseException as e:
		print("http请求失败，详情:%s,%s" %(cryptopia_data,e))
		return

if __name__ == '__main__':
	n = 120
	while( --n ):
		data = npw()
