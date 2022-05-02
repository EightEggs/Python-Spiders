# Intro

## Asyncio

> https://docs.python.org/zh-cn/3.10/library/asyncio.html

asyncio 是用来编写并发代码的库，使用 async/await 语法。被用作多个提供高性能 Python 异步框架的基础，包括网络和网站服务，数据库连接库，分布式任务队列等等。往往是构建IO密集型和高层级结构化网络代码的最佳选择。

asyncio 提供一组高层级API用于:

- 并发地运行Python协程并对其执行过程实现完全控制;

- 执行网络IO和IPC;

- 控制子进程;

- 通过队列实现分布式任务;

- 同步并发代码。

此外，还有一些 低层级API以支持库和框架的开发者实现:

- 创建和管理事件循环，以提供异步API用于网络化, 运行子进程，处理OS信号等等;

- 使用 transports 实现高效率协议;

- 通过 async/await 语法桥接基于回调的库和代码。

## Aiohttp

> https://docs.aiohttp.org/

Asynchronous HTTP Client/Server for asyncio and Python.

- Supports both Client and HTTP Server.

- Supports both Server WebSockets and Client WebSockets out-of-the-box without the Callback Hell.

- Web-server has Middlewares, Signals and plugable routing.
