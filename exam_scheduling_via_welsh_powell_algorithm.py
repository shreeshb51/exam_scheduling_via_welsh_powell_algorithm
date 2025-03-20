import streamlit as st
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
from typing import List, Tuple, Dict
from matplotlib.colors import CSS4_COLORS  # To convert color names to hex codes

# Constants
COURSES = [
    "Math", "Science", "History", "English", "Art", "Music", "Geography", "Biology",
    "Chemistry", "Physics", "Economics", "Philosophy", "Sociology", "Psychology",
    "Physical Education", "Literature", "Computer Science", "Business Studies", "Dance", "Soccer", "Driving"
]

# Convert color names to hex codes
DEFAULT_COLORS = [CSS4_COLORS[color_name] for color_name in [
    'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque',
    'blanchedalmond', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse',
    'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue',
    'darkcyan', 'darkgoldenrod', 'darkgray', 'darkkhaki', 'darkmagenta', 'darkolivegreen',
    'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue',
    'darkslategray', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray',
    'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
    'ghostwhite', 'gold', 'goldenrod', 'lightgray', 'lightgreen', 'greenyellow'
]]

# Streamlit App Title
st.title("Exam Scheduling via Welsh Powell Algorithm")

# Sidebar for user input
st.sidebar.header("Input Parameters")
num_students = st.sidebar.number_input("Enter the number of students", min_value=1, max_value=20, value=1)

# Node and Font Size Customization
st.sidebar.subheader("Node and Font Size")
node_size = st.sidebar.slider("Node Size", min_value=10, max_value=50, value=20)
font_size = st.sidebar.slider("Font Size", min_value=8, max_value=20, value=10)

def input_courses(student: int, courses: List[str]) -> Tuple[List[str], List[Tuple[str, str]]]:
    """
    Prompts the user to input courses for a student and creates cyclic edges between them.

    Args:
        student (int): The student number.
        courses (List[str]): List of available courses.

    Returns:
        Tuple[List[str], List[Tuple[str, str]]]: A tuple containing the selected courses and the edges created.
    """
    st.sidebar.subheader(f"Student {student}")
    selected_courses = st.sidebar.multiselect(
        f"Select courses for Student {student}", courses, key=f"student_{student}"
    )

    # Validate input
    if not selected_courses:
        st.sidebar.error("Please select at least one course.")
        return [], []

    # Create cyclic edges for multiple courses
    edges = [(selected_courses[i], selected_courses[i + 1]) for i in range(len(selected_courses) - 1)]
    if len(selected_courses) > 1:
        edges.append((selected_courses[-1], selected_courses[0]))  # Add cyclic edge

    return selected_courses, edges

def greedy_coloring(graph: nx.Graph) -> Dict[str, int]:
    """
    Applies the greedy coloring algorithm (Welsh Powell) to the graph.

    Args:
        graph (nx.Graph): The graph to be colored.

    Returns:
        Dict[str, int]: A dictionary mapping each node to its assigned color.
    """
    return nx.coloring.greedy_color(graph, strategy="largest_first")

def create_schedule_table(coloring: Dict[str, int]) -> pd.DataFrame:
    """
    Creates a table showing the schedule of courses by day.

    Args:
        coloring (Dict[str, int]): A dictionary mapping each course to its assigned day.

    Returns:
        pd.DataFrame: A DataFrame representing the schedule.
    """
    schedule = {}
    for course, day in coloring.items():
        day_name = f"Day {day + 1}"
        if day_name not in schedule:
            schedule[day_name] = []
        schedule[day_name].append(course)

    # Convert to DataFrame
    max_courses = max(len(courses) for courses in schedule.values())
    for day in schedule:
        schedule[day] += [""] * (max_courses - len(schedule[day]))

    return pd.DataFrame(schedule)

def visualize_graph(graph: nx.Graph, coloring: Dict[str, int], layout: str, custom_colors: List[str], node_size: int, font_size: int):
    """
    Visualizes the graph with node colors based on the greedy coloring result using Plotly.

    Args:
        graph (nx.Graph): The graph to be visualized.
        coloring (Dict[str, int]): A dictionary mapping each node to its assigned color.
        layout (str): The layout to use for the graph.
        custom_colors (List[str]): List of custom colors for each day.
        node_size (int): Size of the nodes.
        font_size (int): Size of the font for node labels.
    """
    if layout == "Spring":
        pos = nx.spring_layout(graph)
    elif layout == "Circular":
        pos = nx.circular_layout(graph)
    elif layout == "Kamada-Kawai":
        pos = nx.kamada_kawai_layout(graph)

    edge_traces = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_traces.append(go.Scatter(
            x=[x0, x1], y=[y0, y1],
            mode="lines",
            line=dict(width=0.5, color="gray"),
            hoverinfo="none"
        ))

    node_trace = go.Scatter(
        x=[pos[course][0] for course in graph.nodes()],
        y=[pos[course][1] for course in graph.nodes()],
        mode="markers+text",
        text=[f"{course} (Day {coloring[course] + 1})" for course in graph.nodes()],
        marker=dict(
            size=node_size,
            color=[custom_colors[coloring[course] % len(custom_colors)] for course in graph.nodes()],
            line=dict(width=2, color="black")
        ),
        textposition="top center",
        hoverinfo="text",
        textfont=dict(size=font_size)
    )

    fig = go.Figure(data=edge_traces + [node_trace], layout=go.Layout(
        showlegend=False,
        hovermode="closest",
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    ))

    st.plotly_chart(fig, use_container_width=True)

def capitalize_course_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Capitalizes all course names in the schedule table.

    Args:
        df (pd.DataFrame): The schedule table.

    Returns:
        pd.DataFrame: The schedule table with capitalized course names.
    """
    return df.applymap(lambda x: x.strip().title() if isinstance(x, str) and x.strip() else x)

def main():
    """
    Main function to execute the program.
    """
    # Create the graph
    G = nx.Graph()
    G.add_nodes_from(COURSES)

    # Generate and add edges based on user input for each student
    for student in range(1, num_students + 1):
        selected_courses, edges = input_courses(student, COURSES)
        if selected_courses:  # Only add edges if courses are selected
            G.add_edges_from(edges)

    # Perform greedy coloring
    course_coloring = greedy_coloring(G)
    chromatic_number = max(course_coloring.values()) + 1
    st.write(f"The chromatic number (minimum number of days) is: {chromatic_number}")

    # Dynamic Color Mapping based on chromatic number
    st.sidebar.subheader("Customize Colors")
    custom_colors = []
    for i in range(chromatic_number):
        color = st.sidebar.color_picker(f"Color for Day {i + 1}", DEFAULT_COLORS[i % len(DEFAULT_COLORS)])
        custom_colors.append(color)

    # Graph Layout Options
    st.sidebar.subheader("Graph Layout")
    layout_options = ["Spring", "Circular", "Kamada-Kawai"]
    selected_layout = st.sidebar.selectbox("Choose a layout", layout_options)

    # Create and display the schedule table
    st.subheader("Course Schedule by Day")
    schedule_table = create_schedule_table(course_coloring)
    st.table(schedule_table)

    # Export functionality
    if st.button("Export Schedule as CSV"):
        schedule_table.to_csv("course_schedule.csv", index=False)
        st.success("Schedule exported as course_schedule.csv")

    # Interactive Schedule Editor
    st.subheader("Interactive Schedule Editor")
    st.write("Manually adjust the schedule below. Note: A course can only be scheduled for one day.")
    
    # Initialize session state for edited schedule
    if "edited_schedule" not in st.session_state:
        st.session_state.edited_schedule = schedule_table.copy()

    # Update the edited schedule if the schedule table changes
    if not st.session_state.edited_schedule.equals(schedule_table):
        st.session_state.edited_schedule = schedule_table.copy()

    # Display the editable table
    edited_schedule = st.data_editor(st.session_state.edited_schedule, num_rows="dynamic")

    # Reprocess the edited schedule to capitalize course names
    if st.button("Apply Changes"):
        edited_schedule = capitalize_course_names(edited_schedule)
        st.session_state.edited_schedule = edited_schedule
        st.success("Changes applied! Course names have been capitalized.")

    # Display the updated schedule
    if "edited_schedule" in st.session_state:
        st.write("Updated Schedule:")
        st.table(st.session_state.edited_schedule)

    # Validate the edited schedule
    if st.button("Validate Schedule"):
        validation_errors = []
        schedule_to_validate = st.session_state.edited_schedule
        for day, courses in schedule_to_validate.items():
            for course in courses:
                if course and schedule_to_validate.apply(lambda col: col[col == course].count()).sum() > 1:
                    validation_errors.append(f"Course '{course}' is scheduled for multiple days.")
        if validation_errors:
            for error in validation_errors:
                st.error(error)
        else:
            st.success("Schedule is valid!")

    # Visualize the graph
    st.subheader("Graph Visualization")
    visualize_graph(G, course_coloring, selected_layout, custom_colors, node_size, font_size)

if __name__ == "__main__":
    main()