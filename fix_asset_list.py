# -*- coding: utf-8 -*-

import os

def save_assets_list(lst:list):
	f=open('assets_list.txt','w')
	for i in lst:
		f.write(f'{i}\n')
	f.close()
	return lst

lst=[]
for root,dirs,files in os.walk('./assets/'):
	for file in files:
		lst.append(file)
save_assets_list(lst)