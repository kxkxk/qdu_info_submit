# qdu_info_submit

QDU校园集结号每日上报+github action，利用后者实现自动化

# Please keep slience!🤐

# How to use ?

1. 注册你的Github账号
2. 点击右上方的fork按钮，fork一下此项目，然后进入你刚刚fork的repo，并设置为private repository（除非你想让别人看到你的个人信息），[不会的可以看这里](https://github.com/waylau/github-help/blob/master/Making%20a%20public%20repository%20private%20%E5%BC%80%E6%94%BE%E5%BA%93%E8%BD%AC%E4%B8%BA%E7%A7%81%E6%9C%89.md)

3. 在刚刚的Setting里，点击Scrects，然后点击右边的`New Repository Screct`按钮，添加一个新的screct。Name中填`QDU_INFO`，然后把下面的内容填好，粘贴进`Value`里。

```
{
    "phone": "your phone number here which registered 校园集结号",
    "password": "your password",
    "name": "your name",
    "stuID": "your student ID like 2016207711",
    "academy": "your academy like '计算机科学与技术学院'",
    "className": "your class name like 16软件"
}
```

4. enjoy it! 之后的运行结果可以在Actions里看到，每天大概四小时运行一次。

# Extra: 邮件通知

进入`https://github.com/settings/notifications`，然后在Action里取消勾选`Send notifications for failed workflows only`