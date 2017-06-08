import platform, subprocess, re

hostname  = "8.8.8.8" 
threshold = ""

def get_latency(hostname):
	try:
		if platform.system() == "Windows":
			cmd = subprocess.Popen('ping -n 1 {}'.format(hostname), shell=True, stdout=subprocess.PIPE)
			string = str(cmd.stdout.read())
			list1 = string.split(',')
			egex = re.compile(".*(Average).*")
			list1 = list(filter(egex.search, list1))
			string = list1[0]
			out_number = ''
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
		else:
			return "OS isn't recognized"
	except:
		return False

def check_threshold(hostname):
	try:
		if int(get_latency(hostname)) >= int(threshold):



print(get_latency("8.8.8.8"))
