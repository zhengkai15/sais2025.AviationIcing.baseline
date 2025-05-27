#!/bin/bash
echo "program start..."
# # on my workstation
# python run.py --base_name "../saisdata/input" --save_name "./output"


python3 run.py --base_name "/saisdata/input" --save_name "./output"

# # docker offline debug
# 将saisdata挂载在根目录, ??为镜像地址
# sudo docker run -it --platform linux/amd64 -v {saisdata_local}:/saisdata ?? bash 
# eg:sudo docker run -it --platform linux/amd64 -v ./saisdata:/saisdata ?? bash 

save_path=/saisresult
mkdir -p $save_path && zip -r -0 $save_path/output.zip ./output