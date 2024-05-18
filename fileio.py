# -*- coding: utf-8 -*-
import os

def read_file(filename:str)->bytes:
	with open(filename,'rb') as f:
		return f.read()

def save_to_file(filename:str,data:str)->None:
	with open(filename,'w') as f:
		f.write(data)

def save_to_fileb(filename:str,data:bytes)->None:
	with open(filename,'wb') as f:
		f.write(data)

def remove_file(filename:str)->None:
	os.remove(filename)