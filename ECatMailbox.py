import sys
from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import YoUtil
from ECatInitCmd import ECatInitCmd as InitCmd
from operator import itemgetter, attrgetter


class ECatMailbox:
	pass
	
	def __init__(self,xml_mailbox):
		self.Protocols = list()
		self.CoEInitCmds = None
		self.Send_Start = None
		self.Send_Length = None
		self.Recv_Start = None
		self.Recv_Length = None
		self.Recv_PollTime = None
		self.Recv_StatusBitAddr = None
		
		self.Send_Start = YoUtil.get_xml_node_as_int(xml_mailbox,'Send/Start')
		self.Send_Length = YoUtil.get_xml_node_as_int(xml_mailbox,'Send/Length')
		self.Recv_Start = YoUtil.get_xml_node_as_int(xml_mailbox,'Recv/Start')
		self.Recv_Length = YoUtil.get_xml_node_as_int(xml_mailbox,'Recv/Length')
		self.Recv_PollTime = YoUtil.get_xml_node_as_int(xml_mailbox,'Recv/PollTime')
		self.Recv_StatusBitAddr = YoUtil.get_xml_node_as_int(xml_mailbox,'Recv/StatusBitAddr')
			
		xml_Protocol_list = xml_mailbox.findall('Protocol')
		if xml_Protocol_list!= None:
			for xml_protocol in xml_Protocol_list:
				self.Protocols.append(xml_protocol.text)
		
		xml_initCmd_list = xml_mailbox.findall('CoE/InitCmds/InitCmd')
		if xml_initCmd_list != None:
			self.CoEInitCmds = list()
			for xml_initCmd in xml_initCmd_list:
				initcmd = InitCmd(xml_initCmd)
				self.CoEInitCmds.append(initcmd)

	
	def tostring(self,ident=0):
		ret = YoUtil.get_indent(ident) + 'Mailbox'
		ret += '\n'+YoUtil.get_indent(ident+1) + 'Protocols: '
		ret += YoUtil.list_to_comma_separated(self.Protocols) +' '
		ret += '\n'+YoUtil.get_indent(ident+1)+("Send: Start=%d Length= %d, Recv: Start=%d, Length=%d" % (self.Send_Start,self.Send_Length,self.Recv_Start,self.Recv_Length))
		if self.Recv_PollTime!= None:
			ret+= (", PollTime=%d") %(self.Recv_PollTime)
		if self.Recv_StatusBitAddr!= None:
			ret+= (", StatusBitAddr=%d") %(self.Recv_StatusBitAddr)
		if self.CoEInitCmds != None:
			self.CoEInitCmds=sorted(self.CoEInitCmds,key=attrgetter('Index'))
			ret += ("\n%sCoE InitCmds count= %d" % (YoUtil.get_indent(ident+1),len(self.CoEInitCmds)))+'\n'
			for initCmd in self.CoEInitCmds:
				str = initCmd.tostring(ident+2)
				ret +=(str)
		return ret
