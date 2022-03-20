### Initialization ###
from pyquery import PyQuery as pq

# 1. HTML string
html = """
<div>
  <ul>
    <li class="item-0"></li>
    <li class="item-1"></li>
    <li class="item-0"></li>
    <li class="item-1"></li>
    <li class="item-0"></li>
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


### Find nodes ###


### Traversal ###


### Nodes operations ###
