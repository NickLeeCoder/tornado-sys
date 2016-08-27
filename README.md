# tornado-sys

### 第一次接触tornado  并且尝试去写一个小demo
- 虽然有坑  但是还好  都一一解决了
- 遗憾的是部分功能由于时间不多  暂时没有实现 后续再慢慢加上吧 毕竟tornado还是值得学习的  异步非阻塞~

## OK  说回正题  
- 该demo基于tornado 以及 postgres,中间层使用了SQLAlchemy ORM  极大的加快了我的开发速度
- 其实做的过程中更多的是在熟悉tornado的基本使用以及开发流程的进一步熟悉
- 如果你想运行该demo   请在本地服务器创建一个Student名称的postgres数据库  
- 当然  你也可以在修改其中的settings文件中的PSQL_DBNAME 参数  并创建新命名的数据库
