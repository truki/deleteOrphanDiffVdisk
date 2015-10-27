#! /usr/bin/env python

############################################
# author				: Sergio Sanchez
# date_created			: 2015-07-28
# email					: ssanchez@epes.es
# modified				: 2015-07-30
############################################

import subprocess
import time

#######################################################################
# getvdis: 	is a function that return a set on string that represent
# all vdi differential disk from VMs in this xenserver pool
#######################################################################

def getvdis():
	'''execute the command that list vdi'''
	getvdi_command = subprocess.Popen(['xe', 'vdi-list', 'params=name-label'], stdout=subprocess.PIPE)

	'''Create a set that storage all vdi with -diff sufijo'''
	vdi_set = set()

	for line in getvdi_command.stdout:
		if (line != '\n'):
			vdi = line.rstrip()[22:]
			if vdi[-5:] == "-diff":
				vdi_set.add(vdi)

	return vdi_set


#######################################################################
# deleteDifferentialVdis:	is a function that delete all differential
#  vdis that xenserver don't remove automatically and are
#  not assigned to a VM (vbd-uuids is null)						
#######################################################################

def deleteDifferentialVdis(vdiName, logfile):

	'''execute command that list all differential vdis from a specific vdiName'''
	command = subprocess.Popen(['xe', 'vdi-list', 'name-label='+vdiName, 'params=uuid,vbd-uuids'], stdout=subprocess.PIPE)
	uuid_set = set()

	for line in command.stdout:
		if (line != '\n'):
			title = line.rstrip()[0:19]
			if title[0:4] == 'uuid':
				temp_uuid = line.rstrip()[21:57]
			else:
				if title[4:13] == 'vbd-uuids':
					if line.rstrip()[21:57]=='':
						uuid_set.add(temp_uuid)

	'''once differential vdi are storaged in the set we proceed to delete them'''
	'''xe vdi-destroy uuid=uuid '''
	for uuid in uuid_set:
		comando_borrar = subprocess.Popen(['xe', 'vdi-destroy', 'uuid='+uuid], stdout=subprocess.PIPE)
		print comando_borrar.stdout.read()
		print ".........Deleting differential with uuid:"+uuid
		logfile.write(time.strftime("%c")+': ..................uuid --> '+uuid+'\n')



logfile = open('borradoVDI.log','a')
logfile.write(time.strftime("%c")+': *********  BEGIN  *********'+'\n')

for dif in getvdis():
	deleteDifferentialVdis(dif, logfile)
	print ""
	print "--------------------------------------------------"
	print "--------------------------------------------------"
	print "DELETING DIFFERENTIALS DISK OF --> "+dif
	print "--------------------------------------------------"
	print "--------------------------------------------------"
	logfile.write(time.strftime("%c")+': DELETING DIFERENTIALS DISK OF --> '+dif+'\n')

logfile.write(time.strftime("%c")+': *********  END  *********'+'\n')
logfile.close()
