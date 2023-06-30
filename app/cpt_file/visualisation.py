from math import floor
import math
import numpy as np
from munch import Munch, unmunchify
from plotly import graph_objects as go
from plotly.subplots import make_subplots
from viktor.geo import GEFData, SoilLayout

from .soil_layout_conversion_functions import (
    Classification,
    convert_input_table_field_to_soil_layout,
    filter_nones_from_params_dict,
)

def visualise_cpt(cpt_params: Munch):

    # parse input file and user input
    classification = Classification(cpt_params.classification)
    cpt_params = unmunchify(cpt_params)
    parsed_cpt = GEFData(filter_nones_from_params_dict(cpt_params))
    soil_layout_original = SoilLayout.from_dict(cpt_params["soil_layout_original"])
    soil_layout_user = convert_input_table_field_to_soil_layout(
        bottom_of_soil_layout_user=cpt_params["bottom_of_soil_layout_user"],
        soil_layers_from_table_input=cpt_params["soil_layout"],
        soils=classification.soil_mapping,
    )

    # Create plotly figure
    fig = make_subplots(
        rows=1,
        cols=3,
        shared_yaxes=True,
        horizontal_spacing=0.00,
        column_widths=[3.5, 1.5, 2],
        subplot_titles=("Cone Resistance", "Friction ratio", "Soil Layout")
    )

    # add left side of the figure: Qc and Rf plot
    fig.add_trace(  # Add the qc curve
        go.Scatter(
            name="Cone Resistance",
            x=parsed_cpt.qc,
            y=[el * 1e-3 for el in parsed_cpt.elevation],
            mode="lines",
            line=dict(color="mediumblue", width=1),
            legendgroup="Cone Resistance",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(  # Add the Rf curve
        go.Scatter(
            name="Friction ratio",
            x=[rfval * 100 if rfval else rfval for rfval in parsed_cpt.Rf],
            y=[el * 1e-3 if el else el for el in parsed_cpt.elevation],
            mode="lines",
            line=dict(color="red", width=1),
            legendgroup="Friction ratio",
        ),
        row=1,
        col=2,
    )

    # add the bars on the right side of the plot
    add_soil_layout_to_fig(fig, soil_layout_original, soil_layout_user)

    # plot phreatic level
    fig.add_hline(
        y=cpt_params["ground_water_level"],
        line=dict(color="Blue", dash="dash", width=1),
        row="all",
        col="all",
    )

    update_fig_layout(fig, parsed_cpt)
    return fig

def visualise_pile(cpt_params: Munch, PILE_params: Munch):
    # parse input file and user input
    classification = Classification(cpt_params.classification)
    PILE_params = unmunchify(PILE_params)
    cpt_params = unmunchify(cpt_params)

    load = PILE_params["Load"]

    parsed_cpt = GEFData(filter_nones_from_params_dict(cpt_params))
    soil_layout_original = SoilLayout.from_dict(cpt_params["soil_layout_original"])
    soil_layout_user = convert_input_table_field_to_soil_layout(
        bottom_of_soil_layout_user=cpt_params["bottom_of_soil_layout_user"],
        soil_layers_from_table_input=cpt_params["soil_layout"],
        soils=classification.soil_mapping,
    )

    qc = [q for q in parsed_cpt.qc]
    Shaft = [138 * (1 - math.exp(-0.21)) * q for q in parsed_cpt.qc]
    # window_size = 1.5 * cpt_params.PILE.Diameter*100
    window_size = 150
    Base = [sum(qc[i:i + window_size]) / window_size for i in range(len(qc) - window_size + 1)]
    Overall = Shaft + Base

    # closest_bearing_strength = min(parsed_results["Bearing Strength GT1B"], key=lambda x: abs(x - max_rz))
    # index_closest_bearing_strength = parsed_results["Bearing Strength GT1B"].index(closest_bearing_strength)
    # required_pile_tip_level = parsed_results["Depth"][index_closest_bearing_strength]

    # Create plotly figure
    fig = make_subplots(
        rows=1,
        cols=3,
        shared_yaxes=True,
        horizontal_spacing=0.2,
        column_widths=[0.3, 0.3, 0.3],
        subplot_titles=("Ultimate Shaft Resistance", "Ultimate Base Resistance", "Overall Pile Capacity"),
    )

    fig.add_trace(  # Add the shaft
        go.Scatter(
            name="Ultimate Shaft Resistance",
            x=Shaft,
            y=[el * 1e-3 for el in parsed_cpt.elevation],
            mode="lines",
            line=dict(color="mediumblue", width=1),
            legendgroup="Ultimate Shaft Resistance",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(  # Add base
        go.Scatter(
            name="Ultimate Base Resistance",
            x=Base,
            y=[el * 1e-3 for el in parsed_cpt.elevation],
            mode="lines",
            line=dict(color="red", width=1),
            legendgroup="Ultimate Base Resistance",
        ),
        row=1,
        col=2,
    )

    fig.add_trace(  # Add base
        go.Scatter(
            name="Overall pile capacity",
            x=Overall,
            y=[el * 1e-3 for el in parsed_cpt.elevation],
            mode="lines",
            line=dict(color="orange", width=1),
            legendgroup="Overall pile capacity",
        ),
        row=1,
        col=3,
    )

    fig.add_trace(
        go.Scatter(
            name="Reaction Load",
            x=cpt_params["Load"] * np.ones(100),
            y=np.linspace(min(el * 1e-3 for el in parsed_cpt.elevation), 0, 100),
            mode="lines",
            line=dict(color="black", width=1),
            legendgroup="Overall pile capacity",
        ),
        row=1,
        col=3,
    )
    fig.add_trace(
        go.Scatter(
            name="Required Pile Tip Level",
            x=np.linspace(0, max(Overall), 100),
            y=cpt_params["ground_water_level"] * np.ones(100),
            mode="lines",
            line=dict(color="black", width=2),
        ),
        row=1,
        col=3,
    )
    update_pile_fig_layout(fig, parsed_cpt)
    return fig

def update_pile_fig_layout(fig, parsed_cpt):
    """Updates layout of the figure and formats the grids"""
    fig.update_layout(barmode="stack", template="plotly_white", legend=dict(x=1.15, y=0.5))
    fig.update_annotations(font_size=12)
    # Format axes and grids per subplot
    standard_grid_options = dict(showgrid=True, gridwidth=1, gridcolor="LightGrey")
    standard_line_options = dict(showline=True, linewidth=2, linecolor="LightGrey")

    # update x-axis for Qc
    fig.update_xaxes(
        row=1,
        col=1,
        **standard_line_options,
        **standard_grid_options,
        # range=[0, 30],
        # tick0=0,
        # dtick=5,
        title_text="Ultimate Shaft Resistance [MPa]",
        title_font=dict(color="mediumblue"),
    )
    # update x-axis for Rf
    fig.update_xaxes(
        row=1,
        col=2,
        **standard_line_options,
        **standard_grid_options,
        # range=[9.9, 0],
        # tick0=0,
        # dtick=5,
        title_text="Ultimate Base Resistance [MPa]",
        title_font=dict(color="red"),
    )
    fig.update_xaxes(
        row=1,
        col=3,
        **standard_line_options,
        **standard_grid_options,
        # range=[9.9, 0],
        # tick0=0,
        # dtick=5,
        title_text="Overall pile capactiy [MPa]",
        title_font=dict(color="black"),
    )

    # update all y axis to ensure they line up
    fig.update_yaxes(
        row=1,
        col=1,
        **standard_grid_options,
        title_text="Depth [m]",
        tick0=floor(parsed_cpt.elevation[-1] / 1e3) - 5,
        dtick=5,
    )  # for Qc

    fig.update_yaxes(
        row=1,
        col=2,
        **standard_line_options,
        **standard_grid_options,  # for Rf
        tick0=floor(parsed_cpt.elevation[-1] / 1e3) - 5,
        dtick=5,
    )

    fig.update_yaxes(
        row=1,
        col=3,
        **standard_line_options,  # for soil layouts
        tick0=floor(parsed_cpt.elevation[-1] / 1e3) - 5,
        dtick=1,
        showticklabels=True,
        side="right",
    )


def update_fig_layout(fig, parsed_cpt):
    """Updates layout of the figure and formats the grids"""
    fig.update_layout(barmode="stack", template="plotly_white", legend=dict(x=1.15, y=0.5))
    fig.update_annotations(font_size=12)
    # Format axes and grids per subplot
    standard_grid_options = dict(showgrid=True, gridwidth=1, gridcolor="LightGrey")
    standard_line_options = dict(showline=True, linewidth=2, linecolor="LightGrey")

    # update x-axis for Qc
    fig.update_xaxes(
        row=1,
        col=1,
        **standard_line_options,
        **standard_grid_options,
        range=[0, 30],
        tick0=0,
        dtick=5,
        title_text="qc [MPa]",
        title_font=dict(color="mediumblue"),
    )
    # update x-axis for Rf
    fig.update_xaxes(
        row=1,
        col=2,
        **standard_line_options,
        **standard_grid_options,
        range=[9.9, 0],
        tick0=0,
        dtick=5,
        title_text="Rf [%]",
        title_font=dict(color="red"),
    )

    # update all y axis to ensure they line up
    fig.update_yaxes(
        row=1,
        col=1,
        **standard_grid_options,
        title_text="Depth [m] w.r.t. NAP",
        tick0=floor(parsed_cpt.elevation[-1] / 1e3) - 5,
        dtick=1,
    )  # for Qc

    fig.update_yaxes(
        row=1,
        col=2,
        **standard_line_options,
        **standard_grid_options,  # for Rf
        tick0=floor(parsed_cpt.elevation[-1] / 1e3) - 5,
        dtick=1,
    )

    fig.update_yaxes(
        row=1,
        col=3,
        **standard_line_options,  # for soil layouts
        tick0=floor(parsed_cpt.elevation[-1] / 1e3) - 5,
        dtick=1,
        showticklabels=True,
        side="right",
    )


def add_soil_layout_to_fig(fig, soil_layout_original, soil_layout_user):
    """Add bars for each soil type separately in order to be able to set legend labels"""
    unique_soil_types = {
        layer.soil.properties.ui_name for layer in [*soil_layout_original.layers, *soil_layout_user.layers]
    }
    for ui_name in unique_soil_types:
        original_layers = [layer for layer in soil_layout_original.layers if layer.soil.properties.ui_name == ui_name]
        interpreted_layers = [layer for layer in soil_layout_user.layers if layer.soil.properties.ui_name == ui_name]
        soil_type_layers = [
            *original_layers,
            *interpreted_layers,
        ]  # have a list of all soils used in both figures

        # add the bar plots to the figures
        fig.add_trace(
            go.Bar(
                name=ui_name,
                x=["Original"] * len(original_layers) + ["Interpreted"] * len(interpreted_layers),
                y=[-layer.thickness * 1e-3 for layer in soil_type_layers],
                width=0.5,
                marker_color=[f"rgb{layer.soil.color.rgb}" for layer in soil_type_layers],
                hovertext=[
                    f"Soil Type: {layer.soil.properties.ui_name}<br>"
                    f"Top of layer: {layer.top_of_layer * 1e-3:.2f}<br>"
                    f"Bottom of layer: {layer.bottom_of_layer * 1e-3:.2f}"
                    for layer in soil_type_layers
                ],
                hoverinfo="text",
                base=[layer.top_of_layer * 1e-3 for layer in soil_type_layers],
            ),
            row=1,
            col=3,
        )
