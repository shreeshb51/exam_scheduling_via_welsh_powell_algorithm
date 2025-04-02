# Exam Scheduling via Welsh Powell Algorithm

## Project Description
A Streamlit web application that solves the exam scheduling problem using graph coloring techniques. This tool helps educational institutions optimize their examination timetables by scheduling exams in the minimum number of days while ensuring no student has multiple exams on the same day. The application uses the Welsh Powell Algorithm (a greedy graph coloring approach) to find an efficient solution to this classic constraint satisfaction problem.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Methodology](#methodology)
  - [Problem Formulation](#problem-formulation)
  - [Welsh Powell Algorithm](#welsh-powell-algorithm)
  - [Process Flow](#process-flow)
- [Examples](#examples)
- [References](#references)
- [Dependencies](#dependencies)
- [Algorithms/Mathematical Concepts Used](#algorithmsmathematical-concepts-used)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation
To set up the project locally, follow these steps:

1. Install individual packages:
   ```bash
   pip install streamlit==1.24.0
   pip install networkx==3.1
   pip install plotly==5.15.0
   pip install pandas==2.0.3
   pip install matplotlib==3.7.2
   ```

3. Run the Streamlit application:
   ```bash
   streamlit run exam_scheduling_via_welsh_powell_algorithm.py
   ```

## Usage
1. Access the application through your web browser (typically at http://localhost:8501 when run locally).

2. Use the sidebar to configure input parameters:
   - Enter the number of students
   - Select courses for each student
   - Customize node and font sizes for the graph visualization
   - Choose colors for each exam day
   - Select a graph layout (Spring, Circular, or Kamada-Kawai)

3. The application will automatically:
   - Generate a conflict graph where courses are nodes and edges represent conflicts
   - Calculate the minimum number of days required (**Chromatic Number**)
   - Create an initial schedule table
   - Visualize the graph with colors representing different days

4. Interactive features:
   - Edit the generated schedule in the interactive editor
   - Validate the schedule to check for conflicts
   - Apply or reset changes as needed
   - Export the final schedule as a CSV file

## Features

### Core Functionality

- **Minimum Day Calculation**: Uses graph coloring principles to determine the theoretically optimal number of days required to schedule all exams without conflicts
- **Interactive Conflict Graph**: Visualizes relationships between courses, providing intuitive understanding of scheduling constraints
- **Automated Schedule Generation**: Creates an initial valid schedule based on the Welsh Powell algorithm

### User Interface and Interaction

- **Dynamic Input Controls**: Adjustable parameters for student count, course selection, and visualization preferences
- **Interactive Schedule Editor**: Full-featured data editor allowing manual refinement of the generated schedule
- **Real-time Validation**: Immediate feedback on schedule validity with clear error identification and highlighting

### Schedule Management

- **Conflict Detection**: Sophisticated validation system that identifies:
  - Courses scheduled on multiple days
  - Students having to take multiple exams on the same day
- **State Preservation**: Maintains schedule state between validation attempts and modifications
- **Export Functionality**: Exports the final validated schedule as a CSV file for integration with other systems

### Visualization and UI

- **Customizable Graph Display**: Adjustable node sizes, font sizes, and color schemes
- **Multiple Layout Algorithms**: Options for Spring, Circular, and Kamada-Kawai layouts to optimize graph readability
- **Color-coded Feedback**: Clear highlighting of conflicts using red backgrounds in the schedule table
- **Success Indicators**: Visual confirmation of successful validation with appropriate status messages

## Methodology

### Problem Formulation

The exam scheduling problem can be formally defined as follows:

1. **Input**:
   - A set of courses C = {c₁, c₂, ..., cₙ}
   - A set of students S = {s₁, s₂, ..., sₘ}
   - A registration matrix R where R[i,j] = 1 if student sᵢ is registered for course cⱼ, and 0 otherwise

2. **Constraints**:
   - No student should have multiple exams scheduled on the same day
   - Each course must be scheduled for exactly one day

3. **Objective**:
   - Minimize the number of days required to schedule all exams

4. **Graph Representation**:
   - Courses are represented as vertices in an undirected graph G = (V, E)
   - An edge (cᵢ, cⱼ) exists if there is at least one student registered for both courses cᵢ and cⱼ
   - This creates a "conflict graph" where connected vertices (courses) cannot be scheduled on the same day

### Welsh Powell Algorithm

The Welsh Powell algorithm is a greedy approach to graph coloring that follows these steps:

1. **Order the vertices** by degree (number of connections) in descending order: V' = {v₁, v₂, ..., vₙ} where degree(vᵢ) ≥ degree(vᵢ₊₁)

2. **Assign the first color** (Day 1):
   - Color the first vertex v₁
   - Iterate through the remaining vertices in order
   - Color each vertex that is not adjacent to any previously colored vertex with the same color

3. **Repeat with a new color** for the remaining uncolored vertices until all vertices are colored

4. **The number of colors used** (equal to the highest color index assigned) represents the chromatic number of the graph, which corresponds to the minimum number of days required for scheduling

### Process Flow

The application follows this detailed process flow:

1. **Data Collection**:
   - Gather student course registrations through the user interface
   - Construct the conflict graph based on shared course enrollments

2. **Initial Schedule Generation**:
   - Apply the Welsh Powell algorithm to the conflict graph
   - Determine the chromatic number (minimum required days)
   - Assign each course to its corresponding day based on its color

3. **Visualization**:
   - Render the conflict graph with color-coded nodes
   - Display the initial schedule in a tabular format

4. **Schedule Refinement**:
   - Enable manual adjustments through the interactive editor
   - Validate modifications against the original constraints
   - Highlight conflicts for resolution

5. **Finalization**:
   - Export the validated schedule to CSV format
   - Provide visual confirmation of successful scheduling

## Examples

### Sample Input
1. Set number of students to 2
2. For Student 1, select: Math, Physics, Computer Science
3. For Student 2, select: Physics, Chemistry, Biology

### Expected Output
- A conflict graph showing connections between courses
- A schedule with minimum days (typically 2 days in this example)
- Day 1: Math, Chemistry, Biology
- Day 2: Physics, Computer Science

[Example in PDF format depicting the notification of conflict in the schedule](exam_scheduling_via_welsh_powell_algorithm_HANDLING_CONFLICT.pdf)

[Example in PDF format depicting the validation of the schedule edited by the user](exam_scheduling_via_welsh_powell_algorithm_VALIDATING_EDITED_SCHEDULE.pdf.pdf)

[Example in PDF format depicting the user's choice to export the edited schedule as a CSV file](exam_scheduling_via_welsh_powell_algorithm_EXPORTING_CSV.pdf)

## References

1. Welsh, D. J. A., & Powell, M. B. (1967). An upper bound for the chromatic number of a graph and its application to timetabling problems. *The Computer Journal*, 10(1), 85-86. https://doi.org/10.1093/comjnl/10.1.85

2. Lewis, R. (2016). *A Guide to Graph Coloring: Algorithms and Applications*. Springer International Publishing. https://doi.org/10.1007/978-3-319-25730-3

3. Burke, E. K., & Petrovic, S. (2002). Recent research directions in automated timetabling. *European Journal of Operational Research*, 140(2), 266-280. https://doi.org/10.1016/S0377-2217(02)00069-3

4. Qu, R., Burke, E. K., McCollum, B., Merlot, L. T., & Lee, S. Y. (2009). A survey of search methodologies and automated system development for examination timetabling. *Journal of Scheduling*, 12(1), 55-89. https://doi.org/10.1007/s10951-008-0077-5

5. Carter, M. W., & Laporte, G. (1996). Recent developments in practical examination timetabling. In *Practice and Theory of Automated Timetabling* (pp. 3-21). Springer, Berlin, Heidelberg. https://doi.org/10.1007/3-540-61794-9_50

## Dependencies

- **Streamlit (v1.24.0+)**: Web application framework that provides the interactive user interface
  - Primary component for UI elements, data input, and state management
  - [Documentation](https://docs.streamlit.io/)

- **NetworkX (v3.1+)**: Graph theory library that implements the Welsh Powell algorithm
  - Handles graph creation, analysis, and coloring algorithms
  - [Documentation](https://networkx.org/documentation/stable/)

- **Plotly (v5.15.0+)**: Interactive visualization library for the conflict graph
  - Creates responsive, detailed graph visualizations
  - [Documentation](https://plotly.com/python/)

- **Pandas (v2.0.3+)**: Data manipulation library for managing schedule data
  - Provides DataFrame structures for schedule representation and manipulation
  - [Documentation](https://pandas.pydata.org/docs/)

- **Matplotlib (v3.7.2+)**: Visualization support for color management
  - Handles color conversion and management through CSS4_COLORS
  - [Documentation](https://matplotlib.org/stable/index.html)

## Algorithms/Mathematical Concepts Used

### Graph Coloring Theory

- **Chromatic Number**: The minimum number of colors needed to color a graph such that no adjacent vertices share the same color. Mathematically denoted as χ(G) for a graph G.
  - In our application: The minimum number of days required for exam scheduling

- **Independent Set**: A set of vertices in a graph where no two vertices are adjacent
  - In our application: Courses that can be scheduled on the same day

- **Vertex Degree**: The number of edges connected to a vertex
  - In our application: The number of conflicts a course has with other courses

### Welsh Powell Algorithm (Detailed)

1. **Initialization**:
   - Let G = (V, E) be the conflict graph
   - Let n be the number of vertices |V|
   - Let C = {} be the set of colors assigned

2. **Vertex Ordering**:
   - Sort vertices by degree in descending order: V' = {v₁, v₂, ..., vₙ} 
   - Where degree(vᵢ) ≥ degree(vᵢ₊₁) for all i ∈ {1, 2, ..., n-1}

3. **Coloring Process**:
   - For each color k = 0, 1, 2, ... until all vertices are colored:
     - Initialize set S = {}
     - For each uncolored vertex v in V' (in order):
       - If v is not adjacent to any vertex in S:
         - Add v to S
         - Assign color k to v: C(v) = k
     - Increment k

4. **Result**:
   - The number of colors used is max(C) + 1
   - The coloring C maps each vertex to its assigned color

### Time Complexity Analysis

- **Sorting vertices by degree**: O(|V|·log|V|)
- **Coloring process**: O(|V|²)
- **Overall worst-case time complexity**: O(|V|²)
  - Where |V| is the number of vertices (courses)

### Graph Layouts

- **Spring Layout (Force-Directed)**:
  - Models the graph as a physical system where edges are springs
  - Minimizes edge crossings and distributes vertices evenly
  - Mathematical basis: Force-directed algorithms solving for minimal energy state
  - Implementation: `nx.spring_layout(graph)`

- **Circular Layout**:
  - Places vertices evenly on a circle
  - Useful for visualizing overall connectivity patterns
  - Implementation: `nx.circular_layout(graph)`

- **Kamada-Kawai Layout**:
  - Energy minimization approach based on graph-theoretic distances
  - Attempts to preserve graph-theoretic distances in the visual layout
  - Based on solving a system of partial differential equations
  - Implementation: `nx.kamada_kawai_layout(graph)`

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NetworkX library developers for their implementation of graph algorithms
- Streamlit team for creating an intuitive framework for interactive data applications
- The academic community for extensive research on graph coloring applications in scheduling
- Early users and testers who provided valuable feedback for improving the application
