# Intro

Splash 是一个 JavaScript 渲染服务，是一个带有 HTTP API 的轻量级浏览器，同时它对接了 Python 中的 Twisted 和 QT 库。利用它，我们同样可以实现动态渲染页面的抓取。

## 功能介绍

- 异步方式处理多个网页渲染过程
- 获取渲染后的页面的源代码或截图
- 通过关闭图片渲染或者使用 Adblock 规则来加快页面渲染速度
- 可执行特定的 JavaScript 脚本
- 可通过 Lua 脚本来控制页面渲染过程
- 获取渲染的详细过程并通过 HAR（HTTP Archive）格式呈现

## Splash Lua 脚本

Splash 可以通过 Lua 脚本执行一系列渲染操作，这样我们就可以用 Splash 来模拟类似 Chrome、PhantomJS 的操作了。

### 入口及返回值

首先，来看一个基本实例：

```lua
function main(splash, args)
  splash:go("http://www.baidu.com")
  splash:wait(0.5)
  local title = splash:evaljs("document.title")
  return {title=title}
end
```

我们将代码粘贴到刚才我们所打开的：http://localhost:8050/ 的代码编辑区域，然后点击 `Render me!` 按钮来测试一下。

我们看到它返回了网页的标题，这里我们通过 evaljs 方法传入 JavaScript 脚本，而 document.title 的执行结果就是返回网页标题，执行完毕后将其赋值给一个 title 变量，随后将其返回。

注意，我们在这里定义的方法名称叫作 main 。这个名称必须是固定的，Splash 会默认调用这个方法。

该方法的返回值既可以是字典形式，也可以是字符串形式，最后都会转化为 Splash HTTP Response，例如：

```lua
function main(splash)
  return {hello="world!"}
end
```
这样即返回了一个字典形式的内容。

```lua
function main(splash)
  return 'hello'
end
```
这样即返回了一个字符串形式的内容。

### 异步处理

Splash 支持异步处理，但是这里并没有显式指明回调方法，其回调的跳转是在 Splash 内部完成的。示例如下：

```lua
function main(splash, args)
  local example_urls = {"www.baidu.com", "www.taobao.com", "www.zhihu.com"}
  local urls = args.urls or example_urls
  local results = {}
  for index, url in ipairs(urls) do
    local ok, reason = splash:go("http://" .. url)
    if ok then
      splash:wait(2)
      results[url] = splash:png()
    end
  end
  return results
end
```

运行后的返回结果是 3 个站点的截图。

在脚本内调用的 wait 方法类似于 Python 中的 sleep 方法，其参数为等待的秒数。当 Splash 执行到此方法时，它会转而去处理其他任务，然后在指定的时间过后再回来继续处理。

> 这里值得注意的是，Lua 脚本中的字符串拼接和 Python 不同，它使用的是..操作符，而不是+。如果有必要，可以简单了解一下 Lua 脚本的语法，详见
> 
> http://www.runoob.com/lua/lua-basic-syntax.html。

另外，这里做了加载时的异常检测。go 方法会返回加载页面的结果状态，如果页面出现 4xx 或 5xx 状态码，ok 变量就为空，就不会返回加载后的图片。

## Splash 对象属性

我们注意到，前面例子中 main 方法的第一个参数是 splash，这个对象非常重要，它类似于 Selenium 中的 WebDriver 对象，我们可以调用它的一些属性和方法来控制加载过程。接下来，先看下它的属性。

### args

该属性可以获取加载时配置的参数，比如 URL，如果为 GET 请求，它还可以获取 GET 请求参数；如果为 POST 请求，它可以获取表单提交的数据。Splash 也支持使用第二个参数直接作为 args，例如：

```lua
function main(splash, args)
  local url = args.url
end
```
这里第二个参数 args 就相当于 splash.args 属性，以上代码等价于：

```lua
function main(splash)
  local url = splash.args.url
end
```

### js_enabled

这个属性是 Splash 的 JavaScript 执行开关，可以将其配置为 true 或 false 来控制是否执行 JavaScript 代码，默认为 true。例如，这里禁止执行 JavaScript 代码：

```lua
function main(splash, args)
  splash:go("https://www.baidu.com")
  splash.js_enabled = false
  local title = splash:evaljs("document.title")
  return {title=title}
end
```

接着我们重新调用了 evaljs 方法执行 JavaScript 代码，此时运行结果就会抛出异常：

```json
{
    "error": 400,
    "type": "ScriptError",
    "info": {
        "type": "JS_ERROR",
        "js_error_message": null,
        "source": "[string \"function main(splash, args)\r...\"]",
        "message": "[string \"function main(splash, args)\r...\"]:4: unknown JS error: None",
        "line_number": 4,
        "error": "unknown JS error: None",
        "splash_method": "evaljs"
    },
    "description": "Error happened while executing Lua script"
}
```

不过一般来说我们不用设置此属性开关，默认开启即可。

### resource_timeou

此属性可以设置加载的超时时间，单位是秒。如果设置为 0 或 nil（类似 Python 中的 None），代表不检测超时。示例如下：

```lua
function main(splash)
  splash.resource_timeout = 0.1
  assert(splash:go('https://www.taobao.com'))
  return splash:png()
end
```

例如，这里将超时时间设置为 0.1 秒。如果在 0.1 秒之内没有得到响应，就会抛出异常，错误如下：

```json
{
    "error": 400,
    "type": "ScriptError",
    "info": {
        "error": "network5",
        "type": "LUA_ERROR",
        "line_number": 3,
        "source": "[string \"function main(splash)\r...\"]",
        "message": "Lua error: [string \"function main(splash)\r...\"]:3: network5"
    },
    "description": "Error happened while executing Lua script"
}
```

此属性适合在网页加载速度较慢的情况下设置。如果超过了某个时间无响应，则直接抛出异常并忽略即可。

#### images_enabled

此属性可以设置图片是否加载，默认情况下是加载的。禁用该属性后，可以节省网络流量并提高网页加载速度。但是需要注意的是，禁用图片加载可能会影响 JavaScript 渲染。因为禁用图片之后，它的外层 DOM 节点的高度会受影响，进而影响 DOM 节点的位置。因此，如果 JavaScript 对图片节点有操作的话，其执行就会受到影响。

另外值得注意的是，Splash 使用了缓存。如果一开始加载出来了网页图片，然后禁用了图片加载，再重新加载页面，之前加载好的图片可能还会显示出来，这时直接重启 Splash 即可。

禁用图片加载的示例如下：

```lua
function main(splash, args)
  splash.images_enabled = false
  assert(splash:go('https://www.jd.com'))
  return {png=splash:png()}
end
```

这样返回的页面截图就不会带有任何图片，加载速度也会快很多。

### plugins_enabled

此属性可以控制浏览器插件（如 Flash 插件）是否开启。默认情况下，此属性是 false，表示不开启。可以使用如下代码控制其开启和关闭：`splash.plugins_enabled = true/false`

### scroll_position

通过设置此属性，我们可以控制页面上下或左右滚动。这是一个比较常用的属性，示例如下：

```lua
function main(splash, args)
  assert(splash:go('https://www.taobao.com'))
  splash.scroll_position = {y=400}
  return {png=splash:png()}
end
```

这样我们就可以控制页面向下滚动 400 像素值。

如果要让页面左右滚动，可以传入 x 参数：`splash.scroll_position = {x=100, y=200}`

## Splash 对象方法

除了前面介绍的属性外，Splash 对象还有如下方法。

### go

该方法用来请求某个链接，而且它可以模拟 GET 和 POST 请求，同时支持传入请求头、表单等数据，其用法如下：

`ok, reason = splash:go{url, baseurl=nil, headers=nil, http_method="GET", body=nil, formdata=nil}`

参数说明如下：

`url`，即请求的 URL。

`baseurl`，可选参数，默认为空，资源加载相对路径。

`headers`，可选参数，默认为空，请求的 Headers。

`http_method`，可选参数，默认为 GET，同时支持 POST。

`body`，可选参数，默认为空，POST 的时候的表单数据，使用的 Content-type 为 application/json。

`formdata`，可选参数，默认为空，POST 的时候表单数据，使用的 Content-type 为 application/x-www-form-urlencoded。

该方法的返回结果是结果 ok 和原因 reason 的组合，如果 ok 为空，代表网页加载出现了错误，此时 reason 变量中包含了错误的原因，否则证明页面加载成功。示例如下：

```lua
function main(splash, args)
  local ok, reason = splash:go{"http://httpbin.org/post", http_method="POST", body="name=Germey"}
  if ok then
    return splash:html()
  end
end
```

这里我们模拟了一个 POST 请求，并传入了 POST 的表单数据，如果成功，则返回页面的源代码。

运行结果如下：

```html
<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">{"args": {}, 
  "data": "","files": {},"form": {"name":"Germey"},"headers": {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Encoding":"gzip, deflate","Accept-Language":"en,*","Connection":"close","Content-Length":"11","Content-Type":"application/x-www-form-urlencoded","Host":"httpbin.org","Origin":"null","User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/602.1 (KHTML, like Gecko) splash Version/9.0 Safari/602.1"},"json": null,"origin":"60.207.237.85","url":"http://httpbin.org/post"
}
</pre></body></html>
```

可以看到，我们成功实现了 POST 请求并发送了表单数据。

### wait

此方法可以控制页面等待时间，使用方法如下：

`ok, reason = splash:wait{time, cancel_on_redirect=false, cancel_on_error=true}`

参数说明如下：

`time`，等待的秒数。

`cancel_on_redirect`，可选参数，默认 False，如果发生了重定向就停止等待，并返回重定向结果。

`cancel_on_error`，可选参数，默认 False，如果发生了加载错误就停止等待。

返回结果同样是结果 ok 和原因 reason 的组合。

用一个实例感受一下：

```lua
function main(splash)
    splash:go("https://www.taobao.com")
    splash:wait(2)
    return {html=splash:html()}
end
```

如上代码可以实现访问淘宝并等待 2 秒，随后返回页面源代码的功能。

### jsfunc

此方法可以直接调用 JavaScript 定义的方法，但是所调用的方法需要用双中括号包围，这相当于实现了 JavaScript 方法到 Lua 脚本的转换。示例如下：


```lua
function main(splash, args)
  local get_div_count = splash:jsfunc([[function () {
    var body = document.body;
    var divs = body.getElementsByTagName('div');
    return divs.length;
  }
  ]])
  splash:go("https://www.baidu.com")
  return ("There are % s DIVs"):format(get_div_count())
end
```

运行结果：

`There are 21 DIVs`

首先，我们声明了一个 JavaScript 定义的方法，然后在页面加载成功后调用了此方法计算出了页面中 div 节点的个数。

> 关于 JavaScript 到 Lua 脚本的更多转换细节，可以参考官方文档:
> 
> https://splash.readthedocs.io/en/stable/scripting-ref.html#splash-jsfunc。

### evaljs

此方法可以执行 JavaScript 代码并返回最后一条 JavaScript 语句的返回结果，使用方法如下：

`result = splash:evaljs(js)`

比如，可以用下面的代码来获取页面标题：

`local title = splash:evaljs("document.title")`

### runjs

此方法可以执行 JavaScript 代码，它与 evaljs 方法的功能类似，但是更偏向于执行某些动作或声明某些方法。例如：

```lua
function main(splash, args)
  splash:go("https://www.baidu.com")
  splash:runjs("foo = function() {return 'bar'}")
  local result = splash:evaljs("foo()")
  return result
end
```

这里我们用 runjs 方法先声明了一个 JavaScript 定义的方法，然后通过 evaljs 方法来调用得到的结果。

运行结果如下：

`bar`

### autoload

此方法可以设置每个页面访问时自动加载的对象，使用方法如下：

`ok, reason = splash:autoload{source_or_url, source=nil, url=nil}`

参数说明如下：

`source_or_url`，JavaScript 代码或者 JavaScript 库链接。

`source`，JavaScript 代码。

`url`，JavaScript 库链接

但是此方法只负责加载 JavaScript 代码或库，不执行任何操作。如果要执行操作，可以调用 evaljs 或 runjs 方法。示例如下：

```lua
function main(splash, args)
  splash:autoload([[function get_document_title(){return document.title;}
  ]])
  splash:go("https://www.baidu.com")
  return splash:evaljs("get_document_title()")
end
```

这里我们调用 autoload 方法声明了一个 JavaScript 方法，然后通过 evaljs 方法来执行此 JavaScript 方法。

运行结果如下：

`百度一下，你就知道`

另外，我们也可以使用 autoload 方法加载某些方法库，如 jQuery，示例如下：

```lua
function main(splash, args)
  assert(splash:autoload("https://code.jquery.com/jquery-2.1.3.min.js"))
  assert(splash:go("https://www.taobao.com"))
  local version = splash:evaljs("$.fn.jquery")
  return 'JQuery version: ' .. version
end
```

运行结果如下：

`JQuery version: 2.1.3`

### call_later

此方法可以通过设置定时任务和延迟时间来实现任务延时执行，并且可以在执行前通过 cancel 方法重新执行定时任务。示例如下：

```lua
function main(splash, args)
  local snapshots = {}
  local timer = splash:call_later(function()
    snapshots["a"] = splash:png()
    splash:wait(1.0)
    snapshots["b"] = splash:png()
  end, 0.2)
  splash:go("https://www.taobao.com")
  splash:wait(3.0)
  return snapshots
end
```

这里我们设置了一个定时任务，0.2 秒的时候获取网页截图，然后等待 1 秒，1.2 秒时再次获取网页截图，访问的页面是淘宝，最后将截图结果返回。

### http_get

此方法可以模拟发送 HTTP 的 GET 请求，使用方法如下：

`response = splash:http_get{url, headers=nil, follow_redirects=true}`

参数说明如下：

`url`，请求 URL。

`headers`，可选参数，默认为空，请求的 Headers。

`follow_redirects`，可选参数，默认为 True，是否启动自动重定向。

示例如下：

```lua
function main(splash, args)
  local treat = require("treat")
  local response = splash:http_get("http://httpbin.org/get")
	return {html=treat.as_string(response.body),
    url=response.url,
    status=response.status
    }
end
```

运行结果如下：

```json
Splash Response: Object
html: String (length 355)
{"args": {}, 
  "headers": {
    "Accept-Encoding": "gzip, deflate", 
    "Accept-Language": "en,*", 
    "Connection": "close", 
    "Host": "httpbin.org", 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/602.1 (KHTML, like Gecko) splash Version/9.0 Safari/602.1"
  }, 
  "origin": "60.207.237.85", 
  "url": "http://httpbin.org/get"
}
status: 200
url: "http://httpbin.org/get"
```

### http_post

和 http_get 方法类似，此方法是模拟发送一个 POST 请求，不过多了一个参数 body，使用方法如下：

`response = splash:http_post{url, headers=nil, follow_redirects=true, body=nil}`

参数说明如下：

`url`，请求 URL。

`headers`，可选参数，默认为空，请求的 Headers。

`follow_redirects`，可选参数，默认为 True，是否启动自动重定向。

`body`，可选参数，默认为空，即表单数据。

示例如下：

```lua
function main(splash, args)
  local treat = require("treat")
  local json = require("json")
  local response = splash:http_post{"http://httpbin.org/post",     
  	body=json.encode({name="Germey"}),
  	headers={["content-type"]="application/json"}
	}
	return {html=treat.as_string(response.body),
    url=response.url,
    status=response.status
    }
end
```

运行结果：

```json
Splash Response: Object
html: String (length 533)
{"args": {}, 
  "data": "{\"name\": \"Germey\"}", 
  "files": {}, 
  "form": {}, 
  "headers": {
    "Accept-Encoding": "gzip, deflate", 
    "Accept-Language": "en,*", 
    "Connection": "close", 
    "Content-Length": "18", 
    "Content-Type": "application/json", 
    "Host": "httpbin.org", 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/602.1 (KHTML, like Gecko) splash Version/9.0 Safari/602.1"
  }, 
  "json": {"name": "Germey"}, 
  "origin": "60.207.237.85", 
  "url": "http://httpbin.org/post"
}
status: 200
url: "http://httpbin.org/post"
```

可以看到在这里我们成功模拟提交了 POST 请求并发送了表单数据。

### set_content

此方法可以用来设置页面的内容，示例如下：

```lua
function main(splash)
    assert(splash:set_content("<html><body><h1>hello</h1></body></html>"))
    return splash:png()
end
```

### html

此方法可以用来获取网页的源代码，它是非常简单又常用的方法，示例如下：

```lua
function main(splash, args)
  splash:go("https://httpbin.org/get")
  return splash:html()
end
```

运行结果：

```html
<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">{"args": {}, 
  "headers": {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "Accept-Encoding": "gzip, deflate", 
    "Accept-Language": "en,*", 
    "Connection": "close", 
    "Host": "httpbin.org", 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/602.1 (KHTML, like Gecko) splash Version/9.0 Safari/602.1"
  }, 
  "origin": "60.207.237.85", 
  "url": "https://httpbin.org/get"
}
</pre></body></html>
```

### png

此方法可以用来获取 PNG 格式的网页截图，示例如下：

```lua
function main(splash, args)
  splash:go("https://www.taobao.com")
  return splash:png()
end
```

### jpeg

此方法可以用来获取 JPEG 格式的网页截图，示例如下：

```lua
function main(splash, args)
  splash:go("https://www.taobao.com")
  return splash:jpeg()
end
```

har
此方法可以用来获取页面加载过程描述，示例如下：

```lua
function main(splash, args)
  splash:go("https://www.baidu.com")
  return splash:har()
end
```

在这里显示了页面加载过程中的每个请求记录详情。

### url

此方法可以获取当前正在访问的 URL，示例如下：

```lua
function main(splash, args)
  splash:go("https://www.baidu.com")
  return splash:url()
end
```

运行结果如下：

`https://www.baidu.com/`

### get_cookies

此方法可以获取当前页面的 Cookies，示例如下：

```lua
function main(splash, args)
  splash:go("https://www.baidu.com")
  return splash:get_cookies()
end
```

运行结果如下：

```json
Splash Response: Array[2]
0: Object
domain: ".baidu.com"
expires: "2085-08-21T20:13:23Z"
httpOnly: false
name: "BAIDUID"
path: "/"
secure: false
value: "C1263A470B02DEF45593B062451C9722:FG=1"
1: Object
domain: ".baidu.com"
expires: "2085-08-21T20:13:23Z"
httpOnly: false
name: "BIDUPSID"
path: "/"
secure: false
value: "C1263A470B02DEF45593B062451C9722"
```

### add_cookie

此方法可以为当前页面添加 Cookies，用法如下：

`cookies = splash:add_cookie{name, value, path=nil, domain=nil, expires=nil, httpOnly=nil, secure=nil}`

方法的各个参数代表了 Cookie 的各个属性。

示例如下：

```lua
function main(splash)
    splash:add_cookie{"sessionid", "237465ghgfsd", "/", domain="http://example.com"}
    splash:go("http://example.com/")
    return splash:html()
end
```

### clear_cookies

此方法可以清除所有的 Cookies，示例如下：

```lua
function main(splash)
    splash:go("https://www.baidu.com/")
    splash:clear_cookies()
    return splash:get_cookies()
end
```

在这里我们清除了所有的 Cookies，然后再调用 get_cookies() 并将结果返回。

运行结果：

`Splash Response: Array[0]`

可以看到 Cookies 被全部清空，没有任何结果。

### get_viewport_size

此方法可以获取当前浏览器页面的大小，即宽高，示例如下：

```lua
function main(splash)
    splash:go("https://www.baidu.com/")
    return splash:get_viewport_size()
end
```

运行结果：

```json
Splash Response: Array[2]
0: 1024
1: 768
```

### set_viewport_size

此方法可以设置当前浏览器页面的大小，即宽高，用法如下：

`splash:set_viewport_size(width, height)`

例如这里我们访问一个宽度自适应的页面，示例如下：

```lua
function main(splash)
    splash:set_viewport_size(400, 700)
    assert(splash:go("http://cuiqingcai.com"))
    return splash:png()
end
```

### set_viewport_full

此方法可以设置浏览器全屏显示，示例如下：

```lua
function main(splash)
    splash:set_viewport_full()
    assert(splash:go("http://cuiqingcai.com"))
    return splash:png()
end
```

### set_user_agent

此方法可以设置浏览器的 User-Agent，示例如下：

```lua
function main(splash)
  splash:set_user_agent('Splash')
  splash:go("http://httpbin.org/get")
  return splash:html()
end
```

在这里我们将浏览器的 User-Agent 设置为 Splash，运行结果如下：

```html
<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">{"args": {}, 
  "headers": {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "Accept-Encoding": "gzip, deflate", 
    "Accept-Language": "en,*", 
    "Connection": "close", 
    "Host": "httpbin.org", 
    "User-Agent": "Splash"
  }, 
  "origin": "60.207.237.85", 
  "url": "http://httpbin.org/get"
}
</pre></body></html>
```

可以看到此处 User-Agent 被成功设置。

### set_custom_headers

此方法可以设置请求的 Headers，示例如下：

```lua
function main(splash)
  splash:set_custom_headers({["User-Agent"] = "Splash",
     ["Site"] = "Splash",
  })
  splash:go("http://httpbin.org/get")
  return splash:html()
end
```

在这里我们设置了 Headers 中的 User-Agent 和 Site 属性，运行结果：

```html
<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">{"args": {}, 
  "headers": {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
    "Accept-Encoding": "gzip, deflate", 
    "Accept-Language": "en,*", 
    "Connection": "close", 
    "Host": "httpbin.org", 
    "Site": "Splash", 
    "User-Agent": "Splash"
  }, 
  "origin": "60.207.237.85", 
  "url": "http://httpbin.org/get"
}
</pre></body></html>
```

可以看到结果的 Headers 中两个字段被成功设置。

### select

该方法可以选中符合条件的第一个节点，如果有多个节点符合条件，则只会返回一个，其参数是 CSS 选择器。示例如下：

```lua
function main(splash)
  splash:go("https://www.baidu.com/")
  input = splash:select("#kw")
  input:send_text('Splash')
  splash:wait(3)
  return splash:png()
end
```

这里我们首先访问了百度，然后选中了搜索框，随后调用了 send_text() 方法填写了文本，然后返回网页截图。

可以看到我们成功填写了输入框。

### select_all

此方法可以选中所有的符合条件的节点，其参数是 CSS 选择器。示例如下：

```lua
function main(splash)
  local treat = require('treat')
  assert(splash:go("http://quotes.toscrape.com/"))
  assert(splash:wait(0.5))
  local texts = splash:select_all('.quote .text')
  local results = {}
  for index, text in ipairs(texts) do
    results[index] = text.node.innerHTML
  end
  return treat.as_array(results)
end
```

这里我们通过 CSS 选择器选中了节点的正文内容，随后遍历了所有节点，将其中的文本获取下来。

运行结果如下：

```json
Splash Response: Array[10]
0: "“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”"
1: "“It is our choices, Harry, that show what we truly are, far more than our abilities.”"
2: "“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”"
3: "“The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.”"
4: "“Imperfection is beauty, madness is genius and it's better to be absolutely ridiculous than absolutely boring.”"
5: "“Try not to become a man of success. Rather become a man of value.”"
6: "“It is better to be hated for what you are than to be loved for what you are not.”"
7: "“I have not failed. I've just found 10,000 ways that won't work.”"
8: "“A woman is like a tea bag; you never know how strong it is until it's in hot water.”"
9: "“A day without sunshine is like, you know, night.”"
```

可以发现我们成功将 10 个节点的正文内容获取了下来。

### mouse_click

此方法可以模拟鼠标点击操作，传入的参数为坐标值 x、y，也可以直接选中某个节点直接调用此方法，示例如下：

```lua
function main(splash)
  splash:go("https://www.baidu.com/")
  input = splash:select("#kw")
  input:send_text('Splash')
  submit = splash:select('#su')
  submit:mouse_click()
  splash:wait(3)
  return splash:png()
end
```

在这里我们首先选中了页面的输入框，输入了文本，然后选中了提交按钮，调用了 mouse_click() 方法提交查询，然后页面等待三秒，返回截图。

可以看到在这里我们成功获取了查询后的页面内容，模拟了百度搜索操作。

-----

以上我们介绍了 Splash 的常用 API 操作，还有一些 API 在这不再一一介绍，更加详细和权威的说明可以参见官方文档。

> https://splash.readthedocs.io/en/stable/scripting-ref.html
> 
> https://splash.readthedocs.io/en/stable/scripting-element-object.html
