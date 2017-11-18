# Author: Ping-Jung Liu
# Date: October 14th 2017
# COSC 76 Assignment 4: Constraints Satisfaction Problems
# Acknowledgement: Professor Devin Balkom for providing suggestions 

###README###

Files in this directory:

- csp.pdf

- csp.md

- CSP.py

- mapCSP.py

- circuitCSP.py

- sudokuCSP.py

- new_circuitCSP.py

#######################################################
To control heuristics and inference
#######################################################
- Open CSP.py and go to line 26 - 29

- MRV is minimum remaining value, LCV is least constraining value, MAC is maintain arc consistency,
  the last one runs AC3 on all arcs before search

- For map color and two versions of circuit boards, MRV with Enforced_AC should be good enough.
  Turning on MAC3 might even cause more computational time.

- For sudoku, turn on MAC3 for best results. MRV does an ok job as well.


