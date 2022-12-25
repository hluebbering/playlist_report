import csv
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from operator import index


# Set client id and client secret
client_id = '4cf3afdca2d74dc48af9999b1b7c9c61'
client_secret = 'f6ca08ad37bb41a0afab5ca1dc74b208'

# Spotify authentication token
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


# Count distinct values in pandas column
tallyArtists = df.value_counts(["artist", "artist_id"]).reset_index(name='counts')
topArtist = tallyArtists['artist_id'][1]
tallyArtists.head(4)


# Create links table
a = sp.artist(topArtist)
ra = sp.artist_related_artists(topArtist)

# Dictionary of lists 
links_dict = {"source_name":[],"source_id":[],"target_name":[],"target_id":[]};
for artist in ra['artists']:
    links_dict["source_name"].append(a['name'])
    links_dict["source_id"].append(a['id'])
    links_dict["target_name"].append(artist['name'])
    links_dict["target_id"].append(artist['id'])

# Two generations of the most similar artists
for i in range(0, 4):
    a = sp.artist(links_dict['target_id'][i])
    ra = sp.artist_related_artists(links_dict['target_id'][i])
    time.sleep(.5)
    for artist in ra['artists']:
        links_dict["source_name"].append(a['name'])
        links_dict["source_id"].append(a['id'])
        links_dict["target_name"].append(artist['name'])
        links_dict["target_id"].append(artist['id'])

# Convert links dict to dataframe
links = pd.DataFrame(links_dict) 
# Export to excel sheet             
links.to_excel("links.xlsx", index = False)




# Create points table             
all_artist_ids = list(set(links_dict['source_id'] + links_dict['target_id']))
# Dictionary of lists 
points_dict = {"id":[],"name":[],"followers":[],"popularity":[],"url":[],"image":[]};
for id in all_artist_ids:
    time.sleep(.5)
    a = sp.artist(id)
    points_dict['id'].append(id)
    points_dict['name'].append(a['name'])
    points_dict['followers'].append(a['followers']['total'])
    points_dict['popularity'].append(a['popularity'])
    points_dict['url'].append(a['external_urls']['spotify'])
    points_dict['image'].append(a['images'][0]['url'])

# Convert links dict to dataframe
points = pd.DataFrame(points_dict) 
# Export to excel sheet             
points.to_excel("points.xlsx", index = False)
