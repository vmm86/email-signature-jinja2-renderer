#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import jinja2
import json
import os
import premailer
import re

# Folder names
tpl_folder = '01_templates'
opt_folder = '02_options'
opt_org_folder = '01_organizations'
opt_emp_folder = '02_employees'
out_folder = '03_output'

# Path to source email subscription templates (*.j2.html files)
tpl_path = os.path.join(os.getcwd(), tpl_folder)

for tpl in os.listdir(tpl_path):
    # Open current template in Jinja2
    tpl_name = tpl[:-8]
    tpl_file = jinja2.Template(
        open(os.path.join(tpl_path, tpl), 'r').read()
    )

    # Paths to organizations' and employees' data (*.json files)
    org_path = os.path.join(
        os.getcwd(), opt_folder, opt_org_folder, tpl_name
    )
    emp_path = os.path.join(
        os.getcwd(), opt_folder, opt_emp_folder, tpl_name
    )

    # Link with corresponding organization data
    for org in os.listdir(org_path):
        if org.endswith('.json'):
            org_name = org[:-5]
            org_file = os.path.abspath(os.path.join(org_path, org))
            current_org = json.load(open(org_file, 'r'))
        # Process renderable organization data only
        if current_org['renderable'] == True:
            # Check or create organization folder for output
            org_output = os.path.join(os.getcwd(), out_folder, tpl_name)
            os.makedirs(org_output, mode=0o755, exist_ok=True)

        # Link with corresponding employee data
        for emp in os.listdir(emp_path):
            if emp.endswith('.json'):
                emp_name = emp[:-5]
                emp_file = os.path.abspath(os.path.join(emp_path, emp))
                current_emp = json.load(open(emp_file, 'r'))

            # Join current organization's and employees's data
            current_emp.update(current_org)

            # Render basic template
            current_tpl = tpl_file.render(current_emp)

            # Inline CSS styles
            current_tpl = premailer.Premailer(
                current_tpl, 
                keep_style_tags=True,
                include_star_selectors=True,
                capitalize_float_margin=True,
                strip_important=False,
                align_floating_images=False,
                remove_unset_properties=False
            ).transform()

            # Prettify result a little bit
            current_tpl = current_tpl.replace(
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
            current_tpl = re.sub(r'^\ +', r'', current_tpl, 0, re.MULTILINE)
            current_tpl = re.sub(r'\n',   r'', current_tpl)

            # Save each output into a HTML file
            if org_name == tpl_name:
                current_output_file = (
                    emp_name + '_' + tpl_name + '.html'
                )
            else:
                current_output_file = (
                    emp_name + '_' + org_name + '_' + tpl_name + '.html'
                )

            current_output = open(
                os.path.join(org_output, current_output_file), 'w'
            )
            current_output.write(current_tpl)
