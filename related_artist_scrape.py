import spotipy
import json
import random
import time
import networkx as nx
from spotipy.oauth2 import SpotifyClientCredentials 

credentials = json.load(open('auth.json'))
client_id = credentials['client_id']
client_secret = credentials['client_secret']
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# initializing data structs
#seed_artist_list= ['100 gecs','yung bae','alan walker','varien','all time low','mod sun','igorrr','drumcorps', 'knocked loose','code orange','alcest','liturgy','inferi','artificial brain']
# two of each pop, synthwave, poppunk, breakcore, beatdown, black, death

seed_artist_list = ['billie eilish','the weeknd','taylor swift','megan thee stallion','drake','ariana grande','bts','beyonce','lady gaga','ed sheeran','bruno mars']
# mainstream artist list
found_artist_list = []
related_db_list = []
G = nx.MultiGraph()

for seed_artist in seed_artist_list:                                                # loop through seed list
    related_database = {"Seed_Artist": "", "Related_Artists": ""}                   # initialize singular db
    seed_result = sp.search(q='artist:' + seed_artist, type='artist')   
    first_level_name = seed_result['artists']['items'][0]['name']                   # set name/uri of searched for artists
    first_level_uri = seed_result['artists']['items'][0]['uri']
    first_related = sp.artist_related_artists(first_level_uri)                      # get related artists from seed_artist
    related_database['Seed_Artist'] = first_level_name                              # fill singular dict 
    related_database['Related_Artists']  = first_related
    related_db_list.append(related_database)                                        # make list of singular dbs 
    #time.sleep(1)

while len(related_db_list) < 2000:                                                    # arbitrary choice but want lots of data
    for related_database in related_db_list:                                        # loop through list of singular dbs
        for related_artist in related_database['Related_Artists']['artists']:       # save artist to list if enough followers
            if related_artist['followers']['total'] > 1500:
                found_artist_list.append(related_artist)

    for related_artist in found_artist_list:                                        # loop through list of related artists
        try:
            related_database = {"Seed_Artist": "", "Related_Artists": ""}               # to find artists related to them
            related_result = sp.search(q='artist:' + related_artist['name'], type='artist')
            related_name = related_result['artists']['items'][0]['name']
            related_uri = related_result['artists']['items'][0]['uri']
            second_related = sp.artist_related_artists(related_uri)
            related_database['Seed_Artist'] = related_name
            related_database['Related_Artists'] = second_related
            related_db_list.append(related_database)
        except IndexError:
            pass
    continue


for artist_dict in related_db_list:                                                 # loop through list of singular dbs
    u = artist_dict['Seed_Artist']                                                  # seed node
    G.add_node(u)
    related_info = artist_dict['Related_Artists']                            
    for related_artist_info in related_info['artists']:                             # loop through dict of related artists from value of singular db key
        try:
            v = related_artist_info['name']                                             # related node
            G.add_node(v, genre = related_artist_info['genres'][0])
            G.add_edge(u, v)
        except IndexError:
            v = related_artist_info['name'] 
            G.add_node(v, genre = 'null')
            G.add_edge(u, v)
    continue


nx.write_gexf(G,"related_network_popular.gexf")
