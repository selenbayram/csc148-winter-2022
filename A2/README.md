# Martian Robot Society

## Assignment 2 for CSC148H1 (Winter 2022) at the University of Toronto.  

<img width="647" alt="martian_robot_society" src="https://github.com/selenbayram/csc148-winter-2022/assets/113145976/4bb97889-8770-49c5-98c8-76d260f01ca9">

### Description

The program is a society management system modelling the organizational hierarchy of the Martian Robot Society using tree data structure.

Every robot in the Martian Robot Society is considered a citizen, represented by the nodes in the tree. 
Citizens have subordinate-superior relationships, i.e., one citizen may work under another. 
Some citizens are leaders of a specific district within the society, and citizens who work under a leader are considered part of that district.

_NOTE: The starter code is provided by the instructors and the copyright statement can be found at the beginning of each relevant file._

### Files
_NOTE: The file descriptions are adapted from the assignment handout provided by the instructors._

- **society_hierarchy.py:** Defines classes that keep track of information about the Martian robot society. 

- **society_ui.py:** Defines a graphical user interface for interacting with information about the Martian robot society.

- **client_code.py:** A layer of code that is between the UI and the back end in society_hierarchy.py.

- **citizens.csv:** A sample file describing a robot society hierarchy. (Use it to create a society for testing by: (a) uncommenting the soc = create_from_file_demo() line at the end of society_hierarchy.py, or (b) using the "Load society from file" button in the UI and choosing this file.)

- **a2_sample_test.py:** The test suite to test the code.
