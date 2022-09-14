import sys
import os
import csv

def main():
	train = sys.argv[1]
	test = sys.argv[2]
	threshold = int(sys.argv[3])
	feature_set = createFeatureSet(train)
	feature_mapping = thresholdFeatureMapping(feature_set, threshold)
	train_bow = createSentences(train, feature_mapping)
	makeOutputFile(train, train_bow, threshold)

def createFeatureSet(file):
	file = open(file)
	feature_set = dict()
	skipLabel = False

	for row in file:
		if skipLabel: 
			skipLabel = False
			continue
		if row == "\n":
			skipLabel = True
			continue

		row = row.rstrip('\n')

		if row in feature_set:
			feature_set[row] += 1
		else:
			feature_set[row] = 1
	return feature_set

def thresholdFeatureMapping(feature_set, threshold):
	sorted_features = [k for k, v in sorted(feature_set.items(), key=lambda kv: (-kv[1], kv[0]))]
	#sorted_features = sorted(feature_set, key=feature_set.get, reverse=True)
	feature_mapping = dict()

	index = 0
	while(threshold <= feature_set[sorted_features[index]]):
		featureName = "F" + str(index)
		feature_mapping[sorted_features[index]] = featureName
		index += 1

	return feature_mapping

def createSentences(file, feature_mapping):
	sentence_bow = []
	features = [0]*(len(feature_mapping)+1)
	skipLabel = True

	file = open(file)
	for row in file:
		if skipLabel: 
			row = row.rstrip('\n')
			features[0] = row
			skipLabel = False
			continue
		if row == "\n":
			sentence_bow.append(features)
			features = [0]*(len(feature_mapping)+1)
			skipLabel = True
			continue
		row = row.rstrip('\n')
		if row in feature_mapping:
			index = int(feature_mapping[row][1:])+1
			features[index] += 1
	sentence_bow.append(features)
	return sentence_bow

def makeOutputFile(inFile, sentences, threshold):
	inFile = inFile.split("/")[-1]
	outFile =  inFile[:len(inFile)-4] + "_BOW" + str(threshold) + ".csv"

	file = open(outFile, 'w')
	writer = csv.writer(file)
	data = ["LABEL"] + ["F" + str(i) for i in range(len(sentences[0])-1)]
	writer.writerow(data)
	for sentence in sentences:
		print(sentence)
		writer.writerow(sentence)



if __name__ == "__main__":
    main()