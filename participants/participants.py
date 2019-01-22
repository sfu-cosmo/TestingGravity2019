#!/usr/bin/env python
# -*- coding: utf8 -*-

import re, csv
import itertools
from sys import argv

assert len(argv) > 1, "Specify output format as html, tags, or list..."
output = argv[1]


participants = [
	# invited speakers
	["Abele", "Hartmut", "TU Wien"],
	["Adelberger", "Eric", "University of Washington"],
	["Broderick", "Avery", "University of Waterloo"],
	["Buonanno", "Alessandra", "Albert Einstein Institute"],
	["Burgess", "Cliff", "McMaster University"],
	["Campanelli", "Manuela", "Rochester Institute of Technology"],
	["Gregory", "Ruth", "University of Durham"],
	["Heyl", "Jeremy", "University of British Columbia"],
	["Hui", "Lam", "Columbia University"],
	["Jain", "Bhuvnesh", "University of Pennsylvania"],
	["Kasevich", "Mark", "Stanford University"],
	["Khoury", "Justin", "University of Pennsylvania"],
	["Percival", "Will", "University of Waterloo"],
	["Psaltis", "Dimitrios", "Arizona University"],
	["Sasaki", "Misao", "IPMU"],
	["Silvestri", "Alessandra", "Leiden University"],
	["Stairs", "Ingrid", "University of British Columbia"],
	["So", "Chukman", "TRIUMF"],
	["Sushkov", "Sergey", "Kazan Federal University"],
	["Trodden", "Mark", "University of Pennsylvania"],
	["Vachaspati", "Tanmay", "Arizona State University"],
	["Wise", "Mark", "Caltech"],
	["Yunes", "Nico", "Montana State University"],
  	# LOC
  	["Frolov", "Andrei", "Simon Fraser University"],
  	["Pogosian", "Levon", "Simon Fraser University"],
]

soc = ["Frolov", "Fujiwara", "Galvez", "Pogosian", "Pospelov", "Psaltis", "Scott", "Silvestri"]
loc = ["Galvez", "Miller", "Pogosian", "Zucca"]

table = []

def mangle(affiliation):
	affiliation = re.sub(r"Royal Astronomical Society", 'RASC', affiliation)
	affiliation = re.sub(r"University of British Columbia", 'UBC', affiliation)
	affiliation = re.sub(r"Simon Fraser (U|u)niversity", 'SFU', affiliation)
	affiliation = re.sub(r"Canadian Institute for Theoretical Astrophysics", 'CITA', affiliation)
	affiliation = re.sub(r"Memorial University of Newfoundland", 'Memorial', affiliation)
	affiliation = re.sub(r"California Institut?e of Technology", 'Caltech', affiliation)
	affiliation = re.sub(r"California State University", 'CSU', affiliation)
	affiliation = re.sub(r"University of California(,|\s+at)?", 'UC', affiliation)
	affiliation = re.sub(r"(The\s+)?University of Texas(,|\s+at)?", 'UT', affiliation)
	affiliation = re.sub(r"University of Pennsylvania", 'UPenn', affiliation)
	affiliation = re.sub(r"Case Western Reserve", 'Case Western', affiliation)
	affiliation = re.sub(r"Perimeter.*", 'Perimeter', affiliation)
	affiliation = re.sub(r"ONERA, France", 'ONERA', affiliation)
	affiliation = re.sub(r"Yukawa Institute for Theoretical Physics", 'YITP', affiliation)
	affiliation = re.sub(r"Tokyo University of Science", 'TUS', affiliation)
	affiliation = re.sub(r"University College Dublin", 'UCD', affiliation)
	affiliation = re.sub(r"National Astronomical Observatory of Japan", 'NAOJ', affiliation)
	affiliation = re.sub(r"Institute of Physics, ASCR, Prague", 'Prague', affiliation)
	affiliation = re.sub(r"Max Planck Institute", 'MPI', affiliation)
	affiliation = re.sub(r"Lebedev.*", 'Lebedev', affiliation)
	affiliation = re.sub(r".*\(IKI\).*", 'IKI', affiliation)
	affiliation = re.sub(r"ITA - Aeronautics Institute of Technology", 'ITA', affiliation)
	affiliation = re.sub(r"Universidad Austral de Chile", 'UACh', affiliation)
	affiliation = re.sub(r"American University of Afghanistan", 'AUAF', affiliation)
	affiliation = re.sub(r"Prince Mohammad Bin Fahd University", 'PMU', affiliation)
	affiliation = re.sub(r"\s*Universit(y|é)(\s+(of|at|de))?(\s+(the))?\s*", '', affiliation)
	affiliation = re.sub(r"\s*Observatory(\s+(of|at|de))?(\s+(the))?\s*", '', affiliation)
	affiliation = re.sub(r",?\s*Dep(ar)?t(ment)?\s+of\s+.*", '', affiliation)
	return affiliation

def grouper(n, iterable, padvalue=None):
	"grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
	return itertools.izip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

def chunker(n, array, padvalue=None):
	"chunker(3, 'abcdefg', 'x') --> ('a','d','g'), ('b','e','x'), ('c','f','x')"
	l = len(array); m = (l+n-1)/n
	chunks = [array[i:min(i+m,l)] for i in range(0,l,m)]
	return itertools.izip_longest(*chunks, fillvalue=padvalue)

with open('participants.csv', 'rU') as csvfile:
	for row in csv.reader(csvfile, dialect=csv.excel):
		public = row[-1].lower()
		if public != 'yes' and not(output == 'tags' and public == 'no'): continue
		if row[5].lower() in [p[0].lower() for p in participants]: continue
		
		# grab names and affiliations
		first,last,affiliation = row[4:7]
		if len(last) == 0: last = row[15]
		if len(first) == 0: first = row[14]
		if len(affiliation) == 0: affiliation = row[16]
		affiliation = re.sub(r"[\(\)]+", '', affiliation)
		
		participants.append([last,first,affiliation])

participants.sort(key = lambda p: p[0])

for p in itertools.groupby(participants):
	last,first,affiliation = p[0]
	
	# fix stuff for people who cannot spell
	if last == "Lebed": affiliation = "University of Arizona"
	if last == "Afshordi": affiliation = "Perimeter Institute"
	if last == "Halenka": affiliation = "University of Michigan"
	if last == "Steer": affiliation = "APC, Paris"
	if last == "Saida": affiliation = "Daido University"
	if last == "Tanahashi": affiliation = "Osaka University"
	if last == "Kunstatter": affiliation = "University of Winnipeg"
	if last == "Rapetti": affiliation = "Boulder/NASA Ames"
	if last == "Deffayet": affiliation = "CNRS"
	if last == "Yamashita": affiliation = "Yukawa Institute for Theoretical Physics"
	if last == "JULIÉ": last = "Julié"
	if last == "SACHDEVA":
		first = "Tarun";last = "Sachdeva"
		affiliation = "Thapar University"
	if last == "de Rham": continue	
	
	# abbreviate name if it is too long
	if (len(first+last) > 24):
		first = re.sub(r'([A-Z])[a-z]+', r'\1.', first)
	
	# special roles...
	role = ""
	if last in soc: role = "[soc]"
	if last in loc: role = "[volunteer]"
	
	# formatted output
	if output == 'html': table.append("%s %s (%s)" % (first, last, mangle(affiliation)))
	if output == 'tags': table.append("\\nametag%s{%s %s}{%s}" % (role, first, last, mangle(affiliation)))
	if output == 'list': table.append("\\nametag%s{%s %s}{%s}" % (role, first, last, affiliation))

if output == 'html':
	print """<meta charset="UTF-8">
<font face="PT Sans Caption" size="6">Registered Participants:
</font>
<table>
<tbody style="vertical-align: top;">
<tr>
"""
	
	#for row in chunker(3, table, ""):
	#	print "<tr>"
	#	for name in row:
	#		print "<td style=\"width: 48ex;\">%s" % name
	
	for column in grouper((len(table)+2)/3, table):
		print "<td style=\"width: 30%;\"><ul>"
		for name in column:
			if name != None: print "<li>" + name
		print "</ul></td>"
	
	print """
</tr>
</tbody>
</table>
"""
else:
	for tag in table:
		print re.sub(r"\&", '\\&', tag)
