# Splash API 调用

在上文中我们说明了 Splash Lua 脚本的用法，但这些脚本是在 Splash 页面里面测试运行的，我们如何才能利用 Splash 来渲染页面呢？怎样才能和 Python 程序结合使用并抓取 JavaScript 渲染的页面呢？

其实 Splash 给我们提供了一些 HTTP API 接口，我们只需要请求这些接口并传递相应的参数即可获取页面渲染后的结果，下面我们对这些接口进行介绍：

## render.html

此接口用于获取 JavaScript 渲染的页面的 HTML 代码，接口地址就是 Splash 的运行地址加此接口名称，例如：`http://localhost:8050/render.html`，我们可以用 curl 来测试一下：

```cli
curl http://localhost:8050/render.html?url=https://www.baidu.com
```

我们给此接口传递了一个 url 参数指定渲染的 URL，返回结果即页面渲染后的源代码。

如果用 Python 实现的话，代码如下：

```python
import requests
url = 'http://localhost:8050/render.html?url=https://www.baidu.com'
response = requests.get(url)
print(response.text)
```

这样就可以成功输出百度页面渲染后的源代码了。

另外，此接口还可以指定其他参数，比如通过 wait 指定等待秒数。如果要确保页面完全加载出来，可以增加等待时间，例如：

```python
import requests  
url = 'http://localhost:8050/render.html?url=https://www.taobao.com&amp;wait=5'  
response = requests.get(url)  
print(response.text)
```

如果增加了此等待时间后，得到响应的时间就会相应变长，如在这里我们会等待大约 5 秒多钟即可获取 JavaScript 渲染后的淘宝页面源代码。

> 另外此接口还支持代理设置、图片加载设置、Headers 设置、请求方法设置，具体的用法可以参见官方文档：
> 
> https://splash.readthedocs.io/en/stable/api.html#render-html。

## render.png

此接口可以获取网页截图，其参数比 render.html 多了几个，比如通过 width 和 height 来控制宽高，它返回的是 PNG 格式的图片二进制数据。示例如下：

```cli
curl http://localhost:8050/render.png?url=https://www.taobao.com&wait=5&width=1000&height=700
```

在这里我们还传入了 width 和 height 来放缩页面大小为 1000x700 像素。

如果用 Python 实现，我们可以将返回的二进制数据保存为 PNG 格式的图片，实现如下：

```python
import requests

url = 'http://localhost:8050/render.png?url=https://www.jd.com&wait=5&width=1000&height=700'
response = requests.get(url)
with open('taobao.png', 'wb') as f:
    f.write(response.content)
```

这样我们就成功获取了京东首页渲染完成后的页面截图。

> 详细的参数设置可以参考官网文档:
> 
> https://splash.readthedocs.io/en/stable/api.html#render-png。

## render.jpeg

此接口和 render.png 类似，不过它返回的是 JPEG 格式的图片二进制数据。

另外此接口相比 render.png 还多了一个参数 quality，可以用来设置图片质量。

## render.har

此接口用于获取页面加载的 HAR 数据，示例如下：

```cli
curl http://localhost:8050/render.har?url=https://www.jd.com&wait=5
```

返回结果非常多，是一个 Json 格式的数据，里面包含了页面加载过程中的 HAR 数据。

## render.json

此接口包含了前面接口的所有功能，返回结果是 Json 格式，示例如下：

```cli
curl http://localhost:8050/render.json?url=https://httpbin.org
```

结果如下：

```json
{"title": "httpbin(1): HTTP Client Testing Service", "url": "https://httpbin.org/", "requestedUrl": "https://httpbin.org/", "geometry": [0, 0, 1024, 768]}
```

可以看到，这里以 JSON 形式返回了相应的请求数据。

我们可以通过传入不同参数控制其返回结果。比如，传入 html=1，返回结果即会增加源代码数据；传入 png=1，返回结果即会增加页面 PNG 截图数据；传入 har=1，则会获得页面 HAR 数据。例如：

```cli
curl http://localhost:8050/render.json?url=https://httpbin.org&html=1&har=1
```

这样返回的 Json 结果便会包含网页源代码和 HAR 数据。

> 更多参数设置可以参考官方文档：
> 
> https://splash.readthedocs.io/en/stable/api.html#render-json。

## execute

此接口才是最为强大的接口。前面说了很多 Splash Lua 脚本的操作，用此接口便可实现与 Lua 脚本的对接。

前面的 render.html 和 render.png 等接口对于一般的 JavaScript 渲染页面是足够了，但是如果要实现一些交互操作的话，它们还是无能为力，这里就需要使用 execute 接口了。

我们先实现一个最简单的脚本，直接返回数据：

```lua
function main(splash)
    return 'hello'
end
```

然后将此脚本转化为 URL 编码后的字符串，拼接到 execute 接口后面，示例如下：

```cli
curl http://localhost:8050/execute?lua_source=function+main%28splash%29%0D%0A++return+%27hello%27%0D%0Aend
```

这里我们通过 lua_source 参数传递了转码后的 Lua 脚本，通过 execute 接口获取了最终脚本的执行结果。

这里我们更加关心的肯定是如何用 Python 来实现，上例用 Python 实现的话，代码如下：

```python
import requests
from urllib.parse import quote

lua = '''
function main(splash)
    return 'hello'
end
'''

url = 'http://localhost:8050/execute?lua_source=' + quote(lua)
response = requests.get(url)
print(response.text)
```

运行结果：

`hello`

这里我们用 Python 中的三引号将 Lua 脚本包括起来，然后用 urllib.parse 模块里的 quote() 方法将脚本进行 URL 转码，随后构造了 Splash 请求 URL，将其作为 lua_source 参数传递，这样运行结果就会显示 Lua 脚本执行后的结果。

我们再通过实例看一下：

```python
import requests
from urllib.parse import quote

lua = '''
function main(splash, args)
  local treat = require("treat")
  local response = splash:http_get("http://httpbin.org/get")
	return {html=treat.as_string(response.body),
    url=response.url,
    status=response.status
    }
end
'''

url = 'http://localhost:8050/execute?lua_source=' + quote(lua)
response = requests.get(url)
print(response.text)
```

运行结果：

```json
{"url": "http://httpbin.org/get", "status": 200, "html": "{\n  \"args\": {}, \n  \"headers\": {\n    \"Accept-Encoding\": \"gzip, deflate\", \n    \"Accept-Language\": \"en,*\", \n    \"Connection\": \"close\", \n    \"Host\": \"httpbin.org\", \n    \"User-Agent\": \"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/602.1 (KHTML, like Gecko) splash Version/9.0 Safari/602.1\"\n  }, \n  \"origin\": \"60.207.237.85\", \n  \"url\": \"http://httpbin.org/get\"\n}\n"}
```

可以看到，返回结果是 JSON 形式，我们成功获取了请求的 URL、状态码和网页源代码。
