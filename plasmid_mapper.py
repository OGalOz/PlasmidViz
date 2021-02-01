#python3

"""
Input is a gbk file (or eventually a gff file)
    config file is at gbk_config.json


"""

"""
Process:
    plasmid_mapper takes gbk file, config file, and output name and does the following:
    1. Genbank file goes through "genbank_prepare" preparation:
        (Clears tmp dir)
         a. Remove duplicate sections

    2. "feature_prepare" (prep_py_feat.py) takes Genbank File and prepares two
        json files: plasmid_info.json, and feature_list.json

    3. "refine_features" takes feature_list.json and removes unnecessary features
    and adds in gap features.

    4. js_prepare takes plasmid_info.json, feature_list.json, and config.json
        and creates js_feats.json

    5. features_to_svg takes js_feats.json and creates plasmid_js.js

    6. html_prepare takes plasmid_js.js and template.html and creates the final
        html_file

"""

import sys
import os
from os import path
import shutil
from prepare_gbk import genbank_prep 
from prep_py_feat import feature_prepare
from py_feat_to_js_feat import js_prepare
from features_to_svg import make_svg_js
from plasmid_html import html_prepare, div_html_prepare


def create_plasmid_map_display(plasmid_inp, typ, op_dir):
    """
    Args:
        plasmid_inp: (str) fp to input file, gbk or gff
        typ: (str) 'gbk' or 'gff' (Currently only gbk)
        op_dir: (str) Output directory loc

    Note:
        config fp: will be at gbk_config.json (?)
    """
   
    config_fp = 'gbk_config.json'
    new_gbk = 'tmp/new.gbk'
    original_gbk_name = genbank_prep(plasmid_inp, config_fp, new_gbk)
    
    
    feature_list_fp = "tmp/feature_list.json"
    plasmid_info_fp = "tmp/plasmid_info.json"

    # Below function returns None, but writes files to above 2 files.
    feature_prepare(new_gbk, config_fp, feature_list_fp, 
            plasmid_info_fp, original_gbk_name)


    js_feats_fp = "tmp/js_feats.json"

    #py_feat_to_js_feat
    js_prepare(feature_list_fp, plasmid_info_fp, config_fp, js_feats_fp)

    #features_to_svg , js_svg_print
    make_svg_js(js_feats_fp, plasmid_js_fp, uniq_dict)

    sys.exit(0)
    
    

def get_cello_plasmid_map_div(gbk_inp, base_div_html_fp, config_fp, uniq_dict):
    """
    Args:
        gbk_inp: filepath
        base_div_html_fp: html of base div filepath
        config_fp: json config filepath
        uniq_dict: (?)
            "file_num": i,
            "uniq_id": "prfx_" + str(i),
            "svg_id": "svg-" + str(i),
            "svg_name": "svg_" + str(i),
            "tmp_name": "plasmid_tmp_" + str(i),
            "scratch_dir": plasmid_vis_info["scratch_dir"]

    """
       

    program_dir = path.dirname(path.abspath(__file__))


    prepared_genbank_fp = path.join(program_dir, "tmp/prepared_genbank.gbk")

    old_gb_name = genbank_prep(gbk_inp, config_fp, prepared_genbank_fp)
    

    feature_list_fp = path.join(program_dir, "tmp/feature_list.json")
    plasmid_info_fp = path.join(program_dir, "tmp/plasmid_info.json")

    feature_prepare(prepared_genbank_fp, config_fp, feature_list_fp, 
            plasmid_info_fp, old_gb_name)


    js_feats_fp = path.join(program_dir, "tmp/js_feats.json")

    js_prepare(feature_list_fp, plasmid_info_fp, config_fp, js_feats_fp, 
            uniq_dict)

    plasmid_js_fp = path.join(program_dir, "tmp/plasmid_js.js")
    make_svg_js(js_feats_fp, plasmid_js_fp, uniq_dict)

    template_html_fp = path.join(program_dir, base_div_html_fp)

    html_dict = div_html_prepare(plasmid_js_fp, template_html_fp, config_fp, 
            plasmid_info_fp, uniq_dict)

    #We copy all the contents of the folder to a tmp folder in the scratch dir
    shutil.copytree(path.join(program_dir, "tmp"),
    path.join(uniq_dict["scratch_dir"],uniq_dict["tmp_name"]))

    return html_dict


def old_main():
    args = sys.argv
    gbk_input    = args[1] 
    config_fp = args[2] 
    out_fp       = args[3] 
       
    program_dir = path.dirname(path.abspath(__file__))

    genbank_prep(gbk_input, config_fp)
    
    prepared_genbank_fp = path.join(program_dir, "tmp/prepared_genbank.gbk")

    feature_list_fp = path.join(program_dir, "tmp/feature_list.json")

    plasmid_info_fp = path.join(program_dir, "tmp/plasmid_info.json")

    feature_prepare(prepared_genbank_fp, config_fp, feature_list_fp, plasmid_info_fp)


    js_feats_fp = path.join(program_dir, "tmp/js_feats.json")

    js_prepare(feature_list_fp, plasmid_info_fp, config_fp, js_feats_fp, 
            uniq_dict)

    plasmid_js_fp = path.join(program_dir, "tmp/plasmid_js.js")
    make_svg_js(js_feats_fp, plasmid_js_fp)

    template_html_fp = path.join(program_dir, "div_svg_template.html")

    html_prepare(plasmid_js_fp, template_html_fp, out_fp, config_fp)

def main():
    # As inputs we take a genbank file or a gff file
    
    # The config file has a stagnant location
    #

    args = sys.argv
    if args[-1] != "1":
        help_str = "python3 plasmid_mapper.py plasmid_gbk op_dir typ 1"
        print(help_str)
        sys.exit(0)
    else:
        plasmid_inp = args[1]
        typ = args[3]
        op_dir = args[2]
        typ  = 'gbk'
        create_plasmid_map_display(plasmid_inp, typ, op_dir)

    return 0


if __name__ == "__main__":
    main()


