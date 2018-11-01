import sys
from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import YoUtil


class ECatDC:
	pass
	
	def __init__(self,xml_dc):
		self.ReferenceClock = YoUtil.get_xml_node_as_int(xml_dc,'ReferenceClock')
		self.CycleTime0 = YoUtil.get_xml_node_as_int(xml_dc,'CycleTime0')
		self.CycleTime1 = YoUtil.get_xml_node_as_int(xml_dc,'CycleTime1')
		self.ShiftTime = YoUtil.get_xml_node_as_int(xml_dc,'ShiftTime')

		
	def tostring(self,indent=0):
		ret = YoUtil.get_indent(indent)+'DC -'+'ReferenceClock='+str(self.ReferenceClock)+' CycleTime0='+str(self.CycleTime0)+' CycleTime1='+str(self.CycleTime1)+' ShiftTime='+str(self.ShiftTime)
		return ret