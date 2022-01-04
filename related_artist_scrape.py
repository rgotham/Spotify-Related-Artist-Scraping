import spotipy
import json
import networkx
import time
from spotipy.oauth2 import SpotifyClientCredentials 

start_time = time.time()

credentials = json.load(open('auth.json'))                                              # put client id/secret here
client_id = credentials['client_id']
client_secret = credentials['client_secret']
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

'''
First step is querying Spotify API and scraping information
Then extraneous information is removed
Afterwards the graph is built and exported to .gexf 
'''

seed_artist_list =[]                                                                    # initial list to search
found_artist_list = []
related_db_list = []

try:
    for seed_artist in seed_artist_list:                                                # loop through seed list
        related_database = {"Seed_Artist": "", "Related_Artists": ""}                   # initialize singular db
        seed_result = sp.search(q='artist:' + seed_artist, type='artist')   
        first_level_name = seed_result['artists']['items'][0]                   # set name/uri of searched for artists, if list index out of range there's no artist
        first_level_uri = seed_result['artists']['items'][0]['uri']
        first_related = sp.artist_related_artists(first_level_uri)                      # get related artists from seed_artist
        related_database['Seed_Artist'] = first_level_name                              # fill singular dict 
        related_database['Related_Artists']  = first_related
        related_db_list.append(related_database)                                        # make list of singular dbs 

    while len(related_db_list) < 2000:                                                    # arbitrary choice but want lots of data
        for related_database in related_db_list:                                        # loop through list of singular dbs
            for related_artist in related_database['Related_Artists']['artists']:       # save artist to list if enough followers
                if related_artist['followers']['total'] > 1000 and related_artist not in found_artist_list:
                    found_artist_list.append(related_artist)

        for related_artist in found_artist_list:                                        # loop through list of related artists
            try:
                related_database = {"Seed_Artist": "", "Related_Artists": ""}               # to find artists related to them
                related_result = sp.search(q='artist:' + related_artist['name'], type='artist')
                related_name = related_result['artists']['items'][0]
                related_uri = related_result['artists']['items'][0]['uri']
                second_related = sp.artist_related_artists(related_uri)
                related_database['Seed_Artist'] = related_name
                related_database['Related_Artists'] = second_related
                related_db_list.append(related_database)
            except IndexError:
                pass
except Exception as e:
    print(str(e))
    time.sleep(15)
    pass


for relation in related_db_list:

    seed = relation['Seed_Artist']
    seed.pop('external_urls',None)
    seed.pop('followers',None)
    seed.pop('href',None)
    seed.pop('id',None)
    seed.pop('images',None)
    seed.pop('type',None)

    related_artists = relation['Related_Artists']
    for artist in related_artists['artists']:
        artist.pop('external_urls',None)
        artist.pop('followers',None)
        artist.pop('href',None)
        artist.pop('id',None)
        artist.pop('images',None)
        artist.pop('type',None)

'''
We keep genres, name, popularity, uri
'''

G = networkx.DiGraph()
for relation in related_db_list:                                                 # loop through list of singular dbs
    u = relation['Seed_Artist']['name']
    if int(len(relation['Seed_Artist']['genres'])) >= 3:
        G.add_node(u, popularity = relation['Seed_Artist']['popularity'],uri = relation['Seed_Artist']['uri'] , genre1 = relation['Seed_Artist']['genres'][0],genre2 = relation['Seed_Artist']['genres'][1],genre3 = relation['Seed_Artist']['genres'][2])
    
    elif int(len(relation['Seed_Artist']['genres'])) == 2:
        G.add_node(u, popularity = relation['Seed_Artist']['popularity'], uri = relation['Seed_Artist']['uri'], genre1 = relation['Seed_Artist']['genres'][0],genre2 = relation['Seed_Artist']['genres'][1])
    
    elif  int(len(relation['Seed_Artist']['genres'])) == 1:
        G.add_node(u, popularity = relation['Seed_Artist']['popularity'], uri = relation['Seed_Artist']['uri'], genre1 = relation['Seed_Artist']['genres'][0])
    
    else :
        G.add_node(u, popularity = relation['Seed_Artist']['popularity'], uri = relation['Seed_Artist']['uri'])
    
    related_info = relation['Related_Artists']                             
    for related_artist_info in related_info['artists']:                             # loop through dict of related artists from value of singular db key
        v = related_artist_info['name']
        if int(len(related_artist_info['genres'])) >= 3:
            G.add_node(v, popularity = related_artist_info['popularity'], uri = related_artist_info['uri'], genre1 = related_artist_info['genres'][0], genre2 = related_artist_info['genres'][1],genre3 = related_artist_info['genres'][2])
        
        elif int(len(related_artist_info['genres'])) == 2:
            G.add_node(v, popularity = related_artist_info['popularity'], uri = related_artist_info['uri'], genre1 = related_artist_info['genres'][0], genre2 = related_artist_info['genres'][1])
        
        elif  int(len(related_artist_info['genres'])) == 1:
            G.add_node(v, popularity = related_artist_info['popularity'], uri = related_artist_info['uri'], genre1 = related_artist_info['genres'][0])
        
        else :
            G.add_node(v, popularity = related_artist_info['popularity'], uri = related_artist_info['uri'])
        G.add_edge(u, v)
    continue

end_time = (time.time() - start_time)
print("this took " + str(end_time) + " seconds to complete")
networkx.write_gexf(G,"filename.gexf")