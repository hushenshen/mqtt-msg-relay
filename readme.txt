大家好，我是QQ频道：“迪粉桌面” 的热心群友，id：“明镜-宋plusdmi4.0-221216”， 感谢Miktone大神开发如此好用的软件，为了替换迪粉桌面手机版《MQTT服务器搭载教程》中的第四步：“运行消息中转脚本”，特制作的该镜像供车友使用， 使用方法：

1.执行教程第一步“群晖docker安装EMQX”，其中该容器名称为emqx：

docker run -d --name emqx -p 18083:18083 -p 1883:1883 -p 8083:8083 -p 8084:8084 --restart always emqx/emqx:latest

2.执行如下命令，注意替换相应IP，用户名、密码，该命令应与步骤一中的容器部署在同一台服务器

docker run -d --name mqtt-msg-relay --network container:emqx -e BROKER_URL="127.0.0.1" -e USERNAME="用户" -e PASSWORD="密码" --restart always deeplakehss/mqtt-msg-relay:1.0