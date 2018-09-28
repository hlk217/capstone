import numpy as np
from scipy import spatial
import pandas as pd
import re
from gensim.utils import simple_preprocess

def loadGloveModel(gloveFile):
	print ("Loading Glove Model")
	f = open(gloveFile,'r',encoding="utf8")#
	model = {}
	for line in f:
		splitLine = line.split()
		word = splitLine[0]
		embedding = np.array([float(val) for val in splitLine[1:]])
		model[word] = embedding
	print ("Done.",len(model)," words loaded!")
	return model


def calcAvg(s,model, avgVec = True):
	words = simple_preprocess(s)
	words_count = len(words)
	embedding_dim = 300
	embedding_matrix = np.zeros((words_count, embedding_dim))
	i = 0
	for word in words:
		embedding_vector = model.get(word)

		if embedding_vector is not None:
			# Words not found in embedding index will be all-zeros.
			embedding_matrix[i] = embedding_vector
		i+=1

	if avgVec:
		return embedding_matrix.mean(axis = 0)
	else:
		return embedding_matrix


def similarity_score(df, i,j,model):
	vec1 = calcAvg(df.iloc[i,0], model)
	vec2 = calcAvg(df.iloc[j,0], model)

	score = 1-spatial.distance.cosine(vec1,vec2)
	return score


def find_similar(df, i, model, count = 10):
	score_dic = {}
	for j in range(0, df.shape[0]):
		score_dic[j] = similarity_score(df,i,j, model)
	sorted_by_value = sorted(score_dic.items(), key=lambda kv: kv[1], reverse = True)
	return sorted_by_value[0:count]
