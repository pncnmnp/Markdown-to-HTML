from os import path
from sys import exit
import re
from bs4 import BeautifulSoup as bs # use if you want prettify feature, else feel free to uncomment it

'''
NOTE: This code is written to automate my blogging process to some extent.
	  I use vanilla HTML and CSS for my blog, hence this parser does not contain
	  any extended Markdown features.
'''

'''
Why have I used Regex instead of string manipulation ? - 1 word -> IndexError!!
Also looks clean while debugging!!
'''

'''
TODO:	
>> ======= support for <h1>
>> spelling error detection
>> grammatical mistake detection
>> ordered list [ done ]
>> unordered list [ done ]
>> simple blockquotes [ done ]
>> prettify with tabs [ not supporting for time being ]
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
		'''
		To add a filepath via command line
		Checks the validity of the filepath
		If the path is valid, will ask for the HTML title
		( If you are sure of validity of file-path, change self.filepath and self.blog_title directly )
		'''
		self.filepath = input("Enter filepath: ")
		if not self.is_valid_file():
			print("filepath" + str(self.filepath) + "does not exists")
			exit(0)
		else:
			self.open_file()
			self.blog_title = input("Enter title: ")

	def load_head(self):
		'''
		returns the head contents from the head_path
		( head content is content which will be appended to the head of the html file )
		'''
		lines = list()
		with open(self.head_path, 'r') as f:
			lines = [line.strip() for line in f.readlines()]
		lines[lines.index('<meta name="description" content=>')] = "<meta name=\"description\" content=" + "\""+self.blog_title+"\">"
		lines[lines.index('<title></title>')] = "<title>" + self.blog_title + "</title>"
		return lines

	def load_tail(self):
		'''
		returns the tail contents from the tail_path
		( tail content is content which will be appended to the tail of the html file )
		'''
		lines = list()
		with open(self.tail_path, 'r') as f:
			lines = [line.strip() for line in f.readlines()]
		return lines

	def is_valid_file(self):
		'''
		returns True if self.filepath is valid
		'''
		return path.isfile(self.filepath)

	def open_file(self):
		'''
		reads contents from self.filepath
		'''
		with open(self.filepath, 'r') as f:
			self.contents = [line.strip() for line in f.readlines()]

	def italic_parse(self, line):
		'''
		returns the italic parsed line
		'''
		italics = re.findall("([_].*?[_])", line)
		for word in italics:
			change = "<i>" + word[1:-1] + "</i>"
			line = line.replace(word, change)
		return line

	def bold_parse(self, line):
		'''
		returns the bold parsed line
		'''
		bold = re.findall("([*]{2}.*?[*]{2})", line)
		for word in bold:
			change = "<b>" + word[2:-2] + "</b>"
			line = line.replace(word, change)
		return line

	def code_parse(self, line):
		'''
		returns the code parsed line
		'''
		code = re.findall("([`].*?[`])", line)
		for word in code:
			change = "<pre>" + word[1:-1] + "</pre>"
			line = line.replace(word, change)
		return line

	def header_1(self, line):
		'''
		returns the # ( h1 ) parsed line
		'''
		head = re.findall("(?m)^#{1}(?!#)(.*)", line)
		if head != list():
			line = "<h1>" + head[0].strip() + "</h1>"
			return line

	def header_2(self, line):
		'''
		returns the ## ( h2 ) parsed line
		'''
		head = re.findall("(?m)^#{2}(?!#)(.*)", line)
		if head != list():
			line = "<h2>" + head[0].strip() + "</h2>"
			return line

	def header_3(self, line):
		'''
		returns the ### ( h3 ) parsed line
		'''
		head = re.findall("(?m)^#{3}(?!#)(.*)", line)
		if head != list():
			line = "<h3>" + head[0].strip() + "</h3>"
			return line

	def check_not_ul(self, line):
		'''
		returns False if unordered list
		else returns True
		'''
		try:
			return False if (line[0] == '-' and line[1] == ' ') else True
		except:
			return True

	def check_not_ol(self, line):
		'''
		returns False if ordered list
		else returns True
		'''
		try:
			return False if (line[0].isnumeric() and line[1] == '.' and line[2].isspace()) else True
		except:
			return True

	def check_not_blockquote(self, line):
		'''
		returns False if contains blockquote
		else returns True
		'''
		try:
			return False if (line[:2] == '> ') else True
		except:
			return True

	def para_parse(self, line):
		'''
		returns the paragraph parsed line
		'''
		para = re.findall("(.*)", line)
		not_contain_misc = len(set(para).intersection(set(['<hr>']))) == 0
		not_contains_header = len(set(para[0][:3]).intersection(set(['#', '##', "###"]))) == 0
		not_contains_ul_list = self.check_not_ul(para[0])
		not_contains_ol_list = self.check_not_ol(para[0])
		not_contains_blockquote = self.check_not_blockquote(para[0])
		if para != list() and not_contain_misc and not_contains_header and not_contains_ul_list and not_contains_ol_list and not_contains_blockquote:
			line = "<p>" + para[0] + "</p>"
			return line

	def hr_parse(self, line):
		'''
		returns the horizontal rule parsed line
		'''
		if line == '---':
			return "<hr>"

	def link_parse(self, line):
		'''
		returns the link parsed line
		'''
		links = re.findall("[^!]\[(.*?)\]\((.*?)\)", line)
		if links != list():
			for link in links:
				title, url = link[0], link[1]
				change = "<a href=\"" + url + "\">" + title + "</a>"
				line = line.replace("["+link[0]+"]"+"("+link[1]+")", change)
			return line

	def img_parse(self, line):
		'''
		returns the image parsed line
		'''
		imgs = re.findall("!\[(.*?)\]\((.*?)\)", line)
		if imgs != list():
			for img in imgs:
				alt, src = img[0], img[1]
				change = "<img src=\"" + src + "\" alt=\"" + alt + "\">"
				line = line.replace("!["+img[0]+"]"+"("+img[1]+")", change)
			return line

	def ul_parse(self, line, next_line):
		'''
		returns the unordered list parsed line
		'''
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
				elif self.check_not_ul(next_line) == True and self.ul_flag == False:
					change = "<ul><li>"	+ sent + "</li></ul>"
				line = line.replace(ul[0]+ul[1], change)
			return line

	def ol_parse(self, line, next_line):
		'''
		returns the ordered list parsed line
		'''
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
				elif self.check_not_ol(next_line) == True and self.ol_flag == False:
					change = "<ol><li>"	+ sent + "</li></ol>"
				line = line.replace(ol[0]+ol[1], change)
			return line

	def blockquote_parse(self, line):
		'''
		returns the blockquote parsed line
		'''
		blocks = re.findall("^(> )(.*)", line)
		if blocks != list():
			change = "<blockquote>" + blocks[0][1] + "</blockquote>"
			line  = line.replace(line, change)
		return line

	def parse(self):
		'''
		main parsing method used for parsing self.contents
		prints 'done!' if parsed successfully
		'''
		methods, parsed = [self.hr_parse, 
							self.para_parse, 
							self.blockquote_parse,
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
		'''
		saves the parsed html file
		'''
		head = self.load_head()
		tail = self.load_tail()
		body = self.contents

		with open(self.blog_title+'.html', 'w') as f:
			for part in [head, body, tail]:
				for line in part:
					f.write(line+'\n')
			f.close()

	def prettify(self):
		'''
		opens and saves the HTML file after indenting the code ( tabs NOT supported )
		'''
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
