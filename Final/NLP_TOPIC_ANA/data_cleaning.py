import numpy as np
import pandas as pd
import re

def data_cleaning(all_data,removeNa = True, keep_percent = False, rmPunctuation = True, rmNums = True, rmStopWords = True):
	
	all_data['alltext'] = all_data['alltext'].apply(lambda x: x.lower())
	
	if removeNa:
		all_data = all_data[all_data['alltext'].isnull() == False]


	if keep_percent:
		def replace_perc(str_perc):
			str_perc02 = re.sub('(\d+\%)\s*([a-z]+)','\\2\\1 \\2,', str_perc)
			return re.sub('([a-z]+)\s+(\d+\%)', '\\1\\2 \\1,', str_perc)

		all_data['alltext'] = all_data['alltext'].apply(replace_perc)

	if rmPunctuation:
		puncList = '!"#$&%\'()*+-,./:;<=>?@[\\]^_`{|}~'
		def rm_punc(s):
			s = re.sub('([a-z]+)\-([a-z]+)', '\\1\\2', s)
			for x in puncList:
				s=s.replace(x,' ')
			return s

		all_data['alltext'] = all_data['alltext'].apply(rm_punc)

	if rmNums:
		def rm_nums(s):
	#		s = re.sub('\s+\d+\s+', '', s)
			s = re.sub('\d+', '', s)
			return s

		all_data['alltext'] = all_data['alltext'].apply(rm_nums)

	if rmStopWords:
		def rm_stop(s):
			stop = ['ASOS', 'macy', 'bloomingdale', "fashion nova", "YAS", "Ditsy", "Noisy", "May", "Ted","Baker", "River","Island", "Karen","Scott","PrettyLittleThing","Roxy","DESIGN","Chi", \
               "Alfani","Boohoo","Sofie","Schnoor","Ellesse", "Jeannie","TFNC","Sacred", "Hawk","Urban","Bliss","Puma","adidas", "Stella", \
               'cm', 'size', 'web id', 'approx', 'model', 'height', 'is', 'and', 'she', 'wearing', 'small', 'approximate', 'measurements', 'height', 
               'bust', 'waist', 'hips', 'made', 'usa', 'things', 'regular', 'right']
			
			lst = r'|'.join([x.lower() for x in stop])
			
			return re.sub(lst,'',s)


		# stop = ['ASOS', "YAS", "Ditsy", "Noisy", "May", "Ted","Baker", "River","Island", "Karen","Scott","PrettyLittleThing","Roxy","DESIGN","Chi",
  #              "Alfani","Boohoo","Sofie","Schnoor","Ellesse", "Jeannie","TFNC","Sacred", "Hawk","Urban","Bliss","Puma","adidas", "Stella"]
		# stop = [x.lower() for x in stop]

		all_data['alltext'] = all_data['alltext'].apply(rm_stop)


	return all_data