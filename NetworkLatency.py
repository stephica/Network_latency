#!/usr/bin/python
import platform, subprocess, re, sys, argparse

def check_os():
	if not(platform.system() == "Windows" or platform.system() == "Linux"):
		sys.exit("OS isn't supported")

def get_latency(hostname):
	try:
		if platform.system() == "Windows":
			cmd = subprocess.Popen('ping -n 1 {}'.format(hostname), shell=True, stdout=subprocess.PIPE)
			string = str(cmd.stdout.read())
			list1 = string.split(',')
			egex = re.compile(".*(Average).*")
			list1 = list(filter(egex.search, list1))
			string = list1[0]
			templist = []
			for numbers in string:
				if numbers.isdigit():
					templist.append(numbers)
			string = ''.join(templist)
			return string
		elif platform.system() == "Linux":
			cmd = subprocess.Popen('ping -c 1 {}'.format(hostname), shell=True, stdout=subprocess.PIPE)
			string = str(cmd.stdout.read())
			list1 = string.split(',')
			string = ''.join(list1[3])
			string = string.split("/")
			return ''.join(string[5])
	except:
		return "UNVISIBLE"

def check_threshold(hostname):
	try:
		latency = get_latency(hostname)
		try:
			if int(latency) >= int(threshold):
				return '1'
			elif int(latency) < int(threshold):
				return '2'
		except:
			pass
		if latency == 'UNVISIBLE':
			return 'UNVISIBLE'
	except:
		return "Problem is detected"


if __name__ == "__main__":
	check_os
	parser = argparse.ArgumentParser(description='Script to do changes in network based on latency calculation')
	parser.add_argument("-H", "--host", help='Host to test')
	parser.add_argument("-t", "--time", help='Threshold time in milliseconds for average latency')
	args = parser.parse_args()
	if args.host:
		hostname = args.host
	else:
		sys.exit("Please provide host to test for more informatiion type filename -h")
	if args.time:
		threshold = args.time
	else:
		sys.exit("Please provide average latency threshold in milliseconds for more informatiion type filename -h")

	threshold_value = check_threshold(hostname)
	if threshold_value == "1":
		print("Latency is too high, need to change routing table")
	elif threshold_value == "2":
		print("Test is passed with success")
	elif threshold_value == "UNVISIBLE":
		print("The {} is not Pingable".format(hostname))
	elif threshold_value == "Problem is detected":
		print("Problem is detected")