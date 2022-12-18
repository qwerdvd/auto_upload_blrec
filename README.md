# 自用版blrec_auto_upload

## 丨如何安装与使用？
+ 1.安装python3.10版本
+ 2.使用你喜欢的方式安装依赖，建议创建虚拟环境
+ 现阶段项目的requirements.txt不完善
+ 其中的[aioflask](https://github.com/miguelgrinberg/aioflask)需要自行合并[aioflask](https://github.com/miguelgrinberg/aioflask/pull/11)的pr才可使用
```text
pip install -r requirements.txt
```
+ 3.新建.env文件，填入信息，模板如下
```text
# .env

#run
WEBHOOK_ADDR= #监听地址
WEBHOOK_PORT= #监听端口
RCLONE_DIR= #rclone挂载的目录
BLREC_WORK_DIR= #blrec的工作目录

#PROXY
USE_PROXY=False #是否使用代理
PROXY_URL= #代理地址

#Telegram
TG_CHAT_ID= # Telegram ID
TG_BOT_TOKEN= # Telegram Bot Token
```
+ 4.设置录播姬文件格式如下
```text
{{ roomId }}-{{ name }}/{{ "now" | time_zone: "Asia/Shanghai" | format_date: "yyyy-MM-dd"}}/录制-{{ roomId }}-{{ "now" | time_zone: "Asia/Shanghai" | format_date: "yyyyMMdd-HHmmss-fff" }}-{{ title }}.flv
```
format后的目录应为
```text
23058-3号直播间/2022-12-18/录制-23058-20221218-214909-056-哔哩哔哩音悦台.flv
```
+ 5.在录播姬的设置里, 将地址填入"webhook v2"即可, 如"http://127.0.0.1:8081"

## 丨TODO:
+ [ ] 优化代码
+ [ ] 优化requirements.txt
+ [ ] 使用sqlite3存储数据
+ [ ] 集成biliup 实现自动投稿b站