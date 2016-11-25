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

1. Takes business data from different JSON files stored in `options` folder recursively.
This folder has 2 subfolders - `employees` and `organizations`.

`employees` JSON file format:

```js
{
    // Employee's name
    "name": "Галина Нехаева",
    // Employee's occupation
    "occupation": "Главный администратор",
    // Phone link and text (for one number - `tel`, for multiple numbers - `tel1`, `tel2`, etc.)
    "tel1_text": "+7 (960) 111 49 86",
    "tel1_link": "+79601114986",
    "tel2_text": "+7 (473) 277 60 60",
    "tel2_link": "+74732776060",
    // Email address
    "email": "galina@gastroli.net"
}
```

`organizations` JSON file format:

```js
{
    // Organization's title
    "org_title": "Бельканто",
    // Organization's alias (used in rendering logic)
    "org_alias": "belcanto",
    // Width and height of organization's logo
    "org_logo_width": "91",
    "org_logo_height": "62",
    // Motto text beyond the logo
    "org_motto": "вместе мы сила!",
    // Organization's web site link
    "org_link": "gastroli.net",
    // Message at the bottom
    "org_footer": "Просьба не удалять переписку из тела письма для удобства коммуникаций",
 
    // Test tag to force all CSS styles to be `!important`
    // "normal"
    // "important"
    "test_tags": "important"
}
```

Each employee's file is prefixed with organization name to link them together.

2. Joins each employee info with its organization by employee's prefix.

3. Renders each template according to input data.
If organization's `test_tags` paramenter is set to `normal`, every CSS style will remain as it is, 
with `important` each CSS style will be apended with `!important` rule.
Such hardcore bulletproof style may be useful for some email clients/web interfaces.

4. Inlines all CSS styles with `premailer`.
5. Each style within the `<style>` tag goes into `style` attribute of each corresponding HTML tag.

5. Minifies code by simple regexps.

5. Saves each template into separate file in `templates` folder.
