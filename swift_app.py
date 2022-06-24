# Import required packages
import streamlit as st
import pandas as pd
from datetime import date
from swift_functions import *

# Define constants including list of albums, released re-recordings, and features
ALBUM_LIST = ["Taylor Swift", "Fearless", "Speak Now", "Red", "1989", "reputation"]
RELEASED = ["Fearless", "Red"]
FEATURE_LIST = ["length", "popularity", "acousticness", "danceability", "energy", "instrumentalness",
                "liveness", "loudness", "speechiness", "tempo", "time_signature", "valence"]

# Import data
df = pd.read_csv("data/swift_data.csv")

# Drop unused features
df = df.drop(["artist", "release_date"], axis = 1)

# Select which features to filter by and drop these features while keeping name and album
numerical_features = st.sidebar.multiselect("Filter features (minimum of 3)", FEATURE_LIST)

features = numerical_features + ["album", "name"]

if len(features) > 4:
    df.drop(df.columns.difference(features), axis = 1, inplace = True)
else:
    numerical_features = FEATURE_LIST


# Initialize MinMax scaler for scaling the data
scaler = MinMaxScaler()

# Obtain user input of which album to display
album = st.sidebar.selectbox("Select an album", ALBUM_LIST)

# Check if re-recording has been released
if album in RELEASED:

    # Display album title
    st.header(f"{album} vs. {album} (Taylor's Version)")

    # Filter dataframe by album
    df_album = df[(df['album'] == album) | (df['album'] == album + " (Taylor's Version)")]

    # Scale data using the MinMaxScaler
    df_album_scaled = df_album[df_album.columns[0:2]]
    df_album_scaled[numerical_features] = scaler.fit_transform(df_album[numerical_features])
    
    # Calculate mean values and store in a dataframe
    mean_values_df = pd.DataFrame(df_album_scaled.groupby('album').mean())

    # Plot radar chart of the mean values of features of the whole album 
    plot_radar_chart(mean_values_df, album, album + " (Taylor's Version)", album)

    # Obtain album tracklist
    tracklist = df[df['album'] == album + " (Taylor's Version)"]["name"].tolist()
    tracklist = [track.replace(" (Taylor's Version)", "") for track in tracklist]

    # Remove the ("Taylor's Version") identifier from the vault tracks for readability
    df_album_scaled = df_album_scaled.replace("\(Taylor's Version\) \(From The Vault\)", "(From The Vault)", regex = True)
    
    # Drop album column and set song name as index
    df_album_scaled = df_album_scaled.drop('album', axis = 1)
    df_album_scaled.set_index('name', inplace = True)

    # Clean song titles for matchability
    if album == "Fearless":
        df_album_scaled.rename(index = {'Forever & Always - Piano Version':'Forever & Always (Piano Version)'}, inplace = True)
        df_album_scaled.rename(index = {'Breathe':'Breathe (feat. Colbie Caillat)'}, inplace = True)
        df_album_scaled.rename(index = {'SuperStar':'Superstar'}, inplace = True)
    elif album == "Red":
        df_album_scaled.rename(index = {'I Knew You Were Trouble.':'I Knew You Were Trouble'}, inplace = True)
        df_album_scaled.rename(index = {'The Last Time':'The Last Time (feat. Gary Lightbody of Snow Patrol)'}, inplace = True)
        df_album_scaled.rename(index = {'Everything Has Changed':'Everything Has Changed (feat. Ed Sheeran)'}, inplace = True)
        df_album_scaled.rename(index = {'State Of Grace - Acoustic':'State Of Grace (Acoustic Version)'}, inplace = True)

    # Select song to plot
    song = st.sidebar.radio("Select a song", tracklist)

    # Display song title
    st.subheader(song)

    # Plot radar chart of song
    if song == "Babe (From The Vault)":
        plot_radar_chart(df_album_scaled, "Babe (feat. Taylor Swift)", song, album)
    elif song == "Better Man (From The Vault)":
        plot_radar_chart(df_album_scaled, "Better Man", song, album)
    elif "(From The Vault)" in song:
        plot_radar_chart(df_album_scaled, "Vault", song, album)
    else:
        plot_radar_chart(df_album_scaled, song, song + " (Taylor's Version)", album)

else:

    # Obtain current date
    today = date.today().strftime("%B %d, %Y")

    # Print message to inform that the re-recording is unavailable.
    st.markdown("As of **{}**, the re-recording for *{}* has not been released yet.".format(today, album))
    st.markdown("This app will be updated when the re-recording is released.")