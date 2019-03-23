import re
import pickle
from collections import Counter
from string import ascii_lowercase, punctuation

'''
NOTE: This is a variant of Peter Norvig's spell coreector ( https://norvig.com/spell-correct.html )
'''

class Spell_Corrector:
	def __init__(self):
		self.WORDS = dict()
		try:
			pickle_in = open("./templates/corpus.pickle", "rb")
			self.WORDS = pickle.load(pickle_in)
		except:
			self.pickled()
		self.N = sum(self.WORDS.values())	

	def pickled(self):
		self.WORDS = Counter(self.words(open('./templates/corpus.txt').read()))
		pickle_out = open("./templates/corpus.pickle", "wb")
		pickle.dump(self.WORDS, pickle_out)
		pickle_out.close()

	def words(self, text):
		return re.findall(r'\w+', text.lower())

	def P(self, word): 
		'''
		Probability of `word`.
		'''
		return self.WORDS[word] / self.N

	def correction(self, word): 
		'''
		Most probable spelling correction for word.
		'''
		return (word, max(self.candidates(word), key=self.P))

	def candidates(self, word): 
		'''
		Generate possible spelling corrections for word.
		'''
		return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])

	def known(self, words): 
		'''
		The subset of `words` that appear in the dictionary of WORDS.
		'''
		return set(w for w in words if w in self.WORDS)

	def edits1(self, word):
		'''
		All edits that are one edit away from `word`.
		'''
		splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
		deletes    = [L + R[1:]               for L, R in splits if R]
		transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
		replaces   = [L + c + R[1:]           for L, R in splits if R for c in ascii_lowercase]
		inserts    = [L + c + R               for L, R in splits for c in ascii_lowercase]
		return set(deletes + transposes + replaces + inserts)

	def edits2(self, word): 
		'''
		All edits that are two edits away from `word`.
		'''
		return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))

	def remove_punctuation(self, word):
		'''
		Returns a string without punctuation
		'''
		return word.translate(dict((ord(punct), None) for punct in punctuation))

if __name__ == '__main__':
	obj = Spell_Corrector()
	file, words = input("Enter file to be scanned: "), tuple()
	with open(file, 'r') as f:
		words = [obj.remove_punctuation(word.lower()) for line in f for word in re.findall(r'\w+', line)]
	for word in words:
		corr = obj.correction(word)[1]
		if corr != word:
			print("Error => Original: " + word + ", Corrected: " + corr)
