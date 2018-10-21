import sys
import os
from xml.etree.ElementTree import ElementTree as ET
import sqlite3
from sqlite3 import Error
import YoUtil


#Usage:
#py ECatEsiUtil.py find 
#

def Main():
	#print("ECatEsiUtil -> ")
	#YoUtil.print_list(sys.argv,1)
	esi = EsiUtil()
	numofParams = len(sys.argv)
	print('>> numofParams=:',numofParams)
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

def print_usage(cmd=None):
	if cmd!= None:
		print('None valid Command option: ',cmd)
	print('PY ECatEsiUtil.py <cmd> <param1> <param2> <param3>')
	print('	cmd - esi_folders ')
	print('	cmd - createDB')
	print('	cmd - find <what> param1 param2 param3')
	print('	      what - esi - list of ESI files')
	print('	      what - vendor <vendorID> list of ESI files of a vendor')
	print('	      what - device_esi <vendorID> <productCode> <revisionNumber>')
		
def cmd_esi_folder(esi):
	YoUtil.print_list(esi.get_ESI_folders(),1)
	
def cmd_find(esi):			
	cmd = sys.argv[2].lower()
	if cmd == 'esi':
		files = esi.get_ESI_files()
		YoUtil.print_list(files,1)
	elif cmd == 'vendor':
		vendor_id = YoUtil.get_int(sys.argv[3])
		files = esi.get_ESI_files_by_vendor(vendor_id)
		YoUtil.print_list(files,1)
	elif cmd == 'createdb':
		if esi.create_esi_db('esi.db') == True:
			print('ESI DB created successfully')
		else:
			print('failed to create ESI DB ')
	elif cmd == 'device_esi':
		vendor_id = YoUtil.get_int(sys.argv[3])
		productCode = YoUtil.get_int(sys.argv[4])
		revisionNumber = None
		if len(sys.argv) > 5:
			revisionNumber = YoUtil.get_int(sys.argv[5])
		files = esi.get_devices(vendor_id,productCode,revisionNumber)
		YoUtil.print_list(files,1)
	else:
		print_usage('find')
		

	
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
		
	def create_esi_db(self, db_name):
		try:
			if os.path.exists(db_name):
				os.remove(db_name)
				YoUtil.debug_print('DB file deleted:',db_name)	
			self.con = sqlite3.connect(db_name)
			cur = self.con.cursor()
			YoUtil.debug_print('SQLite version: ',cur.fetchone())	
			with self.con:
				cur.execute("CREATE TABLE IF NOT EXISTS Vendors(VendorId INT, Name TEXT, Path TEXT)")
				cur.execute("CREATE TABLE IF NOT EXISTS Devices(VendorId INT, productCode INT, revisionNumber INT, Name TEXT, Xml TEXT)")
			
			files = self.get_ESI_files()
			for esi_path in files:
				vendor_id,vendor_name = self.get_ESI_info(esi_path)
				if vendor_id!= 0:
					with self.con:
						cur.execute("INSERT INTO Vendors (VendorId,Name,Path) VALUES(?,?,?)",(vendor_id,vendor_name,esi_path))
					device_list = self.get_ESI_devices()
					for device in device_list:
						with self.con:
							cur.execute("INSERT INTO Devices (VendorId,productCode,revisionNumber,Name) VALUES(?,?,?,?)",(vendor_id,device[0],device[1],device[2]))
			return True
		except sqlite3.Error as e:
			print(e)
			return False
		finally:
			if self.con:
				self.con.close()
		
	def get_ESI_info(self,esi_path):
		vendor_id = 0
		vendor_name  = None
		self.esi_path = esi_path
		self.xml_esi = self.load_esi(esi_path)
		if self.xml_esi!= None:
			xml_vendor = self.xml_esi.find('Vendor')
			if xml_vendor!= None:
				xml_id = xml_vendor.find('Id')
				if xml_id != None:
					vendor_id = YoUtil.get_int(xml_id.text)
				xml_name = xml_vendor.find('Name')
				if xml_name != None:
					vendor_name = xml_name.text
						
		return vendor_id,vendor_name
	
	def get_ESI_devices(self):
		ret = list()
		#devices
		if self.xml_esi!= None:
			YoUtil.debug_print('read devices of esi=',self.esi_path)
			xml_list_device = self.xml_esi.findall('Descriptions/Devices/Device')
			YoUtil.debug_print('num of devices in esi=',len(xml_list_device))
			for xml_device in xml_list_device:
				pc = None
				rev=None
				name=None
				xml_type = xml_device.find('Type')
				if xml_type != None:
					if 'ProductCode' in xml_type.attrib.keys():
						pc = YoUtil.get_int(xml_type.attrib['ProductCode'])
					if 'RevisionNo' in xml_type.attrib.keys():
						rev = YoUtil.get_int(xml_type.attrib['RevisionNo'])
					YoUtil.debug_print('ProductCode=',pc)
				if pc != None:
					ret.append((pc,rev,name))
		return ret
		
	def get_devices(self, vendor_id,productCode,revisionNumber):
		ret = list()
		files = self.get_ESI_files_by_vendor(vendor_id)
		YoUtil.debug_print('num of files=',len(files))
		for file_path in files:
			xml_esi = self.load_esi(file_path)
			if xml_esi!= None:
				xml_list_device = xml_esi.findall('Descriptions/Devices/Device')
				YoUtil.debug_print('num of devices=',len(xml_list_device))
				for xml_device in xml_list_device:
					xml_type = xml_device.find('Type')
					if xml_type != None:
						pc = YoUtil.get_int(xml_type.attrib['ProductCode'])
						YoUtil.debug_print('ProductCode=',pc)
						if pc == productCode:
							ret.append(file_path)
		return ret
		
	def load_esi(self,esi_path):
		self.tree = ET()
		self.tree.parse(esi_path)
		return self.tree.getroot()
		
	
	
if (__name__=='__main__'):
	Main()