#python3



from Bio import SeqIO
import json
import math
from calculate_feats import *




"""
Inputs:
    feature_list_fp: (str) file path to feature list json file.
    plasmid_info_fp: (str) file path to plasmid info json file.
    config_fp: (str) file path to config info json file
"""
def js_prepare(feature_list_fp, plasmid_info_fp, config_fp,
        js_feats_fp, uniq_dict=None):
    with open(feature_list_fp, "r") as f:
        feature_dict_list = json.loads(f.read())

    with open(plasmid_info_fp, "r") as f:
        plasmid_info = json.loads(f.read())

    with open(config_fp, "r") as f:
        config_dict = json.loads(f.read())


    javascript_object_list = create_javascript_object_list(feature_dict_list,
            plasmid_info, config_dict, uniq_dict)

    '''
    javascript_object_list = update_javascript_object_list(
            javascript_object_list, uniq_dict)
    '''

    with open(js_feats_fp, "w") as f:
        f.write(json.dumps(javascript_object_list, indent=2, sort_keys=True))
    

    return 0 


def create_javascript_object_list(feature_dict_list, plasmid_info, config_dict,
        uniq_dict):
   
    javascript_object_list = []
    types_dict = config_dict["genbank_info"]["types_dict"]

    for feature_dict in feature_dict_list:
        arc_object = create_arc(feature_dict, config_dict)
        javascript_object_list.append(arc_object)

        feat_type = feature_dict['feat_type']
        if feat_type != "feature_gap":
            pointer_and_text_object = calculate_pointer_and_text(feature_dict, 
                config_dict)
            javascript_object_list.append(pointer_and_text_object)

        
        #Note, all the functions that begin with "calculate"
        # come from plasmid_sbol_visuals
        if feat_type in types_dict["promoter"]:
            javascript_object_list.append(calculate_promoter_feature(feature_dict, config_dict))
        elif feat_type in types_dict["terminator"]:
            javascript_object_list.append(calculate_terminator_feature(feature_dict, config_dict))
        elif feat_type in types_dict["rbs"]:
            javascript_object_list.append(calculate_rbs_feature(feature_dict, config_dict))
        elif feat_type in types_dict["cds"]:
            javascript_object_list.append(calculate_cds_feature(feature_dict, config_dict))
        elif feat_type in types_dict["scar"]:
            pass
        elif feat_type in types_dict["ribozyme"]:
            pass
        elif feat_type in types_dict["backbone"]:
            pass
        elif feat_type in types_dict["misc_feature"]:
            pass
        else:
            logging.critical("Did not recognize type of feature: \
                    {}".format(feat_type))

    """
    plasmid_name_object = create_center_text(plasmid_info, config_dict, 
            uniq_dict)
    javascript_object_list.append(plasmid_name_object)

    #Creating delete box
    user_delete_box = create_delete_box(config_dict, uniq_dict)
    javascript_object_list.append(user_delete_box)

    #Creating reset box
    user_reset_box = create_reset_box(config_dict, uniq_dict)
    javascript_object_list.append(user_reset_box)

    #Creating color legend box
    color_legend_box = create_color_legend_box(config_dict, uniq_dict)
    javascript_object_list.append(color_legend_box)
    """

    return javascript_object_list

def create_arc(feature_dict, config_dict):
    
    feat_type = feature_dict['feat_type']
    if feat_type not in config_dict["genbank_info"]["gap_names"]:
        #Regular arc
        if feature_dict['feat_strand'] == 1:
            #Positive arc
            cx = config_dict['js_info']['center_coordinates'][0]
            cy = config_dict['js_info']['center_coordinates'][1]
            start_point = calculate_position(cx,cy,config_dict['js_info']['circle_radius'], 
                    feature_dict['angle_start'])
            end_point = calculate_position(cx,cy,config_dict['js_info']['circle_radius'], 
                    feature_dict['angle_end'])

            js_object = {
                    "type": "plasmid_arc_forward",
                    "html_id": feature_dict['feat_html_id'] + "-arc",
                    "start_point": start_point,
                    "end_point": end_point,
                    "feat_name": feature_dict['feat_name'],
                    "arc_start": feature_dict['angle_start'],
                    "arc_end": feature_dict['angle_end'],
                    "arc_angle":feature_dict['angle_end'] - feature_dict['angle_start'],
                    "line_width": config_dict['js_info']['circle_line_width'],
                    "internal_color":feature_dict['feat_color'],
                    "center_x":cx,
                    "center_y":cy,
                    "radius": config_dict['js_info']['circle_radius']
            }


        else:
            #Complementary arc
            cx = config_dict['js_info']['center_coordinates'][0]
            cy = config_dict['js_info']['center_coordinates'][1]
            start_point = calculate_position(cx,cy,config_dict['js_info']['circle_radius'], 
                    feature_dict['angle_start'])
            end_point = calculate_position(cx,cy,config_dict['js_info']['circle_radius'], 
                    feature_dict['angle_end'])

            js_object = {
                    "type": "plasmid_arc_reverse",
                    "start_point": start_point,
                    "end_point": end_point,
                    "html_id": feature_dict['feat_html_id'] + "-arc",
                    "feat_name": feature_dict['feat_name'],
                    "arc_start": feature_dict['angle_start'],
                    "arc_end": feature_dict['angle_end'],
                    "arc_angle":feature_dict['angle_end'] - feature_dict['angle_start'],
                    "line_width": config_dict['js_info']['circle_line_width'],
                    "internal_color":feature_dict['feat_color'],
                    "center_x":cx,
                    "center_y": cy,
                    "radius": config_dict['js_info']['complementary_radius']
            }

    else:
        #gap arc
        cx = config_dict['js_info']['center_coordinates'][0]
        cy = config_dict['js_info']['center_coordinates'][1]
        start_point = calculate_position(cx,cy,config_dict['js_info']['circle_radius'], 
                feature_dict['angle_start'])
        end_point = calculate_position(cx,cy,config_dict['js_info']['circle_radius'], 
                feature_dict['angle_end'])

        js_object = {
                    "type": "gap_arc",
                    "start_point": start_point,
                    "end_point": end_point,
                    "html_id": feature_dict['feat_html_id'] + "-gap",
                    "feat_name": feature_dict['feat_name'],
                    "arc_start": feature_dict['angle_start'],
                    "arc_end": feature_dict['angle_end'],
                    "arc_angle":feature_dict['angle_end'] - feature_dict['angle_start'],
                    "line_width": config_dict['js_info']['gap_arc_info']['circle_line_width'],
                    "internal_color": config_dict['js_info']['gap_arc_info']['color'],

                    "center_x":cx,
                    "center_y":cy,
                    "radius": config_dict['js_info']['circle_radius']
            }

    return js_object


def create_center_text(plasmid_info, config_dict, uniq_dict):

    js_info = config_dict['js_info']
    plasmid_name_str = plasmid_info['plasmid_name']
    cc = js_info['center_coordinates']

    if "max_title_length" in js_info:
        max_t_len = js_info["max_title_length"]
    else:
        max_t_len = 45
    if len(plasmid_name_str) > max_t_len:
        logging.critical("Plasmid name is too long - using placeholder name: 'Plasmid'")
        plasmid_name_str = "Plasmid"

    #We add the text box with the name, calculating center of the word to be center of circle,
    # and each letter has length 12 pixels
    plasmid_name_length = len(plasmid_name_str)*15
    plasmid_name_start = cc[0] - float(plasmid_name_length)/1.5

    #Getting length of plasmid and placing it under plasmid name
    plasmid_length_str = str(plasmid_info['plasmid_length']) + " bp"
    if len(plasmid_length_str) > 13:
        logging.warning("Plasmid string length is over ten digits.")
        plasmid_length = '? bp'

    #We add the text box with the length, 20 to the left of center, and 20 below
    plasmid_length_str_len = len(plasmid_length_str)*15
    plasmid_length_str_start = cc[0] - float(plasmid_length_str_len)/1.5

    font_weight = "bold"
    font_size = "{}pt".format(str(js_info['title_text_size']))
    font_family = "Calibri"

    center_text_obj = {
        "type" : "center_text",
        "html_id": { "name": "plasmid-center-text-name-{}".format(
            uniq_dict['file_num']),
        "length": "plasmid-center-text-length-{}".format(uniq_dict['file_num'])
            },
        "plasmid_name": plasmid_name_str,
        "name_start_x": plasmid_name_start,
        "name_start_y": cc[1] - 17,
        "length_str": plasmid_length_str,
        "length_start_x": plasmid_length_str_start,
        "length_start_y": cc[1] + 17,
        "font_weight" : font_weight,
        "font_size": font_size,
        "font_family": font_family,
        "fill_color": js_info["title_text_color"]
    }


    return center_text_obj 


def create_delete_box(config_dict, uniq_dict):
    delete_box_object = {"type": "delete_box"}
    delete_box_object["html_id"] = "delete-box-{}".format(uniq_dict['file_num'])
    db_info = config_dict["js_info"]["delete_box_info"]
    delete_box_object["x"] = db_info["top_left_corner_x"]
    delete_box_object["y"] = db_info["top_left_corner_y"]
    delete_box_object["width"] = db_info["width"]
    delete_box_object["height"] = db_info["height"]
    delete_box_object["internal_color"] = db_info["internal_color"]
    delete_box_object["border_color"] = db_info["border_color"]
    delete_box_object["img_link"] = db_info["img_link"]

    return delete_box_object

def create_reset_box(config_dict, uniq_dict):
    reset_box_object = {"type": "reset_box"}
    reset_box_object["html_id"] = "reset-box-{}".format(uniq_dict['file_num'])
    rb_info = config_dict["js_info"]["reset_box_info"]
    reset_box_object["x"] = rb_info["top_left_corner_x"]
    reset_box_object["y"] = rb_info["top_left_corner_y"]
    reset_box_object["width"] = rb_info["width"]
    reset_box_object["height"] = rb_info["height"]
    reset_box_object["internal_color"] = rb_info["internal_color"]
    reset_box_object["border_color"] = rb_info["border_color"]
    reset_box_object["img_link"] = rb_info["img_link"]
    reset_box_object['include_bool'] = rb_info['include_bool']

    return reset_box_object


def create_color_legend_box(config_dict, uniq_dict):

    legend_box_object = {"type": "legend_box"}
    legend_box_object["html_id"] = "legend-box-{}".format(uniq_dict['file_num'])
    lb_info = config_dict["js_info"]["legend_box_info"]
    legend_box_object['include_bool'] = lb_info['include_bool']
    legend_box_object["x"] = lb_info["top_left_corner_x"]
    legend_box_object["y"] = lb_info["top_left_corner_y"]
    legend_box_object["width"] = lb_info["width"]
    legend_box_object["height"] = lb_info["height"]
    text_box_width = lb_info["text_box_width"]
    color_box_width = lb_info["color_box_width"]
    legend_box_object["row_font_weight"] = lb_info["row_font_weight"]
    legend_box_object["row_font_size"] = lb_info["row_font_size"]
    legend_box_object["row_font_color"] = lb_info["row_font_color"]
    legend_box_object["title_font_weight"] = lb_info["title_font_weight"]
    legend_box_object["title_font_size"] = lb_info["title_font_size"]
    legend_box_object["title_font_color"] = lb_info["title_font_color"]
    legend_box_object["border_color"] = lb_info["border_color"]
    legend_box_object["title_text"] = lb_info["title_text"]
    legend_box_object["internal_color"] = lb_info["internal_color"]
    colors_dict = config_dict["genbank_info"]["colors_dict"]
    #The number of rows is number of features and colors plus title (1)
    num_rows = len(colors_dict.keys()) + 1
    row_height = lb_info['height']/num_rows
    title_row_dict = {
            "x" : lb_info["top_left_corner_x"] + 1,
            "y" : lb_info["top_left_corner_y"] + 1,
            "width": lb_info["width"],
            "height" : row_height,
            "text": lb_info["title_text"],
            "internal_color": "white",
            "border_color": "black"
            }
    legend_box_object["title_row_dict"] = title_row_dict

    row_info_list = []
    color_keys = list(colors_dict.keys())
    for i in range(len(color_keys)):
        new_row_dict = {
                "left_box": {
            "x" : lb_info["top_left_corner_x"],
            "y" : lb_info["top_left_corner_y"] + row_height*(i+1),
            "width": lb_info["text_box_width"],
            "height": row_height,
            "text": color_keys[i]
            },
                "right_box": {
            "x": lb_info["top_left_corner_x"] + lb_info["text_box_width"],
            "y" : lb_info["top_left_corner_y"] + row_height*(i+1),
            "width": lb_info["color_box_width"],
            "height": row_height,
            "internal_color": colors_dict[color_keys[i]]
                    }
                }
        row_info_list.append(new_row_dict)
    legend_box_object["row_info_list"] = row_info_list

    return legend_box_object


def update_javascript_object_list(javascript_object_list, uniq_dict):

    #We add the uniq prefix to every object in this list.
    for obj in javascript_object_list:
        obj['const_prefix'] = uniq_dict["uniq_id"]
        obj['svg_name'] = uniq_dict['svg_name']

    return javascript_object_list
