import sys
from xml.etree.ElementTree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import YoUtil


class ECatInitCmd:
	def __init__(self,xml_initCmd):
		self.Transition = list()
		self.Comment = None
		self.Cmd = None
		self.Adp=None
		self.Ado=None
		self.Data=None
		
		
		