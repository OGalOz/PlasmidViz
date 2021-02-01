#python3

"""
The functions in this filed are called by plasmid_mapper.py.
It takes a prepared genbank file and the config file.
    prepared genbank has the following rules:
    No overlapping sections.
    Every bp is accounted for by some feature, even if unsure
It creates two files: plasmid_info.json, and feature_list.json
"""

import sys
import os
import logging
import math
import random
import string
import json
from Bio import SeqIO
from calculate_feats import calc_dist


def feature_prepare(prepared_genbank_fp, config_fp, op_feature_list_fp, 
        op_plasmid_info_fp, old_gb_name):

    """
    Inputs:
        prepared_genbank_fp: (str) Filepath to input genbank
        config_fp: (str) Filepath to config file
        op_feature_list_fp: (str) Path to write feature list (JSON)
        op_plasmid_info_fp: (str) Path to write plasmid info (JSON)
        old_gb_name: (str) Original genbank file name of data
    Returns:
        None
    """
    logging.basicConfig(level=logging.DEBUG)
    with open(config_fp, "r") as f:
        config_dict = json.loads(f.read())
    gb_record = SeqIO.read(open(prepared_genbank_fp,"r"), "genbank")


    plasmid_info = get_plasmid_info(gb_record, config_dict, op_plasmid_info_fp,
            old_gb_name)

    feat_info_list = get_features(gb_record, config_dict)
    complex_feat_info_list = get_complex_features(gb_record, config_dict)

    feat_info_dict_list = add_gap_elements(complex_feat_info_list, config_dict, plasmid_info)
    feat_info_dict_list = add_ids(feat_info_dict_list)

    plasmid_info_obj = {
            "plasmid_info": plasmid_info,
            "feat_info_list": feat_info_list,
            "plasmid_seq": str(gb_record.seq)
            }

    with open("tmp/plasmid_obj.js", "w") as g:
        g.write("window.plasmid_object = " + json.dumps(plasmid_info_obj,
                                                          indent=2))

    with open("tmp/feature_list.json", "w") as g:
        g.write(json.dumps(feat_info_dict_list, indent=2))

    return None


    
def get_plasmid_info(gb_record, config_dict, plasmid_info_fp,
        old_gb_name):
    """
    Args:
        gb_record: Bio SeqRecord object
        config_dict: (dict) python dict of config.json from this dir.
    Returns:
        plasmid_info: (dict)
            plasmid_name: (str)
            plasmid_length: (int)
            num_features: (int)
            old_gb_name: (str)
    Writes JSON file with plasmid_info at plasmid_info_fp
    """

    plasmid_name = gb_record.name

    logging.warning("PLASMID NAME : {}".format(plasmid_name))

    if config_dict["genbank_info"]["cello_bool"] == True:
        plasmid_name = "_".join(old_gb_name.split("_")[3:])

    plasmid_info = {
            "plasmid_name": plasmid_name,
            "plasmid_length": len(gb_record.seq),
            "num_features": len(gb_record.features),
            "old_gb_name": old_gb_name
    }
    
    #Checking
    if plasmid_info["num_features"] > config_dict["genbank_info"]["max_num_feat"]:
        raise ValueError("Too many features in genbank file: {}\
                ".format(plasmid_name))

    with open(plasmid_info_fp,"w") as g:
        g.write(json.dumps(plasmid_info, indent=2, sort_keys=True))

    return plasmid_info



"""
"""
def get_features(gb_record, config_dict):
    """
    We get the following info:
        [feature_start (int), feature_end (int), strand (str) (+/-),
         feature_type (str)]
    Inputs:
        gb_record: Bio SeqRecord object
        config_dict: (dict) python dict of config.json from this dir.
            genbank_info: (dict)
                name_tags: list<str>
                
    Outputs:
        
        feature_info_list: list<feature_info>
            feature_info: list<feature_start (int),
                               feature_end (int),
                               strand (str) (+/-),
                               feature_type (str),
                               feature_name (str)>
    """

    features_list = gb_record.features



    plasmid_len = len(gb_record.seq)
    circle_center = config_dict['js_info']['center_coordinates']
    genbank_info = config_dict["genbank_info"]

    feat_info_list =  []


    for i in range(len(features_list)):
        feat = features_list[i]
        feat_type = feat.type
        feat_loc = feat.location
        feat_strand = '+' if feat.strand == 1 else '-'
        bp_start = feat_loc.nofuzzy_start + 1
        bp_end = feat_loc.nofuzzy_end

        # name_opt
        name_opt = genbank_info["name_tags"]
        feat_name = ""
        for qual in feat.qualifiers.keys():
            if qual in name_opt:
                feat_name = feat.qualifiers[qual][0]
                break
        if feat_name == "":
            feat_name = "unknown"
        feat_info_list.append([
            bp_start,
            bp_end,
            feat_strand,
            feat_type,
            feat_name
        ])


    '''
    for i in range(len(features_list)):
        feat = features_list[i]
        feat_type = feat.type
        feat_loc = feat.location
        feat_strand = feat.strand
        if feat_strand == -1:
            radius = config_dict['js_info']['complementary_radius'] 
        else:
            radius = config_dict['js_info']['circle_radius']
        bp_start = feat_loc.nofuzzy_start + 1
        bp_end = feat_loc.nofuzzy_end
        bp_len = bp_end - bp_start
        plasmid_percentage = float(float(bp_len)/float(plasmid_len))
        start_percentage = float(float(bp_start)/float(plasmid_len))
        end_percentage = start_percentage + plasmid_percentage
        mid_percentage = start_percentage + (plasmid_percentage/2)
        name_opt = genbank_info["name_tags"]
        feat_name = ""
        for qual in feat.qualifiers.keys():
            if qual in name_opt:
                feat_name = feat.qualifiers[qual]
        if feat_name == "":
            feat_name = "unknown"

        #Choosing color:
        types_dict = genbank_info["types_dict"]
        colors_dict = genbank_info["colors_dict"] 
        main_key = ""
        for k in types_dict.keys():
            if feat_type in types_dict[k]:
                main_key = k
        if main_key == "":
            feat_color = colors_dict["unknown"] 
        else:
            feat_color = colors_dict[main_key]
        



        

        #Feature brightness
        feat_shade = "bright"
        if i > 0:
            if feat_info_dict_list[-1]["feat_shade"] == "bright":
                feat_shade = "dark"


        """ OLD COLOR IMPLEMENTATION
        #Feature color
        feat_color = get_random_color(feat_shade)
        """

        #Calculating positions in the canvas:
        angle_start = (2*math.pi)*start_percentage 
        angle_mid = (2*math.pi)*mid_percentage  
        angle_end = (2*math.pi)*end_percentage 
        

        point_start = [circle_center[0] + radius*math.cos(-1*(angle_start - (math.pi/2) )),
        circle_center[1] - radius*math.sin(-1*(angle_start - (math.pi/2)))]

        point_mid = [circle_center[0] + radius*math.cos(-1*(angle_mid-(math.pi/2))), 
        circle_center[1] - radius*math.sin(-1*(angle_mid - (math.pi/2)))]

        point_end = [circle_center[0] + radius*math.cos(-1*(angle_end-(math.pi/2))),
        circle_center[1] - radius*math.sin(-1*(angle_end - (math.pi/2)))]



        #This is either short, medium, or long
        feat_pointer_len = "short"
        if i > 0:
            if feat_info_dict_list[-1]["feat_pointer_len"] in ["short","long"]:
                feat_pointer_len = "medium"
            else:
                if feat_info_dict_list[-2]["feat_pointer_len"] == "short":
                    feat_pointer_len = "long"
                else:
                    feat_pointer_len = "short"

        #This is in or out:
        feat_pointer_direction = "out"
        if i > 0:
            old_midpoint = feat_info_dict_list[-1]["point_mid"]
            dist = calc_dist(point_mid, old_midpoint)
            if dist < config_dict['js_info']['midpoint_distance']:
                feat_pointer_direction = "in"




        feat_info_dict = {
            "feat_type": feat_type,
            "bp_start": bp_start,
            "bp_end": bp_end,
            "bp_len": bp_len,
            "plasmid_percentage": plasmid_percentage,
            "start_percentage": start_percentage,
            "mid_percentage": mid_percentage,
            "end_percentage": end_percentage,
            "feat_name": feat_name,
            "feat_strand":feat_strand,
            "feat_pointer_len":feat_pointer_len,
            "feat_pointer_direction":feat_pointer_direction,
            "feat_shade":feat_shade,
            "feat_color":feat_color,
            "point_start":point_start,
            "point_mid":point_mid,
            "point_end":point_end,
            "angle_start": angle_start,
            "angle_mid": angle_mid,
            "angle_end": angle_end
        }
        feat_info_dict_list.append(feat_info_dict)
    '''

    return feat_info_list 


def get_complex_features(gb_record, config_dict):
    """
    We get the following info:
        [feature_start (int), feature_end (int), strand (str) (+/-),
         feature_type (str)]
    Inputs:
        gb_record: Bio SeqRecord object
        config_dict: (dict) python dict of config.json from this dir.
            genbank_info: (dict)
                name_tags: list<str>
                
    Outputs:
        
        feature_info_list: list<feature_info>
            feature_info: list<feature_start (int),
                               feature_end (int),
                               strand (str) (+/-),
                               feature_type (str),
                               feature_name (str)>
    """

    features_list = gb_record.features



    plasmid_len = len(gb_record.seq)
    circle_center = config_dict['js_info']['center_coordinates']
    genbank_info = config_dict["genbank_info"]

    feat_info_dict_list =  []

    for i in range(len(features_list)):
        feat = features_list[i]
        feat_type = feat.type
        feat_loc = feat.location
        feat_strand = feat.strand
        if feat_strand == -1:
            radius = config_dict['js_info']['complementary_radius'] 
        else:
            radius = config_dict['js_info']['circle_radius']
        bp_start = feat_loc.nofuzzy_start + 1
        bp_end = feat_loc.nofuzzy_end
        bp_len = bp_end - bp_start
        plasmid_percentage = float(float(bp_len)/float(plasmid_len))
        start_percentage = float(float(bp_start)/float(plasmid_len))
        end_percentage = start_percentage + plasmid_percentage
        mid_percentage = start_percentage + (plasmid_percentage/2)
        name_opt = genbank_info["name_tags"]
        feat_name = ""
        for qual in feat.qualifiers.keys():
            if qual in name_opt:
                feat_name = feat.qualifiers[qual]
        if feat_name == "":
            feat_name = "unknown"

        #Choosing color:
        types_dict = genbank_info["types_dict"]
        colors_dict = genbank_info["colors_dict"] 
        main_key = ""
        for k in types_dict.keys():
            if feat_type in types_dict[k]:
                main_key = k
        if main_key == "":
            feat_color = colors_dict["unknown"] 
        else:
            feat_color = colors_dict[main_key]
        



        

        #Feature brightness
        feat_shade = "bright"
        if i > 0:
            if feat_info_dict_list[-1]["feat_shade"] == "bright":
                feat_shade = "dark"


        """ OLD COLOR IMPLEMENTATION
        #Feature color
        feat_color = get_random_color(feat_shade)
        """

        #Calculating positions in the canvas:
        angle_start = (2*math.pi)*start_percentage 
        angle_mid = (2*math.pi)*mid_percentage  
        angle_end = (2*math.pi)*end_percentage 
        

        point_start = [circle_center[0] + radius*math.cos(-1*(angle_start - (math.pi/2) )),
        circle_center[1] - radius*math.sin(-1*(angle_start - (math.pi/2)))]

        point_mid = [circle_center[0] + radius*math.cos(-1*(angle_mid-(math.pi/2))), 
        circle_center[1] - radius*math.sin(-1*(angle_mid - (math.pi/2)))]

        point_end = [circle_center[0] + radius*math.cos(-1*(angle_end-(math.pi/2))),
        circle_center[1] - radius*math.sin(-1*(angle_end - (math.pi/2)))]



        #This is either short, medium, or long
        feat_pointer_len = "short"
        if i > 0:
            if feat_info_dict_list[-1]["feat_pointer_len"] in ["short","long"]:
                feat_pointer_len = "medium"
            else:
                if feat_info_dict_list[-2]["feat_pointer_len"] == "short":
                    feat_pointer_len = "long"
                else:
                    feat_pointer_len = "short"

        #This is in or out:
        feat_pointer_direction = "out"
        if i > 0:
            old_midpoint = feat_info_dict_list[-1]["point_mid"]
            dist = calc_dist(point_mid, old_midpoint)
            if dist < config_dict['js_info']['midpoint_distance']:
                feat_pointer_direction = "in"




        feat_info_dict = {
            "feat_type": feat_type,
            "bp_start": bp_start,
            "bp_end": bp_end,
            "bp_len": bp_len,
            "plasmid_percentage": plasmid_percentage,
            "start_percentage": start_percentage,
            "mid_percentage": mid_percentage,
            "end_percentage": end_percentage,
            "feat_name": feat_name,
            "feat_strand":feat_strand,
            "feat_pointer_len":feat_pointer_len,
            "feat_pointer_direction":feat_pointer_direction,
            "feat_shade":feat_shade,
            "feat_color":feat_color,
            "point_start":point_start,
            "point_mid":point_mid,
            "point_end":point_end,
            "angle_start": angle_start,
            "angle_mid": angle_mid,
            "angle_end": angle_end
        }
        feat_info_dict_list.append(feat_info_dict)

    return feat_info_dict_list 

        
        
def add_gap_elements(feat_info_dict_list, config_dict, plasmid_info):
    plasmid_len = plasmid_info['plasmid_length']
    gap_feat_list = []
    circle_center = config_dict['js_info']['center_coordinates']

    logging.debug("ADDING GAP ELEMENTS:")
    for i in range(len(feat_info_dict_list) - 1):
        feat_dict = feat_info_dict_list[i]
        next_feat_dict = feat_info_dict_list[i+1]
        diff = next_feat_dict['bp_start'] - feat_dict['bp_end']
        if diff > 1:
            logging.debug("making new feat (gap)")
            feat_type = "feature_gap" 
            radius = config_dict['js_info']['circle_radius']
            bp_start =   feat_dict['bp_end'] + 1
            feat_strand = 1
            bp_end = next_feat_dict['bp_start'] - 1
            bp_len = bp_end - bp_start
            plasmid_percentage = float(float(bp_len)/float(plasmid_len))
            start_percentage = float(float(bp_start)/float(plasmid_len))
            end_percentage = start_percentage + plasmid_percentage
            mid_percentage = start_percentage + (plasmid_percentage/2)
            feat_color = "black"
            #Calculating positions in the canvas:
    
            angle_start = (2*math.pi)*start_percentage 
            angle_mid = (2*math.pi)*mid_percentage  
            angle_end = (2*math.pi)*end_percentage 
    
            point_start = [circle_center[0] + radius*math.cos(angle_start),
            circle_center[1] + radius*math.sin(angle_start) ]
    
            point_mid = [circle_center[0] + radius*math.cos(angle_mid), 
            circle_center[1] + radius*math.sin(angle_mid)]
    
            point_end = [circle_center[0] + radius*math.cos(angle_end),
            circle_center[1] + radius*math.sin(angle_end)]

            gap_feat_dict = {
            "feat_type": feat_type,
            "feat_list_loc": [i, i+1],
            "bp_start": bp_start,
            "bp_end": bp_end,
            "bp_len": bp_len,
            "plasmid_percentage": plasmid_percentage,
            "start_percentage": start_percentage,
            "mid_percentage": mid_percentage,
            "end_percentage": end_percentage,
            "feat_name": "gap",
            "feat_strand":feat_strand,
            "feat_color":feat_color,
            "point_start":point_start,
            "point_mid":point_mid,
            "point_end":point_end,
            "angle_start": angle_start,
            "angle_mid": angle_mid,
            "angle_end": angle_end
            }
            gap_feat_list.append(gap_feat_dict)

    feat_info_dict_list += gap_feat_list

    return feat_info_dict_list

        
def add_ids(feat_info_dict_list):
    #Create ids for each feature
    feature_id_list = create_id_list(len(feat_info_dict_list))
    for i in range(len(feat_info_dict_list)):
        feature_dict = feat_info_dict_list[i]
        feature_dict['feat_html_id'] = feature_id_list[i]
    return feat_info_dict_list



        

"""
Inputs:
    shade : (str) Either "bright" or "dark"
Outputs:
    color_str: (str) format 6 hex, e.g. #adef3e
"""
def get_random_color(shade):
    color = "#"
    if shade == "bright":
        for j in range(6):
            color += random.choice(["a","b","c","d","e","f"])
    elif shade == "dark":
        for j in range(6):
            color += random.choice([str(k) for k in range(10)])
    return color



"""
This function is designed to create a list of ids of length n.
Inputs:
    n (int)
Outputs:
    id_list: (list) list of IDs in format dldldl where d is a digit, and l is a letter.
"""
def create_id_list(n):
    id_list = []
    for i in range(n):
        new_id = create_new_id()
        while new_id in id_list:
            new_id = create_new_id()
        id_list.append(new_id)
    return id_list

def create_new_id():
        new_id = "{}{}{}{}{}{}".format(
                random.choice(string.ascii_letters),
                random.choice([str(k) for k in range(10)]),
                random.choice(string.ascii_letters),
                random.choice([str(k) for k in range(10)]),
                random.choice(string.ascii_letters),
                random.choice([str(k) for k in range(10)]))
        return new_id


def main():
    args = sys.ar



