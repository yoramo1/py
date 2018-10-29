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
		self.Index=None
		self.SubIndex=None
		self.Data=None
		
		xml_transitions = xml_initCmd.findall('Transition')
		for xml_transition in  xml_transitions:
			self.Transition.append(xml_transition.text)
		
		xml_comment = xml_initCmd.find('Comment')
		if xml_comment!=None:
			self.Comment = xml_comment.text		
		xml_ado = xml_initCmd.find('Ado')
		if xml_ado!=None:
			self.Ado = YoUtil.get_int(xml_ado.text)		
		xml_adp = xml_initCmd.find('Adp')
		if xml_adp!=None:
			self.Adp = YoUtil.get_int(xml_adp.text)	
		xml_Index = xml_initCmd.find('Index')
		if xml_Index!=None:
			self.Index = YoUtil.get_int(xml_Index.text)	
		xml_SubIndex = xml_initCmd.find('SubIndex')
		if xml_SubIndex!=None:
			self.SubIndex = YoUtil.get_int(xml_SubIndex.text)	
			
		xml_Data = xml_initCmd.find('Data')
		if xml_Data!=None:
			self.Data = xml_Data.text
			
	def tostring(self,indent=0):
		if self.Ado!=None:
			ret = YoUtil.get_indent(indent)+ 'InitCmd Ado,Adp=(0x%4.4x,0x%4.4x) [%s] - "%s" - Data=[%s]'%(self.Ado,self.Adp,self.get_transitions(),self.Comment,self.Data) + '\n'
		elif self.Index!=None:
			ret = YoUtil.get_indent(indent)+'InitCmd  Index=(0x%4.4x.%d) [%s] - "%s" - Data=[%s]'%(self.Index,self.SubIndex,self.get_transitions(),self.Comment,self.Data) + '\n'
		return ret
		
	def get_transitions(self):
		ret = ''
		for t in self.Transition:
			if len(ret)==0:
				ret+= t
			else:
				ret+=','+t
		return ret
		
		