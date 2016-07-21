#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import jinja2
import json
import os
import premailer
import re

# Source email subscription template
template = jinja2.Template(
    open('template.j2.html', 'r').read()
)

# Paths to employees and organization data
employees     = os.path.join(os.getcwd(), 'options', 'employees')
organizations = os.path.join(os.getcwd(), 'options', 'organizations')

for opt in os.listdir(employees):
    if opt.endswith('.json'):
        # Get each employee's self data
        cur_employee = json.load(
            open(os.path.join(employees, opt), 'r')
        )

        # Get each employee's organization data
        if opt.split('_')[0] == 'belcanto':
            cur_organization = json.load(
                open(os.path.join(organizations, 'belcanto.json'), 'r')
            )
        if opt.split('_')[0] == 'bezantrakta':
            cur_organization = json.load(
                open(os.path.join(organizations, 'bezantrakta.json'), 'r')
            )

        # Join employees's and organization's dicts
        cur_employee.update(cur_organization)

        # Render basic template
        cur_template = template.render(cur_employee)

        # Inline CSS styles
        cur_template = premailer.Premailer(
            cur_template, 
            keep_style_tags=True,
            include_star_selectors=True,
            capitalize_float_margin=True,
            strip_important=False,
            align_floating_images=False,
            remove_unset_properties=False
        ).transform()

        # Prettify result a little bit
        cur_template = cur_template.replace(
            'align="center !important"', 
            'align="center"'
        ).replace(
            'valign="middle !important"',
            'valign="middle"'
        ).replace(
            'nbsp',
            '&nbsp;'
        )

        # Minify code
        cur_template = re.sub(r'^\ +', r'', cur_template, 0, re.MULTILINE)
        cur_template = re.sub(r'\n',   r'', cur_template)

        # Save each result into HTML file

        cur_output = open(
            os.path.join(os.getcwd(), 'templates',
                opt[:-5] + '.html'
            ), 'w'
        )
        cur_output.write(cur_template)
