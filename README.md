# PushMessagesPlugin
xxxbot-pad 机器人插件 接收消息给数据转发到自定义的地址

config.toml
```toml
[basic]
# 是否启用插件
enable = false
# 推送地址
base_uri = ""

push_list =[
    "handle_text" #转发消息列表
]
```
发送数据为 bot 抓取的 message:Dict
