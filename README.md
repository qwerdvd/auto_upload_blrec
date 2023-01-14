# blrec_auto_upload

## 丨介绍
#### 基于`fastapi`构建的`b站录播姬`自动上传脚本
#### 目前支持上传至`rclone`，并通过`telegrame`推送信息
#### 由于`Celery`整不明白，先暂时在项目中禁用`Celery`

## 丨如何安装与使用？
+ 1.安装`Python3.10`以上的版本
+ 2.使用你喜欢的方式安装依赖，建议使用`poetry`创建虚拟环境
```text
# 克隆项目
git clone https://github.com/qwerdvd/auto_upload_blrec.git
cd auto_upload_blrec

# 安装依赖
poetry install
# 进入虚拟环境
poetry shell
```
+ 3.安装`rclone`并配置好`rclone`，这里就不赘述了
+ 3.新建.env文件，填入信息，模板如下
```text
# .env

#run
RCLONE_DIR= #rclone挂载的目录
BLREC_WORK_DIR= #blrec的工作目录

#PROXY
USE_PROXY=False #是否使用代理
PROXY_URL= #代理地址

#Telegram
TG_CHAT_ID= # Telegram ID
TG_BOT_TOKEN= # Telegram Bot Token

#功能开关
UPLOAD_TO_RCLONE=True
UPLOAD_TO_BILIBILI=True

#是否删除本地文件？
DELETE_LOCAL=True
```
+ 4.设置录播姬文件格式如下
```text
{{ roomId }}-{{ name }}/{{ "now" | time_zone: "Asia/Shanghai" | format_date: "yyyy-MM-dd"}}/录制-{{ roomId }}-{{ "now" | time_zone: "Asia/Shanghai" | format_date: "yyyyMMdd-HHmmss-fff" }}-{{ title }}.flv
```
`format`后应为:
```text
23058-3号直播间/2022-12-18/录制-23058-20221218-214909-056-哔哩哔哩音悦台.flv
```
+ 5.在录播姬的`webhook V2`设置里填入下面的地址
```text
http://127.0.0.1:5000/webhook
```
+ 6.运行
```text
python main.py
```

## 丨TODO:
+ [x] 使用`fastapi`重构整体代码
+ [x] 异步优化
+ [ ] 支持更多推送平台
+ [ ] 抛弃`.env`文件，使用`config.toml`文件
+ [x] 优化`README.md`
+ [ ] 集成`biliup`实现自动投稿b站
+ [ ] 自动调用录播姬的修复功能
+ [ ] 提供转封装功能，压制弹幕功能等
+ [ ] 实现多账户`cookie`储存，实现多账户投稿
+ [ ] 支持`brec`的`webhook`
+ [ ] 提供`webUI`实现更多功能
+ [ ] 提供`docker`镜像
+ [ ] 提供`docker-compose`文件
+ [ ] 实现操作录播姬，在`webUI`中提供录播姬操作
+ [ ] 提供`api`接口，可以接入`nonebot`等