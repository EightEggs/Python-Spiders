from bs4 import BeautifulSoup

html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <title>The Dormous's story</title>
</head>
<body>
  <p class="title" name="dormous"><b>The Dormous's story</b></p>
  <p class="story">One upon a time there were three little sisters; and their names were
  <a href="http://example.com/elsie" class="sister" id="link1"><span>Elsie</span></a>,
  <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
  <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
  and they lived at the bottom of a well.
  </p>
  <p class="story">...</p>
</body>
</html>
"""

### Basic usage ###
soup = BeautifulSoup(html, 'lxml')
print(soup.prettify())
print(soup.title.string)


### Nodes selector ###
print(soup.head)
print(soup.p)  # only the first p element can be selected.


### Extract information ###
# 1. name
print(soup.title.name)

# 2. attributes
print(soup.p.attrs)
print(soup.p.attrs['name'])  # == print(soup.p['name'])

# 3. contents
print(soup.p.string)      # str
print(soup.p.text)        # str
print(soup.p.get_text())  # str
print(soup.p.contents)    # list


### Relation selector ###
# 1. children and descendants
print(soup.body.children)
for i, child in enumerate(soup.body.children):
    print(i, child)
print(soup.body.descendants)
for i, child in enumerate(soup.body.descendants):
    print(i, child)

# 2. parent and parents
print(soup.a.parent)  # only the first a element can be selected.
print(soup.a.parents)
for i, parent in enumerate(soup.a.parents):
    print(i, parent)

# 3. siblings
print("Next sibling:", soup.a.next_sibling)
print("Prev sibling:", soup.a.previous_sibling)
print("Next siblings:", list(soup.a.next_siblings))
print("Prev siblings:", list(soup.a.previous_siblings))


### Method selector ###
"""
find(), find_all(),
find_parent(), find_parents(),
find_next_sibling(), find_next_siblings(),
find_previous_sibling(), find_previous_siblings(),
find_next(), find_all_next(),
find_previous(), find_all_previous()
...
"""


### CSS selector ###
print(soup.select('.title'))
print(soup.select('p a'))
print(soup.select_one('p a'))
