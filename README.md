# pyegrep

Pyegrep is a very similar package to Grep(on linux) in python
=======


Raw use
-------


```python   
    from pyegrep.greps import grep_service

    params = {
        "before": 2,
        "after": 3,
        "patterns": ["xyz"],
        "address": file_address,
        "hide_colors": True,
        "max_line_numbers": 1000,
        "is_regex": False,
        "is_case_sensitive" : False,
    }
    output = grep_service.grep(params)
    print(output)
```




Installation
------------

To install pyegrep, simply:

```shell
    $ pip install pyegrep
```

On Debian systems:

```shell
    coming soon...
```
