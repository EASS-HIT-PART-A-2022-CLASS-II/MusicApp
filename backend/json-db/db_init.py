import json
import random

tracks = [
    {
        "id": 1,
        "name": "Song 1",
        "artist": "Artist 1",
        "album": "Album 1",
        "genre": "Pop",
        "duration": 180
    },
    {
        "id": 2,
        "name": "Song 2",
        "artist": "Artist 2",
        "album": "Album 2",
        "genre": "Rock",
        "duration": 210
    },
    {
        "id": 3,
        "name": "Song 3",
        "artist": "Artist 3",
        "album": "Album 3",
        "genre": "Jazz",
        "duration": 240
    },
    {
        "id": 4,
        "name": "Song 4",
        "artist": "Artist 4",
        "album": "Album 4",
        "genre": "Hip hop",
        "duration": 300
    },
    {
        "id": 5,
        "name": "Song 5",
        "artist": "Artist 5",
        "album": "Album 5",
        "genre": "Country",
        "duration": 270
    }
]

playlists = [
    {
        "id": 1,
        "name": "Playlist 1",
        "tracks": [1, 2, 3, 4, 5]
    },
    {
        "id": 2,
        "name": "Playlist 2",
        "tracks": [1,2,3]
    },
    {
        "id": 3,
        "name": "Playlist 3",
        "tracks": [3,4,5]
    }
]

with open("./backend/db/tracks.json", "w") as f:
    json.dump(tracks, f, indent=2)

with open("./backend/db/playlists.json", "w") as f:
    json.dump(playlists, f, indent=2)
