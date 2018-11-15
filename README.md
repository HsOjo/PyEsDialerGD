# PyEsDialerGD

广东天翼校园三方客户端（登陆器）（Python3版）

## 简介

抄袭自[EsDialerGD](https://github.com/claw6148/EsDialerGD)。

* 因客户端协议更新，本项目已无法工作。

* 不知道哪个**小人**把原作者项目拿去卖了，原作者不再更新，而本人又没能力逆向分析，所以这个抄袭的项目也就没法更新了。<del>（问候卖project的小人全家）</del>

## 使用方法

需要**requests**模块。

~~~shell
pip3 install requests
~~~

* client_id请自行抓包！！！

复制```data/config.sample.json```为```data/config.json```，填写账号密码，运行。

## 关于Project

请通过**wireshark**抓取官方客户端的特征（cdc_开头的字段），自行修改sample文件。

在本项目的研究过程中，本人依然遵守“一人一号”规则（即本人所在宿舍是每人一个宽带账号的），本项目的研究目的是为了本人的设备在 Linux 平台（官方未提供 Linux 平台的软件）下能够正常接入校园网。

本项目遵循 GNU GPLv3 开源协议，这意味着：
你可以免费使用、引用和修改本项目的代码以及衍生代码，但不允许将修改后和衍生的代码做为闭源的商业软件发布和销售。
