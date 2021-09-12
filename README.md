# poker

轻量级的德州扑克对战服务器，主要面向德州扑克智能体的开发和评估。

## 德州扑克

德州扑克的简介与通用规则可以参考 [这里](https://zh.wikipedia.org/wiki/德州扑克)。

## 参数和限制

基于德州扑克的通用规则，本项目对游戏规则作出了如下限制：

- 采用无限注规则，玩家的加注额不设上限
- 大盲注固定为 100 筹码，小盲注固定为 50 筹码
- 每一手开始时，玩家的筹码数被重置为 20000。
- 每一手结束后，庄家位顺时针移动一位
- 每一个阶段中，所有玩家一共可以进行最多 4 次加注，此后加注将不被允许

具体规则和示例可以参考 [这里](http://holdem.ia.ac.cn:9002/upload/无限注德州扑克游戏规则--289b3b7017c61709a333742633590576.pdf)。

## 快速上手

### 环境准备

- python3

代码测试于 python 3.7 版本。

### 获取代码

```shell
git clone https://github.com/RL-MLDM/poker.git
cd poker
```

### 服务器模式

```shell
python3 serve.py
```

服务器将运行于 127.0.0.1 (本地) 的 2333 端口。

暂可以在 serve.py 中修改服务器的地址与端口。

### 客户端模式

本项目与 [OpenHoldem](http://holdem.ia.ac.cn/) 平台的通信协议兼容，通信协议的具体内容可以参考 [这里](http://holdem.ia.ac.cn:9002/upload/通信协议--5fe42ce9af89c4d84eb695a878691fe9.pdf)。

可以从 [这里](http://holdem.ia.ac.cn:9002/upload/demo--89ffb814995ea7e6de20dc02e95d384c.zip) 下载示例程序，运行前注意对服务器地址和端口的设罝。

需要注意的是，本项目暂不支持对房间号的设罝，即任意房间号都会被识别为同一房间。

## 贡献

如果你发现该项目在运行时出现了预期之外的行为，你可以提出Issue，Issue应包括以下内容：

- 可能运行出错的输入数据
- 程序的预期外行为
- 该输入数据下的预期行为

如果短时间内没有得到反馈，建议抄送 [xuehongyan17@mails.ucas.ac.cn](mailto:xuehongyan17@mails.ucas.ac.cn)

## Acknowledgement

本项目的规则实现参考了 [中国科学院自动化研究所智能系统与工程研究中心](http://www.crise.ia.ac.cn/) 的 [相关工作](http://holdem.ia.ac.cn/)，并使用了部分代码。
