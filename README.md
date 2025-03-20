# Exam Scheduling via Welsh Powell Algorithm

## Overview
This project models exam scheduling as a graph coloring problem. It uses the Welsh Powell algorithm to assign exams to days such that no two exams attended by the same student are scheduled on the same day. The project is implemented as an interactive web application using Streamlit, allowing users to input data, visualize the scheduling graph, and interactively edit the schedule.

## Features
	•	Input: Users can input the number of students and their selected courses.
	•	Graph Construction: Creates a graph where nodes represent courses and edges represent conflicts (courses taken by the same student).
	•	Coloring: Applies the Welsh Powell algorithm to assign days to courses.
	•	Visualization: Displays the graph with nodes colored according to their assigned day.
	•	Interactive Schedule Editor: Allows users to manually adjust the schedule and validate it.
	•	Export: Exports the schedule as a CSV file.

## Methodology
	✓	Graph Creation:
	      	⁃	Each course is represented as a node in the graph.
	      	⁃	Edges are added between courses taken by the same student to represent conflicts.
	✓	Graph Coloring:
	      	⁃	The Welsh Powell algorithm is used to color the graph, ensuring that no two connected nodes (conflicting courses) share the same color.
	      	⁃	Each color represents a unique day for scheduling.
	✓	Visualization:
	      	⁃	The graph is visualized using Plotly, with nodes colored according to their assigned day.
	      	⁃	Users can customize node size, font size, and graph layout.
	✓	Interactive Editing:
	      	⁃	Users can manually edit the schedule in an interactive table.
	      	⁃	Course names are automatically capitalized for consistency.
	      	⁃	The schedule is validated to ensure no course is scheduled for multiple days.

## Usage

### Input
	⁃	Number of Students: Enter the number of students in the sidebar.
	⁃	Courses per Student: For each student, select their courses from the dropdown menu.

### Output
	⁃	Schedule Table: Displays the courses assigned to each day.
	⁃	Graph Visualization: Shows the graph with nodes colored by day.
	⁃	Interactive Editor: Allows manual editing of the schedule.
	⁃	Validation: Validates the schedule to ensure no conflicts.

### Customization
	⁃	Node Size: Adjust the size of nodes in the graph.
	⁃	Font Size: Adjust the size of labels on nodes.
	⁃	Graph Layout: Choose between Spring, Circular, and Kamada-Kawai layouts.
	⁃	Colors: Customize the colors for each day.


## How to Run the Code
	1.	Install Dependencies:
		-> Ensure you have the following Python libraries installed:
			-> pip install streamlit networkx plotly pandas matplotlib 
	2.	Run the App: 
		-> Save the code in a file named app.py and run it using Streamlit: 
			-> streamlit run app.py 
	3.	Interact with the App:
		-> Open the app in your web browser.
		-> Follow the instructions in the sidebar to input data and customize the visualization.
		-> Use the interactive editor to adjust the schedule and validate it.
