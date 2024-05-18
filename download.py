# -*- coding: utf-8 -*-
import settings
import fileio

import requests
import urllib3
import decrypt
import zipfile
import json
import tqdm
import re

def download_sb3_to_file(projectid:int,cookie:str)->None:
	urllib3.disable_warnings()
	apiresult=requests.post(f'https://gitblock.cn/WebApi/Projects/{projectid}/Get',headers={
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Encoding': 'gzip, deflate, br, zstd',
		'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
		'Cache-Control': 'no-cache',
		'Connection': 'keep-alive',
		'Cookie': cookie,
		'Host': 'gitblock.cn',
		'Origin': 'https://gitblock.cn',
		'Pragma': 'no-cache',
		'Referer': f'https://gitblock.cn/Projects/{projectid}',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
		'X-Requested-With': 'XMLHttpRequest'
	})
	apiresult_json=json.loads(apiresult.text)
	version=apiresult_json['project']['version']
	title=apiresult_json['project']['title']
	jsonurl=f'https://asset.gitblock.cn/Project/download?id={projectid}&v={version}'
	print(f'Downloading project.json...')
	plaintext=decrypt.decrypt(requests.get(jsonurl,headers={
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate, br, zstd',
		'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
		'Connection': 'keep-alive',
		'Origin': 'https://gitblock.cn',
		'Referer': 'https://gitblock.cn/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
	}).content)
	fileio.save_to_file('project.json',plaintext)
	assetlist=[]
	assetlist+=re.findall(r'[a-f0-9]{32}\.svg',plaintext)
	assetlist+=re.findall(r'[a-f0-9]{32}\.jpg',plaintext)
	assetlist+=re.findall(r'[a-f0-9]{32}\.jpeg',plaintext)
	assetlist+=re.findall(r'[a-f0-9]{32}\.png',plaintext)
	assetlist+=re.findall(r'[a-f0-9]{32}\.mp3',plaintext)
	assetlist+=re.findall(r'[a-f0-9]{32}\.m4a',plaintext)
	assetlist+=re.findall(r'[a-f0-9]{32}\.wav',plaintext)
	assetlist=list(set(assetlist))
	# i'm not sure which of these formats will be used
	print('Downloading assets...')
	for id in tqdm.tqdm(range(0,len(assetlist))):
		i=assetlist[id]
		asseturl=f'https://cdn.gitblock.cn/Project/GetAsset?name={i}'
		success=False
		while not success:
			try:
				fileio.save_to_fileb(f'{i}',requests.get(asseturl,verify=False,headers={
					'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
					'Accept-Encoding': 'gzip, deflate, br, zstd',
					'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
					'Connection': 'keep-alive',
					'Cookie': '__jsluid_s=f949a294bb6fb5ab6f01a7baa16304ee',
					'Host': 'cdn.gitblock.cn',
					'Referer': 'https://gitblock.cn/',
					'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
				}).content)
				success=True
			except requests.exceptions.ProxyError:
				pass
			except requests.exceptions.SSLError:
				pass
	print('Zipping files...')
	with zipfile.ZipFile(f'{title}.sb3','w') as zipf:
		zipf.write('project.json')
		for i in assetlist:
			zipf.write(i)
	print('Removing temporary files...')
	for i in assetlist:
		fileio.remove_file(i)
	fileio.remove_file('project.json')
	print('Done.')
		
download_sb3_to_file(int(input("Project ID: ")),settings.cookie)