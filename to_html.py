from os import path
from sys import exit
import re
from bs4 import BeautifulSoup as bs

'''
NOTE: This code is written to automate my blogging process to some extent.
	  I use vanilla HTML and CSS for my blog, hence this parser does not contain
	  any extended Markdown features.
'''

'''
TODO:	1. ordered list [ done ]
		2. unordered list [ done ]
		3. blockquotes
		4. prettify with tabs
		5. spelling error detection
		6. grammatical mistake detection
'''

class Convert:
	'''
	This parser supports all the elements mentioned in John Gruber’s original markdown design.
	It converts a '.md' file to '.html' file
	'''
	def __init__(self):
		self.filepath = str()
		self.head_path = './templates/head.txt'
		self.tail_path = './templates/tail.txt'
		self.contents = list()
		self.blog_title = str()
		self.ul_flag = False
		self.ol_flag = False

	def add_filepath(self):
		self.filepath = input("Enter filepath: ")
		if not self.is_valid_file():
			print("filepath" + str(self.filepath) + "does not exists")
			exit(0)
		else:
			self.open_file()
			self.blog_title = input("Enter blog title: ")

	def load_head(self):
		lines = list()
		with open(self.head_path, 'r') as f:
			lines = [line.strip() for line in f.readlines()]
		lines[lines.index('<meta name="description" content=>')] = "<meta name=\"description\" content=" + "\""+self.blog_title+"\">"
		lines[lines.index('<title></title>')] = "<title>" + self.blog_title + "</title>"
		return lines

	def load_tail(self):
		lines = list()
		with open(self.tail_path, 'r') as f:
			lines = [line.strip() for line in f.readlines()]
		return lines

	def is_valid_file(self):
		return path.isfile(self.filepath)

	def open_file(self):
		with open(self.filepath, 'r') as f:
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

	def check_not_ul(self, line):
		try:
			return False if (line[0] == '-' and line[1] == ' ') else True
		except:
			return True

	def check_not_ol(self, line):
		try:
			return False if (line[0].isnumeric() and line[1] == '.' and line[2].isspace()) else True
		except:
			return True

	def para_parse(self, line):
		para = re.findall("(.*)", line)
		not_contain_misc = len(set(para).intersection(set(['<hr>']))) == 0
		not_contains_header = len(set(para[0][:3]).intersection(set(['#', '##', "###"]))) == 0
		not_contains_ul_list = self.check_not_ul(para[0])
		not_contains_ol_list = self.check_not_ol(para[0])
		if para != list() and not_contain_misc and not_contains_header and not_contains_ul_list and not_contains_ol_list:
			line = "<p>" + para[0] + "</p>"
			return line

	def hr_parse(self, line):
		if line == '---':
			return "<hr>"

	def link_parse(self, line):
		links = re.findall("[^!]\[(.*?)\]\((.*?)\)", line)
		if links != list():
			for link in links:
				title, url = link[0], link[1]
				change = "<a href=\"" + url + "\">" + title + "</a>"
				line = line.replace("["+link[0]+"]"+"("+link[1]+")", change)
			return line

	def img_parse(self, line):
		imgs = re.findall("!\[(.*?)\]\((.*?)\)", line)
		if imgs != list():
			for img in imgs:
				alt, src = img[0], img[1]
				change = "<img src=\"" + src + "\" alt=\"" + alt + "\">"
				line = line.replace("!["+img[0]+"]"+"("+img[1]+")", change)
			return line

	def ul_parse(self, line, next_line):
		uls = re.findall("(?m)^(-)(.*)", line)
		if uls != list():
			for ul in uls:
				sent = ul[1]
				if self.check_not_ul(next_line) == False and self.ul_flag == False:
					change = "<ul><li>" + sent + "</li>"
					self.ul_flag = True
				elif self.check_not_ul(next_line) == False and self.ul_flag == True:
					change = "<li>" + sent + "</li>"
				elif self.check_not_ul(next_line) == True and self.ul_flag == True:
					change = "<li>" + sent + "</li></ul>"
					self.ul_flag = False
				line = line.replace(ul[0]+ul[1], change)
			return line

	def ol_parse(self, line, next_line):
		ols = re.findall("^(\d\.)(.*)", line)
		if ols != list():
			for ol in ols:
				sent = ol[1][1:]
				if self.check_not_ol(next_line) == False and self.ol_flag == False:
					change = "<ol><li>" + sent + "</li>"
					self.ol_flag = True
				elif self.check_not_ol(next_line) == False and self.ol_flag == True:
					change = "<li>" + sent + "</li>"
				elif self.check_not_ol(next_line) == True and self.ol_flag == True:
					change = "<li>" + sent + "</li></ol>"
					self.ol_flag = False
				line = line.replace(ol[0]+ol[1], change)
			return line

	def parse(self):
		methods, parsed = [self.hr_parse, 
							self.para_parse, 
							self.ol_parse,
							self.ul_parse,
							self.link_parse, 
							self.img_parse, 
							self.italic_parse, 
							self.bold_parse, 
							self.code_parse, 
							self.header_1, 
							self.header_2, 
							self.header_3], ''
		for line in range(len(self.contents)):
			for method in methods:
				# To insert <ol></ol> and <ul></ul> tags
				if method == self.ol_parse or method == self.ul_parse:
					try:
						parsed = method(self.contents[line], self.contents[line+1])
					except IndexError:
						parsed = method(self.contents[line], '')
				else:
					parsed = method(self.contents[line])

				if parsed:
					self.contents[line] = self.contents[line].replace(self.contents[line], parsed)
			print(self.contents[line])
		print("done!")

	def save_parsed_html(self):
		head = self.load_head()
		tail = self.load_tail()
		body = self.contents

		with open(self.blog_title+'.html', 'w') as f:
			for part in [head, body, tail]:
				for line in part:
					f.write(line+'\n')
			f.close()

	def prettify(self):
		lines = list()
		with open(self.blog_title+'.html', 'r') as f:
			lines = f.readlines()

		with open(self.blog_title+'.html', 'w') as f:
			soup = bs(''.join(lines), features="lxml")
			prettyHTML = soup.prettify()
			f.writelines(prettyHTML)
			f.close()

if __name__ == '__main__':
	o = Convert()
	o.filepath = 'demo.md'
	o.blog_title = 'demo'
	o.open_file()
	o.parse()
	o.save_parsed_html()
