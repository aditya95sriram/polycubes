#Notes

## TODO

* Implement brute force n^3 algorithm
    * Phase 1: checks every cell and exor of adjacent/neighboring polycubes presence
    * only add cell as face if exactly one polycube present
    * Phase 2: Union-find algo over all planes (over all 3 directions) to merge single cell faces into panels
