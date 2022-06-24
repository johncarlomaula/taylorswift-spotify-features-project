# Import required packages
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go

# Define dictionary of colors associated with each album's aesthetic
COLORS = {"Taylor Swift": ["teal", "navy"],
          "Fearless": ["gold", "darkgoldenrod"],
          "Speak Now": ["plum", "indigo"],
          "Red": ["lightcoral", "maroon"],
          "1989": ["peachpuff", "peru"],
          "reputation": ["dimgray", "black"]}


# Define function to plot radar chart
def plot_radar_chart(df, song_og, song_tv, album):

    """ plot_radar_chart plots a polar chart of the features of the dataframe

    :df (pandas.core.frame.DataFrame'): dataframe of the song with features with track names as the index
    :song_og (str): song title of the original song or "Vault" if not applicable
    :song_tv (str): song title of the re-recording
    :album (str): album title  

    """

    # Create a list of features and calculate the number of features
    features = list(df)

    # Initialize radar chart figure
    fig = go.Figure()

    # Plot original song if applicable
    if song_og != "Vault":
        add_trace(df, song_og, COLORS[album][0], features, fig)

    # Plot re-recording or vault track
    add_trace(df, song_tv, COLORS[album][1], features, fig)

    # Set radar chart layout
    fig.update_layout(
        polar = dict(
            radialaxis = dict(
                visible = True,
                range = [0, 1],
            )),
        legend = dict(
            yanchor = "bottom",
            y = -0.3,
            xanchor = "left",
            x = -0.1
        ),
        showlegend = True
    )

    # Plot radar chart on app
    st.plotly_chart(fig, use_container_width=True)

# Define function to add trace to the polar chart
def add_trace(df, song, color, features, fig):

    """ add_trace adds the individual trace to the polar chart

    :df (pandas.core.frame.DataFrame'): dataframe of the song with features with track names as the index
    :song (str): song title
    :color (str): color of the plot
    :features (list): list of features
    :fig (plotly.graph_objs._figure.Figure): figure object of the polar chart to add the trace to
    
    """

    # Get feature values of the song
    values = df.loc[song].values.flatten().tolist()
    values += values[:1]

    # Add trace to chart
    fig.add_trace(go.Scatterpolar(
        r = values,
        theta = features,
        fill = 'toself',
        opacity = 0.8,
        marker = dict(color = color),
        name = song,
    ))