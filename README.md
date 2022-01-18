# Simple VLSI solvers

University (UniBo) project about Combinatorial Decision Making and Optimization.  
The goal and all the specification of the project are written in detail in the file CDMO_Project_2021.pdf  

The aim is to place some blocks (given width and height) in a rectangle (silicon chip), minimizing its height (not with the SAT-solver).  
Given a file in the following format:
```
maximum width of the rectangle
number of blocks
[list of width and height of the blocks]
```
the solvers return:
```
maximum width and height of the rectangle
number of blocks
[list of width and height of the blocks and their position (x and y coordinate of the bottom-left corner)]
```

The height is minimized in the **minizinc** and in the **SMT** proposal. The **SAT** solver only place the blocks given the height of the rectangle.
