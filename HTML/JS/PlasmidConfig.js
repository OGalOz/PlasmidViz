window.plasmid_config_obj = {
    "supported_feature_types": [
        "gap",
        "cds",
        "terminator",
        "promoter",
        "scar",
        "output",
        "rbs"
    ],
    "features_with_arcs": [
        "gap",
        "cds",
        "terminator",
        "promoter",
        "scar",
        "output",
        "rbs"
    ],
    "feature_arc_to_color": {
        "gap": "black",
        "cds": "DarkBlue",
        "terminator":"DarkRed",
        "promoter": "#00cc7e",
        "scar": "Red",
        "output": "GreenYellow",
        "rbs": "Gold"

    },
    "center_frac":[.5,.5],
    "circle_radius_frac": .3, 
    "complementary_radius_frac": .27,
    "pointer_len_short": .1,
    "pointer_len_medium": .13,
    "pointer_len_long": .16,
    "pointer_thick":1,
    "pointer_color": "black",
    "text_size" : 25,
    "text_color": "black",
    "highlight_color": "#FFFFD5",
    "arc_width": .03, 

    "title_text_size" : 28,
    "midpoint_distance": 30,
    "pointer_distance": 5,
    "title_text_color": "#333",
    "max_title_length" : 35,
    "delete_box_info": {
        "top_left_corner_x": 0,
        "top_left_corner_y": 300,
        "width": 50,
        "height": 50,
        "internal_color": "red",
        "border_color": "black",
        "img_link": "delete_img.png",
        "include_bool" : true

    },
    "reset_box_info": {
        "top_left_corner_x": 0,
        "top_left_corner_y": 350,
        "width": 50,
        "height": 50,
        "internal_color": "blue",
        "border_color": "black",
        "img_link": "reset_img.png",
        "include_bool" : false
    },
    "legend_box_info": {
        "top_left_corner_x": 0,
        "top_left_corner_y": 700,
        "width": 120,
        "height": 300,
        "text_box_width": 80,
        "color_box_width": 40,
        "title_text": "Color Legend",
        "border_color": "black",
        "internal_color": "white",
        "row_font_weight": "normal",
        "row_font_color": "black",
        "row_font_size": 12,
        "title_font_weight": "bold",
        "title_font_color": "black",
        "title_font_size": 12,

        "include_bool" : true
    },

    "text_rect_info": {
        "x_diff": 8,
        "y_diff": 20,
        "border_color": "gray",
        "clicked_border_color": "black",
        "internal_color": "white",
        "clicked_internal": "#E6E6FA"
    },

    "feature_typ_info": {
        "gap_arc_info" : {
            "circle_line_width": 3,
            "color": "black"
        },
        "promoter_info" : {
            "include_bool" : true,
            "frac_start": .40,
            "line_width": 1,
            "tiny_arrow_frac": .02,
            "arrow_angle": 35.0,
            "radius_frac_from": 0.1,
            "arrow_color": "black"
        },
        "terminator_info" : {
            "percent_center": 50,
            "base_width": 4,
            "base_height": 16,
            "top_width": 12,
            "top_height": 4,
            "internal_color": "#EA6062",
            "border_color": "black",
            "border_width": 2
        },
        "ribosome_site_info": {
            "percent_center": 50,
            "radius": 8,
            "border_width": 1,
            "border_color": "black",
            "internal_color": "#bb99ff"
        },
        "cds_info": {
            "frac_start": .3,
            "arrow_height_frac": .035
        }
    }
}
