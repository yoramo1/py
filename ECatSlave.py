import sys
from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import YoUtil
import ECatInitCmd
from ECatMailbox import ECatMailbox as Mailbox


class ECatSlave:
	pass
	
	def __init__(self,xml_slave):
		self.name_in_res = None
		self.device_name = None
		self.ProductName = None
		self.vendor_id = None
		self.productCode = None
		self.revisionNo = None
		self.InitCmds = list()
		self.Mailbox = None
		
		xml_nameInres = xml_slave.find('Info/NameInResource')
		if xml_nameInres != None:
			self.name_in_res = xml_nameInres.text
		xml_name = xml_slave.find('Info/Name')
		if xml_name != None:
			self.device_name = xml_name.text
		xml_ProductName = xml_slave.find('Info/ProductName')
		if xml_ProductName != None:
			self.ProductName = xml_ProductName.text
		xml_vendor_id = xml_slave.find('Info/VendorId')
		if xml_vendor_id!=None:
			self.vendor_id = YoUtil.get_int(xml_vendor_id.text)
		xml_productCode = xml_slave.find('Info/ProductCode')
		if xml_productCode!=None:
			self.productCode = YoUtil.get_int(xml_productCode.text)
		xml_revisionNo = xml_slave.find('Info/RevisionNo')
		if xml_revisionNo!=None:
			self.revisionNo = YoUtil.get_int(xml_revisionNo.text)
				
		self.load_initCmds(xml_slave)
		self.load_mailbox(xml_slave)
		self.load_DC(xml_slave)

	def load_initCmds(self,xml_slave):
		xml_initCmd_list = xml_slave.findall('InitCmds/InitCmd')
		if xml_initCmd_list!=None:
			for xml_initCmd in xml_initCmd_list:
				initcmd = ECatInitCmd.ECatInitCmd(xml_initCmd)
				self.InitCmds.append(initcmd)
		
	def load_mailbox(self,xml_slave):
		xml_mailbox = xml_slave.find('Mailbox')
		if xml_mailbox!=None:
			self.Mailbox = Mailbox(xml_mailbox)
					
		
	def load_DC(self,xml_slave):
		xml_dc = xml_slave.find('DC')
		if xml_dc!=None:
			pass
		
	def tostring(self, type):
		ret = ("Slave (%s,%s, (%8x,%8x,%8x) -> %s) " % (self.name_in_res, self.device_name,self.vendor_id,self.productCode,self.revisionNo,self.ProductName))
		if self.Mailbox!= None:
			ret+='\n'+self.Mailbox.tostring()
		if type >=1:
			ret += ("\n   InitCmds count= %d" % (len(self.InitCmds)))+'\n'
			for initCmd in self.InitCmds:
				str = initCmd.tostring()
				ret +=(str)
		return ret
		