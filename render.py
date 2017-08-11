#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import os
import premailer
import re
from jinja2 import Environment, FileSystemLoader

# Folder names
opt_dir = '01_options'
org_dir = '01_organizations'
emp_dir = '02_employees'
css_dir = '02_styles'
tpl_dir = '03_templates'
out_dir = '04_output'

# File extensions
opt_ext = 'json'
css_ext = 'j2.json'
tpl_ext = 'j2.html'
out_ext = 'html'

# Path to source organizations info (organization subfolders with *.json files)
org_path = os.path.join(os.getcwd(), opt_dir, org_dir)
# Path to source organizations employees info (organization subfolders with *.json files)
emp_path = os.path.join(os.getcwd(), opt_dir, emp_dir)
# Path to style info for source email subscription templates (*.j2.json files)
css_path = os.path.join(os.getcwd(), css_dir)
# Path to source email subscription templates (*.j2.html files)
tpl_path = os.path.join(os.getcwd(), tpl_dir)
# Path to rendered signatures (*.html files)
out_path = os.path.join(os.getcwd(), out_dir)

for org in os.listdir(org_path):
    print('org: ', org)
    # Initialize context for rendering
    context = {}

    # Get style for current template
    css_file_name = '{name}.{ext}'.format(name=org, ext=css_ext)
    css_file_path = os.path.abspath(
        os.path.join(css_path, css_file_name)
    )
    css_context = json.load(open(css_file_path, 'r'))

    # Open current template
    tpl_file_name = '{name}.{ext}'.format(name=org, ext=tpl_ext)
    tpl = Environment(
        loader=FileSystemLoader(tpl_path),
        trim_blocks=True
    ).get_template(tpl_file_name)

    # Get current organization data
    org_data_path = os.path.join(org_path, org)
    for org_data in os.listdir(org_data_path):
        org_data_name = org_data[:-5]
        org_data_file_name = '{name}.{ext}'.format(name=org_data_name, ext=opt_ext)
        org_data_file_path = os.path.abspath(
            os.path.join(org_data_path, org_data_file_name)
        )
        org_context = json.load(open(org_data_file_path, 'r'))

        # Process renderable organization data only
        if org_context['renderable'] is True:
            # Check or create organization folder for output
            org_output = os.path.join(out_path, org)
            os.makedirs(org_output, mode=0o755, exist_ok=True)

        # Get organization employees data
        for emp in os.listdir(os.path.join(emp_path, org)):
            emp_name = emp[:-5]
            emp_file_name = '{name}.{ext}'.format(name=emp_name, ext=opt_ext)
            emp_file_path = os.path.abspath(
                os.path.join(emp_path, org, emp_file_name)
            )
            emp_context = json.load(open(emp_file_path, 'r'))

            # Fill rendering context with current style, organization and employee data
            for c in (css_context, org_context, emp_context):
                context.update(c)

            # Render template
            tpl_rendered = tpl.render(context)

            # Inline CSS styles
            tpl_rendered = premailer.Premailer(
                tpl_rendered,
                keep_style_tags=True,
                include_star_selectors=True,
                capitalize_float_margin=True,
                strip_important=False,
                align_floating_images=False,
                remove_unset_properties=False
            ).transform()

            # Prettify result a little bit
            tpl_rendered = tpl_rendered.replace(
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
            tpl_rendered = re.sub(r'^\ +', r'', tpl_rendered, 0, re.MULTILINE)
            tpl_rendered = re.sub(r'\n',   r'', tpl_rendered)

            # Save each output into a HTML file
            current_output_file = (
                emp_name + '_' + org_data_name + '.' + out_ext
            )
            current_output = open(
                os.path.join(org_output, current_output_file), 'w'
            )
            current_output.write(tpl_rendered)
