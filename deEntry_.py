#-*-coding: utf-8 -*-

import string
import re,collections
import sys
from java.lang import String
import java.lang

from com.pnfsoftware.jeb.client.api import IScript  
from com.pnfsoftware.jeb.client.api import IScript, IGraphicalClientContext  
from com.pnfsoftware.jeb.core import RuntimeProjectUtil  
from com.pnfsoftware.jeb.core.actions import Actions, ActionContext, ActionXrefsData  
from com.pnfsoftware.jeb.core.events import JebEvent, J  
from com.pnfsoftware.jeb.core.output import AbstractUnitRepresentation, UnitRepresentationAdapter  
from com.pnfsoftware.jeb.core.units.code import ICodeUnit, ICodeItem  
from com.pnfsoftware.jeb.core.units.code.java import IJavaSourceUnit, IJavaStaticField, IJavaNewArray, IJavaAssignment, IJavaConstant, IJavaCall, IJavaField, IJavaMethod, IJavaClass  
from com.pnfsoftware.jeb.core.actions import ActionTypeHierarchyData  
from com.pnfsoftware.jeb.core.actions import ActionRenameData  
from com.pnfsoftware.jeb.core.util import DecompilerHelper  
from com.pnfsoftware.jeb.core.output.text import ITextDocument  
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit  

from java.lang import Runnable

# 将Dec.jar包加入到sys.path中
sys.path.append(r"E:\Download\JEB.android.decompiler.3.0.0.201808031948Pro\scripts\app-debug-dex2jar.jar")

from com.example.myapplication import dxshield

class deEntry(IScript):
    def run(self, ctx):
		ctx.executeAsync("Running name detection...", JEB2AutoRename(ctx))
		print('Done')

class JEB2AutoRename(Runnable):  
	def __init__(self, ctx):
		self.ctx = ctx

	def decrypt(self, target):
		return dxshield.E(target)
		
	def run(self):
		ctx = self.ctx

		# print self.dec("Y\\\\@W[\\\u001CQ\\LWVF\u0016S[FQ]V\u001C|wtwlw")
		self.decr_method = "Lcom/xshield/aa;->E(Ljava/lang/String;)Ljava/lang/String;"

		engctx = ctx.getEnginesContext()
		if not engctx:
			print('Back-end engines not initialized')

		projects = engctx.getProjects()
		if not projects:
			print('There is no opened project')

		project = projects[0] # Get current project(IRuntimeProject)
		#获取所有的java类
		units = RuntimeProjectUtil.findUnitsByType(project, IJavaSourceUnit, False)
		print('-------------------------')
		for unit in units:
			cstbuilder = unit.getFactories().getConstantFactory()
			class_ = unit.getClassElement()
			# 遍历每个类的方法
			for method in class_.getMethods():
				# print class_.getName(), "  ", method.getName()
				body = method.getBody()
				# 遍历方法中的每行语句
				for i in range(body.size()):
					part = body.get(i)
					print class_.getName(), ", ", method.getName(), ", part ", part
					# 如果是赋值语句，取右操作数
					if isinstance(part, IJavaAssignment):
						right = part.getRight()
						print "IJavaAssignment right ", right
						if isinstance(right, IJavaCall):
							# print "JavaCall:", right.getMethod().getSignature()
							# 如果右操作数是函数调用且调用了解密函数
							if right.getMethod().getSignature() == self.decr_method:
								# print "IJavaAssignment JavaCall:", method.getName()
								for arg in right.getArguments():
									if isinstance(arg, IJavaConstant):
										# print ('replace ' + arg.getString() + ' to ' + self.decrypt(arg.getString()))
										part.replaceSubElement(
											right,
											cstbuilder.createString(
												self.decrypt(arg.getString())
											)
										)
					elif isinstance(part, IJavaCall):
						print "IJavaCall part ", part, " fun ", part.getMethod().getSignature()
						subElements = part.getSubElements()
						for element in subElements :
							print "element ", element.toString()
							if isinstance(element, IJavaCall):
								print "element call ", element.getMethod().getSignature()
								if element.getMethod().getSignature() == self.decr_method:
									for arg in element.getArguments():
										if isinstance(arg, IJavaConstant):
											# print ('replace ' + arg.getString() + ' to ' + self.decrypt(arg.getString()))
											part.replaceSubElement(
												element,
												cstbuilder.createString(
													self.decrypt(arg.getString())
												)
											)