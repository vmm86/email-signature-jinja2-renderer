# Jinja2 templater for email signatures

Python Jinja2 templater to create multiple HTML email signatures for different organization's employees.

# Requirements

```python
cssselect==1.0.1
cssutils==1.0.1
Jinja2==2.9.5
lxml==3.7.2
MarkupSafe==0.23
premailer==3.0.1
requests==2.13.0
```

# Project Structure

You should create a new virtual environment with Python 3 and install everything from `requirements.txt`.

You may have several organizations and their employees within the same project 
and render their files simultaneously or seperately.

Project has 3 main folders:

1. `01_templates` - source Jinja2 templates for email subscription that contain specific logic for rendering. It should contain template files in the following way: `01_templates/{organization}.j2.html`.

2. `02_options` - JSON files with options for various organizations and their employees. It should contain organizations option files in the following way: `02_options/organizations/{organization}/{organization}.json` and employees option files in the following way: `02_options/employees/{organization}/{employee}.json`.

3. `03_output` - output HTML files with rendered templates. It would contain output files in the following way: `03_output/{organization}/{employee}_{organization}.html`.

`{organization}` JSON file format:

```js
{
    // Boolean option to render current organization's files or not
    "randerable": true,

    // Organization's title
    "org_title": "Бельканто",
    // Organization's alias (used in rendering logic)
    "org_alias": "belcanto",
    // Width and height of organization's logo
    "org_logo_width":  "91",
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

You may also create various organization JSON files within the same `{organization}` folder 
to render different files with slightly different options.

`{employee}` JSON file format:

```js
{
    "emp_name_ru":       "Барсуков Анатолий Геннадьевич",
    "emp_occupation_ru": "Начальник кузовного цеха",
    "emp_department_ru": "Кузовной цех",

    "emp_name_en":       "Barsukov Anatoliy Gennadyevich",
    "emp_occupation_en": "Head of body workshop",
    "emp_department_en": "Body workshop",

    "emp_ext_tel": "806",
    "emp_mob_tel": "+7(905) 654-42-83",
    "emp_email":   "dp@scanezh.ru"
}
```
# Usage

Prepare all the source data and simply run `python render.py`.

It does the following steps:

1. Takes business data from different JSON files stored recursively in `02_options` folder.

Each employee's file is linked with organization by its parent folder name.

2. Joins each employee info with its organization info.

3. Renders each template according to input data.
If organization's `test_tags` paramenter is set to `normal`, every CSS style will remain as it is, 
with `important` each CSS style will be apended with `!important` rule.
Such hardcore bulletproof style may be useful to override some email clients/web interfaces default styles.

4. Inlines all CSS styles with `premailer`.
Each style within the `<style>` tag goes into `style` attribute of each corresponding HTML tag.

5. Minifies code by simple regexps.

5. Saves each template into separate file in `03_output` folder within its `{organization}` subfolder.
