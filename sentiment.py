import sys
import os
import csv

class Phrase():
	def __init__(self):
		self.label = -1
		self.diff = 0
		self.excl = 0
		self.neg = 0
		self.ngtneg = 0
		self.ngtpos = 0
		self.pos = 0
		self.w1 = "UNK"
		self.w2 = "UNK"
		self.w3 = "UNK"
		self.w4 = "UNK"
		self.w5 = "UNK"


def main():
	index = generateIndex(sys.argv[3])
	phrases = processPhrases(sys.argv[1], index)
	makeOutputFile(sys.argv[1], phrases)
	phrases = processPhrases(sys.argv[2], index)
	makeOutputFile(sys.argv[2], phrases)

def makeOutputFile(inFile, phrases):
	inFile = inFile.split("/")[-1]
	outFile =  inFile[:len(inFile)-4] + "_features.csv"
	print(outFile)

	file = open(outFile, 'w')
	writer = csv.writer(file)
	data = ['LABEL', 'DIFF', 'EXCL', 'NEG', 'NGTNEG', 'NGTPOS', 'POS', 'W1', 'W2', 'W3', 'W4', 'W5']
	writer.writerow(data)
	for phrase in phrases:
		writer.writerow([phrase.label, phrase.diff, phrase.excl, phrase.neg, phrase.ngtneg, \
			phrase.ngtpos, phrase.pos, phrase.w1, phrase.w2, phrase.w3, phrase.w4, phrase.w5])

def generateIndex(lexFile):
	index = dict()
	file = open(lexFile)
	reader = csv.reader(file, delimiter=' ')
	for row in reader:
		if row == []:
			break
		index[row[0]] = row[-1]
	return index

def processPhrases(file, index):
	negs = ["no", "not", "never", "isn't", "wasn't", "won't"]
	phrases = []
	curr = []
	phr = Phrase()
	idx = 0
	waitPos = 0
	waitNeg = 0

	file = open(file)
	reader = csv.reader(file, delimiter=' ')
	for row in file:
		if row == "\n":
			phr.diff = phr.pos - phr.neg
			phrases.append(phr)
			phr = Phrase()
			idx = 0
			curr = []
			continue
		row = row.rstrip('\n')
		
		if waitPos > 0:
			if row in index and index[row] == "POS":
				phr.ngtpos += 1
				waitPos = 0
			else:
				waitPos -= 1
		if waitNeg > 0:
			if row in index and index[row] == "NEG":
				phr.ngtneg += 1
				waitNeg = 0
			else:
				waitNeg -= 1

		if idx == 0:
			phr.label = row
		elif idx == 1:
			phr.w1 = row
		elif idx == 2:
			phr.w2 = row
		elif idx == 3:
			phr.w3 = row
		elif idx == 4:
			phr.w4 = row
		elif idx == 5:
			phr.w5 = row
		idx += 1

		if row == "!":
			phr.excl += 1

		if row in index and index[row] == "POS":
			phr.pos += 1
		elif row in index and index[row] == "NEG":
			phr.neg += 1

		if row in negs:
			if len(curr) > 0 and (curr[-1] in index and index[curr[-1]] == "POS"):
				phr.ngtpos += 1
			elif len(curr) > 1 and (curr[-2] in index and index[curr[-2]] == "POS"):
				phr.ngtpos += 1
			else:
				waitPos = 2

			if len(curr) > 0 and (curr[-1] in index and index[curr[-1]] == "NEG"):
				phr.ngtneg += 1
			elif len(curr) > 1 and (curr[-2] in index and index[curr[-2]] == "NEG"):
				phr.ngtneg += 1
			else:
				waitNeg = 2
		curr.append(row)
	phr.diff = phr.pos - phr.neg
	phrases.append(phr)

	return phrases

if __name__ == "__main__":
    main()