#Notes

## Future work

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
