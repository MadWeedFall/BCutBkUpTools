#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import os.path as op
import yaml
import shutil
from datetime import datetime

def readConfig():
	cwd = op.dirname(sys.path[0])
	cfg_path = op.join(cwd,"config.yaml")
	if op.exists(cfg_path):
		with open(cfg_path) as f:
			cfg = yaml.safe_load(f)
			print(cfg)	
			return cfg
	else:
		print("未找到配置文件config.yaml");
	return none

def recoverOne(ori_path,bk_path):
	if op.exists(ori_path) and op.isdir(ori_path):
		os.rename(ori_path,op.join(op.split(ori_path)[0],op.split(ori_path)[1])+"_"+datetime.now().strftime("%Y%m%d%H%M%S")+"_bk")
		os.makedirs(ori_path)
	for p,d,f in os.walk(bk_path):
		for fn in f:
			org_f_path = op.join(p,fn)
			rel_path = op.relpath(org_f_path,bk_path)
			dst_path = op.join(ori_path,rel_path)
			dst_dir = op.dirname(dst_path)
			if not op.exists(dst_dir):
				os.makedirs(dst_dir)
			print(org_f_path)
			print(dst_path)
			shutil.copy2(org_f_path,dst_path);
	pass

def recover(ori_path,bk_root,retry=0):
	if not op.exists(bk_root) or not op.isdir(bk_root):
		print("找不到备份根目录")
		return
	if retry>3:
		print("输入序号错误次数过多，终止恢复")
		return
	bk_list = os.listdir(bk_root)
	bk_list = [d for d in bk_list if op.isdir(op.join(bk_root,d))]
	if len(bk_list)==0:
		print("您还没有进行过备份，无法进行还原")
		return
	print("序号"+"\t"+"备份")
	idx = 0
	for bk in bk_list:
		idx+=1
		print(""+str(idx)+"\t"+bk)
	raw_idx = input("输入要还原的备份序号并回车:")
	try:
		idx_choose = int(raw_idx)
	except:
		print("请从列表序号中选择输入数字")
		retry+=1
		recover(ori_path,bk_root,retry)
		return
	if idx_choose>0 and idx_choose-1<len(bk_list):
		choice = bk_list[idx_choose-1]
		bk_path = op.join(bk_root,choice)
		y_or_n = input("是否还原,y或Y确认，其他输入重新选择:")
		if y_or_n == "y" or y_or_n == "Y":
			recoverOne(ori_path,bk_path)
		else:
			print(f"重新选择，还可在尝试{3-retry}次，请重新输入")
			retry+=1
			recover(ori_path,bk_root,retry)
			return
	else:
		print(f"输入序号不正确，还可在尝试{3-retry}次，请重新输入")
		retry+=1
		recover(ori_path,bk_root,retry)
		return
		

def run():
	cfg = readConfig();
	ori_path = cfg.get("path","")
	bk_root = cfg.get("bkpath","")
	recover(ori_path,bk_root);
	input("按任意键退出")

if __name__ == '__main__':
	run()