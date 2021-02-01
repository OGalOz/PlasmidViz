window.BasicShellData = {
    "lyt_vls": {
        "largest_container": {
            "tag_type": "DIV",
            "id_i": {
                "parent_id": "body",
                "id": "largest-container-div",
                "class": "base-shell"
            },
            "size_loc_i": {
                "values_type": "fractions",
                "l": 0.1,
                "t": 0.1,
                "h": 0.8,
                "w": 0.8
            },
            "style_i": {
                "position": "absolute",
                "border": "2px solid gray"
            }
        },
        "full_graph_div": {
            "tag_type": "DIV",
            "id_i": {
                "parent_id": "largest-container-div",
                "id": "graph-div",
                "class": "base-shell"
            },
            "size_loc_i": {
                "values_type": "fractions",
                "l": 0,
                "t": 0,
                "h": 1,
                "w": 0.8
            },
            "style_i": {
                "position": "absolute",
                "border": "2px solid gray"
            }
        },
        "graph_title_div": {
            "tag_type": "DIV",
            "id_i": {
                "parent_id": "graph-div",
                "id": "graph-title-div",
                "class": "base-shell"
            },
            "size_loc_i": {
                "values_type": "fractions",
                "l": 0,
                "t": 0,
                "h": .1,
                "w": 1
            },
            "style_i": {
                "position": "absolute",
                "border": "2px solid gray",
                "fontWeight": "bold",
                "textAlign": "center",
                "justifyContent": "center",
                "display": "flex",
                "alignItems": "center",
                "textDecoration": "underline",
                "fontSize": "30px"

            },
            "unq_prp": {
                "innerHTML": "Plasmid"
            }
        },
        "graph_svg_container_div": {
            "tag_type": "DIV",
            "id_i": {
                "parent_id": "graph-div",
                "id": "graph-svg-container-div",
                "class": "base-shell"
            },
            "size_loc_i": {
                "values_type": "fractions",
                "l": 0,
                "t": .1,
                "h": .9,
                "w": 1
            },
            "style_i": {
                "position": "absolute",
                "border": "2px solid gray",

            }
        },
        "graph_svg": {
            "tag_type": "SVG",
            "id_i": {
                "parent_id": "graph-svg-container-div",
                "id": "graph-svg",
                "class": "base-shell"
            },
            "size_loc_i": {
                "values_type": "fractions",
                "l": 0,
                "t": 0,
                "h": 1,
                "w": 1
            },
            "style_i": {
                "position": "absolute",
                "border": "2px solid gray",
            }
        },
        "sidebar": {
            "tag_type": "div",
            "id_i": {
                "parent_id": "largest-container-div",
                "id": "graph-sidebar",
                "class": "base-shell"
            },
            "size_loc_i": {
                "values_type": "fractions",
                "l": 0.8,
                "t": 0,
                "h": 1,
                "w": 0.2
            },
            "style_i": {
                "position": "absolute",
                "border": "2px solid gray",
                "textAlign": "center"
            },
            "unq_prp": {
                "innerHTML": "sidebar"
            }
        }
        

    }
}


