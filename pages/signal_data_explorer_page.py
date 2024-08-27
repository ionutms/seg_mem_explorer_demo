"""
Signal Data Explorer Page for interactive signal data visualization and
analysis.

This module provides a Dash-based web application page for exploring and
visualizing signal data from CSV and ZIP files containing CSV data. It offers
an interactive interface for file upload, data selection, and dynamic plotting.

Key Features:
- File upload support for CSV and ZIP files containing CSV data
- Interactive selection of files, frames, records, and data channels
- Dynamic updating of data visualizations based on user selections
- Responsive layout using Dash Bootstrap Components
- Integrated signal processing utilities for data analysis
- Themeable interface with light and dark mode support

Components:
- File upload area for CSV and ZIP files
- Range sliders for selecting specific files, frames, records, and channels
- Interactive graph for data visualization
- Theme switch for toggling between light and dark modes

The page is designed to be part of a larger Dash application and is registered
as a page using the Dash pages plugin. It leverages various utility modules
for styling, component creation, and signal processing.

Usage:
1. Upload a CSV or ZIP file containing CSV data
2. Use range sliders to select specific portions of the data
3. Click 'View selected data' to update the visualization
4. Interact with the generated plot for detailed data exploration
5. Toggle between light and dark themes as needed

Dependencies:
- dash and its components (dcc, html, callback, etc.)
- dash_bootstrap_components
- Custom utility modules (style_utils, dash_component_utils,
  signal_processing_utils)

Note: This module is part of a larger application and relies on custom utility
functions and components defined in separate modules.
"""

from typing import Any, Dict, List, Tuple
from dash import html, dcc, register_page, callback, Input, Output, State
from dash import no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import pages.utils.style_utils as styles
import pages.utils.dash_component_utils as dcu
import pages.utils.signal_processing_utils as spu

link_name = __name__.rsplit('.', maxsplit=1)[-1].replace('_page', '').title()
module_name = __name__.rsplit('.', maxsplit=1)[-1]

register_page(__name__, name=link_name, order=2)


TITLE = "Signal Data Explorer"
ABOUT = (
    "The Signal Data Explorer is an advanced interactive web application "
    "designed for visualizing and analyzing complex signal data from ZIP "
    "files containing CSV data.",
    "It offers a powerful and user-friendly interface for exploring "
    "multi-channel, multi-segment signal data sets, allowing users to "
    "select and analyze specific portions of the data with precision.",
    "This tool is particularly effective for working with oscilloscope "
    "segmented memory data, enabling efficient analysis of long-duration "
    "captures with intermittent signals of interest across multiple channels.")

features = [
    "Support for ZIP files containing multiple CSV data files",
    "Interactive selection of files, frames (segments), records, and channels",
    "Multi-axis plotting capabilities for comparing different data channels",
    "Dynamic updating of data visualization based on user selections",
    "Responsive layout adapting to various screen sizes",
    "Integrated signal processing utilities for advanced data analysis",
    "Support for oscilloscope segmented memory data, allowing analysis "
    "of multiple waveform segments captured over extended time periods",
    "Customizable Y-axis placement for optimal data comparison",
    "Theme switching between light and dark modes for comfortable viewing"]

usage_steps = [
    "Upload a ZIP file containing CSV signal data using "
    "the drag-and-drop area or file selector.",
    "Use the range sliders to select specific files within the ZIP archive.",
    "Adjust the frames slider to navigate between "
    "different segments of the data.",
    "Use the records slider to focus on specific portions within each frame.",
    "Select the data channels you wish to "
    "visualize using the data sets slider.",
    "Customize the Y-axis placement for each channel using the radio buttons.",
    "Click the 'View selected data' button to generate the visualization.",
    "Interact with the multi-axis plot to explore "
    "relationships between channels.",
    "Use the zoom and pan tools to investigate areas of interest in detail.",
    "Toggle between light and dark themes for optimal viewing."]


MAIN_DIV_CHILDREN = [
    dbc.Row([dbc.Col([dcc.Link('Go back Home', href='/')])]),
    dbc.Row([dbc.Col([html.H3(
        f"{link_name.replace('_', ' ')}", style=styles.heading_3_style)])]),
    dbc.Row([dcu.app_description(TITLE, ABOUT, features, usage_steps)])]


layout = dbc.Container([
    html.Div(MAIN_DIV_CHILDREN, style=styles.GLOBAL_STYLE)], fluid=True)


file_upload_component = dcc.Upload(
    id=f'{module_name}_upload', children=[dbc.Row([dbc.Col(html.Div([
        "Drag and Drop or ", html.A("Select a zip with csv file(s)")
    ]), className="text-center")], className="align-items-center h-100")],
    style={
        'width': '100%', 'height': '60px', 'borderStyle': 'dashed',
        'borderRadius': '10px', 'borderWidth': '1px'}, multiple=False)
file_upload_row = dbc.Row([dbc.Col([file_upload_component, html.Hr()])])


file_selection_row = dbc.Row(id=f'{module_name}_files_row', children=[
    dcu.labeled_counter_trio(
        f'{module_name}_files', '0 files detected',
        limits={"min_count": 1, "max_count": 2}),
    dcu.labeled_range_slider(
        f'{module_name}_files', "Select which files to explore", [1])])

frames_selection_row = dbc.Row(id=f'{module_name}_frames_row', children=[
    dcu.labeled_counter_trio(
        f'{module_name}_frames', '0 frames detected',
        limits={"min_count": 1, "max_count": 2}),
    dcu.labeled_range_slider(
        f'{module_name}_frames', "Select which frames to explore", [1])])

records_selection_row = dbc.Row(id=f'{module_name}_records_row', children=[
    dcu.labeled_counter_quintet(
        id_section=f'{module_name}_records',
        label="0 records per-frame detected", default_count=1,
        limits={"min_count": 1, "max_count": 2}),
    dcu.labeled_range_slider(
        f'{module_name}_records',
        "Select a minimum number of records per-frame to explore", [0, 1], 0)])

data_sets_selection_row = dbc.Row(id=f'{module_name}_data_sets_row', children=[
    dcu.labeled_counter_trio(
        f'{module_name}_data_sets', '0 data sets detected',
        limits={"min_count": 2, "max_count": 3}, default_count=2),
    dcu.labeled_range_slider(
        f'{module_name}_data_sets', "Select which data sets to explore", [1])])

radioitems_row = dbc.Row([
    dbc.Col([dbc.Row(id="radioitems_row")], xs=12, md=9),

    dbc.Col([dbc.Row([
        dbc.Col([dbc.Card(id="group_legend_card", children=[
            dbc.Label("Group Legend", className=styles.CENTER_CLASS_NAME),
            dbc.Switch(
                id="legend_group_switch", value=False,
                className=styles.CENTER_CLASS_NAME)
        ], body=True, style={
            "border": "1px dashed", "border-radius": "10px", "display": "none",
            "padding": "1px", "background-color": "transparent"}),
            html.Br(),
        ], xs=12, md=6),

        dbc.Col([dbc.Card([
            dbc.Button(
                "View", id="view_data_button",
                className=styles.CENTER_CLASS_NAME)
        ], body=True, style={
            "border": "none", "background-color": "transparent",
            "padding-top": "10px", "padding-bottom": "10px"})
        ], xs=12, md=6)
    ])
    ], xs=12, md=3)
])


selection_row = dbc.Row([dbc.Col([dcc.Loading([
    file_selection_row, frames_selection_row, records_selection_row,
    data_sets_selection_row, radioitems_row], delay_show=2000), html.Hr()
])], id='selection_row', style={'display': 'none'})

graph_row = dbc.Row([dbc.Col([
    dcc.Store('filtering_store', data={}),
    dcc.Loading([dcc.Graph(id=f"{module_name}_data_graph")]),
    html.Hr()], id="graph_column", style={'display': 'none'})])

MAIN_DIV_CHILDREN.extend([file_upload_row, selection_row, graph_row])


dcu.callback_update_store_at_upload(
    f'{module_name}_files', f'{module_name}_upload', 'filtering_store',
    spu.count_csv_files_from_zip)

dcu.callback_update_store_at_upload(
    f'{module_name}_frames', f'{module_name}_upload', 'filtering_store',
    dcu.extract_info_from_zip_as_int, "FastFrame Count")

dcu.callback_update_store_at_upload(
    f'{module_name}_records', f'{module_name}_upload', 'filtering_store',
    dcu.extract_info_from_zip_as_int, "Record Length")

dcu.callback_update_store_at_upload(
    f'{module_name}_data_sets', f'{module_name}_upload', 'filtering_store',
    spu.extract_data_frame_from_zip_contents)


dcu.callbacks_radioitems(f'{module_name}_data_sets', "radioitems_row")


@callback(
    Output('group_legend_card', 'style'),
    Input(f"{module_name}_data_sets_range_slider", 'value'),
    State('group_legend_card', 'style'),
    prevent_initial_call=True
)
def set_group_legend_card_style(
    slider_value,
    style_state
):
    """TODO"""
    style_state['display'] = '' if len(slider_value) > 2 else 'none'
    return style_state


@callback(
    Output('filtering_store', 'data'),
    Input(f"{module_name}_files_range_slider", 'value'),
    Input(f"{module_name}_frames_range_slider", 'value'),
    Input(f"{module_name}_records_range_slider", 'value'),
    Input(f"{module_name}_data_sets_range_slider", 'value'),
    Input(f"{module_name}_records_range_slider", 'max'),
    Input(f"{module_name}_data_sets_range_slider", 'marks'),
    State(f'{module_name}_upload', 'contents'),
    State(f'{module_name}_upload', 'filename'),
    prevent_initial_call=True
)
def update_files_filtering_store_with_slider_values(
    files: List[int],
    frames: List[int],
    records_range: List[int],
    value: List[int],
    records_max: int,
    marks: Dict[str, str],
    contents: str,
    filename: str,
) -> Dict[str, Any]:
    """Update filtering store with slider values and file information.

    Args:
        files: List of selected file indices.
        frames: List of selected frame indices.
        records_range: Range of selected records.
        value: List of selected data set indices.
        records_max: Maximum number of records.
        marks: Dictionary of marks for data sets slider.
        contents: File contents.
        filename: Name of the uploaded file.

    Returns:
        Updated filtering dictionary or no_update if file is not a ZIP.
    """
    if filename.lower().endswith('.zip'):
        units_info = spu.extract_info_from_zip(
            contents, ["Horizontal Units", "Vertical Units"])
        horizontal_units, vertical_units = units_info.values()
        filtering = {
            "files_to_keep": [file - 1 for file in files],
            "frames_to_keep": [frame - 1 for frame in frames],
            "x_axis_data": marks[str(value[0])],
            "y_axis_data": [marks[str(position)] for position in value[1:]],
            "records_slice": records_range,
            "records_max": records_max,
            "Horizontal Units": horizontal_units,
            "Vertical Units": vertical_units
        }
        return filtering
    return no_update


@callback(
    Output('selection_row', 'style'),
    Output("graph_column", 'style', allow_duplicate=True),
    Input(f'{module_name}_upload', 'filename'),
    prevent_initial_call=True
)
def toggle_file_selection_visibility(
    filename: str
) -> Dict[str, str]:
    """Toggle visibility of file selection div based on uploaded file type.

    This callback function shows or hides the file selection div
    depending on whether a ZIP file is uploaded.

    Args:
        filename: Name of the uploaded file.

    Returns:
        Dictionary controlling file selection div visibility.

    Raises:
        PreventUpdate: If the uploaded file is neither CSV nor ZIP.
    """
    if filename.lower().endswith('.zip'):
        return {'display': ''}, {'display': 'none'}

    return {'display': 'none'}, {'display': 'none'}


@callback(
    Output(f"{module_name}_data_graph", 'figure'),
    Output("graph_column", 'style'),
    Input("view_data_button", "n_clicks"),
    Input('theme_switch_value_store', 'data'),
    State(f'{module_name}_upload', 'contents'),
    State(f'{module_name}_upload', 'filename'),
    State('filtering_store', 'data'),
    prevent_initial_call=True
)
def update_graph_with_uploaded_file(
    _view_data_button: int,
    theme_switch: bool,
    contents: str,
    filename: str,
    filtering: Dict[str, Any],
) -> Tuple[Any, Dict[str, str]]:
    """
    Update the graph with the contents of the uploaded file.

    Args:
        _view_data_button: Number of clicks on the view data button (unused).
        theme_switch: Boolean indicating the theme switch state.
        contents: Contents of the uploaded file.
        filename: Name of the uploaded file.
        filtering: Dictionary containing filtering options.

    Returns:
        A tuple containing the updated figure and its style.

    Raises:
        PreventUpdate:
            If no file is uploaded or the file type is not supported.
    """
    if filename is None:
        raise PreventUpdate

    file_extension = filename.lower().split('.')[-1]

    if file_extension == 'zip':
        figure = spu.plot_selected_zip_contents(
            contents, filename, filtering, theme_switch)
        return figure, {'display': ''}

    return no_update, no_update


dcu.callback_update_range_slider_max_and_label(
    f'{module_name}_files', f'{module_name}_upload')
dcu.callback_labeled_counter_trio(f'{module_name}_files')
dcu.callback_update_range_slider_value(f'{module_name}_files')

dcu.callback_update_range_slider_max_and_label(
    f'{module_name}_frames', f'{module_name}_upload')
dcu.callback_labeled_counter_trio(f'{module_name}_frames')
dcu.callback_update_range_slider_value(f'{module_name}_frames')

dcu.callback_update_range_slider_max_and_label(
    f'{module_name}_records', f'{module_name}_upload')
dcu.callback_labeled_counter_quintet(f'{module_name}_records', resolution=1)
dcu.callback_update_range_slider_pushable_and_value(f'{module_name}_records')

dcu.callback_update_range_slider_max_and_label(
    f'{module_name}_data_sets', f'{module_name}_upload', reset_value=2)
dcu.callback_labeled_counter_trio(f'{module_name}_data_sets')
dcu.callback_update_range_slider_value(f'{module_name}_data_sets', 0)
