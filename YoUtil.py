import sys
import os
from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree 

# usfull links:
# https://docs.python.org/3.7/library/stdtypes.html

def Main():
	print("Main -> ")
	print ("argv[1]=",sys.argv[1])
	print ("argv[2]=",sys.argv[2])
	esi_path = get_elmo_user_ESI_path()
	#print("Esi Path=",esi_path)
	lst = get_list_of_files(esi_path,'.xml')
	for f in lst:
		full_path = esi_path+'\\'+f
		aa = get_esi_vendor(full_path)
		if aa!= None:
			print ('File=',f,' Vendor Name=',aa)
			devices = get_devices_desc(full_path)
			for item in devices:
				print ('    ProductCode=',item[0],'Revision=',item[1],'Name=',item[2])
		else:
			print ('file=',f,)
	
	
def get_elmo_local_appdata():
	"""Return the elmo local appdata directory."""
	path=os.getenv('LOCALAPPDATA')+'Elmo Motion Control\Application Studio'
	return path
	
def get_elmo_user_ESI_path():
	"""Return the user ESI appdata directory."""
	path=os.getenv('USERPROFILE')+'\Documents\Elmo Application Studio\EtherCAT Slave User Library'
	return path

def get_list_of_files(dirName, filter):
	# create a list of file and sub directories 
	# names in the given directory 
	listOfFile = os.listdir(dirName)
	allFiles = list()
	# Iterate over all the entries
	for entry in listOfFile:
		if entry.lower().endswith(filter):
			# Create full path
			fullPath = os.path.join(dirName, entry)
			# If entry is a directory then get the list of files in this directory 
			if os.path.isdir(fullPath):
				allFiles = allFiles + get_list_of_files(fullPath,filter)
			else:
				allFiles.append(entry)
				
	return allFiles        
	
def print_list(lst,ident=0):
	if lst is None or len(lst)==0:
		return
	ident_str = ''
	for num in range(ident):
		ident_str += ' '
	for aa in lst:
		print(ident_str,aa)

def get_esi_vendor(path):
	#print('>> ',path)
	tree = ET()
	tree.parse(path)
	vNode = tree.find('Vendor') 
	if vNode!=None:
		name_node = vNode.find('Name')
		if name_node != None:
			return name_node.text
	return None
	
def get_devices_desc(path):
	pass
	tree = ET()
	tree.parse(path)
	lst = tree.findall('./Descriptions/Devices/Device')
	all_devices = list()
	for device_node in lst:
		device_name = None
		last_name = None
		if device_node != None:
			type_node = device_node.find('Type')
			if type_node != None:
				prod = type_node.attrib['ProductCode']
				rev = type_node.attrib['RevisionNo']
				
				for name_node in device_node.findall('Name'):
					if name_node != None:
						last_name = name_node.text
						#print('>> ',name_node.text)
						if 'LcId' in name_node.attrib.keys():
							lcid = name_node.attrib['LcId']
							if lcid == '1031':
								device_name = name_node.text
				if device_name is None:
					device_name = last_name
				all_devices.append((prod,rev,device_name))
	return all_devices

def get_xml_content(tag):
	return xml.etree.ElementTree.tostring(tag) 
	
def get_int(str):
	ret = None
	if str.startswith('#x'):
		str = str.replace('#x','0x')
		ret = int(str,16)
		return ret
	else:
		ret = int(str,10)
	return ret
	
def get_xml_node_as_int(xml_node,xpath_str):
	ret = None
	if xml_node!= None:
		xml_find_node = xml_node.find(xpath_str)
		if xml_find_node != None:
			ret = get_int(xml_find_node.text)
	return ret
	
def get_xml_node_as_text(xml_node,xpath_str):
	ret = None
	if xml_node!= None:
		xml_find_node = xml_node.find(xpath_str)
		if xml_find_node != None:
			ret = xml_find_node.text
	return ret
	
def debug_print(text,lst):
	print('>>',text,lst)
	
def list_to_comma_separated(lst):
	ret = ''
	for t in lst:
		if len(ret)==0:
			ret+= t
		else:
			ret+=','+t
	return ret

def get_indent(indent):
	ret=''
	i = 0
	while i< indent:
		ret+='   '
		i+=1
	return ret
	
if (__name__=='__main__'):
	Main()
	
