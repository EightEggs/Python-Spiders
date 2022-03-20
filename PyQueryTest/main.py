### Initialization ###
from pyquery import PyQuery as pq

# 1. HTML string
html = """
<div id="container">
  <ul class="mylist">
    <li class="item-0">text1</li>
    <li class="item-1"><a href="http://example.com/link2">text2</a></li>
    <li class="item-0 active"><a href="http://example.com/link3"><b>text3</b></a></li>
    <li class="item-1 active"><a href="http://example.com/link4">text4</a></li>
    <li class="item-0">text5</li>
  </ul>
</div>
"""

doc = pq(html)
print(doc(".item-0"))

# 2. URL link
doc = pq(url="https://cuiqingcai.com")
print(doc("title"))

# 3. File path
doc = pq(filename="demo.html")
print(doc("p"))


### CSS selector ###
doc = pq(html)
items = doc("#container .mylist li").items()
for item in items:
  print(item.text())


### Find nodes ###
print(doc(".mylist").children(".active"))
print(doc(".mylist").find("li"))
print(doc("li").parent())
print(doc("li").parents())
print(doc(".item-0.active").siblings(".active"))


### EXtract information ###
a = doc(".item-0.active a")
print(a.attr.href) # == print(a.attr("href"))
print(a.text())
print(a.html())


### Nodes operations ###
li = doc(".item-0.active")
print(li)
print(li.remove_class("active"))
print(li.add_class("myclass"))
print(li.attr("name", "link"))
print(li.text("changed text"))
