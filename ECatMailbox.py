import sys
from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import YoUtil
from ECatInitCmd import ECatInitCmd as InitCmd



class ECatMailbox:
	pass
	
	def __init__(self,xml_mailbox):
		self.Protocols = list()
		self.CoE = None
		
		xml_Protocol_list = xml_mailbox.findall('Protocol')
		if xml_Protocol_list!= None:
			for xml_protocol in xml_Protocol_list:
				self.Protocols.append(xml_protocol.text)
		
		xml_initCmd_list = xml_mailbox.findall('CoE/InitCmds/InitCmd')
		if xml_initCmd_list != None:
			self.CoE = list()
			for xml_initCmd in xml_initCmd_list:
				initcmd = InitCmd(xml_initCmd)
				self.CoE.append(initcmd)

	
	def tostring(self,ident=0):
		ret = YoUtil.get_indent(ident) + 'Mailbox Protocols: '
		ret += YoUtil.list_to_comma_separated(self.Protocols) +' '
		if self.CoE != None:
			ret += ("\n   InitCmds count= %d" % (len(self.CoE)))+'\n'
			for initCmd in self.CoE:
				str = initCmd.tostring(ident+1)
				ret +=(str)
		return ret
