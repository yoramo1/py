import sys
import os
from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree 

import YoUtil
from ECatSlave import ECatSlave as Slave

#Usage:
#c:\TestDev\py>py ECatConfigUtil.py "C:\Users\yoramo\Documents\Elmo Application Studio\Workspaces\Ws3\Targets\P01\Resources\Config.xml" g01
#

def Main():
	print("ECatConfigUtil -> ")
	YoUtil.print_list(sys.argv,1)
	numofParams = len(sys.argv)
	if numofParams > 1:
		cmd = sys.argv[1].lower()
		command_options = {
		'slaves' : cmd_slave_list,
		'full' : cmd_load_config_full,
		}
		
		if cmd in command_options.keys():
			command_options[cmd]()
		else:
			print_usage(cmd)
	else:
		print_usage()
		
	
def print_usage(cmd=None):
	if cmd!= None:
		print('None valid Command option: ',cmd)
	print('ECatConfigUtil Usage:')
	print('PY ECatConfigUtil.py <cmd> <cfgFile> <param2> <param3>')
	print('	cmd - slaves  <cfg_file> - list the slaves in the config')
	print('	cmd - full  <cfg_file> - ')
	
def cmd_slave_list():
	if len(sys.argv) >= 3:
		cfg = Config(sys.argv[2])
		cfg.load_config()
		lst = cfg.get_slaves()
		YoUtil.print_list(lst,1)
	else:
		print_usage()
		
def cmd_load_config_full():
	if len(sys.argv) >= 3:
		cfg = Config(sys.argv[2])
		cfg.load_config()
		lst = cfg.get_slaves()
		YoUtil.print_list(lst,1)
	else:
		print_usage()
	
	
	
	
	
	
class Config:
	def __init__(self,path):
		self.path = path
		
	
	def load_config(self):
		print('loading ->', self.path)
		self.tree = ET()
		self.tree.parse(self.path)
	
	def get_resid(self):
		node_resid  = self.tree.find('ResID')
		if node_resid!=None:
			print('>>',node_resid.text)
			return node_resid.text
		return None
	
	def get_slaves(self):
		ret = list()
		xml_list = self.tree.findall('Config/Slave')
		#print('>>',len(xml_list))
		if xml_list != None:
			for xml_slave in xml_list:
				slave = Slave(xml_slave)
				ret.append(slave)	
		return ret			
		
	def get_slaves_names(self):
		ret = list()
		xml_list = self.tree.findall('Config/Slave')
		#print('>>',len(xml_list))
		if xml_list != None:
			for xml_slave in xml_list:
				slave = Slave(xml_slave)
				ret.append(slave.device_name)	
		return ret			
	
	def get_xml_slave_by_name(self, slave_Name):
		print('get_xml_slave_by_name')
		xml_slave_list = self.tree.findall('Config/Slave')
		if xml_slave_list != None:
			print('xml_slave_list not None')
			for xml_slave in xml_slave_list:
				xml_nameInres = xml_slave.find('Info/NameInResource')
				if xml_nameInres != None:
					if xml_nameInres.text == slave_Name:
						print('find slave with name=',slave_Name)
						#print(ET.tostring(xml_slave))
						return xml_slave
				else:
					print('xml_slave has no Info/NameInResource')
		return None
		
	def decode_slave_InitCmds(self,slave_name):
		#print('decode_slave_InitCmds')
		ret = list()
		xml_slave = self.get_xml_slave_by_name(slave_name)
		if xml_slave != None:
			print ('Slave found:')
			print (YoUtil.get_xml_content(xml_slave))
			pass
			# get the list of InitCmds
			# build the list 
			# get the list of mailbox\CoE\InitCmds
			# build the list 
		return ret
		
	
if (__name__=='__main__'):
	Main()