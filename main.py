import time
import paho.mqtt.client as mqtt
import os




# MQTT 服务器地址
broker_url = os.getenv('BROKER_URL')
broker_port = 1883
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

rTopic = {}


# 当客户端从服务器收到响应时调用
def on_connect(client, userdata, flags, rc,t):
    print(f"Connected {userdata} {flags} {rc} {t}")
    if rc == 0:
        print("Connected successfully")
        # 订阅主题
        client.subscribe("/msgProxy")
    else:
        print(f"Failed to connect, return code {rc}")


# 当从服务器接收到消息时调用
def on_message(client, userdata, msg):
    # print(f"Message received '{msg.payload.decode()}' on topic '{msg.topic}' with QoS {msg.qos}")
    print(f"Message  topic '{msg.topic}' received '{msg.payload.decode()}' with QoS {msg.qos}")
    if msg.topic == '/msgProxy':
        tmp = msg.payload.decode().split('#')
        print(f"subscribe tmp :{tmp}")
        deviceName = tmp[1]
        dTopic = tmp[2]
        if tmp[0] == '1':#手机端通知中转保存订阅，或者已经有订阅，则把缓存的信息退给手机端
            deviceMap = None
            try:
                deviceMap = rTopic[dTopic][deviceName]
            except:
                print("没有数据")
            if deviceMap is None:
                print(f"subscribe topic :{dTopic}  {deviceName} ")
                client.subscribe(dTopic)
                rTopic[dTopic] = {}
                rTopic[dTopic][deviceName] = []
            else:
                for m in deviceMap:
                    sendMsg(client, dTopic+"C", m)
                    time.sleep(0.2)
                rTopic[dTopic][deviceName] = []
        elif tmp[0] == '2':#手机端收到了原始订阅，通知中转
            m = tmp[3]
            deviceMap = None
            try:
                deviceMap = rTopic[dTopic][deviceName]
            except:
                print("没有数据")
            if deviceMap is None:
                client.subscribe(dTopic)
                rTopic[dTopic] = {}
                rTopic[dTopic][deviceName] = []
            else:
                print(f"subscribe remove topic :{dTopic}  {deviceName}")
                try:
                    deviceMap.remove(m)
                    print(f"subscribe remove topic :{dTopic}  {deviceMap}")
                except:
                    print("没有缓存")
    else:
        if msg.payload.decode() == '0':
            return
        dMaps = rTopic[msg.topic]
        if dMaps is not None:
            for deviceName in dMaps:
                try:
                    dMsgList = dMaps[deviceName]
                    dMsgList.append(msg.payload.decode())
                    print(f"get topic :{deviceName}  {dMsgList}")
                except:
                    print("缓存异常")


def sendMsg(client, sT, msg):
    client.publish(topic=sT, payload=msg, qos=1, retain=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 设置 MQTT 客户端实例
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"中转服务")
    client.on_connect = on_connect
    client.on_message = on_message
    # 设置用户名和密码
    client.username_pw_set(username, password)
    # 连接到 MQTT 服务器
    client.connect(broker_url, broker_port)
    # 循环以保持客户端运行，等待接收消息
    client.loop_forever()
