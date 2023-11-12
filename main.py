#!/bin/python3
import requests
from bs4 import BeautifulSoup
import argparse
import threading
import queue
import signal
import sys

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', type=str, help='List to be checked', required=True)
	parser.add_argument('-o', type=str, help='Output file', required=True)
	parser.add_argument('-t', type=int, help='Threads', required=True)
	return parser.parse_args()

def disable_warnings():
	requests.packages.urllib3.disable_warnings()

def scrape_title(ip, outputfile, timeout_event):
	url = f"http://{ip}"
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0'}
	
	try:
		req = requests.get(url, headers=headers, verify=False, timeout=3)
		req.raise_for_status()
		soup = BeautifulSoup(req.text, 'lxml')
	except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
		return 1, 0  # invalid count, title count
	
	try:
		if soup is None:
			return 0, 0
	except Exception as e:
		return 0, 0
	
	title = soup.find('title')
	if title:
		output = (ip, title.get_text())
		with open(outputfile, 'a+', encoding='utf-8') as f:
			f.write(str(output) + "\n")
		return 0, 1
	else:
		return 0, 0

def checker_thread(ip_queue, outputfile, invalid_count, title_count, run_count, lock, timeout_event):
	while not timeout_event.is_set() and not ip_queue.empty():
		ip = ip_queue.get()
		invalid, title = scrape_title(ip, outputfile, timeout_event)
		with lock:
			invalid_count[0] += invalid
			title_count[0] += title
			run_count[0] += 1
			print(f"|Invalid: {invalid_count[0]} | Titles: {title_count[0]} | Total Checked: {run_count[0]}|\r", end='', flush=True)

def signal_handler(sig, frame):
	print("\nScript interrupted. Cleaning up threads...")
	sys.exit(0)

ASCII='''
   __  ___           _______ __  __    _______           __
  /  |/  /__ ____ __/_  __(_) /_/ /__ / ___/ /  ___ ____/ /__
 / /|_/ / _ `(_-<(_-</ / / / __/ / -_) /__/ _ \/ -_) __/  '_/
/_/  /_/\_,_/___/___/_/ /_/\__/_/\__/\___/_//_/\__/\__/_/\_\
'''

def main():
	signal.signal(signal.SIGINT, signal_handler)
	
	print(ASCII)
	print("By Lord SkeletonMan and CRAWNiiK")
	print("Some hosts may cause errors, but can be ignored")
	print("Checking titles...")

	args = parse_arguments()
	disable_warnings()

	invalid_count = [0]
	title_count = [0]
	run_count = [0]
	lock = threading.Lock()
	timeout_event = threading.Event()

	with open(args.c, 'r', encoding='utf-8') as iplist:
		ip_list = list(map(str.strip, iplist))

	ip_queue = queue.Queue()
	for ip in ip_list:
		ip_queue.put(ip)

	threads = []

	for _ in range(args.t):
		thread = threading.Thread(target=checker_thread, args=(ip_queue, args.o, invalid_count, title_count, run_count, lock, timeout_event))
		threads.append(thread)
		thread.start()

	for thread in threads:
		thread.join()

	print("\nFinished checking titles!")

if __name__ == "__main__":
	main()
