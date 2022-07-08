# chaaat_bot

这个项目使用了pyautogui+opencv+paddleocr来驱动一个机器人监听某信的操作界面，平台为mac、conda做的环境

主要的项目结构为：
main.py为pyautogui,操作鼠标打开聊天界面，并且定位到主聊天窗口，并且每隔一段时间开始截图

之后传给parser.py(通过文件形式)，解析图片，定位到头像（根据面积特征），已经说话的框（根据顶点数范围以及边框拓宽后的长宽比）
最后还需要通过相对定位法，拿到说话的人的当前的id，这一部分依赖了opencv的能力，ocr则是依赖了paddleocr

最后回传给main.py的已经是解析好了的聊天记录

之后可以选择persistence.py存入数据库，但这没有什么意义，于是注释掉了，这里用到了sqlite3的一些小技巧

我选择了，传入给servant.py,仆人，模块拿到聊天记录，根据祈使句与应答配对的原则，来看是否有做应答，否则说一个你好，不断复读
那就傻了，这个模块写得就很难受了

最后是weather.py，就是简单的使用了request、bs4等模块解析了某个天气的网页，这属于无聊的给机器人增加的第一个算是实用的功能

整个项目全部依赖图片，而不对某信做任何侵入式的hook，当然局限就在于，机器学习的这套以及图像的这套东西相当消耗计算资源

没有GPU的情况下，性能很差，所以我的主循环设定为sleep了15秒，有点性能瓶颈

封存此代码，待机器性能问题解决后再说