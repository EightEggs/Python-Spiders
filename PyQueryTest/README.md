# Intro

> https://github.com/gawel/pyquery/
>
> https://jquery.com/

PyQuery 让你使用 jQuery 的风格来遍历 XML 文档，它使用了 lxml 来处理 XML 乃至 HTML 文档。

你可以直接从字符串、URL或者文件中加载文档：

```Python
>>> from pyquery import PyQuery as pq

>>> from lxml import etree

>>> import urllib

>>> d = pq("<html></html>")

>>> d = pq(etree.fromstring("<html></html>"))

>>> d = pq(url='http://google.com/')

>>> # d = pq(url='http://google.com/', opener=lambda url: urllib.urlopen(url).read())

>>> d = pq(filename=path_to_html_file)
```

然后进行遍历：

```Python
>>> d("#hello")

[<p#hello.hello>]

>>> p = d("#hello")

>>> print(p.html())

Hello world !

>>> p.html("you know <a href='http://python.org/'>Python</a> rocks")

[<p#hello.hello>]

>>> print(p.html())

you know <a href="http://python.org/">Python</a> rocks

>>> print(p.text())

you know Python rocks
```