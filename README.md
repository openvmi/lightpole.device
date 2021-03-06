# 简介

智能路杆硬件设备相关文档。

## 通讯协议

```
02 03 00 02 00 02 65 f8  //光照 --> 返回9字节
02 03 00 00 00 02 c4 38 //温湿度 --> 返回9字节
01 03 00 09 00 01 54 08 // 风速 --> 返回7字节 
```

* 路灯工作模式

```js
//mode: manual, timer, smart
//
{
    "jsonrpc": "2.0",
    "method": "mqtt.lightMode",
    "params": {
        "mode": "timer",
        "config": {
            "hour": 12, //起始时间的小时字段
            "minute": 35, //起始时间的分钟字段
            "hourDuration": 7, //持续多少小时
            "minutesDuration": 30, //持续多少分钟
        } 
    }
}
//当mode是manual的时候， config字段如下
{
    "start": "on" //on代表打开， off代表关闭
}
//当mode为smart的时候，config的值为待定
```

## 测试

```js
//设置为手动模式
device/temparea/tempid/request
{
    "jsonrpc": "2.0",
    "method": "mqtt.lightMode",
    "params": {
        "mode": "manual",
        "config": {
            "start": "off"
        } 
    }
}

//设置为定时模式
device/temparea/tempid/request
{
    "jsonrpc": "2.0",
    "method": "mqtt.lightMode",
    "params": {
        "mode": "timer",
        "config": {
            "hour": 18,
            "minute": 0,
            "hourDuration": 1,
            "minutesDuration": 30,
        } 
    }
}
```

## 运行参数配置

```js
{
    "deviceId": "001",
    "deviceArea": "湖北工程职业技术学院",
	"host": "192.168.0.107",
	"port": 1883,
    "user": "xxxxx",
    "pwd": "xxxx",
    "consoleLog": "enable",
    "fileLog": "enable",
    "logLevel": "debug"
}
```