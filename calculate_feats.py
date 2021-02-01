#python
'''
File divided into used functions, and functions not in use.
Consider: https://sbolstandard.org/wp-content/uploads/2017/04/SBOL-Visual-2.1.pdf
'''


import math
import logging



"""
Inputs:
    a: (list) [x,y]
    b: (list) [x,y]
Function must be true
"""
def calc_dist(a,b):
    return math.sqrt( (a[0]-b[0])**2 + (a[1] - b[1])**2 )


"""
Inputs:
    cx: (float) center position (x)
    cy: (float) center position (y)
    radius: (float)
    angle: (float)
"""
def calculate_position(cx, cy, radius, angle):
    return [cx + radius*(math.cos(-1*(angle - math.pi/2))),
        cy - radius*(math.sin(-1*(angle - math.pi/2)))]


"""
Angles are always kept in regular Cartesian 
Inputs: 
    circle_coordinates: (list) floats [x,y] for a point on the circle.
    center_coordinates: (list) floats [x,y] for the center of the circle.
Output:
    theta: (float) The angle to the point

"""
def get_angle_from_point(circle_coordinates ,center_coordinates):

    logging.warning("circle coordinates: {} {}".format(str(circle_coordinates[0]),
        str(circle_coordinates[1])))
   
    d_y = -1*(circle_coordinates[1] - center_coordinates[1])
    d_x = circle_coordinates[0] - center_coordinates[0]
    logging.warning("d_y: {}".format(str(d_y)))
    logging.warning("d_x: {}".format(str(d_x)))
    #We apply a transformation on the angle to keep it consistent
    theta = (-1*(math.atan2(d_y, d_x) - math.pi/2))
    logging.warning("theta: {}".format(str(theta)))

    return theta

"""
Inputs:
    A: (list) list of floats [x,y] starting point.
    B: (list) list of floats [a,b] ending point.
Outputs:
    slope: (float) represents slope from A to B.
Tested
"""
def calculate_slope(A,B):

    logging.debug("Calculating Slope: ")
    logging.debug("Start Point: ({},{})".format(A[0], A[1]))
    logging.debug("End Point: ({},{})".format(B[0], B[1]))

    if B[0] >= A[0]:
        rise = -1*(B[1] - A[1])
        run = B[0] - A[0]
    else: #B[0] < A[0]
        rise = -1*(A[1] - B[1])
        run = A[0] - B[0]
    if run == 0:
        if rise == 0:
            raise Exception("A = B, cannot calculate slope")
        run = 0.000001
    slope = rise/run
    logging.debug("Slope: {}".format(str(slope)))
    return slope



"""
Inputs:
    A: (list) list of floats [x,y] starting point.
    B: (list) list of floats [a,b] ending point (add extension to these coordinates).
    prcnt_pixel_indicator: (str) limited vocab to "prcnt" or "pixels"
    prcnt: (float) -1.0<p<1.0 [necessary if no pixels] A float representing the percent increase/decrease in length you want in the line.
    pixels: (int) [necessary if no pixels] An integer representing increase/decrease in length in pixels if wanted.
Outputs:
    ext_c: (list) A list of floats [c,d] representing an extension of the line
"""
def line_extension_coordinates(A,B,prcnt_pixel_indicator, prcnt_or_pixels_value):

    #Getting change_length (amount change in pixels)
    if prcnt_pixel_indicator == "prcnt":
        prcnt = prcnt_or_pixels_value
        if prcnt > 1.0 or prcnt < -1.0:
            raise Exception("Percent must be decimal point between -1 and 1")
        line_length = math.sqrt(((A[0] - B[0])**2) + ((A[1] - B[1])**2))
        change_length = prcnt * (line_length)
    elif prcnt_pixel_indicator == "pixels":
        pixels = prcnt_or_pixels_value
        if abs(pixels) > 600:
            raise ValueError("pixel change must be less than 600")
        change_length = pixels
    else:
        raise Exception("Did not recognize prcnt_pixel_indicator, must be one of prcnt or pixels")

    slope = calculate_slope(A,B)


    if B[0] >= A[0]:
        if change_length >= 0:
            d_x = (change_length/math.sqrt(1+(slope**2)))
            d_y = slope * d_x
            ext_c = [B[0] + d_x, B[1] - d_y]
        else: #change_length < 0:
            change_length = -1 * change_length
            d_x = (change_length/math.sqrt(1+(slope**2)))
            d_y = slope * d_x
            ext_c = [B[0] - d_x, B[1] + d_y]
    else: #B[0] < A[0]
        if change_length >= 0:
            d_x = (change_length/math.sqrt(1+(slope**2)))
            d_y = slope * d_x
            ext_c = [B[0] - d_x, B[1] + d_y]
        else: #change_length < 0:
            d_x = (change_length/math.sqrt(1+(slope**2)))
            d_y = slope * d_x
            ext_c = [B[0] + d_x, B[1] - d_y]
    return ext_c






"""
Inputs:
    A: (list) coordinates of a point in the canvas [x,y] (Would normally be the center)
    B: (list) coordinates of a point in the canvas [x,y] (Would normally be the outer point on a circle)
Outputs:
    p_slope: (float) The perpendicular slope

"""
def get_perpendicular_slope(A,B):
    slope = calculate_slope(A,B)
    logging.debug("original slope: {}".format(str(slope)))
    if slope != 0:
        p_slope = (-1/slope)
        return p_slope
    else:
        if A[0] < B[0]:
            return -10000
        elif B[0] < A[0]:
            return 10000
        else:
            raise Exception("A = B, cannot calculate slope")


    


"""
Inputs:
    point: (list) [x,y] location of point in the plane.
    angle: (float) Angle in radians to shift point.
Outputs:
    rotated_point: (list) [x,y] location of rotated point in the plane.
"""
def perform_rotation(point, angle):
    x_coordinate = (math.cos(angle)*point[0]) - (math.sin(angle)*point[1])
    y_coordinate = (math.sin(angle)*point[0]) + (math.cos(angle)*point[1])
    return [x_coordinate, y_coordinate]
    

"""
Inputs:
    center_point: (list) A list of coordinates for the point from which we calculate the distances.
    slope: (float) The rise over run of the line on which we're returning the points.
    pixels: (float) The distance from the center_point in the direction of the slope.

Outputs:
    points_dict: (dict)
        with_slope_point: (list) Coordinates for the point that goes in the direction of the slope.
        against_slope_point: (list) Coordinates for the point that goes against the direction of the slope.
"""
def get_points_in_both_directions_from_center_with_slope(center_point, slope, pixels):
    
    dx = pixels/(math.sqrt(1+slope**2))
    dy = dx*slope
    with_slope_point = [center_point[0] + dx, center_point[1] - dy]
    against_slope_point = [center_point[0] - dx, center_point[1] + dy]    

    points_dict = {
            "with_slope_point": with_slope_point,
            "against_slope_point": against_slope_point
            }

    return points_dict


"""
Inputs:
    feature_dict: (dict from feature_list.json)
    config_dict: (dict from config.json)
Output:
    js_object:
        type: (str) pointer_and_text
        pointer:
            type: (str) "pointer"
            new_line_width_bool: (bool)
            line_width: (int)
            line_color: (str)
            start_point: list<int>
            end_point: list<int>
        text:
            text_point: list<int>
            text_str: (str)
            new_text_font_bool: bool
            text_font: (str)

"""
def calculate_pointer_and_text(feature_dict, config_dict):

    
    js_info = config_dict["js_info"]

    js_object = {"type": "pointer_and_text"}
    pointer_dict = {"type": "pointer"}
    pointer_dict['html_id'] = feature_dict['feat_html_id'] + "-pointer"
    pointer_dict['new_line_width_bool'] = False
    pointer_dict['line_width'] = js_info['pointer_thick']
    pointer_dict['line_color'] = js_info['pointer_color']
    end_point = feature_dict["point_mid"]
    pointer_dict['end_point'] = end_point

    line_length = js_info["pointer_len_" + feature_dict["feat_pointer_len"]]

    if feature_dict["feat_pointer_direction"] == "out":
        start_key = "with_slope_point"
    else:
        start_key = "against_slope_point"

    points_options = get_points_in_both_directions_from_center_with_slope(
            end_point, 
            calculate_slope(js_info['center_coordinates'], end_point), 
            line_length)
    start_point = points_options[start_key]
    pointer_dict["start_point"] = start_point
    js_object["pointer"] = pointer_dict

    
    #Making text
    text_coords = line_extension_coordinates(end_point, start_point, 
            "pixels", js_info["pointer_distance"])
    text_dict = {"type": "text"}
    text_dict['html_id'] = feature_dict['feat_html_id'] + "-text"
    text_dict["text_point"] = [text_coords[0] , text_coords[1]]
    text_dict["text_str"] = feature_dict["feat_name"][0] 
    text_dict["new_text_font_bool"] = False
    text_dict["text_font"] = str(js_info["text_size"]) + "pt Calibri"
    text_dict["font_size"] = str(js_info["text_size"])
    text_dict["fill_color"] = js_info["text_color"]
    text_dict["font_weight"] = "normal"
    js_object["text"] = text_dict

    #Making text rectangle
    text_rect_dict = {"type": "text-rect"}
    text_rect_dict['html_id'] = feature_dict['feat_html_id'] + "-text-rect"
    text_rect_info = calculate_text_rect(text_coords, text_dict["text_str"],
            js_info)
    for k in text_rect_info.keys():
        text_rect_dict[k] = text_rect_info[k]
    js_object["text_rect"] = text_rect_dict

    return js_object


"""
Inputs:
    text_start_coordinates: (floats) [x,y]
    text_str: (str)
    js_info: (dict) from config.json
Outputs:
    text_rect_dict:
        x:
        y:
        width:
        height:
        border_color:
        internal_color:
"""
def calculate_text_rect(text_start_coordinates, text_str, js_info):

    text_rect_info_dict = js_info['text_rect_info']
    text_size = js_info['text_size']
    height = text_size + 10
    text_rect_info_dict['height'] = height
    width_to_pixel_ratio = text_size/1.62
    text_box_width = len(text_str) * width_to_pixel_ratio
    text_rect_info_dict['width'] = text_box_width 
    #x and y represent the top left corner of the rectangle
    x = text_start_coordinates[0] - text_rect_info_dict["x_diff"]
    y = text_start_coordinates[1] - text_rect_info_dict["y_diff"]
    text_rect_info_dict['x'] = x
    text_rect_info_dict['y'] = y
    return text_rect_info_dict



"""
Inputs:
    feature_dict: (dict from feature_list.json)
    config_dict: (dict from config.json)
Outputs:
    coordinates - list<float>
    js_object:
        type: (str) "promoter"
        color: (str)
        line_width: (int)
        p_line_coordinate_start: list<float>
        big_radius: (int)
        arc_begin_point: list<float>
        arc_start_angle: list<float>
        arc_angle: (float)
        arc_end_angle: (float)
        arc_end_point: list<float>
        inner_flag_start: list<float>
        outer_flag_start: list<float>
        flags_end: list<float>
"""
def calculate_promoter_feature(feature_dict, config_dict):
    js_object = {"type": "promoter"}
    js_object["html_id"] = feature_dict["feat_html_id"] + "-promoter"
    js_info = config_dict['js_info']
    promoter_info = js_info['promoter_info']
    js_object['include_bool'] = promoter_info['include_bool']
    js_object["color"] = promoter_info["arrow_color"]
    js_object["line_width"] = promoter_info["line_width"]

    if feature_dict['feat_strand'] == -1:
        radius = js_info['complementary_radius']
    else:
        radius = js_info['circle_radius']

    cc = js_info['center_coordinates']
    js_object['center_x'] = cc[0]
    js_object['center_y'] = cc[1]
    js_object['feat_name'] = feature_dict['feat_name']

    percent_angle_to_promoter = promoter_info['percent_start']

    relative_angle_to_start = (feature_dict['plasmid_percentage'] * \
            (percent_angle_to_promoter/100))*(math.pi * 2)

    starting_angle = get_angle_from_point(feature_dict['point_start'],cc)
    promoter_symbol_start_angle = starting_angle + relative_angle_to_start
    starting_coordinates = calculate_position(cc[0], cc[1], radius, promoter_symbol_start_angle)
    

    if 'prcnt' in promoter_info:
        end_line_coordinates =  line_extension_coordinates(cc,starting_coordinates,"prcnt", promoter_info['prcnt'])
    elif 'pixels' in promoter_info:
        end_line_coordinates = line_extension_coordinates(cc,starting_coordinates,"pixels", promoter_info['pixels'])
    else:
        raise Exception("Neither pixels nor percent provided in promoter line extension info dict.")
    if 'line_width' in promoter_info:
        line_width = promoter_info['line_width']
    else:
        line_width = 3
    if 'arrow_angle' in promoter_info:
        arrow_angle = promoter_info['arrow_angle']
        if arrow_angle > 80 or arrow_angle < 10:
            raise Exception("Angle of flags of arrow must be between 10 and 80 degrees.")
    else:
        arrow_angle = 35.0
    if 'flag_length' in promoter_info:
        flag_length = promoter_info['flag_length']
    else:
        flag_length = 10


    js_object['p_line_coordinate_start'] = starting_coordinates
    js_object['arc_begin_point'] = end_line_coordinates
    js_object["arc_start_angle"] = promoter_symbol_start_angle


    #Now we must draw an arrow- first we use an extended radius to create an arc around the promoter area.
    #Then we make a small arrow at the end of the promoter region.
    big_radius = math.sqrt(((end_line_coordinates[0] - cc[0])**2) + ((end_line_coordinates[1] - cc[0])**2))
    js_object["big_radius"] = big_radius
    ending_angle = get_angle_from_point(feature_dict['point_end'],cc)
    js_object["arc_end_angle"] = ending_angle


    #The ending point for the promoter symbol arc:
    p_symbol_end = [cc[0] + big_radius*(math.cos(-1*(ending_angle - math.pi/2))),
            cc[1] - big_radius*(math.sin(-1*(ending_angle - math.pi/2)))]
    js_object["arc_end_point"] = p_symbol_end

    logging.warning("p_symbol_end: {}, {}".format(str(p_symbol_end[0]),str(p_symbol_end[1])))

    #We get the values for the arrow flags
    arrow_dict = calculate_arrow_values(cc ,p_symbol_end, arrow_angle, flag_length, line_width)

    for k in arrow_dict.keys():
        js_object[k] = arrow_dict[k]

    return js_object





def calculate_terminator_feature(feature_dict, config_dict):
    """
    The terminator symbol will look like a capital T with filled in color light red: "#EA6062"
    We will use two rectangles and two thin black lines to outline it (size 2)
    There are 8 variables - 8 points that symbolize the T, each is a list of floats.
    We calculate those and then build the rectangle using them.
    """
    logging.debug("Making terminator")
    js_info = config_dict["js_info"]
    if "terminator_info" in js_info:
        terminator_info = js_info["terminator_info"]
    else:
        raise Exception("terminator info not in config.json")

    if feature_dict["feat_strand"] == 1:
        radius = js_info['circle_radius']
    else:
        radius = js_info['complementary_radius']

    cc = js_info['center_coordinates']

    
    """
    First, we find the 8 variables.
    """
    percent_center =  terminator_info["percent_center"]
    relative_angle_to_t_center = (feature_dict['plasmid_percentage'] * (percent_center/100))*(math.pi * 2)

    starting_angle = get_angle_from_point(feature_dict['point_start'],cc)
    terminator_symbol_center_angle = starting_angle + relative_angle_to_t_center

    """
    We start using names of variables specific to the terminator symbol shape.
    alpha represents the center of the base of the T on the circle's circumference.
    beta represents the extension of the line from center to alpha where the base of T intersects the top section of the T.
    gamma represents the extension of the same line from center to alpha and beta to the top of the T.
    """

    alpha = [cc[0] + radius*(math.cos(-1*(terminator_symbol_center_angle - (math.pi/2)))),
            cc[1] - radius*(math.sin(-1*(terminator_symbol_center_angle - (math.pi/2))))]
    logging.debug("ALPHA:")
    logging.debug(alpha)

    if "base_height" in terminator_info:
        beta = line_extension_coordinates(cc,alpha,"pixels", terminator_info["base_height"])
        logging.debug("BETA:")
        logging.debug(beta)
    else:
        raise Exception("base_height must be included in the terminator info in the config file.")
    if "top_height" in terminator_info:
        gamma = line_extension_coordinates(cc,beta,"pixels", terminator_info["top_height"])
        logging.debug("GAMMA:")
        logging.debug(gamma)
    else:
        raise Exception("top_height must be included in the terminator info in the config file.")

    
    """
    We start finding the variables on the edge of the T that represent it.
    var_a is one base, var_b is intersection from a-base to a-side of top, var_c is a-side bottom corner of top,
    var_d is top a-side corner of top, var_h is base opposite to var_a, var_e is top h-side corner of top, 
    var_f is bottom h-side corner of top, var_g is intersection of base with h-side of top, var_h is base opposite to var_a.
    """
    perpendicular_slope = get_perpendicular_slope(cc, alpha)
    
    if "base_width" in terminator_info:
        b_w = terminator_info["base_width"]
        two_bases_dict = get_points_in_both_directions_from_center_with_slope(alpha, perpendicular_slope, b_w/2)
        var_a = two_bases_dict["with_slope_point"]
        var_h = two_bases_dict["against_slope_point"]
        base_top_intersect_points = get_points_in_both_directions_from_center_with_slope(beta, perpendicular_slope, b_w/2)
        var_b = base_top_intersect_points["with_slope_point"]
        var_g = base_top_intersect_points["against_slope_point"]
    else:
        raise Exception("base_width must be included in terminator_info in json config file.")

    if "top_width" in terminator_info:
        t_w = terminator_info["top_width"]
        two_bottom_top_dict = get_points_in_both_directions_from_center_with_slope(beta, perpendicular_slope, t_w/2)
        var_c = two_bottom_top_dict["with_slope_point"]
        var_f = two_bottom_top_dict["against_slope_point"]
        top_points = get_points_in_both_directions_from_center_with_slope(gamma, perpendicular_slope, t_w/2)
        var_d = top_points["with_slope_point"]
        var_e = top_points["against_slope_point"]
    else:
        raise Exception("top_width must be included in terminator_info in json config file.")

    list_of_coordinates = [var_a, var_b, var_c, var_d, var_e, var_f, var_g, var_h]

    js_object = {"type": "terminator",
            "html_id": feature_dict["feat_html_id"] + "-terminator",
            "border_color": terminator_info["border_color"],
            "internal_color": terminator_info["internal_color"],
            "border_width": terminator_info['border_width'],
            "feat_name": feature_dict['feat_name'],
            "base_1": var_a,
            "armpit_1": var_b,
            "palm_hand_1":var_c,
            "back_hand_1": var_d,
            "back_hand_2": var_e,
            "palm_hand_2": var_f,
            "armpit_2": var_g,
            "base_2": var_h,
            }

    return js_object


def calculate_rbs_feature(feature_dict, config_dict):
    js_info = config_dict["js_info"]

    """
    The ribosome binding/entry site symbol will look like a half circle with filled in color light purple.
    We calculate the center point of the rbs circle. Then we find the angle of the line perpendicular to the center 
    of the plasmid map circle.
    """
    logging.debug("Making rbs")
    if "ribosome_site_info" in js_info:
        rbs_info = js_info["ribosome_site_info"]
    else:
        raise Exception("Ribosome Site Info not found in js_info.")
    

    if feature_dict["feat_strand"] == 1:
        radius = js_info['circle_radius']
    else:
        radius = js_info['complementary_radius']

    cc = js_info['center_coordinates']

    rbs_radius = rbs_info["radius"]
    """
    First, we find the center of the rbs circle we will make.
    """
    percent_center = rbs_info["percent_center"]
    relative_angle_to_t_center = (feature_dict['plasmid_percentage'] * \
            (percent_center/100))*(math.pi * 2)

    starting_angle = feature_dict['angle_start'] 
    rbs_symbol_center_angle = starting_angle + relative_angle_to_t_center
    rbs_circle_center = [cc[0] + radius*(math.cos(-1*(rbs_symbol_center_angle - (math.pi/2)))),
            cc[1] - radius*(math.sin(-1*(rbs_symbol_center_angle - (math.pi/2))))]
    
    #Notice, here we add some distance from center of plasmid circle to the center of the rbs circle in order
    #  to get the circle to sit on top of the plasmid visual, and not inside it.
    extension_length = js_info['circle_line_width']/2
    rbs_circle_center = line_extension_coordinates(cc,rbs_circle_center,"pixels", extension_length)

    #We add math.pi/2 to make the angle perpendicular to circle
    start_angle = get_angle_from_point(rbs_circle_center, cc) + (math.pi/2)

    rbs_circle_start_point = [rbs_circle_center[0] + rbs_radius*(math.cos(-1*(start_angle - \
            (math.pi/2)))), rbs_circle_center[1] - \
            rbs_radius*(math.sin(-1*(start_angle - (math.pi/2))))]

    rbs_circle_end_point = [rbs_circle_center[0] + rbs_radius*(math.cos(-1*(start_angle - \
            (math.pi/2)) + math.pi )), rbs_circle_center[1] - \
            rbs_radius*(math.sin(-1*(start_angle - (math.pi/2)) + math.pi ))]


    js_object = {
            "type": "rbs",
            "html_id": feature_dict["feat_html_id"] + "-rbs",
            "start_point": rbs_circle_start_point,
            "end_point": rbs_circle_end_point,
            "radius": rbs_radius,
            "feat_name": feature_dict['feat_name'],
            "circle_center": rbs_circle_center,
            "start_angle": start_angle,
            "end_angle": start_angle + math.pi,
            "border_color": rbs_info["border_color"],
            "internal_color": rbs_info["internal_color"],
            "border_width": rbs_info["border_width"],
            }

    return js_object


def calculate_cds_feature(feature_dict, config_dict):
    js_info = config_dict["js_info"]

    """
    The CDS visual will look like an arrow head ending at the end of the CDS.
    In order to draw this, we need 6 variables. The variables represent:
        var_a: point on plasmid map that outer arrow starts.
        var_b: point outside plasmid map that outer arrow has its peak.
        var_c: point on plasmid map, same as end of cds, where arrow ends.
        var_d: inner complement to a.
        var_e: inner complement to b.
        var_f: inner complement to c.
    """
    logging.debug("Making CDS Visual")

    if "cds_info" in js_info:
        cds_info = js_info["cds_info"]
    else:
        raise Exception("CDS Info not found in js_info.")

    


    if feature_dict["feat_strand"] == 1:
        complement_bool = False
        radius = js_info['circle_radius']
    else:
        radius = js_info['complementary_radius']
        complement_bool = True

    cc = js_info['center_coordinates']




    
    """
    First, we find the start of the CDS arrow we will make.
    """
    percent_start = cds_info["percent_start"]
    if complement_bool:
        percent_start = 100 - percent_start
        arrow_end = feature_dict['point_start']
    else:
        arrow_end = feature_dict['point_end']

    relative_angle_to_t_center = (feature_dict['plasmid_percentage'] * (percent_start/100))*(math.pi * 2)

    starting_angle = get_angle_from_point(feature_dict['point_start'],cc)
    cds_symbol_start_angle = starting_angle + relative_angle_to_t_center
    cds_symbol_start_point = calculate_position(cc[0],cc[1],radius,cds_symbol_start_angle)
    var_a = line_extension_coordinates(cc,cds_symbol_start_point,"pixels", js_info['circle_line_width']/2)
    var_b = line_extension_coordinates(cc,var_a,"pixels",cds_info["arrow_height"])
    var_c = line_extension_coordinates(cc,arrow_end,"pixels", js_info['circle_line_width']/2)
    var_d = line_extension_coordinates(var_a, cds_symbol_start_point,"pixels", js_info['circle_line_width']/2)
    var_e = line_extension_coordinates(var_a,var_d,"pixels",cds_info["arrow_height"])
    var_f = line_extension_coordinates(var_c, arrow_end, "pixels", js_info['circle_line_width']/2)

    js_object = {
        "type": "cds",
        "html_id": feature_dict["feat_html_id"] + "-cds",
        "feat_name": feature_dict['feat_name'],
        "internal_color": feature_dict["feat_color"], 
        "a": var_a ,
        "b": var_b,
        "c": var_c,
        "d": var_d,
        "e": var_e,
        "f": var_f,
    }

    return js_object



##--------------------OTHER FUNCTIONS----------
"""
Inputs:
    A and B are points to which the arrow will be drawn perpendicularly
    A: (list) coordinates of a point in the canvas [x,y] (Would normally be the center)
    B: (list) coordinates of a point in the canvas [x,y] (Would normally be the outer point on a circle)
    arrow_angle: (float) (in degrees) between 10 and 80. 
    flag_length: (float) length of the flag
Outputs:
        arrow_dict:
            inner_flag_start: list<int>
            outer_flag_start: list<int>
            flags_end: list<int>

"""
def calculate_arrow_values(A,B,arrow_angle, flag_length, line_width):
    #B is ending point for the arrow.
    # Angles for the arrow must be calculated using the perpendicular slope - (from center to end of promoter symbol)
    slope = get_perpendicular_slope(A,B)
    logging.debug("Slope: {}".format(str(slope)))
    rotation_angle = math.atan(slope)
    logging.debug("Rotation angle: ")
    logging.debug(rotation_angle)

    #The following part is confusing, do not rely on Cartesian coordinates. The y coordinates here are flipped (ascending is descending on graph).
    if slope < 0:
        #This means slope is actually descending visually
        if B[0] > A[0]:
            #We are in the 1st quadrant.
            logging.debug("1st quadrant.")
            flag_a_1 = [flag_length*math.cos((180+arrow_angle)*(math.pi/180)), flag_length*math.sin((180+arrow_angle)*(math.pi/180))]
            flag_a_2 = perform_rotation(flag_a_1, rotation_angle)
            flag_b_1 = [flag_length*math.cos((180-arrow_angle)*(math.pi/180)), flag_length*math.sin((180-arrow_angle)*(math.pi/180))]
            flag_b_2 = perform_rotation(flag_b_1, rotation_angle)

        elif B[0] < A[0]:
            #We are in the 3rd quadrant.
            logging.debug("3rd quadrant.")
            flag_a_1 = [flag_length*math.cos((arrow_angle)*(math.pi/180)), flag_length*math.sin((arrow_angle)*(math.pi/180))]
            flag_a_2 = perform_rotation(flag_a_1, rotation_angle)
            flag_b_1 = [flag_length*math.cos(((-1)*arrow_angle)*(math.pi/180)), flag_length*math.sin(((-1)*arrow_angle)*(math.pi/180))]
            flag_b_2 = perform_rotation(flag_b_1, rotation_angle)

    elif slope > 0:
        #Visually ascending slope
        if B[0] > A[0]:
            #We are in the fourth quadrant.
            logging.debug("4th quadrant.")
            flag_a_1 = [flag_length*math.cos((arrow_angle)*(math.pi/180)), flag_length*math.sin((arrow_angle)*(math.pi/180))]
            flag_a_2 = perform_rotation(flag_a_1, rotation_angle)
            flag_b_1 = [flag_length*math.cos(((-1)*arrow_angle)*(math.pi/180)), flag_length*math.sin(((-1)*arrow_angle)*(math.pi/180))]
            flag_b_2 = perform_rotation(flag_b_1, rotation_angle)

        elif B[0] < A[0]:
            #We are in the second quadrant.
            logging.debug("2nd quadrant.")
            flag_a_1 = [flag_length*math.cos((180+arrow_angle)*(math.pi/180)), flag_length*math.sin((180+arrow_angle)*(math.pi/180))]
            flag_a_2 = perform_rotation(flag_a_1, rotation_angle)
            flag_b_1 = [flag_length*math.cos((180-arrow_angle)*(math.pi/180)), flag_length*math.sin((180-arrow_angle)*(math.pi/180))]
            flag_b_2 = perform_rotation(flag_b_1, rotation_angle)

    flag_a_2 = [B[0] + flag_a_2[0], B[1] + flag_a_2[1]]
    flag_b_2 = [B[0] + flag_b_2[0], B[1] + flag_b_2[1]]

    arrow_dict = {
            "flags_end": B,
            "inner_flag_start" : flag_a_2,
            "outer_flag_start" : flag_b_2,

            }
    return arrow_dict




