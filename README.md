# Ebuilder-Ultra
![Tests Passing](https://github.com/RhinoCodes/Ebuilder-Ultra/workflows/Tests%20Passing/badge.svg)
A web framework intended for use with the Ebuilder static site generator.
## Hello, World!
The classic! Anyways here we go:
```python
from ultra import Ultra
@app.route("/")
def index():
    return "Hello, World!"
```
## Hello, _name_!
```python
from ultra import Ultra
@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name}!"
```
