#! /usr/bin/python

class preprocessor:
	@staticmethod
	def fetch(file):
		import os
		cmd = "wget -O " + file + " http://resource.data.one.gov.hk/td/journeytime.xml"
		os.system(cmd)

	@staticmethod
	def do(file):
		preprocessor.fetch(file)
		import re
		f = open(file, "r")
		b = "" 
		for l in f:
			if re.search("<jtis_journey_list", l):
				b += "<jtis_journey_list>"
			else:
				b += l + "\n"
		f.close()
		return b

class route:
	def __init__(self, to, fr):
		self._to = to
		self._fr = fr
		self._delim = "-"

	def name(self):
		return self._to + self._delim + self._fr

	def __eq__(self, other):
		return self.name() == other.name()

	def __hash__(self):
		return int(''.join(str(ord(c)) for c in self.name()))

class parser:
	def __init__(self, str):
		import xml.etree.ElementTree as et
		self._xmlRoot = et.fromstring(str)
		self.data = {}
		self.buildDict()

	def buildDict(self):
		for i in self._xmlRoot:
			r = route(i.find("LOCATION_ID").text,i.find("DESTINATION_ID").text)
			datum = {}
			for j in i:
				datum[j.tag] = j.text
			self.data[r] = datum
		return self.data
	
	def getColour(self, r):
		b = self.data[r]
		return b["COLOUR_ID"]

pa = parser(preprocessor.do("journeytime.xml"))
print pa.getColour(route("H11", "CH"))
