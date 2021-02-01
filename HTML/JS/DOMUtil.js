
// We hold on to a set of functions that is useful for building
// Web apps:


function StringToValidHTMLID(inp_str) {
    /*
     * Args:
     *      inp_str: (str) String to be changed
     *              into something that can be used as
     *              an id for a tag.
     *
     *  Note for HTML 5 the only restriction is no spaces
     */
    new_str = inp_str.replace("/","-");
    new_str = new_str.replace(" ","-");

    return new_str
    

}





