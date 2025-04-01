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
        f"Select courses for Student {student}",
        courses,
        key=f"student_courses_{student}"  # Changed to more unique key
    )

    # Validate input
    if not selected_courses:
        st.sidebar.error(f"Student {student}: Please select at least one course.")
        return [], []

    # Create edges between ALL pairs of courses (fully connected subgraph)
    edges = []
    for i in range(len(selected_courses)):
        for j in range(i + 1, len(selected_courses)):
            edges.append((selected_courses[i], selected_courses[j]))

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
    return df.map(lambda x: x.strip().title() if isinstance(x, str) and x.strip() else x)

def create_course_day_mapping(schedule):
    """
    Creates a mapping of courses to their scheduled days.

    Parameters:
    schedule (pandas.DataFrame): The schedule with days as columns

    Returns:
    dict: A dictionary mapping course names to lists of days
    """
    course_to_days = {}
    for day_col in schedule.columns:
        day_num = int(day_col.split(" ")[1])
        for course in schedule[day_col]:
            if course and course.strip():
                if course not in course_to_days:
                    course_to_days[course] = []
                course_to_days[course].append(day_num)
    return course_to_days

def main():
    """
    Main function to execute the program.
    """
    # Create the graph
    G = nx.Graph()
    G.add_nodes_from(COURSES)

    # Generate and add edges based on user input for each student
    # Store student course selections for conflict detection
    student_courses = {}
    for student in range(1, num_students + 1):
        selected_courses, edges = input_courses(student, COURSES)
        if selected_courses:  # Only add edges if courses are selected
            G.add_edges_from(edges)
            student_courses[f"Student {student}"] = selected_courses

    # Perform greedy coloring
    course_coloring = greedy_coloring(G)
    chromatic_number = max(course_coloring.values()) + 1

    # Display chromatic number with improved formatting
    st.markdown(f"<div style='padding: 10px; background-color: #007AE8; border-radius: 5px;'>"
                f"<h3 style='margin:0'>Minimum Required Days (Chromatic Number): {chromatic_number}</h3></div>",
                unsafe_allow_html=True)

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

    # Interactive Schedule Editor
    st.subheader("Interactive Schedule Editor")
    st.write("Manually adjust the schedule below. Note: A course can only be scheduled for one day.")

    # Initialize session state for edited schedule and original schedule
    if "edited_schedule" not in st.session_state:
        st.session_state.edited_schedule = schedule_table.copy()
        st.session_state.original_schedule = schedule_table.copy()

    # Initialize validation status if not present
    if "is_validated" not in st.session_state:
        st.session_state.is_validated = False

    # Initialize success message if not present
    if "success_message" not in st.session_state:
        st.session_state.success_message = ""

    # Update the edited schedule and original schedule if the schedule table changes
    if not hasattr(st.session_state, 'previous_schedule') or not st.session_state.previous_schedule.equals(schedule_table):
        st.session_state.edited_schedule = schedule_table.copy()
        st.session_state.original_schedule = schedule_table.copy()
        st.session_state.previous_schedule = schedule_table.copy()
        # Reset validation status and errors if schedule changes
        st.session_state.is_validated = False
        if "validation_errors" in st.session_state:
            del st.session_state.validation_errors

    # Store current validation status
    if "validation_errors" not in st.session_state:
        st.session_state.validation_errors = {}

    # Display validation errors if they exist (before the table)
    if st.session_state.validation_errors:
        st.error("Schedule Validation Failed 🚨")

        # Display detailed errors in a clear, bulleted list
        if "multi_day" in st.session_state.validation_errors:
            st.markdown("**Courses scheduled on multiple days:**")
            # Create a mapping of courses to their scheduled days for error display
            course_to_days = create_course_day_mapping(st.session_state.edited_schedule)
            for course in st.session_state.validation_errors["multi_day"]:
                days = ", ".join([f"Day {day}" for day in course_to_days[course]])
                st.markdown(f"- {course} is scheduled on {days}")

        if "student_conflicts" in st.session_state.validation_errors:
            st.markdown("**Student scheduling conflicts:**")
            for student, days in st.session_state.student_conflicts.items():
                for day, courses in days.items():
                    st.markdown(f"- {student} has multiple exams on Day {day}: {', '.join(courses)}")

        st.info("Please fix the highlighted conflicts by moving courses to different days.")

    # Apply styling for validation errors
    edited_df = st.session_state.edited_schedule.copy()

    # Display styled dataframe with conflicts highlighted if there are errors
    if st.session_state.validation_errors:
        # Get list of all courses with errors
        error_courses = []
        for error_type, courses in st.session_state.validation_errors.items():
            error_courses.extend(courses)

        # Define a row-wise function for styling
        def highlight_errors(row):
            styles = [''] * len(row)
            for i, val in enumerate(row):
                if val in error_courses:
                    styles[i] = 'background-color: #FF1F33'
            return styles

        # Apply styling to dataframe
        styled_df = edited_df.style.apply(highlight_errors, axis=1)

        # Display styled dataframe (read-only)
        st.write("Schedule with conflicts highlighted in red:")
        st.dataframe(styled_df)

    # Display the editable dataframe
    st.session_state.edited_schedule = st.data_editor(edited_df, num_rows="dynamic", key="schedule_editor")

    # Display success messages from previous actions if they exist
    if "success_message" in st.session_state and st.session_state.success_message:
        st.success(st.session_state.success_message)
        # Clear the message after displaying it once
        st.session_state.success_message = ""

    # Button row for schedule actions
    col1, col2, col3 = st.columns(3)

    # Apply Changes button
    with col1:
        if st.button("Apply Changes", key="apply", type="primary"):
            st.session_state.edited_schedule = capitalize_course_names(st.session_state.edited_schedule)
            st.session_state.validation_errors = {}  # Reset validation errors
            st.session_state.is_validated = False  # Reset validation status
            # Store the success message in session state instead of displaying it directly
            st.session_state.success_message = "Changes applied!"
            st.rerun()

    # Reset changes button
    with col2:
        if st.button("Reset Changes", key="reset"):
            st.session_state.edited_schedule = st.session_state.original_schedule.copy()
            st.session_state.validation_errors = {}  # Reset validation errors
            st.session_state.is_validated = False  # Reset validation status
            # Store the success message in session state instead of displaying it directly
            st.session_state.success_message = "Schedule reset to original version."
            st.rerun()

    # Validate button
    with col3:
        validate_button = st.button("Validate Schedule", key="validate", type="secondary")

    # Validate the edited schedule
    if validate_button:
        # Clear previous validation errors
        st.session_state.validation_errors = {}

        # Use the most up-to-date version of the edited schedule
        schedule_to_validate = st.session_state.edited_schedule

        # Create a mapping of courses to their scheduled days
        course_to_days = create_course_day_mapping(schedule_to_validate)

        # 1. Check for courses scheduled on multiple days
        multi_day_courses = []
        for course, days in course_to_days.items():
            if len(days) > 1:
                multi_day_courses.append(course)

        if multi_day_courses:
            st.session_state.validation_errors["multi_day"] = multi_day_courses

        # 2. Check for student conflicts (multiple exams on same day)
        student_conflicts = {}

        for student, courses in student_courses.items():
            # Get days for each of the student's courses
            for course in courses:
                if course in course_to_days:
                    # Check each day this course is scheduled
                    for day in course_to_days[course]:
                        # Find other courses for this student on the same day
                        same_day_courses = [c for c in courses if c in course_to_days and day in course_to_days[c] and c != course]

                        if same_day_courses:
                            if student not in student_conflicts:
                                student_conflicts[student] = {}

                            if day not in student_conflicts[student]:
                                student_conflicts[student][day] = []

                            # Add this course and conflicts to the list
                            conflict_set = set(same_day_courses + [course])
                            for c in conflict_set:
                                if c not in student_conflicts[student][day]:
                                    student_conflicts[student][day].append(c)

        # Store the conflicts in session state for display
        st.session_state.student_conflicts = student_conflicts

        # Collect all courses involved in student conflicts
        student_conflict_courses = []
        for student, days in student_conflicts.items():
            for day, courses in days.items():
                student_conflict_courses.extend(courses)

        if student_conflict_courses:
            st.session_state.validation_errors["student_conflicts"] = list(set(student_conflict_courses))

        # Display validation results
        if st.session_state.validation_errors:
            # Store error message in session state
            st.session_state.success_message = ""  # Clear any success message
            st.session_state.is_validated = False  # Mark as not validated
            st.error("Schedule validation failed. Please review the highlighted conflicts.")
            st.rerun()  # Rerun to display errors at the top
        else:
            # Store success message in session state
            st.session_state.success_message = "✅ Schedule is valid! No conflicts detected."
            st.session_state.is_validated = True  # Mark as validated
            st.rerun()  # Rerun to display the success message

    # Only show export button if schedule is validated
    if st.session_state.is_validated:
        if st.button("Export Schedule as CSV"):
            # Use the most recent edited schedule
            schedule_to_export = st.session_state.edited_schedule
            schedule_to_export.to_csv("course_schedule.csv", index=False)
            st.success("Schedule exported as course_schedule.csv")
            st.balloons()  # Optional: Add celebration effect

    # Visualize the graph
    st.subheader("Graph Visualization")
    visualize_graph(G, course_coloring, selected_layout, custom_colors, node_size, font_size)

if __name__ == "__main__":
    main()
