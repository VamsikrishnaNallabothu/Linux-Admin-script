from subprocess import call
import subprocess
import os
import smtplib
import time
#from apscheduler.schedulers.blocking import BlockingScheduler


#sudo apt-get install mpstat

def mntpt_status():
	#print(os.system('df -h'))
	cmd = ["df", "-h"]
	#proc = call(["df", "-h"])
	#print ("Next cmd")
	with open("res.txt", "w") as f:
		proc = subprocess.Popen(cmd, stdout=f, stderr=f)
		out, err = proc.communicate()
	#print ("stored the result to the file")	
	with open("res.txt", "r") as f:
		for line in f:
			line=f.read()
			nlist = line.splitlines()
	newval = []
	newres = []
	for strng in nlist:
		val = strng.split()
		newval.append(val[0])
		newres.append(val[4].strip('%'))
		val = []
	#print ("Got the required keys and values")
	#print ("newval:", newval)
	#print ("newres:", newres)

	newres1 = []
	for i in newres:
		newres1.append(int(i))
	print (newres1)
	mydict = dict(zip(newval, newres1))
	#print ("Got the dictionary")	
	#print (mydict)


	for k,v in mydict.items():
		if v >= 90:
			print ("exceeded", k, v)
			message = "Your Mount point: {0} is {1} % Full ".format(k,v)
			send_email(message)
		else:
			#print ("not exceeded")
			pass


	'''	
for i in newval:
	print (i.strip())

initialcmd_output = subprocess.check_output("df -h", shell=True)
print (initialcmd_output)

#manual Pipe
for i in newval:
	# for finding mount points
	cmd1 = ["df","-h" ]
	proc1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
	# for holding the i value column from the output
	proc2 = subprocess.Popen(['grep', i.strip()],stdin=proc1.stdout, stdout=subprocess.PIPE)
	#for awk extraction of result from grep
	cmd3 = ["awk", "{print $5}"]
	proc3 = subprocess.Popen(cmd3, stdin=proc2.stdout, stdout=subprocess.PIPE)
	cmd4 = ["tr", "-d", "%"]
	proc4 = subprocess.Popen(cmd4, stdin=proc3.stdout, stdout=subprocess.PIPE)
	#fullcmd_output = subprocess.check_output("df -h | grep /dev/sda1 | awk '{print $5}'| tr -d '%'", 		shell=True)
	(out, err) = proc4.communicate()
	print (out)
	#fullcmd_output = os.system("")
	
	output = int(out)
	print (output)
	if output >= 90:
		print ('exceeded')
	else:
		print ('not exceeded')
'''



def cpu_utilization():
	cpu_util = ["mpstat"]
	proc1 = subprocess.Popen(cpu_util, stdout=subprocess.PIPE)
	cpu_util2 = ["awk","$13 ~ /[0-9.]+/ {print 100-$13}"]
	proc2 = subprocess.Popen(cpu_util2,stdin=proc1.stdout, stdout=subprocess.PIPE)
	out, err = proc2.communicate()
	myout = out.decode('ascii')
	myout = myout.strip()
	cpu_utilization = int(float(myout))
	if cpu_utilization >= 95 :
		msg = "Your CPU Utilization crossed 95%%. Now it is at %s" %myout
		send_email(msg)
	
'''
mpstat | awk '$13 ~ /[0-9.]+/ { print 100-$13"%" }'
'''


def free_memory():
	with open("cpu_util.txt", "w") as n:
		cpu_cmd = ["cat", "/proc/meminfo"]
		proc = subprocess.Popen(cpu_cmd,stdin=n, stdout=n)
		out, err = proc.communicate()
	
	with open("cpu_util.txt", "r") as f:
		lines =f.readlines()
		#print (lines)
		cpulist =[]
		cpures = []
		i = 0
		for strng in lines:
			if i <= 2:
				val = strng.split()
				cpulist.append(val[0].strip(':'))
				cpures.append(val[1])
				val = []
				i += 1
	cpures1 = []
	for i in cpures:
		cpures1.append(int(i))
	#print(cpulist, cpures1)
	cpudict = dict(zip(cpulist, cpures1))
	#print ("Got the cpu_dictionary")	
	#print (cpudict)
	#'MemAvailable'
	#'MemTotal'
	#'MemFree'
	value1 = cpudict['MemTotal']
	value2  = cpudict['MemFree']
	if value2 < (value1 * 0.05):
		Message = "The Free memory: {0} is less than 5% of the Total memory: {1}".format(value2, value1)
		send_email(Message)
	else:
		pass


def send_email(MSG):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("XXXXX@gmail.com", "mypassword")
	#my_msg = MSG
	server.sendmail("xxxxxxx@gmail.com", "yyyyyyyy@gmail.com", MSG)
	server.quit()


def main():
	free_memory()
	mntpt_status()
	cpu_utilization()

if __name__=="__main__":
	mntpt_status()
	cpu_utilization()
	free_memory()
	#scheduler = BlockingScheduler()
	#scheduler.add_job(main(), 'interval', minutes=5)
	#scheduler.start()



