# Arcaea

基于HoshinoBotV2的Arcaea查询插件

项目地址：https://github.com/Yuri-YuzuChaN/Arcaea

有任何疑问或者不会使用插件，可联系QQ：806235364

**由于我的技术不足，无法实现其它arcbot的功能，如查询单曲成绩，快速查询B30成绩（本插件使用est查分器）等，非常抱歉**

## 使用方法

1. 将该项目放在HoshinoBot插件目录 `modules` 下，或者clone本项目 `git clone https://github.com/Yuri-YuzuChaN/Arcaea`
2. pip以下依赖：`websockets`，`brotli`
3. 在`config/__bot__.py`模块列表中添加`Arcaea`
4. 在数据库`.hoshino/arcaea.db`中`LOGIN`表添加查分账号密码以及绑定ID（随意数字），`IS_FULL` 字段请根据查分账号的好友数量填写，如果已经到达10个上限请输入`1`，否则为`0`

**该插件默认关闭，请手动开启**

**注意：查分账号需要自行注册，查询自己也需要查分账号添加自己为好友，每次添加完好友必须使用一次`arcup`指令**

## 更新说明

**2022-03-07**

1. 新增查询队列，防止多人同时使用`arcinfo`指令导致其余人查询失败
2. 优化正式绑定代码

**2022-01-14**

1. 已实装在线更新搭档图片，曲绘，曲目信息的功能
2. 自动计算曲目定数，该功能计算出的定数不一定准确
3. 修复新版本hoshino不导入new_logger的问题
4. 修复误删正式绑定时返回值

**2021-12-30**

1. 修改 `arcre` 指令以图片的形式发送，删除文字版本
2. 修改 `arcinfo` 指令的图片
3. 更新绑定用户时，以群@的形式提醒用户账号已完全绑定

**2021-12-15**

1. 修改请求est查分器遇到错误的返回值
2. 修改b30图片发送方式为`base64`编码，不在保存图片
3. 新增 `arcrd` 指令，随机获取一首曲目

**2021-08-27**

1. 修改数据库结构
2. 添加好友的过程中不在重复登陆好友已满的账号

**2021-08-13**

1. 修复`LOGIN`数据库未创建的问题

**2021-08-12**

1. 修改api请求

**2021-08-04**

1. 恢复查询B30指令`arcinfo`
2. 添加est查分器

# 指令

| 指令              | 功能     | 可选参数              | 说明                            |
| :---------------- | :------- | :-------------------- | :------------------------------ |
| arcinfo           | 查询B30  |  无                   | 使用est查分器查询自己的B30成绩                |
| arcre             | 查询最近  | 无                   | 使用本地查分器查询最近一次游玩成绩              |
|                   |          | [:]                  | 使用est查分器查询最近一次游玩成绩，全角半角都可以            |
|                   |          | [:] [@]              | 冒号结尾@好友使用est查询最近一次游玩成绩            |
|                   |          | [:] [arcid]          | 冒号结尾带好友码使用est查询最近一次游玩成绩            |
| arcup             | 账号绑定  | 无                   | 查询用账号添加完好友，使用该指令绑定查询账号，添加成功即可使用`arcre`指令|
| arcbind           | 绑定     | [arcid] [arcname]     | 绑定用户                        |
| arcun             | 解绑     | 无                    | 解除绑定                        |
| arcrd             | 随机曲目  | [定数] [难度]         | 随机一首该定数的曲目，例如：`arcrd 10.8`，`arcrd 10+`，`arcrd 9+ byd` |