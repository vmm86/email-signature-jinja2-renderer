# Jinja2 templater for email signatures

Python Jinja2 templater to create multiple HTML files for email signatures of some organization's employees.

# Requirements

```python
cssselect==0.9.2
cssutils==1.0.1
Jinja2==2.8
lxml==3.6.0
MarkupSafe==0.23
premailer==3.0.0
requests==2.10.0
```

# Usage

You should create a new virtual environment with Python 3 and install everything from `requirements.txt`.

Then prepare the source data and simply run `renderer.py`. It does the following:

1. Take business data from different JSON files stored in `options` folder recursively.
This folder has 2 subfolders - `employees` and `organizations`.
Each employee's file is prefixed with organization name to link them together.
2. Join each employee info with its organization by employee's prefix.
3. Render each template according to input data.
If organization's `test_tags` paramenter is set to `normal`, every CSS style will remain as it is, 
with `important` each CSS style will be apended with `!important` rule.
Such hardcore bulletproof style may be useful for some email clients/web interfaces.
4. Inline all CSS styles with `premailer`.
5. Minify code by simple regexps.
5. Save each template into separate file in `templates` folder.
