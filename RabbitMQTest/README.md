# Intro

> https://www.rabbitmq.com/documentation.html
>
> https://pika.readthedocs.io/
>
> https://rabbitpy.readthedocs.io/

-----

`RabbitMQ` 是使用 `Erlang` 语言开发的开源消息队列系统，基于 `AMQP` 协议实现。AMQP 的全称是 Advanced Message Queue，即高级消息队列协议，它的主要特征是面向消息、队列、路由（包括点对点和发布/订阅）、可靠性、安全。

RabbitMQ 最初起源于金融系统，用于在分布式系统中存储转发消息，在易用性、扩展性、高可用性等方面表现不俗。具体特点包括：

- 可靠性（Reliability）：RabbitMQ 使用一些机制来保证可靠性，如持久化、传输确认、发布确认。

- 灵活的路由（Flexible Routing）：在消息进入队列之前，通过 Exchange 来路由消息的。对于典型的路由功能，RabbitMQ 已经提供了一些内置的 Exchange 来实现。针对更复杂的路由功能，可以将多个 Exchange 绑定在一起，也通过插件机制实现自己的 - Exchange 。

- 消息集群（Clustering）：多个 RabbitMQ 服务器可以组成一个集群，形成一个逻辑 Broker 。

- 高可用（Highly Available Queues）：队列可以在集群中的机器上进行镜像，使得在部分节点出问题的情况下队列仍然可用。

- 多种协议支持（Multi-protocol）：RabbitMQ 支持多种消息队列协议，比如 STOMP、MQTT 等等。

- 多语言客户端（Many Clients）：RabbitMQ 几乎支持所有常用语言，比如 Java、.NET、Ruby 等等。

- 管理界面（Management UI）：RabbitMQ 提供了一个易用的用户界面，使得用户可以监控和管理消息 Broker 的许多方面。

- 跟踪机制（Tracing）：如果消息异常，RabbitMQ 提供了消息跟踪机制，使用者可以找出发生了什么。

- 插件机制（Plugin System）：RabbitMQ 提供了许多插件，来从多方面进行扩展，也可以编写自己的插件。

-----

`Pika` is a pure-Python implementation of the AMQP 0-9-1 protocol including RabbitMQ’s extensions.

- Python 2.7 and 3.4+ are supported.

- Since threads aren’t appropriate to every situation, it doesn’t require threads. Pika core takes care not to forbid them, either. The same goes for greenlets, callbacks, continuations, and generators. An instance of Pika’s built-in connection adapters **isn’t thread-safe**, however.

- People may be using direct sockets, plain old select(), or any of the wide variety of ways of getting network events to and from a Python application. Pika tries to stay compatible with all of these, and to make adapting it to a new environment as simple as possible.

`Pika` 是AMQP 0-9-1协议的纯Python实现，包括RabbitMQ的扩展。

- 支持Python 2.7和3.4+。

- 由于线程并不适用于所有情况，因此它不需要线程。Pika core也注意不禁止它们。Greenlets、callbacks、continuations和生成器也是如此。然而，Pika内置连接适配器的一个实例**并不是线程安全的**。

- 人们可能正在使用直接套接字、普通的旧 select() 或各种各样的方法来获取Python应用程序中的网络事件。Pika试图与所有这些保持兼容，并尽可能简单地使其适应新环境。

-----

`Rabbitpy` is a pure-Python, **thread-safe**, minimalistic and Pythonic BSD Licensed AMQP/RabbitMQ library that supports Python 2.7+ and Python 3.4+. Rabbitpy aims to provide a simple and easy to use API for interfacing with RabbitMQ, minimizing the programming overhead often found in other libraries.

`Rabbitpy` 是一个纯python、**线程安全**、简约且符合Python BSD许可的AMQP/RabbitMQ库，支持Python 2.7+和Python 3.4+。Rabbitpy旨在为与RabbitMQ的接口提供一个简单易用的API，最大限度地减少其他库中经常出现的编程开销。