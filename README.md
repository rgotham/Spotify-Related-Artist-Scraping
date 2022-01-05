# Spotify-Related-Artist-Scraping
Using Spotipy and NetworkX, scraping spotify and visualizing results with Gephi

Data captured allows one to see the top three genre descriptors as defined by Spotify, as well as Spotify popularity index and URI. 

The Spotify popularity index is proprietary and thus we don't know exactly how it's calculated, however we know that it's a ranking system from 0-100 that ranks an artist relative to all other artists on the platform. This index seems to influence how an artist places on algorithmically made playlists and Spotify discovery and recommendation. It also seems to be derived from metrics such as the age of tracks, number of listens and saves among others, but it's not known for sure. However, I believe it's a useful metric for the end-user as it allows an "at a glance" look for an artist's popularity; that is, the higher the number, the higher chance the artist is well known.

The Spotify URI capture allows the user to copy/paste URI into Spotify and be directed to the artist's Spotify entry. I find this to be a more reliable way of searching for artists, especially with the similarly/exactly named artists. 

The visualization itself is colored by modularity class; this statistic determines the number of communities within some network. It's also interactive; it's searchable by artist and when an artist is selected, one may see the artist's genres, Spotify URI and other statistics, as well as the ingoing/outgoing edges. 

Check out the visualization at https://luneth.pachipatch.com/network_website/
