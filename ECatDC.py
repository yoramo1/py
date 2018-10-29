import sys
from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import YoUtil


class ECatDC:
	pass
	
	def __init__(self,xml_dc):
		self.ReferenceClock = None
		self.CycleTime0 = None
		self.CycleTime1 = None
		self.ShiftTime= None
		
		xml_ReferenceClock = xml_dc.find('ReferenceClock')
		if xml_ReferenceClock != None:
			self.ReferenceClock = YoUtil.get_int(xml_ReferenceClock.text)
		
		xml_CycleTime0 = xml_dc.find('CycleTime0')
		if xml_CycleTime0 != None:
			self.CycleTime0 = YoUtil.get_int(xml_CycleTime0.text)
		xml_CycleTime1 = xml_dc.find('CycleTime1')
		if xml_CycleTime1 != None:
			self.CycleTime1 = YoUtil.get_int(xml_CycleTime1.text)
		xml_ShiftTime = xml_dc.find('ShiftTime')
		if xml_ShiftTime != None:
			self.ShiftTime = YoUtil.get_int(xml_ShiftTime.text)

		
	def tostring(self,indent=0):
		ret = YoUtil.get_indent(indent)+'DC -'+'ReferenceClock='+str(self.ReferenceClock)+' CycleTime0='+str(self.CycleTime0)+' CycleTime1='+str(self.CycleTime1)+' ShiftTime='+str(self.ShiftTime)+'\n'
		return ret