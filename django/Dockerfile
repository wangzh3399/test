# 二开推荐阅读[如何提高项目构建效率](https://developers.weixin.qq.com/miniprogram/dev/wxcloudrun/src/scene/build/speed.html)
# 选择构建用基础镜像（选择原则：在包含所有用到的依赖前提下尽可能体积小）。如需更换，请到[dockerhub官方仓库](https://hub.docker.com/_/python?tab=tags)自行选择后替换。
# 已知alpine镜像与pytorch有兼容性问题会导致构建失败，如需使用pytorch请务必按需更换基础镜像。
FROM alpine:3.13

# 容器默认时区为UTC，如需使用上海时间请启用以下时区设置命令
# RUN apk add tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo Asia/Shanghai > /etc/timezone
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories

# 使用 HTTPS 协议访问容器云调用证书安装
RUN apk add ca-certificates
RUN apk add gcc g++
RUN apk add python3-dev
RUN apk add libffi-dev
RUN apk add openssl-dev
RUN apk add git
RUN apk add --no-cache openssh-server
RUN apk add --no-cache openssh-client
RUN apk add nodejs
RUN apk add zip
# 选用国内镜像源以提高下载速度
#RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tencent.com/g' /etc/apk/repositories \
RUN apk add --update --no-cache python3 py3-pip \
&& rm -rf /var/cache/apk/*

# 拷贝当前项目到/app目录下(.dockerignore中文件除外)
COPY . /app
# 设定当前的工作目录
WORKDIR /app

# 安装依赖到指定的/install文件夹
# 选用国内镜像源以提高下载速度
RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple \
&& pip config set global.trusted-host mirrors.cloud.tencent.com \
&& pip install --upgrade pip \
# pip install scipy 等数学包失败，可使用 apk add py3-scipy 进行， 参考安装 https://pkgs.alpinelinux.org/packages?name=py3-scipy&branch=v3.13
&& pip install --user -r requirements.txt\
&& pip install wechatpy\
&& pip install cryptography\
&& pip uninstall -y xlrd\
&& pip install xlrd==1.2.0\
&& pip install cpython\
&& pip install /app/whl/numpy-1.24.2-cp38-cp38-linux_x86_64.whl\
&& pip install /app/whl/pandas-2.0.0-cp38-cp38-linux_x86_64.whl\
&& pip install /app/whl/akshare-1.9.43-py3-none-any.whl
&& pip install celery
&& pip install django-celery
#&& pip install akshare==1.9.43
#RUN dd if=gitid.des3 |openssl des3 -d -k otwind|tar zxf -
#RUN mkdir -p /root/.ssh/
#RUN mv id_rsa* /root/.ssh/
#akshare要安装很久
#RUN tar zxvf akshare-release-v1.9.36.tar.gz
#WORKDIR /app/akshare-release-v1.9.36
#RUN python3 setup.py install
#WORKDIR /app

#开发环境替换为生产环境
RUN sed -i 's/env = dev/env = prd/g' globalconfig.ini
# 暴露端口
# 此处端口必须与「服务设置」-「流水线」以及「手动上传代码包」部署时填写的端口一致，否则会部署失败。
EXPOSE 80

# 执行启动命令
# 写多行独立的CMD命令是错误写法！只有最后一行CMD命令会被执行，之前的都会被忽略，导致业务报错。
# 请参考[Docker官方文档之CMD命令](https://docs.docker.com/engine/reference/builder/#cmd)
CMD ["python3", "manage.py", "runserver", "0.0.0.0:80"]
