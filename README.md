# Jinja2 templater for email signatures

Python Jinja2 templater to create multiple HTML email signatures for different organization's employees.

# Requirements

```python
appdirs==1.4.0
cssselect==1.0.1
cssutils==1.0.1
Jinja2==2.9.5
lxml==3.7.2
MarkupSafe==0.23
packaging==16.8
premailer==3.0.1
pyparsing==2.1.10
requests==2.13.0
six==1.10.0
```

# Project Structure

Project has 4 main folders:

1. `01_options` - JSON files with options for various organizations and their employees. It should contain organizations option files in the following way: `01_options/01_organizations/{organization}/{organization}.json` and employees option files in the following way: `01_options/02_employees/{organization}/{employee}.json`.

2. `02_styles` - CSS styles for specific organization stored in JSON files, stored in the following way: `{organization}.j2.json`. Every CSS selector from JSON file goes to template engine to style specific organization's template with the help of `css.j2.html` macros from the `03_templates/macros`.

3. `03_templates` - source Jinja2 templates for email subscription that contain specific logic for rendering. It should contain template files in the following way: `03_templates/{organization}.j2.html`.

4. `04_output` - output HTML files with rendered templates. It would contain output files in the following way: `04_output/{organization}/{employee}_{organization}.html`.

You may have several organizations and their employees within the same project and render their files simultaneously or separately.

# Organization JSON files

`{organization}` JSON file format:

```js
{
    // Boolean option to render current organization's files or to skip rendering
    "renderable": true,

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
to render different files with slightly different options, for example:

* *internal* or *external* email communiaction (inside the company or with external partners).
* *primary* or *secondary* email messagess.
* email communiaction with *Russian*-speaking or *English*-speaking partners.

# Employee JSON files

`{employee}` JSON file format:

```js
{
    "emp_name_ru":       "Барсуков Анатолий Геннадьевич",
    "emp_occupation_ru": "Начальник кузовного цеха",
    "emp_department_ru": "Кузовной цех",

    "emp_name_en":       "Barsukov Anatoliy Gennadyevich",
    "emp_occupation_en": "Head of body workshop",
    "emp_department_en": "Body workshop",

    "emp_ext_tel":       "806",
    "emp_mob_tel":       "+7(905) 654-42-83",
    "emp_email":         "dp@scanezh.ru"
}
```

# Usage

You should create a new virtual environment with Python 3 and install everything from `requirements.txt`.

Prepare all of the source data and simply run `python render.py`.

It walks through the following steps:

1. Takes business data from different JSON files stored recursively in `01_options` folder. Each employee's file is linked with his/her organization by its parent folder's name.

2. Joins each employee info with his/her organization info.

3. Renders each template according to input data. If organization's `test_tags` paramenter is set to `normal`, every CSS style will remain as it is, with `important` each CSS style will be apended with `!important` rule to strictly override any possible email client's or web interface's default CSS rules.

4. Inlines all CSS styles with `premailer`. Each style within the `<style>` tag goes into `style` attribute of each corresponding HTML tag.

5. Minifies code by simple regexps.

6. Saves each template into separate file in `04_output` folder within its `{organization}` subfolder.
