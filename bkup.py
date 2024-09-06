#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import os.path as op
import yaml;
import shutil;
from datetime import datetime

def readConfig():
	cwd = op.dirname(sys.path[0])
	print(cwd)
	cfg_path = op.join(cwd,"config.yaml")
	if op.exists(cfg_path):
		with open(cfg_path) as f:
			cfg = yaml.safe_load(f)
			print(cfg)	
			return cfg
	else:
		print("未找到配置文件config.yaml");
	return none

def genBKpath(bk_root):
	if op.exists(bk_root):
		return op.join(bk_root,datetime.now().strftime("%Y%m%d%H%M%S"))
	return none

def bkup(org_path,bk_path):
	for p,d,f in os.walk(org_path):
		for fn in f:
			org_f_path = op.join(p,fn)
			rel_path = op.relpath(org_f_path,org_path)
			dst_path = op.join(bk_path,rel_path)
			dst_dir = op.dirname(dst_path)
			if not op.exists(dst_dir):
				os.makedirs(dst_dir)
			print(org_f_path,dst_path)
			shutil.copy2(org_f_path,dst_path);

def run():
	cfg = readConfig()
	bk_path = genBKpath(cfg.get("bkpath",""))
	bkup(cfg.get("path",""),bk_path)
	print("备份完成")


if __name__ == '__main__':
	run();
	input("按任意键退出");