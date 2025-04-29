### Step
```
1、编写代码：app文件夹里面编写好你的代码 
2、本地测试：本地你可以生成一些测试输入放到tcdata里面（tcdata文件夹和app文件夹同级），运行run.sh里面的run on my workstation下面的python命令，可以正常生成输出文件
3、编写dockerfile：RUN apt-get update && apt-get upgrade -y && apt-get install -y curl zip vim， 增加安装zip等命令，启动入口为CMD ["bash", "run.sh"]
4、构建docker：build.sh, ps:run.sh里面保留第七行和14行 
5、本地启动容器测试：sudo docker run -it --platform linux/amd64 -v ./tcdata:/tcdata 镜像地址 bash, 容器就类似一个新机器，容器内app文件夹下生成output.zip文件即测试通过
6、push确认无误的镜像到远程镜像仓库地址
7、线上提交远程镜像仓库地址
