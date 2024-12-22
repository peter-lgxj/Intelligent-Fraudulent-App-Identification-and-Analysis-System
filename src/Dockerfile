	#基于的基础镜像
	FROM python:3.8
	USER root
	RUN sudo apt-get install libzbar-dev
	RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
	#代码添加当前目录所有内容到code文件夹
	ADD . /cnsoftbei_final
	# 设置code文件夹是工作目录
	WORKDIR /cnsoftbei_final
	# 安装支持
	
	
	# CMD ["sudo","apt-get","install","libzbar-dev"]
	CMD ["python", "apk_judge.py"]
