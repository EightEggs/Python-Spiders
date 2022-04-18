# Intro

> https://redis.io/

Redis is an open source (BSD licensed), in-memory data structure store used as a database, cache, message broker, and streaming engine. Redis provides data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs, geospatial indexes, and streams. Redis has built-in replication, Lua scripting, LRU eviction, transactions, and different levels of on-disk persistence, and provides high availability via Redis Sentinel and automatic partitioning with Redis Cluster.

You can run atomic operations on these types, like appending to a string; incrementing the value in a hash; pushing an element to a list; computing set intersection, union and difference; or getting the member with highest ranking in a sorted set.

To achieve top performance, Redis works with an in-memory dataset. Depending on your use case, Redis can persist your data either by periodically dumping the dataset to disk or by appending each command to a disk-based log. You can also disable persistence if you just need a feature-rich, networked, in-memory cache.

Redis supports asynchronous replication, with fast non-blocking synchronization and auto-reconnection with partial resynchronization on net split.

Redis also includes:

- Transactions

- Pub/Sub

- Lua scripting

- Keys with a limited time-to-live

- LRU eviction of keys

- Automatic failover

- You can use Redis from most programming languages.

Redis is written in ANSI C and works on most POSIX systems like Linux, *BSD, and Mac OS X, without external dependencies. Linux and OS X are the two operating systems where Redis is developed and tested the most, and we recommend using Linux for deployment. Redis may work in Solaris-derived systems like SmartOS, but support is best effort. There is no official support for Windows builds.

-----

Redis 是一个开源（BSD 许可）的内存数据结构存储，用作数据库、缓存、消息代理和流引擎。 Redis 提供数据结构，例如字符串、散列、列表、集合、具有范围查询的排序集合、位图、超日志、地理空间索引和流。 Redis 具有内置复制、Lua 脚本、LRU 驱逐、事务和不同级别的磁盘持久性，并通过 Redis Sentinel 和 Redis Cluster 自动分区提供高可用性。

您可以对这些类型运行原子操作，例如附加到字符串；增加哈希值；将元素推送到列表中；计算集交、并、差；或获取排序集中排名最高的成员。

为了达到最佳性能，Redis 使用内存数据集。根据您的用例，Redis 可以通过定期将数据集转储到磁盘或将每个命令附加到基于磁盘的日志来持久化您的数据。如果您只需要一个功能丰富的网络内存缓存，您也可以禁用持久性。

Redis 支持异步复制，具有快速非阻塞同步和自动重新连接以及网络拆分上的部分重新同步。

Redis 还包括：

- 交易

- 发布/订阅

- Lua 脚本

- 生命周期有限的密钥

- LRU 驱逐密钥

- 自动故障转移

- 您可以从大多数编程语言中使用 Redis。

Redis 是用 ANSI C 编写的，可以在大多数 POSIX 系统上运行，比如 Linux、*BSD 和 Mac OS X，没有外部依赖。 Linux 和 OS X 是 Redis 开发和测试最多的两个操作系统，我们推荐使用 Linux 进行部署。 Redis 可以在 Solaris 派生的系统（如 SmartOS）中工作，但要尽最大努力提供支持。 Windows 版本没有官方支持。