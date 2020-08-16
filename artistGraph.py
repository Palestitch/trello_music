
'''
PSEUDOCODE:
INPUT:
x = #similar artists
y = #artists to put into new playlist
ALGORITHM
graph_dict = dict(key=artists, value=(similar artists)
artist_dict = dict(key=sim_artist, value=count)
for artist in playlist:
    sim_artists = find_similar_artists(artist)[:x]
    graph_dict[artist] = sim_artists
    for each sim in similar_artists:
        artist_dict[sim] += 1
sort(artist_dict by value)
extract y largest that are not in graph_dict (key comparison)
make playlist with top 10 songs by the y artists
OUTPUT:
Finished playlist, and a dictionary of artists in playlist and x neighbours
NEXT STEP:
Visualize the adjacency list
'''