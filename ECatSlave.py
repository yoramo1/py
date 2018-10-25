import sys
from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import YoUtil
import ECatInitCmd


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
		xml_initCmd_list = xml_slave.findall('InitCmds/InitCmd')
		if xml_initCmd_list!=None:
			for xml_initCmd in xml_initCmd_list:
				initcmd = ECatInitCmd.ECatInitCmd(xml_initCmd)
				self.InitCmds.append(initcmd)

	def print(self, type):
		print("(%s,%s, (%8x,%8x,%8x) -> %s) " % (self.name_in_res, self.device_name,self.vendor_id,self.productCode,self.revisionNo,self.ProductName))
		if type >=1:
			print ("InitCmds count= %d" % (len(self.InitCmds)))
		
		