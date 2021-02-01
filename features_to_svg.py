#python3
"""
This file takes list of features prepared by py_feat_to_js_feat
and converts them into actual javascript.
We are using SVG and d3 js by Mike Bostock.
"""

import json
import logging
from js_svg_print import *
#from js_svg_print import *

def make_svg_js(js_feats_fp, plasmid_js_fp, uniq_dict):

    logging.info("Creating Javascript File from feats file.")

    with open(js_feats_fp) as f:
        js_feats_list = json.loads(f.read())


    javascript_str = "//SVG Code Start \n"
    javascript_str += "const {} = d3.select('#{}');\n\n".format(
            uniq_dict['svg_name'], uniq_dict['svg_id'])


    logging.warning(len(js_feats_list))
    for i in range(len(js_feats_list)):
        js_str = ""
        js_feat = js_feats_list[i]
        typ = js_feat["type"]

        if typ == "plasmid_arc_forward":
            js_str = print_plasmid_arc_forward(js_feat, i)
        elif typ == "plasmid_arc_reverse":
            js_str = print_plasmid_arc_reverse(js_feat, i)

        elif typ == "pointer_and_text":
            js_str = print_pointer_and_text(js_feat, i)

        elif typ == "center_text":
            js_str = print_center_text(js_feat, i)

        elif typ == "promoter":
            js_str = print_promoter(js_feat, i)
        #""" 
        #FOR NOW WE AVOID TERMINATOR SYMBOL
        #elif typ == "terminator":
        #    js_str = print_terminator(js_feat, i)
        #"""
        #""" 
        #FOR NOW WE AVOID RBS SYMBOL
        #elif typ == "rbs":
        #    js_str = print_rbs(js_feat, i)
        #"""
        elif typ == "cds":
            js_str = print_cds(js_feat, i)

        elif typ == "gap_arc":
            js_str = print_gap_arc(js_feat, i)
        else:
            logging.info("Did not recognize feature to translate to javascipt.")
            continue

        javascript_str += "//Feature: {} \n".format(str(i)) + js_str



    #Adding delete box:
    js_str = print_delete_box(js_feats_list[-3])
    javascript_str += "//DELETE BOX \n" + js_str

    #Adding reset box:
    js_str = print_reset_box(js_feats_list[-2])
    javascript_str += "//RESET BOX \n" + js_str

    #Adding color legend:
    js_str = print_legend_box(js_feats_list[-1])
    javascript_str += "//COLOR LEGEND  \n" + js_str


    with open(plasmid_js_fp,"w") as g:
        g.write(javascript_str)

    return 0






