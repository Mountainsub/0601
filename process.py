
import pandas as pd
import numpy as np
import time 
import sys
import os
import random
import math
import datetime

from price_logger import ClientHolder 
from price_logger import LastNPerfTime

def ind():
	indexes = pd.read_csv("nf_nikkei.csv")

	
	indexes_code = indexes["コード"]
	shares_no = indexes["株数"]
	for i,j in enumerate(indexes_code):
		try:
			j = int(float(j))
		except:
			continue
		else:
			indexes_code[i] = str(j) + ".T"
	indexes = indexes["純資産比率"].astype(float)
	return [indexes_code, indexes, shares_no]


def code_s(k):
	array = []
	weights = []
	count = 0
	
	
	# 以下csvファイルを都合いいようにエディット

	inde = ind()
	indexes_code, indexes, shares_no = inde[0], inde[1], inde[2]
	box = []
	# ddeを取得、格納、ウエイトをかけて計算
	
	for i,j in enumerate(indexes_code, start = k): 
		count += 1
		
		c = indexes_code[i]
		w = indexes[i]
		s = shares_no[i]
		weights.append(w)
		array.append(str(c))
		box.append(s)
		# 2142 ~ 2182 まで
		if k == 126 and count ==99:
			break

		if count >= 126:
			break
	return [array, weights,box]

def stop_execute():
	now = datetime.datetime.now()
	currently = np.datetime64(now)
	Y= now.year
	M = now.month
	D = now.day
	
	h = now.hour
	m = now.minute
	if h >= 15:
		print("今日は閉場です。")
	if (h== 11 and m > 30 ) or (h==12 and m <30):
		print("お昼休みです。")
		"""
		temp = pd.datetime(str(Y), str(M), str(D), 12, 30)		
		temp = np.datetime64(temp)
		sleep_num = float(temp.astype("float64")-currently.astype("float64")-60 )
		time.sleep(sleep_num)
		"""
	elif h< 9:
		print("success")
		temp = pd.datetime(Y, M, D, 9, 0)		
		temp = np.datetime64(temp)
		sleep_num = float(temp.astype("float64")-currently.astype("float64")-60 )
		t = float(sleep_num) / 10**6 
		time.sleep(t)
	else:
		pass


if __name__ == '__main__':
    
    args = sys.argv # コマンドライン引数として開始地点のインデックスを数字で入力する
    
    count = 0
    
	
	
	# 引数　0 →　0 ~ 125, 1 →　126 ~ 251, 2 →　252 ~ 377, 3 →　378 ~ 503, 4 →　504 ~ 629
	# 5 →　630 ~ 755, 6 →　756 ~ 881, 7 →　882 ~ 1007, 8 →　1008 ~ 1133, 9 →　1134 ~ 1259, 10 →　1260 ~ 1385
	# 11 →　1386 ~ 1511, 12 →　1512 ~ 1637, 13 →　1638 ~ 1763, 14 →　1764 ~ 1889, 15 →　1890 ~ 2015, 16 →　2016 ~ 2141, 17 →　2142 ~ 2182
    idx = int(args[1]) * 126
    if len(args) > 2:
        switch = args[2]
        if switch == "on":
            #止める
            stop_execute()
    #　idx : どのプロセスか示す指標,  code_s(idx)[0] ：　銘柄番号, code_s(idx)[1] : ウエイト       
    holder = ClientHolder(idx, code_s(idx)[0], code_s(idx)[1],code_s(idx)[2])
    holder.get_prices_forever()
    """
	for i in range(len(cabin[0])):
        print(codes[i] ,weights[i])
        dde = DDEClient("RSS", codes[i])
        calc +=  float(dde.request("現在値").decode("sjis"))* float(weights[i])
    print(calc)
    if args[2] is not None:
        switch = args[2]
    if switch == "on":
        stop_execute()
		#止める
    holder = ClientHolder(idx, code_s(idx)[0], code_s(idx)[1])
    timer = LastNPerfTime(2**20)
    if True:
        #timer.start()
        holder.get_prices_forever()
        #timer.end()
        #temp = timer.get_sum_time()    
        #print(temp)
        #timer.count_one()
    """           
        
    


        


        