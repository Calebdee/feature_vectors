# How to generate feature_vectors
python sentiment.py [train-file] [test-file] [lexicon-file]

# With provided data files
python sentiment.py data-files/trainB.txt data-files/testB.txt data-files/lexicon.txt

# How to generate bag of words
python sentimentBOW.py [train-file] [test-file] [threshold]

# With provided data files and threshold of 5
python sentimentBOW.py data-files/trainB.txt data-files/testB.txt 5

I tested my code on EngmanLab0-15

I am unaware of any problems or limitations, when I run the diff command on files I do not get any differences.
