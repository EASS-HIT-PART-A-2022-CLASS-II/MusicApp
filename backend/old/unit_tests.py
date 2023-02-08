from models import Track

track_data = {
    "id": 1,
    "name": "Sweet Child o' Mine",
    "artist": "Guns N' Roses",
    "album": "Appetite for Destruction",
    "genre": "Rock",
    "duration": 180
}

track_obj = Track(id=track_data["id"], name=track_data["name"], artist=track_data["artist"], album=track_data["album"], genre=track_data["genre"], duration=track_data["duration"])
 

def test_get_info():
    print(track_data)
    print(track_obj.get_info())
    assert track_obj.get_info() == track_data
