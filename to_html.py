from os import path
from sys import exit
import re

class Convert:
	'''
	This parser supports all the elements mentioned in John Gruber’s original markdown design.
	It converts a '.md' file to '.html' file
	'''
	def __init__(self):
		self.filepath = str()
		self.contents = list()

	def add_filepath(self):
		self.filepath = input("Enter filepath: ")
		if not self.is_valid_file():
			print("filepath" + str(self.filepath) + "does not exists")
			exit(0)
		else:
			self.open_file()

	def is_valid_file(self):
		return path.isfile(self.filepath)

	def open_file(self):
		with open(self.filepath) as f:
			self.contents = [line.strip() for line in f.readlines()]

	def italic_parse(self, line):
		italics = re.findall("([_].*?[_])", line)
		for word in italics:
			change = "<i>" + word[1:-1] + "</i>"
			line = line.replace(word, change)
		return line

	def bold_parse(self, line):
		bold = re.findall("([*]{2}.*?[*]{2})", line)
		for word in bold:
			change = "<b>" + word[2:-2] + "</b>"
			line = line.replace(word, change)
		return line

	def code_parse(self, line):
		code = re.findall("([`].*?[`])", line)
		for word in code:
			change = "<pre>" + word[1:-1] + "</pre>"
			line = line.replace(word, change)
		return line

	def header_1(self, line):
		head = re.findall("(?m)^#{1}(?!#)(.*)", line)
		if head != list():
			line = "<h1>" + head[0].strip() + "</h1>"
			return line

	def header_2(self, line):
		head = re.findall("(?m)^#{2}(?!#)(.*)", line)
		if head != list():
			line = "<h2>" + head[0].strip() + "</h2>"
			return line

	def header_3(self, line):
		head = re.findall("(?m)^#{3}(?!#)(.*)", line)
		if head != list():
			line = "<h3>" + head[0].strip() + "</h3>"
			return line

	def para_parse(self, line):
		para = re.findall("(.*)", line)
		not_contain_misc = len(set(para).intersection(set(['<hr>']))) == 0
		contains_header = len(set(para[0][:3]).intersection(set(['#', '##', "###"]))) == 0
		if para != list() and not_contain_misc and contains_header:
			line = "<p>" + para[0] + "</p>"
			return line

	def hr_parse(self, line):
		if line == '---':
			return "<hr>"

	def link_parse(self, line):
		links = re.findall("\[(.*?)\]\((.*?)\)", line)
		if links != list():
			for link in links:
				title = link[0]
				url = link[1]
				change = "<a href=\"" + url + "\">" + title + "</a>"
				line = line.replace("["+link[0]+"]"+"("+link[1]+")", change)
			return line

	def parse(self):
		methods, parsed = [self.hr_parse, self.para_parse, self.link_parse, self.italic_parse, 
							self.bold_parse, self.code_parse, self.header_1, 
							self.header_2, self.header_3], ''
		for line in range(len(self.contents)):
			for method in methods:
				parsed = method(self.contents[line])
				if parsed:
					self.contents[line] = self.contents[line].replace(self.contents[line], parsed)
			print(self.contents[line])

if __name__ == '__main__':
	o = Convert()
	o.filepath = 'demo.md'
	o.open_file()
	o.parse()