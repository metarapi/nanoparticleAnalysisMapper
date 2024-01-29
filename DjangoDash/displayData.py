from django_plotly_dash import DjangoDash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import plotly.express as px
from django_plotly_dash import DjangoDash
from django.core.cache import cache

app = DjangoDash("YourDashApp")

app.layout = html.Div([
    dcc.Graph(id='graph'),
])

@app.callback(
    Output('graph', 'figure'),
    Input('graph', 'id'),  # Dummy input
)

def update_graph(_):
    numpy_file = cache.get('numpy_file', 'default_numpy_file_path')
    data = np.load(numpy_file)
    npTotalMap = data['npTotalMap']
    filtered_maps_list = [data['arr_%d' % i] for i in range(len(data.files) - 4)]  # Adjust this based on the number of non-filtered_maps arrays

    # Pad amount
    pad = np.round(0.1*np.shape(filtered_maps_list[0])[0]).astype(int)

    # Pad each map with NaNs
    padded_maps_list = [np.pad(map, ((pad, pad), (pad, pad)), constant_values=np.nan) for map in filtered_maps_list]

    # Concatenate the padded maps into a single large map
    large_map = np.concatenate([
        np.concatenate(padded_maps_list[i*5:(i+1)*5], axis=1) for i in range(2)
    ], axis=0)

    figure = px.imshow(large_map)
    figure.update_xaxes(showticklabels=False, showgrid=False,zeroline=False).update_yaxes(showticklabels=False, showgrid=False, zeroline=False)
    figure.update_layout(
        autosize=False, 
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor='rgba(0,0,0,0)',  # Make paper background transparent
        plot_bgcolor='rgba(171,184,250,1)',
        coloraxis_colorbar=dict(
            titlefont=dict(color='white'),  # Change colorbar title color
            tickfont=dict(color='white'),  # Change colorbar tick labels color
        ),
    )

    # Add colorbar
    labels = [
    ['<20 nm', '21-30 nm', '31-40 nm', '41-50 nm', '51-60 nm'],
    ['61-70 nm', '71-80 nm', '81-90 nm', '91-100 nm', '>100 nm']
    ]

    # Add labels
    map_height, map_width = filtered_maps_list[0].shape
    for i in range(2):
        for j in range(5):
            # Background annotation (outline)
            figure.add_annotation(
                x=j*(map_width+2*pad)+map_width/2+pad,  
                y=i*(map_height+2*pad)+pad/2,  
                text=labels[i][j],
                showarrow=False,
                font=dict(size=14, color='black', family='Arial Black')
            )
    return figure

app2 = DjangoDash("YourDashApp2")

app2.layout = html.Div([
    dcc.Graph(id='graph'),
])

@app2.callback(
    Output('graph', 'figure'),
    Input('graph', 'id'),  # Dummy input
)

def update_graph(_):
    numpy_file = cache.get('numpy_file', 'default_numpy_file_path')
    data = np.load(numpy_file)
    npTotalMap = data['npTotalMap']
    figure = px.imshow(npTotalMap)
    figure.update_xaxes(showticklabels=False, showgrid=False,zeroline=False).update_yaxes(showticklabels=False, showgrid=False, zeroline=False)
    figure.update_layout(
        autosize=False, 
        margin=dict(l=0, r=0, b=0, t=0),
        paper_bgcolor='rgba(0,0,0,0)',  # Make paper background transparent
        plot_bgcolor='rgba(171,184,250,1)',
        coloraxis_colorbar=dict(
            titlefont=dict(color='white'),  # Change colorbar title color
            tickfont=dict(color='white'),  # Change colorbar tick labels color
        ),
    )
    return figure