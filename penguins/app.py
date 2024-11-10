# Import necessary libraries
import plotly.express as px  # For creating interactive visualizations
from palmerpenguins import load_penguins  # To load the penguins dataset
from shiny.express import input, ui, render  # For creating the UI and handling user input
from shinywidgets import render_plotly  # For rendering Plotly plots
import seaborn as sns  # Not used in this code but useful for visualizations
from shiny import reactive  # To create reactive functions

# Load the penguins dataset into a variable
penguins = load_penguins()

# Set up the page options for the Shiny app
ui.page_opts(title="Penguins Data", fillable=True)

# Create a sidebar for user interaction
with ui.sidebar(position="right", bg="#f8f8f8", open="open"):
    ui.h2("Sidebar")  # Header for the sidebar

    # Dropdown menu for selecting an attribute to visualize
    ui.input_selectize(
        "selected_attribute",  # ID for the input
        "Select column to visualize",  # Label for the input
        choices=["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],  # Options
        selected="bill_length_mm"  # Default selected option
    )

    # Numeric input for specifying the number of bins in the histogram
    ui.input_numeric("plotly_bin_count", "Plotly bin numeric", 1, min=1, max=10)

    # Checkbox group for selecting species to filter the data
    ui.input_checkbox_group(
        "selected_species_list",  # ID for the input
        "Select a species",  # Label for the input
        choices=["Adelie", "Gentoo", "Chinstrap"],  # Species options
        selected=["Adelie"],  # Default selected option
        inline=True  # Display options inline
    )

    ui.hr()  # Horizontal line as a divider

# Main content area with visualizations
with ui.layout_columns():
    # Card for the Plotly Histogram
    with ui.card():
        ui.card_header("Plotly Histogram")  # Title for the card

        @render_plotly  # Decorator for rendering a Plotly plot
        def plotly_histogram():
            # Create and return a histogram based on user input
            return px.histogram(
                filtered_data(),  # Data to visualize
                x=input.selected_attribute(),  # X-axis attribute from user selection
                nbins=input.plotly_bin_count(),  # Number of bins for the histogram
                color="species"  # Color by species
            )

    # Card for the Data Table
    with ui.card():
        ui.card_header("Data Table")  # Title for the card

        @render.data_frame  # Decorator for rendering a data frame
        def data_table():
            # Return a DataTable of the filtered data
            return render.DataTable(filtered_data())

# Additional layout for more visualizations
with ui.layout_columns():
    # Card for the Plotly Scatterplot
    with ui.card():
        ui.card_header("Plotly Scatterplot: Species")  # Title for the card

        @render_plotly  # Decorator for rendering a Plotly plot
        def plotly_scatterplot():
            # Create and return a scatterplot based on the filtered data
            return px.scatter(
                data_frame=filtered_data(),  # Data to visualize
                x="body_mass_g",  # X-axis variable
                y="bill_depth_mm",  # Y-axis variable
                color="species",  # Color by species
                labels={"bill_depth_mm": "Bill Depth (mm)", "body_mass_g": "Body Mass (g)"}  # Custom labels
            )

    # Card for Summary Statistics
    with ui.card():
        ui.card_header("Summary Statistics")  # Title for the card

        @render.data_frame  # Decorator for rendering a data frame
        def summary_table():
            # Calculate summary statistics and return the result
            summary = penguins.describe()  # Get summary statistics
            return summary.reset_index()  # Reset index for better display

# Reactive function to filter data based on selected species
@reactive.calc  # This function will automatically update when inputs change
def filtered_data():
    selected_species = input.selected_species_list()  # Get selected species from user input
    # Return only the rows of penguins that match the selected species
    return penguins[penguins["species"].isin(selected_species)]