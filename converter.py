#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb; cgitb.enable()
import os
import sys
import codecs
import re
import time
import shutil
import random
import zipfile
import commands

def convert(fileName, form):
	content = replaceElements(fileName, form)

	writer = open(fileName, "w")
	writer.write(content)
	writer.close()


def replaceElements(fileName, form):
	lines = open(fileName).read()

	for key in form:
		value = form.getvalue(key)
		lines = lines.replace('%' + key + '%', value)

	return re.sub("%[^\"#$%&'()=-]+?%", "", lines);


def createDirectoryName():
	return str(int(time.time())) + "-" + hex(random.randint(0, 1000000000)).upper()[2:-1].zfill(8)


print "Content-type: text/plain; charset=utf-8;"
print

if os.environ['REQUEST_METHOD'] == "POST":
	form = cgi.FieldStorage()
	result = ""
	
	src = '../Templates/order'
	dirname = createDirectoryName()
	dest =  '../tmp/' + dirname
	shutil.copytree(src, dest)

	#convert('../Templates/order/content.xml', form)
	convert(str(dest) + '/content.xml', form)
	convert(str(dest) + '/styles.xml', form)
	os.system('../odt.sh ' + dirname)
	print dirname

	path = 'java -jar ~/jodconverter-2.2.2/lib/jodconverter-cli-2.2.2.jar ' + '../tmp/' + dirname + '.odt ' + '../tmp/' + dirname + '.pdf'
	os.system(path)
	#print commands.getoutput(path)

