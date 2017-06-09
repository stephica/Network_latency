import platform, subprocess, re, sys

hostname  = "8.8.8.8"
#Threshold in ms
threshold = "4"

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

check_os()

if len(sys.argv) > 1:
	print("Hostname is assigned to: {}".format(sys.argv[1]))
	hostname = sys.argv[1]
else:
	print("Please use syntax: python {} hostname".format(sys.argv[0]))
	sys.exit()

threshold_value = check_threshold(hostname)
if threshold_value == "1":
	print("Latency is too high, need to change routing table")
elif threshold_value == "2":
	print("Everying is OK")
elif threshold_value == "UNVISIBLE":
	print("The {} is not Pingable".format(hostname))
elif threshold_value == "Problem is detected":
	print("Problem is detected")