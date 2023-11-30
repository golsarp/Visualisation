from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot

from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
#test

if __name__ == "__main__":
    img = './Soccer.jpeg'  # replace with your image path

    # # replace these with your actual data
    # x = np.random.rand(100)  # random data, you should replace this with your actual x-coordinates
    # y = np.random.rand(100)  # random data, you should replace this with your actual y-coordinates
    #
    # scatter = go.Scatter(
    #     x=x,
    #     y=y,
    #     mode='markers',
    #     marker=dict(
    #         color='rgba(0, 0, 0, 0.5)'  # adjust this value to change the color and transparency of the points
    #     )
    # )
    #
    # layout = go.Layout(
    #     images=[go.layout.Image(
    #         source=img,
    #         xref="x",
    #         yref="y",
    #         x=0,
    #         y=1,
    #         sizex=1,
    #         sizey=1,
    #         sizing="stretch",
    #         opacity=0.5,  # adjust this value to make the background more or less transparent
    #         layer="below")],
    #     plot_bgcolor='rgba(0,0,0,0)',  # this makes the plot background transparent
    #     xaxis=dict(range=[0, 1]),  # these ranges should match the dimensions of your image
    #     yaxis=dict(range=[0, 1])  # these ranges should match the dimensions of your image
    # )
    #
    # fig = go.Figure(data=[scatter], layout=layout)
    # fig.show()

    import plotly.graph_objects as go

    from PIL import Image

    # Create figure
    fig = go.Figure()

    # Add trace
    fig.add_trace(
        go.Scatter(x=[0, 0.5, 1, 2, 2.2], y=[1.23, 2.5, 0.42, 3, 1])
    )

    with Image.open("Soccer.jpeg") as img:

# Add images
        fig.add_layout_image(
            dict(
                source=img,
                xref="x",
                yref="y",
                x=0,
                y=3,
                sizex=2,
                sizey=2,
                sizing="stretch",
                opacity=0.5,
                layer="below")
        )

    # Set templates
        fig.update_layout(template="plotly_white")

        fig.show()






    # Comment
    # Define interactions
    # @app.callback(
    #     Output(scatterplot1.html_id, "figure"),
    #     [
    #         Input("select-color-scatter-1", "value"),
    #         Input(scatterplot1.html_id, "selectedData"),
    #     ],
    # )
    # def update_scatter_1(selected_color, selected_data):
    #     print("Plot 1 hello")
    #     return scatterplot1.update(selected_color, selected_data)
    #
    # @app.callback(
    #     Output(scatterplot2.html_id, "figure"),
    #     [
    #         Input("select-color-scatter-2", "value"),
    #         Input(scatterplot1.html_id, "selectedData"),
    #     ],
    # )
    # def update_scatter_2(selected_color, selected_data):
    #     return scatterplot2.update(selected_color, selected_data)
    #
    # @app.callback(
    #     Output(scatterplot3.html_id, "figure"),
    #     [
    #         Input("select-color-scatter-3", "value"),
    #         Input(scatterplot3.html_id, "selectedData"),
    #     ],
    # )
    # def update_scatter_3(selected_color, selected_data):
    #     return scatterplot3.update(selected_color, selected_data)

    app.run_server(debug=False, dev_tools_ui=False)
