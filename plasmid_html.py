#python3

"""
Takes template and inserts javascript into template html
"""
import json
"""
Inputs:
    plasmid_js: (str) filepath to file containing javascript string.
    out_fp: (str) filepath to where we'll write the file out.
"""
def html_prepare(plasmid_js_fp, template_html_fp, out_fp, config_fp):

    with open (plasmid_js_fp, "r") as f:
        js_str = f.read()
    with open(template_html_fp, "r") as g:
        html_str = g.read()
    with open(config_fp, "r") as g:
        config_dict = json.loads(g.read())


    html_str = html_str.replace("&{--Highlight Color--}&",
            '#' + config_dict['js_info']['highlight_color'])
    html_str = html_str.replace("SVG_ID_HERE",
            uniq_dict['svg_id'])
    html_and_js_str = html_str.replace("{--Insert JS--}", js_str)

    with open(out_fp, "w") as h:
        h.write(html_and_js_str)



    return 0

def div_html_prepare(plasmid_js_fp, template_html_fp, config_fp, 
        plasmid_info_fp, uniq_dict):

    with open (plasmid_js_fp, "r") as f:
        js_str = f.read()
    with open(template_html_fp, "r") as g:
        html_str = g.read()
    with open(config_fp, "r") as g:
        config_dict = json.loads(g.read())
    with open(plasmid_info_fp, "r") as g:
        plasmid_info_dict = json.loads(g.read())


    html_str = html_str.replace("SVG_ID_HERE",
            uniq_dict['svg_id'])
    html_and_js_str = html_str.replace("{--Insert JS--}", js_str)
    html_and_js_str = html_and_js_str.replace("&{--Highlight Color--}&",
            '#' + config_dict['js_info']['highlight_color'])



    html_dict = {
        "plasmid_name": plasmid_info_dict["plasmid_name"], 
        "complete_div_str": html_and_js_str

            }

    '''
    with open(out_fp, "w") as h:
        h.write(html_and_js_str)
    '''


    return html_dict


