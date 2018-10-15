import sys
import os
from xml.etree.ElementTree import ElementTree as ET
import YoUtil


#Usage:
#py ECatEsiUtil.py find 
#

def Main():
	#print("ECatEsiUtil -> ")
	#YoUtil.print_list(sys.argv,1)
	esi = EsiUtil()
	numofParams = len(sys.argv)
	if numofParams > 1:
		cmd = sys.argv[1].lower()
		command_options = {
		'esi_folders' : cmd_esi_folder,
		'find':cmd_find
		}
		
		if cmd in command_options.keys():
			command_options[cmd](esi)
		else:
			print_usage(cmd)
	else:
		print_usage()
			
def cmd_esi_folder(esi):
	YoUtil.print_list(esi.get_ESI_folders(),1)
	
def cmd_find(esi):
	if sys.argv[2] == 'esi':
		files = esi.get_ESI_files()
		YoUtil.print_list(files,1)
	elif sys.argv[2] == 'vendor':
		vendor_id = YoUtil.get_int(sys.argv[3])
		files = esi.get_ESI_files_by_vendor(vendor_id)
		YoUtil.print_list(files,1)
		

def print_usage(cmd=None):
	if cmd!= None:
		print('None valid Command option: ',cmd)
	print('PY ECatEsiUtil.py <cmd> <param1> <param2> <param3>')
	print('	cmd - esi_folders ')
	print('	cmd - find <what> param1 param2 param3')
	print('	      what - esi - list of ESI files')
	print('	      what - vendor <vendorID> list of ESI files of a vendor')
	
class EsiUtil:
	def __init__(self):
		pass
	
	def get_ESI_files(self):
		esi_folders = self.get_ESI_folders()
		ret = list()
		for folder in esi_folders:
			files = YoUtil.get_list_of_files(folder,'.xml')
			for file in files:
				full_path = os.path.join(folder,file)
				ret.append(full_path)
		return ret

	def get_ESI_files_by_vendor(self, vendor_id):
		files = self.get_ESI_files()
		ret = list()
		for file_path in files:
			xml_esi = self.load_esi(file_path)
			if xml_esi!= None:
				xml_vendor = xml_esi.find('Vendor')
				if xml_vendor!= None:
					xml_id = xml_vendor.find('Id')
					if xml_id != None:
						id = YoUtil.get_int(xml_id.text)
						if id == vendor_id:
							ret.append(file_path)
		return ret
	
	def get_ESI_folders(self):
		ret = list()
		userESIPath= YoUtil.get_elmo_user_ESI_path()
		ret.append(userESIPath)
		ret.append('C:\Dev\eas\View\ElmoMotionControl.View.Main\EtherCATSlaveLib')
		return ret
		
	def load_esi(self,esi_path):
		self.tree = ET()
		self.tree.parse(esi_path)
		return self.tree.getroot()
		
	
	
if (__name__=='__main__'):
	Main()