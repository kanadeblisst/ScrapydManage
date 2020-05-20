## ScrapydManage

scrapyd的Windows管理客户端，软件只是将scrapyd的api集成到exe文件中，软件是由aardio写的，上面有源码，可以自行编译，也可以下载release已编译的exe文件。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200519234517952.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1F3ZXJ0eXVpb3AyMDE2,size_16,color_FFFFFF,t_70)
## 主机管理界面
右键菜单：
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200519234823627.png)
#### 添加主机
添加主机顾名思义就是添加scrapyd的api地址，例如127.0.0.1:6800。不理解scrapyd怎么使用的可以参考官方文档：https://scrapyd.readthedocs.io/en/stable/index.html 。其实很简单，pip install scrapyd，然后命令行输入scrapyd，或者先在当前目录创建scrapyd.conf，修改一些配置参数然后在输入scrapyd运行。

#### 刷新列表状态
只是向所有主机发起请求更新状态和节点名两栏，看第一张图应该很好理解
#### 同步所有项目到所有主机
顾名思义、默认版本号(version)为当前时间戳

#### 查看任务队列
listjobs这个接口，返回scrapyd服务端当前pending(待抓取)、running(正抓取)、finished(已抓取)的相关信息
#### 删除主机
顾名思义

## 项目管理界面
项目管理主要是读取当前exe文件同级目录下projects目录内的文件夹，有点绕口大概就这意思吧。
右键有三个功能：刷新项目列表、同步所有项目到、同步到(需要右键某个项目)
## 创建任务界面
右键有两个功能：创建任务、取消任务
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200520000257974.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1F3ZXJ0eXVpb3AyMDE2,size_16,color_FFFFFF,t_70)
注意这里需要一级一级填写，软件步骤如下：
选择主机->软件请求服务端返回该主机下的所有项目->选择项目->软件请求服务端返回该项目下的所有爬虫

运行时间可以是如图的字符串格式,表示在指定时间运行；也可以是数字(单位秒)，在指定秒数之后运行。时间间隔表示是否重复运行爬虫，重复时间间隔，只支持数字(单位秒)，比如一天运行一次就填86400。

因为需要等服务器返回数据，即使用多线程也要等返回值，所以选择主机或者项目后会有卡顿，卡顿时间看返回延迟，本地的话很快。
