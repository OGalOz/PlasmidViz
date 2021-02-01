#python3
"""
    gap_arc:
        line_width:
        line_color:
        start_angle
        end_angle
        angle:
        center_x:
        center_y:
        radius:

"""

import math
import logging

def print_plasmid_arc_forward(js_feat, num):


    js_str = "//Plasmid Arc Forward: {}\n".format(js_feat['feat_name'][0])

    arc_dict = {
            'const_name': js_feat['const_prefix'] + "_plasmid_arc_" + str(num),
            'svg_name' : js_feat['svg_name'],
            'final_id': js_feat['html_id'],
            'start_point': js_feat['start_point'],
            'end_point': js_feat['end_point'],
            'center_x': js_feat['center_x'],
            'center_y': js_feat['center_y'],
            'internal_color': js_feat['internal_color'],
            'line_width': js_feat['line_width'],
            'radius': js_feat['radius'],
            'arc_start': js_feat['arc_start'],
            'arc_end': js_feat['arc_end']
        }
    js_str += ut_arc(arc_dict)

    return js_str


def print_plasmid_arc_reverse(js_feat, num):
    js_str = "//Plasmid Arc Reverse: {}\n".format(js_feat['feat_name'][0])
    arc_dict = {
            'const_name': js_feat['const_prefix'] + "_reverse_arc_" + str(num),

            'svg_name' : js_feat['svg_name'],
            'final_id': js_feat['html_id'],
            'start_point': js_feat['start_point'],
            'end_point': js_feat['end_point'],

            'center_x': js_feat['center_x'],
            'center_y': js_feat['center_y'],
            'internal_color': js_feat['internal_color'],
            'line_width': js_feat['line_width'],
            'radius': js_feat['radius'],
            'arc_start': js_feat['arc_start'],
            'arc_end': js_feat['arc_end']
        }
    js_str += ut_arc(arc_dict)


    return js_str


def print_gap_arc(js_feat, num):

    js_str = "//Plasmid Gap Arc: {}\n".format(js_feat['feat_name'][0])

    arc_dict = {
            'const_name': js_feat['const_prefix'] + "_gap_arc_" + str(num),

            'svg_name' : js_feat['svg_name'],
            'final_id': js_feat['html_id'],
            'start_point': js_feat['start_point'],
            'end_point': js_feat['end_point'],

            'center_x': js_feat['center_x'],
            'center_y': js_feat['center_y'],
            'internal_color': js_feat['internal_color'],
            'line_width': js_feat['line_width'],
            'radius': js_feat['radius'],
            'arc_start': js_feat['arc_start'],
            'arc_end': js_feat['arc_end']
        }
    js_str += ut_arc(arc_dict)

    return js_str


def print_pointer_and_text(js_feat, num):

    text_dict = js_feat['text']
    pointer_dict = js_feat['pointer']
    text_rect_dict = js_feat['text_rect']
    js_str = "//Pointer and Text: {}\n".format(text_dict['text_str'])

    #Pointer
    js_str += "//\tPointer: \n"
    pointer_dict['const_name'] = js_feat['const_prefix'] + "_pointer_" + str(num)
    pointer_dict['svg_name'] = js_feat['svg_name']
    pointer_dict['final_id'] = pointer_dict['html_id']
    js_str += ut_line(pointer_dict)


    #Text Box
    js_str += "//\t Text-Box: {} \n".format(text_dict['text_str'])
    const_str = js_feat['const_prefix'] + "_text_rect_" + str(num)
    js_str += "const {} = {}.insert('rect', 'text')\n".format(const_str, 
            js_feat['svg_name'])
    js_str += ".attr('id', '{}')\n".format(text_rect_dict['html_id'])
    js_str += ".attr('x', '{}')\n".format(text_rect_dict["x"])
    js_str += ".attr('y', '{}')\n".format(text_rect_dict["y"])
    js_str += ".attr('width', '{}')\n".format(text_rect_dict["width"])
    js_str += ".attr('height', '{}')\n".format(text_rect_dict["height"])
    js_str += ".attr('stroke', '{}')\n".format(text_rect_dict['border_color'])
    on_click_str = ".on('click', () => [& \n" + \
        "let click_id = '{}';\n".format(text_rect_dict['html_id']) + \
        "pointer_text_selection(click_id)&])\n"
    on_click_str = on_click_str.replace('[&', '{').replace('&]', '}')
    js_str += on_click_str
    js_str += '.call(d3.drag().on("start", drag_started))\n'
    js_str += ".attr('fill', '{}');\n\n".format(text_rect_dict['internal_color'])

    #Text (after text box)

    js_str += "//\t Text: {} \n".format(text_dict['text_str'])
    txt_dict = {
            'const_name': js_feat['const_prefix'] + "_text_" + str(num),

            'svg_name' : js_feat['svg_name'],
        'final_id': text_dict['html_id'],
        'font_weight': text_dict["font_weight"],
        'font_size': text_dict["font_size"],
        'font_color': text_dict["fill_color"],
        'start_x': text_dict["text_point"][0],
        'start_y':  text_dict["text_point"][1],
        'text_str':  text_dict['text_str'],
        'text_rect_bool': True,
            }

    js_str += ut_text(txt_dict)

    return js_str




"""
Inputs:
        "type" : "center_text",
        "plasmid_name": plasmid_name_str,
        "name_start_x":(float) ,
        "name_start_y":(float) ,
        "length_str": plasmid_length_str,
        "length_start_x":(float) ,
        "length_start_y":(float) ,
        "font_style": (str) ,
        "fill_color": (str)
"""
def print_center_text(js_feat, num):

    js_str = "//Center Text: \n"
    ct_dict = {
        'const_name': js_feat['const_prefix'] + "_center_name",

        'svg_name' : js_feat['svg_name'],
        'final_id': js_feat['html_id']["name"],
        'font_weight': js_feat["font_weight"],
        'font_size': js_feat["font_size"],
        'font_color': js_feat["fill_color"],
        'start_x': js_feat["name_start_x"],
        'start_y': js_feat["name_start_y"],
        'text_str':  js_feat['plasmid_name'],

            }
    js_str += ut_text(ct_dict) 

    pl_dict = {
            'const_name': js_feat['const_prefix'] + "_center_length",
            
        'svg_name' : js_feat['svg_name'],
        'final_id': js_feat['html_id']['length'], 
        'font_weight': js_feat["font_weight"],
        'font_size': js_feat["font_size"],
        'font_color': js_feat["fill_color"],
        'start_x': js_feat["length_start_x"],
        'start_y': js_feat["length_start_y"],
        'text_str':  js_feat['length_str'],

            }

    js_str += ut_text(pl_dict)
    return js_str


def print_promoter(js_feat, num):
    js_str = "//Promoter Symbol: {} \n".format(js_feat['feat_name'][0])

    #Initial Line
    line_dict = {
        'const_name': js_feat['const_prefix'] + "_promoter_" + str(num) + \
        "_start_line",

        'svg_name' : js_feat['svg_name'],
        'final_id': js_feat['html_id'] + "-start-line",
        'start_point':  js_feat['p_line_coordinate_start'],
        'end_point': js_feat['arc_begin_point'],
        'line_color': js_feat["color"],
        'line_width': js_feat["line_width"]
            }
    js_str += ut_line(line_dict)

    #Arc
    arc_dict = {
            'const_name': js_feat['const_prefix'] + "_promoter_" + str(num) + \
            "arc",

            'svg_name' : js_feat['svg_name'],
            'final_id': js_feat['html_id'] + "-arc",
            'start_point': js_feat['arc_begin_point'],
            'end_point': js_feat['arc_end_point'],
            'center_x': js_feat['center_x'],
            'center_y': js_feat['center_y'],
            'internal_color': js_feat['color'],
            'line_width': js_feat['line_width'],
            'radius': js_feat['big_radius'],
            'arc_start': js_feat['arc_start_angle'],
            'arc_end': js_feat['arc_end_angle']

            }
    js_str += ut_arc(arc_dict)


    arrow_bool = js_feat['include_bool']
    
    if arrow_bool:
        #Arrow (Part 1)
        line_dict = {
            'const_name': js_feat['const_prefix'] + "_promoter_" + str(num) + \
                    "_arrow_1",

            'svg_name' : js_feat['svg_name'],
            'final_id': js_feat['html_id'] + "-arrow-1",
            'start_point':  js_feat['inner_flag_start'],
            'end_point': js_feat['flags_end'],
            'line_color': js_feat["color"],
            'line_width': js_feat["line_width"]
                }
        js_str += ut_line(line_dict)

        #Arrow (Part 2)
        line_dict = {
            'const_name': js_feat['const_prefix'] + "_promoter_" + str(num) + \
                    "_arrow_2",

            'svg_name' : js_feat['svg_name'],
            'final_id': js_feat['html_id'] + "-arrow-2",
            'start_point':  js_feat['outer_flag_start'],
            'end_point': js_feat['flags_end'],
            'line_color': js_feat["color"],
            'line_width': js_feat["line_width"]
                }
        js_str += ut_line(line_dict)

    return js_str



def print_terminator(js_feat, num):


    js_str = "//Terminator Symbol: {} \n".format(js_feat['feat_name'][0])

    #Setting variables:
    b_1 = js_feat['base_1']
    b_2 = js_feat['base_2']
    ap_1 = js_feat['armpit_1']
    ap_2 = js_feat['armpit_2']
    ph_1 = js_feat['palm_hand_1']
    ph_2 = js_feat['palm_hand_2']
    bh_1 = js_feat['back_hand_1']
    bh_2 = js_feat['back_hand_2']

    const_str =  js_feat['const_prefix'] + "_terminator_" + str(num)
    js_str += "const {} = {}.insert('polygon')\n".format(const_str, js_feat['svg_name'])
    js_str += ".attr('id', '{}')\n".format(js_feat['html_id'])
    js_str += ".attr('stroke', '{}')\n".format(js_feat['border_color'])
    js_str += ".attr('stroke-width', '{}')\n".format(js_feat['border_width'])
    js_str += ".attr('fill', '{}')\n".format(js_feat["internal_color"])
    
    points_str = "{},{} {},{} {},{}  \
    {},{} {},{} {},{} {},{} {},{}".format(
        str(b_1[0]),str(b_1[1]),str(ap_1[0]),str(ap_1[1]),
        str(ph_1[0]),str(ph_1[1]),str(bh_1[0]),str(bh_1[1]),
        str(bh_2[0]),str(bh_2[1]),str(ph_2[0]),str(ph_2[1]),
        str(ap_2[0]),str(ap_2[1]),str(b_2[0]),str(b_2[1]))
    js_str += ".attr('points', '{}');\n\n".format(points_str)

    return js_str


def print_rbs(js_feat, num):

    js_str = "//RBS Symbol: {} \n".format(js_feat['feat_name'][0])

    arc_dict= {
        'const_name': js_feat['const_prefix'] + "_rbs_border_" + str(num),

        'svg_name' : js_feat['svg_name'],
        'final_id': js_feat['html_id'] + "-border",
        'start_point': js_feat['start_point'],
        'end_point': js_feat['end_point'],
        'center_x': js_feat['circle_center'][0],
        'center_y': js_feat['circle_center'][1],
        'internal_color': js_feat['border_color'],
        'line_width': js_feat['border_width'],
        'radius': js_feat['radius'],
        'arc_start': js_feat['start_angle'],
        'arc_end': js_feat['end_angle']
    }
    #js_str += ut_arc(arc_dict)
    
    arc_dict['const_name'] = js_feat['const_prefix'] + "_rbs_border_" + str(num)
    arc_dict['final_id'] = js_feat['html_id'] + "-circle"
    arc_dict['radius'] = js_feat['radius'] - (arc_dict["line_width"]/2)
    arc_dict['internal_color'] = js_feat["internal_color"]
    #js_str += ut_arc(arc_dict)
    js_str += ut_semi_circle(arc_dict)

    return js_str
 


def print_cds(js_feat, num):
    js_str = "//CDS Symbol: {} \n".format(js_feat['feat_name'][0])

    a = js_feat["a"]
    b = js_feat["b"]
    c = js_feat["c"]
    d = js_feat["d"]
    e = js_feat["e"]
    f = js_feat["f"]

    #In triangle
    const_str = js_feat['const_prefix'] + "_cds_" + str(num) + "_in"
    js_str += "const {} = {}.insert('polygon')\n".format(const_str, js_feat['svg_name'])
    js_str += ".attr('id', '{}')\n".format(js_feat['html_id'] + "-in")
    js_str += ".attr('fill', '{}')\n".format(js_feat["internal_color"])
    points_str = "{},{} {},{} {},{} ".format(
        str(a[0]),str(a[1]),str(b[0]),str(b[1]),
        str(c[0]),str(c[1]))
    js_str += ".attr('points', '{}');\n\n".format(points_str)

    #Out Triangle
    const_str = js_feat['const_prefix'] + "_cds_" + str(num) + "_out"
    js_str += "const {} = {}.insert('polygon')\n".format(const_str, js_feat['svg_name'])
    js_str += ".attr('id', '{}')\n".format(js_feat['html_id'] + "-out")
    js_str += ".attr('fill', '{}')\n".format(js_feat["internal_color"])
    points_str = "{},{} {},{} {},{} ".format(
        str(d[0]),str(d[1]),str(e[0]),str(e[1]),
        str(f[0]),str(f[1]))
    js_str += ".attr('points', '{}');\n\n".format(points_str)

    return js_str


def print_delete_box(js_feat):

    
    js_str = "// Delete-Box: \n"
    const_str =  js_feat['const_prefix'] + "_delete_box"
    js_str += "const {} = {}.insert('image')\n".format(const_str, js_feat['svg_name'])
    js_str += ".attr('id', '{}')\n".format(js_feat['html_id'])
    js_str += ".attr('x', '{}')\n".format(js_feat["x"])
    js_str += ".attr('y', '{}')\n".format(js_feat["y"])
    js_str += ".attr('width', '{}')\n".format(js_feat["width"])
    js_str += ".attr('height', '{}')\n".format(js_feat["height"])
    js_str += ".attr('xlink:href', '{}')".format(js_feat['img_link'])
    on_click_str = ".on('click', () => [& \n delete_all_selected();\n&]);\n" 
    on_click_str = on_click_str.replace('[&', '{').replace('&]','}')
    js_str += on_click_str

    return js_str

def print_reset_box(js_feat):

    
    js_str = "// Reset-Box: \n"
    include_reset_bool = js_feat['include_bool']
    if include_reset_bool:
        const_str = js_feat['const_prefix'] + "_reset_box"
        js_str += "const {} = {}.insert('image')\n".format(const_str, js_feat['svg_name'])
        js_str += ".attr('id', '{}')\n".format(js_feat['html_id'])
        js_str += ".attr('x', '{}')\n".format(js_feat["x"])
        js_str += ".attr('y', '{}')\n".format(js_feat["y"])
        js_str += ".attr('width', '{}')\n".format(js_feat["width"])
        js_str += ".attr('height', '{}')\n".format(js_feat["height"])
        js_str += ".attr('stroke', '{}')\n".format(js_feat['border_color'])
        js_str += ".attr('xlink:href', '{}')".format(js_feat['img_link'])
        on_click_str = ".on('click', () => [& \n reset_all_deleted_features();\n&]);\n" 
        on_click_str = on_click_str.replace('[&', '{').replace('&]','}')
        js_str += on_click_str

    return js_str

def print_legend_box(js_feat):

    js_str = "// Color Legend -Box: \n"
    include_legend_bool = js_feat['include_bool']

    if include_legend_bool:

        #First we create the entire rectangle
        js_feat["const_name"] = js_feat["const_prefix"] + "_legend_box"
        js_feat["html_id"] = js_feat["html_id"] + "-main-box"
        js_str += ut_box(js_feat)

        # Then we create the title row
        # first the box
        js_str += "//TITLE ROW  \n"
        title_row = js_feat["title_row_dict"]
        title_row["const_name"] = js_feat["const_prefix"] + "_legend_title_box"
        title_row["svg_name"] = js_feat["svg_name"]
        title_row["html_id"] = js_feat["html_id"] + "-title-box"
        js_str += ut_box(title_row)
        # then the text
        js_str += "//TITLE TEXT \n"
        title_text_dict = title_row
        title_text_dict["const_name"] = js_feat["const_prefix"] + "_legend_title_txt"
        title_text_dict["final_id"] = js_feat["html_id"] + "-title-text"
        title_text_dict["start_x"] = title_text_dict["x"] + 2
        title_text_dict["start_y"] = title_text_dict["y"] + 15
        title_text_dict['font_weight'] = js_feat["title_font_weight"]
        title_text_dict['font_size'] = js_feat["title_font_size"]
        title_text_dict['font_color'] = js_feat["title_font_color"]
        title_text_dict['text_str'] = js_feat['title_text']
        title_text_dict['text_rect_bool'] = False
        js_str += ut_text(title_text_dict) 

        # Then we create the rest of the rows, printing left rectangle first,
        # then text, then right rectangle
        js_str += "//LEGEND ROWS: \n"
        row_info_list = js_feat['row_info_list']
        for j in range(len(row_info_list)):
            row_info_dict = row_info_list[j]
            # first the left box
            js_str += "// LEFT BOX {}\n".format(j)
            left_box = row_info_dict["left_box"]
            left_box['const_name'] = js_feat["const_prefix"] + "_lb_" + str(j)
            left_box['svg_name'] = js_feat['svg_name']
            left_box['html_id'] = js_feat["html_id"] + "-lb-" + str(j)
            left_box['border_color'] = "black"
            left_box['internal_color'] = "white"
            js_str += ut_box(left_box)

            #Then to the text in the left box
            js_str += "// LEFT BOX TEXT {}\n".format(j)
            left_box['const_name'] = js_feat["const_prefix"] + "_lbtxt_" + str(j)
            left_box['final_id'] = js_feat["html_id"] + "-lbtxt-" + str(j)
            left_box["start_x"] = left_box["x"] + 2
            left_box["start_y"] = left_box["y"] + 15
            left_box['font_weight'] = js_feat["row_font_weight"]
            left_box['font_size'] = js_feat["row_font_size"]
            left_box['font_color'] = js_feat["row_font_color"]
            left_box['text_str'] = left_box['text']
            left_box['text_rect_bool'] = False
            js_str += ut_text(left_box) 

            #Now right box

            js_str += "// RIGHT BOX {}\n".format(j)
            right_box = row_info_dict["right_box"]
            right_box['const_name'] = js_feat["const_prefix"] + "_rb_" + str(j)
            right_box['svg_name'] = js_feat['svg_name']
            right_box['html_id'] = js_feat["html_id"] + "-rb-" + str(j)
            right_box['border_color'] = "black"
            js_str += ut_box(right_box)

        return js_str


#UTILITY FUNCTIONS:
"""
Inputs:
    inp_dict needs:
        const_name: (str)
        svg_name: (str)
        final_id: (str)
        font_weight:
        font_size:
        font_color:
        start_x:
        start_y:
        text_str:
        text_rect_bool:
"""
def ut_text(inp_dict):

    js_str = "const {} = {}.append('text')\n".format(inp_dict['const_name'],
            inp_dict['svg_name'])
    js_str += ".attr('id', '{}')\n".format(inp_dict['final_id'])
    js_str += ".attr('font-weight', '{}')\n".format(inp_dict["font_weight"])
    js_str += ".attr('font-size', '{}')".format(inp_dict['font_size'])
    js_str += ".attr('x', '{}')\n".format(inp_dict["start_x"])
    js_str += ".attr('y', '{}')\n".format(inp_dict["start_y"])
    
    if "text_rect_bool" in inp_dict.keys():
        if inp_dict["text_rect_bool"] == True:
            on_click_str = ".on('click', () => [& \n" + \
                "let click_id = '{}';\n".format(inp_dict['final_id']) + \
                "pointer_text_selection(click_id)&])\n"
            on_click_str = on_click_str.replace('[&', '{').replace('&]', '}')
            js_str += on_click_str


    
    logging.warning("TEXT STRING: {}".format(inp_dict['text_str']))
    logging.warning(inp_dict)
    js_str += ".text('{}');\n\n".format(inp_dict['text_str'])
    logging.warning(js_str)
    return js_str



"""
Inputs:
    inp_dict needs:
        const_name: (str)
        final_id: (str)
        start_point: list<(float)>
        end_point: list<(float)>
        line_color: (str)
        line_width: (float)
"""
def ut_line(inp_dict):
    js_str = "const {} = {}.append('line')\n".format(inp_dict['const_name'],
            inp_dict['svg_name'])
    js_str += ".attr('id', '{}')\n".format(inp_dict['final_id'])
    js_str += ".attr('x1', '{}')\n".format(inp_dict["start_point"][0])
    js_str += ".attr('y1', '{}')\n".format(inp_dict["start_point"][1])
    js_str += ".attr('x2', '{}')\n".format(inp_dict["end_point"][0])
    js_str += ".attr('y2', '{}')\n".format(inp_dict["end_point"][1])
    js_str += ".attr('stroke', '{}')\n".format(inp_dict['line_color'])
    if "pointer" in inp_dict['final_id']:
        on_click_str = ".on('click', () => [& \n" + \
        "let click_id = '{}';\n".format(inp_dict['final_id']) + \
        "pointer_text_selection(click_id)&])\n".format(
            inp_dict['const_name'])
        on_click_str = on_click_str.replace('[&', '{').replace('&]','}')
        js_str += on_click_str
    js_str += ".attr('stroke-width', '{}');\n\n".format(inp_dict['line_width'])

    return js_str



"""
Inputs:
    inp_dict needs:
        const_name: (str)
        start_point: list<float>
        end_point: list<float>
        final_id: (str)
        center_x: (float)
        center_y: (float)
        internal_color: (str)
        line_width: (float)
        radius:
        arc_start: (float)
        arc_end: (float)
"""
def ut_arc(inp_dict):
    js_str = "const {} = {}.append('path')\n".format(inp_dict['const_name'],inp_dict['svg_name'])
    js_str += ".attr('id', '{}')\n".format(inp_dict['final_id'])
    js_str += ".attr('transform', 'translate({},{})')\n".format(
            inp_dict['center_x'], inp_dict['center_y'])
    js_str += ".attr('fill', '{}')\n".format(inp_dict['internal_color'])
    js_str += ".attr('stroke-width', '{}')\n".format(inp_dict['line_width'])

    """
    arc_text = "M {} {} ".format(
           inp_dict["start_point"][0],
           inp_dict["start_point"][1]
            )
    arc_text += "A {} {} {} {} {} {} {} ".format(
            str(inp_dict["radius"]),
            str(inp_dict["radius"]),
            "0",
            "0",
            "0",
            str(inp_dict["end_point"][0]),
            str(inp_dict["end_point"][1])
            )
    """


    js_str += ".attr('d', d3.arc() ({\n"
    js_str += "innerRadius: '{}',\n".format(str(inp_dict['radius'] - (inp_dict['line_width'])/2))
    js_str += "outerRadius: '{}',\n".format(str(inp_dict['radius'] + (inp_dict['line_width'])/2))
    js_str += "startAngle: {},\n".format(str(inp_dict['arc_start']))
    js_str += "endAngle: {},\n".format(str(inp_dict['arc_end'] - 0.01))
    js_str += "}));\n\n"


    return js_str





"""
Inputs:
    inp_dict needs:
        const_name: (str)
        start_point: list<float>
        end_point: list<float>
        final_id: (str)
        center_x: (float)
        center_y: (float)
        internal_color: (str)
        line_width: (float)
        radius:
        arc_start: (float)
        arc_end: (float)
"""
def ut_arc_line(inp_dict):
    js_str = "const {} = {}.append('path')\n".format(inp_dict['const_name'],inp_dict['svg_name'])
    js_str += ".attr('id', '{}')\n".format(inp_dict['final_id'])
    js_str += ".attr('transform', 'translate({},{})')\n".format(
            inp_dict['center_x'], inp_dict['center_y'])
    js_str += ".attr('fill', '{}')\n".format(inp_dict['internal_color'])
    js_str += ".attr('stroke-width', '{}')\n".format(inp_dict['line_width'])

    arc_text = "M {} {} ".format(
           inp_dict["start_point"][0],
           inp_dict["start_point"][1]
            )
    arc_text += "A {} {} {} {} {} {} {} ".format(
            str(inp_dict["radius"]),
            str(inp_dict["radius"]),
            "0",
            "0",
            "0",
            str(inp_dict["end_point"][0]),
            str(inp_dict["end_point"][1])
            )


    js_str += ".attr('d','{}');\n".format(arc_text)

    """
    js_str += "innerRadius: '{}',\n".format(str(inp_dict['radius'] - (inp_dict['line_width'])/2))
    js_str += "outerRadius: '{}',\n".format(str(inp_dict['radius'] + (inp_dict['line_width'])/2))
    js_str += "startAngle: {},\n".format(str(inp_dict['arc_start']))
    js_str += "endAngle: {},\n".format(str(inp_dict['arc_end'] - 0.01))
    js_str += "}));\n\n"
    """


    return js_str

"""
Inputs:
    inp_dict needs:
        start_point: list<float>
        end_point: list<float>
        const_name: (str)
        final_id: (str)
        center_x: (float)
        center_y: (float)
        internal_color: (str)
        line_width: (float)
        radius:
        arc_start: (float)
        arc_end: (float)
"""

def ut_semi_circle(inp_dict):
    js_str = "const {} = {}.append('path')\n".format(inp_dict['const_name'],inp_dict['svg_name'])
    js_str += ".attr('id', '{}')\n".format(inp_dict['final_id'])
    #js_str += ".attr('transform', 'translate({},{})')\n".format(
    #        inp_dict['center_x'], inp_dict['center_y'])
    js_str += ".attr('fill', '{}')\n".format(inp_dict['internal_color'])

    arc_text = "M {} {} ".format(
           inp_dict["start_point"][0],
           inp_dict["start_point"][1]
            )
    arc_text += "A {} {} {} {} {} {} {} ".format(
            str(inp_dict['radius'] - .5),
            str(inp_dict['radius'] - .5),
            "0",
            "0",
            "0",
            str(inp_dict["end_point"][0]),
            str(inp_dict["end_point"][1])
            )
    js_str += ".attr('d','{}');\n\n".format(arc_text)

    return js_str


"""
const_name: (str) Name of constant
svg_name: (str) Name of related svg object
x:
y:
width:
height:
border_color:
html_id:
internal_color:
"""
def ut_box(inp_dict):
    #Text Box
    js_str = "const {} = {}.insert('rect', 'text')\n".format(inp_dict['const_name'],
            inp_dict['svg_name'])

            
    js_str += ".attr('id', '{}')\n".format(inp_dict['html_id'])
    js_str += ".attr('x', '{}')\n".format(inp_dict["x"])
    js_str += ".attr('y', '{}')\n".format(inp_dict["y"])
    js_str += ".attr('width', '{}')\n".format(inp_dict["width"])
    js_str += ".attr('height', '{}')\n".format(inp_dict["height"])
    js_str += ".attr('stroke', '{}')\n".format(inp_dict['border_color'])

    """
    on_click_str = ".on('click', () => [& \n" + \
        "let click_id = '{}';\n".format(inp_dict['html_id']) + \
        "pointer_text_selection(click_id)&])\n"
    on_click_str = on_click_str.replace('[&', '{').replace('&]', '}')
    js_str += on_click_str
    js_str += '.call(d3.drag().on("start", drag_started))\n'
    """
    js_str += ".attr('fill', '{}');\n\n".format(inp_dict['internal_color'])

    return js_str

