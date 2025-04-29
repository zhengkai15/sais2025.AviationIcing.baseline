#!/bin/bash
echo "program start..."
# # on my workstation
# python run.py --base_name "../tcdata/input" --save_name "./output"


python run.py --base_name "/tcdata/input" --save_name "./output"

# docker offline debug
# sudo docker run -it --platform linux/amd64 -v ./tcdata:/tcdata ?? bash 



zip -r -0 output.zip ./output