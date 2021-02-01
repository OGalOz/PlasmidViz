

function calcDist(a,b){
    /*
    Args:
        a: (list) [x,y]
        b: (list) [x,y]
    Returns:
        Num, distance (+) between a and b
    */
    return Math.sqrt(Math.pow(a[0]-b[0],2) + Math.pow(a[1] - b[1], 2))
}

function calculateCirclePosition(cx, cy, radius, angle) {
    /* Given the circle center, radius, and angle, get points on circle.
    Args:
        cx: (float) center position (x)
        cy: (float) center position (y)
        radius: (float)
        angle: (float)
    Returns:
        New point <x,y>
    */
    return [cx + radius*(Math.cos(-1*(angle - (Math.PI/2)))),
        cy - radius*(Math.sin(-1*(angle - (Math.PI/2))))]
}



function getRadianAngleFromPoint(circle_coordinates, center_coordinates) {
    /* Given two points, get angle in radians (above x axis)

    Args: 
        circle_coordinates: (list) floats [x,y] for a point on the circle.
        center_coordinates: (list) floats [x,y] for the center of the circle.
    Returns:
        theta: (float) The angle to the point (in Radians)
    
    */

    let d_y = -1*(circle_coordinates[1] - center_coordinates[1])
    let d_x = circle_coordinates[0] - center_coordinates[0]
    //logging.warning("d_y: {}".format(str(d_y)))
    //logging.warning("d_x: {}".format(str(d_x)))
    //#We apply a transformation on the angle to keep it consistent
    let theta = (-1*(Math.atan2(d_y, d_x) - Math.PI/2))
    //logging.warning("theta: {}".format(str(theta)))

    return theta
}



function calculateSlope(A,B) {
    /*
    Args:
        A: (list) list of floats [x,y] starting point.
        B: (list) list of floats [a,b] ending point.
    Returns:
        slope: (float) represents slope from A to B if A and B aren't
                vertically aligned. If vertically aligned, returns
                string "+" for yB>yA, "-" for yB < yA
                if points are the same, returns null
    Tested
    */

    //logging.debug("Calculating Slope: ")
    //logging.debug("Start Point: ({},{})".format(A[0], A[1]))
    //logging.debug("End Point: ({},{})".format(B[0], B[1]))

    let rise = null
    let run = null
    if (B[0] >= A[0]) {
        rise = -1*(B[1] - A[1])
        run = B[0] - A[0]
    } else {
        //#B[0] < A[0]
        rise = -1*(A[1] - B[1])
        run = A[0] - B[0]
    }
    if (run == 0) {
        if (rise == 0) {
            console.log("Slope between to equal points")
            return null 
        }
        if (B[1] > A[1]) {
            return "+" 
        } else {
            return "-"
        }
    }
    let slope = rise/run

    return slope
}


function lineExtensionCoordinates(A,B,prcnt_pixel_indicator, prcnt_or_pixels_value) {
    /*
    Args:
        A: (list) list of floats [x,y] starting point.
        B: (list) list of floats [a,b] ending point (add extension to these coordinates).
        prcnt_pixel_indicator: (str) limited vocab to "prcnt" or "pixels"
        prcnt_or_pixels_value: Num
            prcnt: (float) -1.0<p<1.0 [necessary if no pixels] A float representing the percent increase/decrease in length you want in the line.
            pixels: (int) [necessary if no pixels] An integer representing increase/decrease in length in pixels if wanted.
    Returns:
        ext_c: (list) A list of floats [c,d] representing an extension of the line
    */

    let change_length = null
    //#Getting change_length (amount change in pixels)
    if (prcnt_pixel_indicator == "prcnt") {
        let prcnt = prcnt_or_pixels_value
        if ((prcnt > 1.0) || (prcnt < -1.0)) {
            throw "Percent must be decimal point between -1 and 1"
        }
        let line_length = Math.sqrt(((A[0] - B[0])**2) + ((A[1] - B[1])**2))
        change_length = prcnt * (line_length)

    } else if (prcnt_pixel_indicator == "pixels") {
        let pixels = prcnt_or_pixels_value
        if (abs(pixels) > 600) {
            throw "pixel change must be less than 600"
        }
        change_length = pixels
    } else {
        throw "Did not recognize prcnt_pixel_indicator, must be one of prcnt or pixels"
    }

    let slope = calculateSlope(A,B)

    let d_x = null
    let d_y = null
    let ext_c = null
    if (B[0] >= A[0]) {
        if (change_length >= 0) {
            d_x = (change_length/Math.sqrt(1+(slope**2)))
            d_y = slope * d_x
            ext_c = [B[0] + d_x, B[1] - d_y]
        } else {
            // #change_length < 0:
            change_length = -1 * change_length
            d_x = (change_length/Math.sqrt(1+(slope**2)))
            d_y = slope * d_x
            ext_c = [B[0] - d_x, B[1] + d_y]
        }
    } else {
        //#B[0] < A[0]
        if (change_length >= 0) {
            d_x = (change_length/Math.sqrt(1+(slope**2)))
            d_y = slope * d_x
            ext_c = [B[0] - d_x, B[1] + d_y]
        } else {
            //#change_length < 0:
            d_x = (change_length/Math.sqrt(1+(slope**2)))
            d_y = slope * d_x
            ext_c = [B[0] + d_x, B[1] - d_y]
        }
    }
    return ext_c

}




function getPerpendicularSlope(A,B) {
    /* returns the slope perpendicular to the given slope between two points 
    Args:
        A: (list) coordinates of a point in the canvas [x,y] (Would normally be the center)
        B: (list) coordinates of a point in the canvas [x,y] (Would normally be the outer point on a circle)
    Returns:
        p_slope: (float) The perpendicular slope
    */

    let slope = calculateSlope(A,B)
    // logging.debug("original slope: {}".format(str(slope)))
    if (slope != 0) {
        if (!([null, "+", "-"].includes(slope))) {
            return (-1/slope) 
        } else if (["+","-"].includes(slope)) {
            return 0
        } else {
            // points are the same
            return null
        }
    } else {
        if (A[0] < B[0]) {
            return "+" 
        } else if (B[0] < A[0]) {
            return "-"
        } else {
            return null 
        }
    }
}

    
function performRotation(point, angle) {
    /*
    Args:
        point: (list) [x,y] location of point in the plane.
        angle: (float) Angle in radians to shift point.
    Returns:
        rotated_point: (list) [x,y] location of rotated point in the plane.
    */

    let x_coordinate = (Math.cos(angle)*point[0]) - (Math.sin(angle)*point[1])
    let y_coordinate = (Math.sin(angle)*point[0]) + (Math.cos(angle)*point[1])
    return [x_coordinate, y_coordinate]
}

function getPointsInBothDirectionsFromCenterWithSlope(center_point, slope, pixels) {
    /*
    Args:
        center_point: (list<x,y> A list of coordinates for the point from which we calculate the distances.
        slope: (float) The rise over run of the line on which we're returning the points.
        pixels: (float) The distance from the center_point in the direction of the slope.
    
    Returns:
        points_dict: (object)
            with_slope_point: (list<x,y>) Coordinates for the point that goes in the direction of the slope.
            against_slope_point: (list <x,y>) Coordinates for the point that goes against the direction of the slope.
    */
    
    let dx = pixels/(Math.sqrt(1+slope**2))
    let dy = dx*slope
    let with_slope_point = [center_point[0] + dx, center_point[1] - dy]
    let against_slope_point = [center_point[0] - dx, center_point[1] + dy]    

    let points_dict = {
            "with_slope_point": with_slope_point,
            "against_slope_point": against_slope_point
    }

    return points_dict
}
