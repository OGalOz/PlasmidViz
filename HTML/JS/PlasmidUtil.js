

// We create the functions needed to build a plasmid map
function plotPlasmidFeatures(graph_svg_id, c_plasmid_object) {
    /*
     * graph_svg_id: (str) The id of the svg we're populating
     * c_plasmid_object: The plasmid info object for this specific plasmid
     *      plasmid_info:
                plasmid_name: str
                plasmid_length: Num
                num_features: Num
                old_gb_name: str
     *      feat_info_list: list<feat_info>
     *          feat_info: list<start_bp (i), end_bp (i), strand (s), typ (s), name (s)>
     */

    // plasmid features
    let p_feats = c_plasmid_object["feat_info_list"]

    let d3svg = getSVG(graph_svg_id) 


    //plasmid config
    let p_cfg = window.plasmid_config_obj
    let updated_p_info = updatePlasmidInfo(graph_svg_id, p_cfg)
    p_cfg["crnt_p_info"] = {
                        ...updated_p_info,
                        ...c_plasmid_object["plasmid_info"]
    }
    //console.log(updated_p_info)
    
    for (let i = 0; i<p_feats.length; i++) {

        let current_feat = p_feats[i]
        let ctyp = current_feat[3]
        if (p_cfg['supported_feature_types'].includes(ctyp)) {
            console.log("Drawing " + ctyp)
            plotSingleFeature(d3svg, current_feat, p_cfg, i)
        } else {
            console.log("Feature type " + ctyp + " not supported.")
        }

    }
}


function updatePlasmidInfo(graph_svg_id, p_cfg, c_plasmid_obj) {
    /* Function generates plasmid basic info, like the center of the
     *      plasmid within the svg, the outer radius, inner radius,
     *      pointer lengths (small, medium, large), BASED on the size
     *      of the encompassing SVG
     *
     * Args:
     *  p_cfg:
            center_frac":[.5,.5], list<Num, Num>
            circle_radius_frac": .3, Num
            complementary_radius_frac": .27, Num
            pointer_len_short": .1, Num
            pointer_len_medium": .13, Num
            pointer_len_long": .16, Num
       Returns:
     *          crnt_p_info:
     *              p_center: Coord [x, y]
     *              p_radius: Num
     *              p_comp_radius: Num
     *              pnt_len_short:
     *              pnt_len_medium:
     *              pnt_len_long:
     *
     *
     */
    
    let bcR_obj = document.getElementById(graph_svg_id).getBoundingClientRect()
    let svg_width = bcR_obj.width;
    let svg_height = bcR_obj.height;
    let min_dim = Math.min(svg_width, svg_height)
    if (min_dim == svg_width) {
        lesser_dimension = 'x'
    } else {
        lesser_dimension = 'y'
    }
    console.log("Lesser dimension: " + lesser_dimension)
    /*
    let svg_width = d3svg.attr("width")
    let svg_height = d3svg.attr("height")
    */
    console.log("x: " + svg_width + " y: " + svg_height)

    let p_center = [svg_width*p_cfg["center_frac"][0],
                svg_height*p_cfg["center_frac"][1]]

    let p_radius = min_dim * p_cfg["circle_radius_frac"]
    let p_comp_radius = min_dim * p_cfg["complementary_radius_frac"]

    let pnt_len_short =  min_dim * p_cfg["pointer_len_short"]
    let pnt_len_medium = min_dim * p_cfg["pointer_len_medium"] 
    let pnt_len_long =  min_dim * p_cfg["pointer_len_long"]
    let arc_width = min_dim * p_cfg["arc_width"]

    let crnt_p_info = {
        "p_center" : p_center,
        "p_radius" : p_radius,
        "p_comp_radius" : p_comp_radius,
        "pnt_len_short" : pnt_len_short,
        "pnt_len_medium" : pnt_len_medium,
        "pnt_len_long" : pnt_len_long,
        "arc_width": arc_width,
        "lesser_dimension_length": min_dim
    }
    return crnt_p_info

        
    
    
}


function plotSingleFeature(d3svg, current_feat, p_cfg, num_feat) {
    /*
     * Args:
     *      d3svg: svg object in d3 form
     *      current_feat: list<start_bp (i), end_bp (i), strand (s), typ (s), name (s)>
     *      p_cfg: object with info relating to how to draw feature
     *          crnt_p_info:
     *              p_center: Coord [x, y]
     *              p_radius: Num
     *              p_comp_radius: Num
     *              pnt_len_short:
     *              pnt_len_medium:
     *              pnt_len_long:
     *              arc_width: Num
     *              plasmid_name: str
     *              plasmid_length: Num
     *              num_features: Num
     *              old_gb_name: str
     *              
     */
    

    if (p_cfg["features_with_arcs"].includes(current_feat[3])) {
        plotFeatureArc(d3svg, current_feat, p_cfg, num_feat)
    }
    if (current_feat[3] == "cds") {
        plotCDS(d3svg, current_feat, p_cfg, num_feat)
    } else if (current_feat[3] == "promoter") {
        plotPlasmidPromoter(d3svg, current_feat, p_cfg, num_feat)
    } else if (current_feat[3] == "terminator") {
        plotPlasmidTerminator(d3svg, current_feat, p_cfg, num_feat)
    }

   return null 
}




function plotPlasmidTerminator(d3svg, feature_info, p_cfg, num_feat) {
    /*
     *  Args:
     *      d3svg: d3 svg object (selected)
     *
     *      feature_info:
     *              list<start_bp (i), end_bp (i), strand (s), typ (s), name (s)>
     *      p_cfg:
     *          crnt_p_info:
     *              p_center: Coord [x, y]
     *              p_radius: Num
     *              p_comp_radius: Num
     *              pnt_len_short: Num
     *              pnt_len_medium: Num
     *              pnt_len_long: Num
     *              arc_width: Num
     *              plasmid_name: str
     *              plasmid_length: Num
     *              num_features: Num
     *              old_gb_name: str
     *          feature_typ_info
     *"             terminator_info":
                        frac_center: .5, (Num) fraction within feature of center
                        base_width_frac": 0.08, (Num) fraction of feature base length of T
                        base_height_frac": 0.1, (Num) fraction of radius base height of T
                        top_width_frac": 0.16,  (Num) fraction of feature, top of T
                        top_height_frac": 0.04, (Num) fraction of radius height of top
                        internal_color": "#EA6062" str internal color of polygon
                        border_color_info": object
                            color: str
                            width: Num
     */

    let cp_info = p_cfg["crnt_p_info"]
    // terminator config info
    let trm_i = p_cfg["feature_typ_info"]["terminator_info"]

    if (!(trm_i["include_bool"])) {
        // Arrow not included in output
        return null
    }

    // The start/end locs of entire feature
    let angle_start = (feature_info[0]/cp_info["plasmid_length"])*Math.PI*2
    let angle_end = (feature_info[1]/cp_info["plasmid_length"])*Math.PI*2
    let full_angle = angle_end - angle_start

    // this radius
    let strand = feature_info[2]
    let crad = null
    let mult_factor = null
    let feat_cntr_angle = trm_i["frac_center"]*full_angle + angle_start 
    if (strand == "+") {
        mult_factor = 1
        crad = cp_info["p_radius"]
    } else if (strand == "-") {
        mult_factor = -1
        crad = cp_info["p_comp_radius"]
    } else {
        console.log("Cannot recognize strand in graphing Promoter")
        return null
    }
    // First point of T
    let point_a = calculateCirclePosition(cp_info["p_center"][0], 
                                          cp_info["p_center"][1], 
                                          crad, 
                                          feat_cntr_angle + 
                                          trm_i["base_width_frac"]*full_angle)

    // Second point of T, above A
    let point_b = calculateCirclePosition(cp_info["p_center"][0], 
                                          cp_info["p_center"][1], 
                                          crad*(1 + mult_factor*(trm_i["base_height_frac"])), 
                                          feat_cntr_angle + 
                                          trm_i["base_width_frac"]*full_angle)
    
    // Third point of T, next to B
    let point_c = calculateCirclePosition(cp_info["p_center"][0], 
                                          cp_info["p_center"][1], 
                                          crad*(1 + mult_factor*(trm_i["base_height_frac"])), 
                                          feat_cntr_angle + 
                                          trm_i["top_width_frac"]*full_angle)

    // Fourth point of T, above C
    let point_d = calculateCirclePosition(cp_info["p_center"][0], 
                                          cp_info["p_center"][1], 
                                          crad*(1 + mult_factor*(trm_i["top_height_frac"])), 
                                          feat_cntr_angle + 
                                          trm_i["top_width_frac"]*full_angle)


    // Fifth point of T, reflection across center from D
    let point_e = calculateCirclePosition(cp_info["p_center"][0], 
                                          cp_info["p_center"][1], 
                                          crad*(1 + mult_factor*(trm_i["top_height_frac"])), 
                                          feat_cntr_angle - 
                                          trm_i["top_width_frac"]*full_angle)

    // Sixth point of T, reflection across center from C
    let point_f = calculateCirclePosition(cp_info["p_center"][0], 
                                          cp_info["p_center"][1], 
                                          crad*(1 + mult_factor*(trm_i["base_height_frac"])), 
                                          feat_cntr_angle -
                                          trm_i["top_width_frac"]*full_angle)
    
    // Seventh point of T, reflection across center from B
    let point_g = calculateCirclePosition(cp_info["p_center"][0], 
                                          cp_info["p_center"][1], 
                                          crad*(1 + mult_factor*(trm_i["base_height_frac"])), 
                                          feat_cntr_angle - 
                                          trm_i["base_width_frac"]*full_angle)

    // Eigth point of T, reflection from A
    let point_h = calculateCirclePosition(cp_info["p_center"][0], 
                                          cp_info["p_center"][1], 
                                          crad, 
                                          feat_cntr_angle -
                                          trm_i["base_width_frac"]*full_angle)
    
    let TerminatorPath = [point_a, point_b, point_c, point_d, point_e,
                          point_f, point_g, point_h]

    addPolygon(d3svg, TerminatorPath, trm_i["internal_color"], 
                    id = 'shape-' + num_feat.toString() + '-terminator',
                    onclick_obj=null, ondrag_obj=null, 
                    border_color_info=trm_i["border_color_info"])

                                            
   return null 

}

function plotPlasmidPromoter(d3svg, feature_info, p_cfg, num_feat) {
   /*
    * Type of feature is Promoter (Gets transcription to start)
    * 
    * We create ascending thin black arrow pointing in direction of promotion 
    *
    *  Args:
    *      d3svg: d3 svg object (selected)
    *
    *      feature_info:
    *              list<start_bp (i), end_bp (i), strand (s), typ (s), name (s)>
    *      p_cfg:
    *          crnt_p_info:
    *              p_center: Coord [x, y]
    *              p_radius: Num
    *              p_comp_radius: Num
    *              pnt_len_short: Num
    *              pnt_len_medium: Num
    *              pnt_len_long: Num
    *              arc_width: Num
    *              plasmid_name: str
    *              plasmid_length: Num
    *              num_features: Num
    *              old_gb_name: str
    *              lesser_dimension_length: Num
    *          feature_typ_info:
    *              promoter_info:
                      include_bool : whether or not to draw these,
                      frac_start": Num, Starting location in arc in fractions
                      line_width": Num, width of promoter drawing in pixels
                      tiny_arrow_frac": .02, length of arrow in fractions
                      radius_frac_from: Num, fraction of radius promoter arrow
                                        extends to
                      arrow_angle": 35.0, Num (in degrees) of arrow angles
                      arrow_color": "black" (str) Color of shape
    *
    *
    */

    let cp_info = p_cfg["crnt_p_info"]

    // promoter config info
    let prm_i = p_cfg["feature_typ_info"]["promoter_info"]

    if (!(prm_i["include_bool"])) {
        // Arrow not included in output
        return null
    }

    // The start/end locs of entire feature
    let angle_start = (feature_info[0]/cp_info["plasmid_length"])*Math.PI*2
    let angle_end = (feature_info[1]/cp_info["plasmid_length"])*Math.PI*2

    // this radius
    let strand = feature_info[2]
    let crad = null
    let feat_start_angle = null
    let feat_end_angle = null
    let mult_factor = null
    if (strand == "+") {
        feat_end_angle = angle_end 
        feat_start_angle = prm_i["frac_start"]*(angle_end - angle_start) + angle_start 
        mult_factor = 1
        crad = cp_info["p_radius"]

    } else if (strand == "-") {
        feat_end_angle = angle_start 
        feat_start_angle = angle_end - prm_i["frac_start"]*(angle_end - angle_start)
        mult_factor = -1
        crad = cp_info["p_comp_radius"]
    } else {
        console.log("Cannot recognize strand in graphing Promoter")
        return null
    }
    // We get total distance to start of promoter arc
    // changed radius to promoter symbol
    let prm_height = prm_i["radius_frac_from"]*crad
    let prm_arc_start_radius = crad + prm_height*mult_factor
    // We get the promoter arc start point's coordinates
    let prm_arc_start_coord = calculateCirclePosition(cp_info["p_center"][0], 
                                                 cp_info["p_center"][1], 
                                                 prm_arc_start_radius, 
                                                 feat_start_angle)
    // End point coordinates
    let prm_end_coord = calculateCirclePosition(cp_info["p_center"][0], 
                                                 cp_info["p_center"][1], 
                                                 crad + prm_height*mult_factor, 
                                                 feat_end_angle)

    // We get the initial points on the plasmid
    let init_arc_start_coord = calculateCirclePosition(cp_info["p_center"][0], 
                                                 cp_info["p_center"][1], 
                                                 crad, 
                                                 feat_start_angle)

    // We draw the initial line and arc without the arrow
    // Line
    makeLine(d3svg, prm_i["arrow_color"], 
            init_arc_start_coord[0],
            init_arc_start_coord[1],
            prm_arc_start_coord[0],
            prm_arc_start_coord[1],
            stroke_width = prm_i["line_width"],
            id = 'shape-' + num_feat.toString() + '-promoter-1')
    // Arc
    addArc(d3svg, feat_start_angle, feat_end_angle, cp_info["p_center"], 
                  inner_radius = prm_arc_start_radius - prm_i["line_width"]/2, 
                  outer_radius = prm_arc_start_radius + prm_i["line_width"]/2,
                  internal_color = prm_i["arrow_color"], 
                  id = 'shape-' + num_feat.toString() + '-promoter-2')

    // We draw the two arrows
    // First we get the length of the arrows
    let tiny_arrow_length = cp_info["lesser_dimension_length"]*prm_i["tiny_arrow_frac"]
    // Then we get the orthogonal angle to the line between center and end point
    let orthogonal_angle = feat_end_angle - mult_factor*(Math.PI/2)
    // Then we get the angle change in radians
    let flag_angle_change = (Math.PI/180)*prm_i["arrow_angle"]
    // Now we get the locs of the ends of the flags from the end point 
    let flag_1_end_coords = calculateCirclePosition(prm_end_coord[0],
                                                    prm_end_coord[1],
                                                    tiny_arrow_length, 
                                                    orthogonal_angle + flag_angle_change)
    let flag_2_end_coords = calculateCirclePosition(prm_end_coord[0],
                                                    prm_end_coord[1],
                                                    tiny_arrow_length, 
                                                    orthogonal_angle - flag_angle_change)
    // Here we actually draw the two lines
    makeLine(d3svg, prm_i["arrow_color"], 
            prm_end_coord[0],
            prm_end_coord[1],
            flag_1_end_coords[0],
            flag_1_end_coords[1],
            stroke_width = prm_i["line_width"],
            id = 'shape-' + num_feat.toString() + '-promoter-3')
    
    makeLine(d3svg, prm_i["arrow_color"], 
            prm_end_coord[0],
            prm_end_coord[1],
            flag_2_end_coords[0],
            flag_2_end_coords[1],
            stroke_width = prm_i["line_width"],
            id = 'shape-' + num_feat.toString() + '-promoter-4')

}


function plotCDS(d3svg, feature_info, p_cfg, num_feat) {
    /* 
     * Type of feature is CDS (Coding Sequence)
     * 
     * We create the arrow at the end of the arc
     *
     *  We need the following info: feature strand or
     *      compliment strand. 
     *
     *
     *  Args:
     *      d3svg: d3 svg object (selected)
     *
     *      feature_info:
     *              list<start_bp (i), end_bp (i), strand (s), typ (s), name (s)>
     *      p_cfg:
     *          crnt_p_info:
     *              p_center: Coord [x, y]
     *              p_radius: Num
     *              p_comp_radius: Num
     *              pnt_len_short: Num
     *              pnt_len_medium: Num
     *              pnt_len_long: Num
     *              arc_width: Num
     *              plasmid_name: str
     *              plasmid_length: Num
     *              num_features: Num
     *              old_gb_name: str
     *              lesser_dimension_length: Num
     *          feature_typ_info:
     *              cds_info:
     *                  frac_start: Num
     *                  arrow_height_frac: Num
     *
     */

    // We get the three points for the arrow
    // current plasmid info
    let cp_info = p_cfg["crnt_p_info"]
    let strand = feature_info[2]
    let end_angle = null
    let angle_start = (feature_info[0]/cp_info["plasmid_length"])*Math.PI*2
    let angle_end = (feature_info[1]/cp_info["plasmid_length"])*Math.PI*2
    let triangle_start_angle_frac = (angle_end - 
                            angle_start)*p_cfg["feature_typ_info"]["cds_info"]["frac_start"]
    let triangle_end_angle = null
    let triangle_start_angle = null
    // this radius
    let crad = null
    if (strand == "+") {
        triangle_end_angle = angle_end 
        triangle_start_angle = angle_end - triangle_start_angle_frac
        crad = cp_info["p_radius"]
    } else if (strand == "-") {
        triangle_end_angle = angle_start
        triangle_start_angle = angle_start + triangle_start_angle_frac
        crad = cp_info["p_comp_radius"]
    } else {
        console.log("Cannot recognize strand in graphing CDS")
        return null
    }
    
    /*
    // Below are the coordinates for the triangle's start (middle of edges)
    let triangle_start_coord = calculateCirclePosition(cp_info["p_center"][0], 
                                                 cp_info["p_center"][1], 
                                                 cp_info["p_radius"], 
                                                 triangle_start_angle)
    */

    // Below are the coordinates for the triangle's end (center of triangle)
    let triangle_end_coord = calculateCirclePosition(cp_info["p_center"][0], 
                                                 cp_info["p_center"][1], 
                                                 crad, 
                                                 triangle_end_angle)
    /*
    // We get the perpendicular slope between the points
    let perp_slope = getPerpendicularSlope(triangle_start_coord, triangle_end_coord)
    */

    // We get the length of the flag:
    let flag_length = cp_info["lesser_dimension_length"]*
                        p_cfg["feature_typ_info"]["cds_info"]["arrow_height_frac"]
    console.log("FLAG LEN: " + flag_length.toString())
    // Coordinates of corner of triangle outside radius
    let out_corner_coord =  calculateCirclePosition(cp_info["p_center"][0], 
                                                 cp_info["p_center"][1], 
                                                 crad + flag_length, 
                                                 triangle_start_angle)

    // Coordinates of corner of triangle inside radius
    let in_corner_coord =  calculateCirclePosition(cp_info["p_center"][0], 
                                                 cp_info["p_center"][1], 
                                                 crad - flag_length, 
                                                 triangle_start_angle)

    // We draw the triangle
    let path_coord = [triangle_end_coord, out_corner_coord, in_corner_coord]
    console.log(path_coord)
    addPolygon(d3svg, path_coord, p_cfg["feature_arc_to_color"][feature_info[3]],
                    id = 'shape-' + num_feat.toString() + '-cds',
                    onclick_obj=null, ondrag_obj=null)



   return null 

}



function plotFeatureArc(d3svg, feature_info, p_cfg, num_feat) {
    // plasmid info
    let pl_i = p_cfg["crnt_p_info"]
    // arc info

    let plasmid_center = pl_i["p_center"]
    let c_radius = null
    if (feature_info[2] == "+") {
        // main radius
        c_radius = pl_i["p_radius"]
    } else if (feature_info[2] == "-") {
        //complement radius
        c_radius = pl_i["p_comp_radius"]
    } else {
        console.log("WARNING, CDS feature does not have proper strand info")
        c_radius = (pl_i["p_radius"] + pl_i["p_comp_radius"])/2
    }

    let arc_id = 'arc-' + num_feat.toString() + "-" + feature_info[3]

    // We draw an arc
    // get the percent of plasmid
    let start_angle = (feature_info[0]/pl_i["plasmid_length"])*Math.PI*2
    let end_angle = (feature_info[1]/pl_i["plasmid_length"])*Math.PI*2

    on_hover_info = {
        "func_over": ArcOnMouseHover,
        "inp_over": arc_id,
        "func_out":  ArcOnMouseOut,
        "inp_out": arc_id
    }
    arc_DOM_data = {
        'origcolor': p_cfg["feature_arc_to_color"][feature_info[3]]
    }

    addArc(d3svg, start_angle, end_angle, plasmid_center, 
                  inner_radius = c_radius - pl_i["arc_width"]/2, 
                  outer_radius = c_radius + pl_i["arc_width"]/2, 
                  internal_color = p_cfg["feature_arc_to_color"][feature_info[3]], 
                  id = arc_id, onclick_obj=null, 
                  on_hover_obj=on_hover_info,
                  DOM_data_obj=arc_DOM_data, debug=true)

}

function ArcOnMouseHover(elem_id) {
    /*
     * d is the data given
     * i is the index of the data
     *
     */
    let my_elem =  document.getElementById(elem_id)
    my_elem.style.fill = "yellow"

    /*
    // Use D3 to select element, change color and size
    d3.select(this).attr({
      fill: "yellow",
    });
    */

}

function ArcOnMouseOut(elem_id) {
    /*
     * d is the data given
     * i is the index of the data
     *
     */

    let myelem =  document.getElementById(elem_id)
    myelem.style.fill = myelem.dataset.origcolor
    /*
    // Use D3 to select element, change color and size
    let orig_color = d3.select(this)
    console.log(orig_color)
    d3.select(this).attr({
      fill: "blue",
    });
    */

}


