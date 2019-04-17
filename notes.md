#Notes

## Future Work

### 18th Apr

* Render Projections of Polycubes over axes (superimpose panels facing same direction)
* From 11th Feb:
    * Implement manage_panels()
    * Implement dxf

### 11th Feb
* Implement function to translate connected compenent (3D) to set of (2D) tuples
* Call draw_panel() on each connected component of mega graph
* Return SVG something back to main from draw_panel
* Implement manage_panels()
* Implement dxf

## Work Done

### 18th Apr
* Implemention of 3D Point to 2D tuples for SVG
* Integrated svg_tools.py with main.py

### 20th Jan
* Implementation of graph
* panels[dir] = {(1.5,0,0): graph, (2.5,0,0): graph}
* planes at 0.5,1.5,2.5...
* new point addition
    * check if common face then delete vertex from graph
    * else 
        * create vertex (instead of create panel) 
        * check 4 neighbors and add edge between neighbor and this point (instead of panel-union)
* get_panels: look at connected components of graph to determine panels        


### 19th Jan
* problem: union-find tree parent panel becoming none because it was common face
* implement all panels properly (currently printing 7/8 panels) 

### 15th Jan
* common face is stored as None, and deleted from polycube neighbor panel
* extending faces using union find one by one when no common face found (max 4 connected neighbors)


## TODO

* Implement brute force n^3 algorithm
    * Phase 1: checks every cell and exor of adjacent/neighboring polycubes presence
    * only add cell as face if exactly one polycube present
    * Phase 2: Union-find algo over all planes (over all 3 directions) to merge single cell faces into panels
