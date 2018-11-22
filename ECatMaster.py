import sys
from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import YoUtil
import ECatInitCmd
from operator import itemgetter, attrgetter


class ECatMaster:
	def __init__(self,xml_master):
		self.InitCmds = list()
		self.name = None
		
		if xml_master!= None:
			self.load_info(xml_master)
			self.load_initCmds(xml_master)
		
	def load_info(self, xml_master):
		xml_info = xml_master.find('Info')
		if xml_info!=None:
			xml_name = xml_info.find('Name')
			if xml_name!=None:
				self.name = xml_name.text

	def load_initCmds(self,xml_master):
		xml_initCmd_list = xml_master.findall('InitCmds/InitCmd')
		if xml_initCmd_list!=None:
			for xml_initCmd in xml_initCmd_list:
				initcmd = ECatInitCmd.ECatInitCmd(xml_initCmd)
				self.InitCmds.append(initcmd)

	def tostring(self, type,indent=0):
		ret = ("Master name='%s' " % (YoUtil.str_strip(self.name)))+'\n'
		ret += ("%sInitCmds count= %d" % (YoUtil.get_indent(indent+1),len(self.InitCmds)))+'\n'
		self.InitCmds=sorted(self.InitCmds,key=attrgetter('Ado'))
		for initCmd in self.InitCmds:
			str = initCmd.tostring(indent+2)
			ret +=(str)
		return ret	
		
