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

def get_assets_list():
	try:
		f=open('assets_list.txt','r')
	except:
		return []
	lst=[]
	for i in f.readlines():
		i=i.replace('\r','').replace('\n','')
		if i!='':
			lst.append(i)
	f.close()
	return lst

def save_assets_list(lst:list):
	f=open('assets_list.txt','w')
	for i in lst:
		f.write(f'{i}\n')
	f.close()
	return lst

def download_sb3_to_file(projectid:int,cookie:str)->None:
	saved_assets=get_assets_list()
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
	title=''.join(['' if char in '"|/<:*>\\?\r\n' else char for char in apiresult_json['project']['title']])
	jsonurl=f'https://asset.gitblock.cn/Project/download?id={projectid}&v={version}'
	print(f'Downloading {projectid}_{title}...')
	print(f'Downloading project.json...')
	json_content=requests.get(jsonurl,headers={
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate, br, zstd',
		'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
		'Connection': 'keep-alive',
		'Origin': 'https://gitblock.cn',
		'Referer': 'https://gitblock.cn/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
	}).content
	try:
		plaintext=decrypt.decrypt(json_content)
	except:
		print('Decryption failed. Try using this as plaintext.')
		plaintext=json_content.decode('utf-8')
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
	from_assets_bank=0
	for id in tqdm.tqdm(range(0,len(assetlist))):
		i=assetlist[id]
		if i in saved_assets:
			from_assets_bank+=1
			continue
		saved_assets.append(i)
		asseturl=f'https://cdn.gitblock.cn/Project/GetAsset?name={i}'
		success=False
		while not success:
			try:
				fileio.save_to_fileb(f'./assets/{i}',requests.get(asseturl,verify=False,headers={
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
	print(f'Assets downloaded: {len(assetlist)-from_assets_bank}')
	print(f'Assets from assets bank: {from_assets_bank}')
	print('Zipping files...')
	with zipfile.ZipFile(f'{projectid}_{title}.sb3','w') as zipf:
		zipf.write('project.json')
		for i in assetlist:
			zipf.write(f'./assets/{i}')
	print('Removing temporary files...')
	fileio.remove_file('project.json')
	print('Updating asset bank...')
	save_assets_list(saved_assets)
	print('Done.')

def download_all(lst:list,cookie:str):
	for i in lst:
		download_sb3_to_file(i,cookie)

# download_all([924267,827622,235552],settings.cookie)
# download_all([1137846,979154,541032,421693,379522,335542,366892,366263,353137,329995,320448,22603,150139,148695,78969,60168,42167,41056],settings.cookie)
download_all([1220321,515257,607777,469999,1222112,1185310,1089801,1090173,1092544,1108720,1135666,1141685,999998,907300,1049022,930974,940558,906363,870014,470000,858175,839545,749317,754870,546887,535940,512945,480990,479934,426469,391220,399188,389822,390005,420115,401058,383555,389503,378000,374831,379262,377975,377826,373046,368417,364573,303683,248864,241096,345127,359545,358325,303573,231003,211712,2606,198123,159881,117745,123701,66662,161154,168349,164729,3087,96295,73056,46595,34234,44486,30594],settings.cookie)