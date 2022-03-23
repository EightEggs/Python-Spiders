from parsel import Selector

html = """
<div>
  <ul>
    <li class="item-0">text1</li>
    <li class="item-1"><a href="http://example.com/link2">text2</a></li>
    <li class="item-0 active"><a href="http://example.com/link3"><b>text3</b></a></li>
    <li class="item-1 active"><a href="http://example.com/link4">text4</a></li>
    <li class="item-0">text5</li>
  </ul>
</div>
"""

### Basic usage ###
selector = Selector(text=html)
items = selector.css(".item-0")  # CSS selector
items2 = selector.xpath("//li[contains(@class, 'item-0')]")  # XPath selector
print(items, '\n', items2)  # the results are both XPath


### Extract text ###
for item in items:
    print(item.xpath(".//text()").get())  # traversal
result = selector.xpath(
    "//li[contains(@class, 'item-0')]//text()").getall()  # return a list
print(result)


### Extract attrs ###
result = selector.css(".item-0.active a::attr(href)").get()
print(result)
result = selector.xpath(
    "//li[contains(@class, 'item-0') and contains(@class, 'active')]/a/@href").get()
print(result)


### Extract info via RegExp ###
result = selector.css(".item-0").re_first("<b>(.*)</b>")
print(result)
result = selector.css(".item-1").re("link.*>(.*)</a>")
print(result)
result = selector.css(".item-0 *::text").re("\d")
print(result)
