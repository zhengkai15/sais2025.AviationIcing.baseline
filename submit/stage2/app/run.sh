#!/bin/bash
echo "program start..."
# # on my workstation
# python run.py --base_name "../saisdata/input" --save_name "./output"
set -x

python3 run.py --base_name "/saisdata/input" --save_name "./output"

# # docker offline debug
# 将saisdata挂载在根目录
# sudo docker run -it --platform linux/amd64 -v {saisdata_local}:/saisdata registry.cn-shanghai.aliyuncs.com/sais-race2024/sais2025aviation:0.1 bash 
# eg:sudo docker run -it --platform linux/amd64 -v ./saisdata:/saisdata registry.cn-shanghai.aliyuncs.com/sais-race2024/sais2025aviation:0.1 bash 

save_path=/saisresult
zip -r -0 output.zip ./output && mv output.zip $save_path