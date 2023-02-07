from fastapi import FastAPI, HTTPException
from models import Track, Playlist
import mysql.connector
# import sqlite3

def create_connection():
    try:
        conn = mysql.connector.connect(
            user='root', password='root', host='database', port="3306", database='db')
        return conn
    except mysql.connector.Error as e:
        print(f'Error: {e}')
        return None

def execute_query(query):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except mysql.connector.Error as e:
            print(f'Error: {e}')
        finally:
            close_connection(conn)
    else:
        print('Error: Connection not established')

def execute_read_query(query):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            print(f'Error: {e}')
        finally:
            close_connection(conn)
    else:
        print('Error: Connection not established')

def close_connection(conn):
    conn.close()


app = FastAPI()


# Read a specific track
@app.get("/tracks/{track_id}")
def read_track(track_id: int):
    query = f"SELECT * FROM tracks WHERE ID={track_id}"
    result = execute_read_query(query)
    if result:
        track_data = result[0]
        # track = Track(ID=track_data[0], TrackName=track_data[1], Artist=track_data[2],
        #               Album=track_data[3], Genre=track_data[4], Duration=track_data[5])
        track = Track(id=track_data[0], name=track_data[1], artist=track_data[2],album=track_data[3], genre=track_data[4], duration=track_data[5])
        return track
    else:
        raise HTTPException(status_code=404, detail="Track not found")


# Create a new track
@app.post("/tracks")
def create_track(track: Track):
    # Insert the new track into the tracks table
    insert_query = f"INSERT INTO tracks (TrackName, Artist, Album, Genre, Duration) VALUES ('{track.name}', '{track.artist}', '{track.album}', '{track.genre}', {track.duration})"
    execute_query(insert_query)
    # Fetch the ID of the inserted track
    select_query = f"SELECT ID FROM tracks WHERE TrackName='{track.name}' AND Artist='{track.artist}' AND Album='{track.album}' AND Genre='{track.genre}' AND Duration={track.duration}"
    result = execute_read_query(select_query)
    track_id = result[0][0]
    # Update the Track instance with the ID
    track.id = track_id
    return track


# Delete a specific track from db, also from all playlist
@app.delete("/tracks/{track_id}")
def delete_track(track_id: int):
    # Check if the track is found in any of the playlists
    playlists = execute_read_query(
        f"SELECT ID, Tracks FROM playlists WHERE Tracks LIKE '%{track_id}%'")
    # Delete the track from all playlists that contain it
    for playlist in playlists:
        playlist_id = int(playlist[0])
        playlist_tracks = playlist[1].split(",")
        playlist_tracks.remove(str(track_id))
        playlist_tracks = ",".join(playlist_tracks)
        execute_query(
            f"UPDATE playlists SET Tracks = '{playlist_tracks}' WHERE ID = {playlist_id}")
    # Delete the track itself
    execute_query(f"DELETE FROM tracks WHERE ID = {track_id}")
    return {"message": "Track deleted"}


# Create a new playlist
@app.post("/playlists")
def create_playlist(playlist: Playlist):
    # Check if the playlist already exists
    result = execute_read_query(
        f"SELECT ID FROM playlists WHERE PlaylistName='{playlist.name}'")
    if result:
        raise HTTPException(
            status_code=409, detail=f"Playlist with name '{playlist.name}' already exists")
    
    track_ids = ",".join(map(str, playlist.tracks)) if playlist.tracks else ""
    # Check if all track ids exist in tracks table  
    if playlist.tracks:
        for track_id in playlist.tracks:
            result = execute_read_query(
                f"SELECT ID FROM tracks WHERE ID={track_id}")
            if not result:
                raise HTTPException(
                    status_code=404, detail=f"Track with id {track_id} not found")
        track_ids = ",".join(map(str, playlist.tracks))

    # Create the playlist in the playlists table
    query = f"INSERT INTO playlists (PlaylistName, Tracks) VALUES ('{playlist.name}', '{track_ids}')"
    execute_query(query)
    result = execute_read_query(
        f"SELECT ID FROM playlists WHERE PlaylistName='{playlist.name}' AND Tracks='{track_ids}'")
    playlist.id = result[0][0]
    return playlist


# Read a specific playlist
@app.get("/playlists/{playlist_id}")
def read_playlist(playlist_id: int):
    # Fetch the playlist from the database
    query = f"SELECT * FROM playlists WHERE ID={playlist_id}"
    result = execute_read_query(query)
    if result:
        playlist_data = result[0]
        tracks = playlist_data[2].split(",") if playlist_data[2] else []
        playlist = Playlist(id=playlist_data[0], name=playlist_data[1], tracks=tracks)
        # Return the playlist as a Playlist object
        return playlist
    else:
        raise HTTPException(status_code=404, detail="Playlist not found")


# Delete a specific playlist
@app.delete("/playlists/{playlist_id}")
def delete_playlist(playlist_id: int):
    # Delete the playlist
    query = f"DELETE FROM playlists WHERE ID = {playlist_id}"
    execute_query(query)
    return {"message": "Playlist deleted"}


# Remove a specific track from playlist
@app.delete("/playlists/{playlist_id}/tracks/{track_id}")
def remove_track_from_playlist(playlist_id: int, track_id: int):
    # Check if the playlist exists
    playlist_data = execute_read_query(
        f"SELECT Tracks FROM playlists WHERE ID={playlist_id}")
    if not playlist_data:
        raise HTTPException(
            status_code=404, detail="Playlist not found")
    # Check if the track is in the playlist
    playlist_tracks = playlist_data[0][0].split(",")
    if str(track_id) not in playlist_tracks:
        raise HTTPException(
            status_code=404, detail="Track not found in playlist")
    # Remove the track from the playlist
    playlist_tracks.remove(str(track_id))
    playlist_tracks = ",".join(playlist_tracks)
    execute_query(
        f"UPDATE playlists SET Tracks = '{playlist_tracks}' WHERE ID = {playlist_id}")
    return {"message": "Track removed from playlist"}


# Add a new track to playlist
@app.patch("/playlists/{playlist_id}/tracks/{track_id}")
def add_track_to_playlist(playlist_id: int, track_id: int):
    # Check if the playlist exists
    playlist_data = execute_read_query(
        f"SELECT Tracks FROM playlists WHERE ID={playlist_id}")
    if not playlist_data:
        raise HTTPException(
            status_code=404, detail="Playlist not found")
    track_data = execute_read_query(
        f"SELECT * FROM tracks WHERE ID={track_id}")
    if not track_data:
        raise HTTPException(
            status_code=407, detail="Track not found")
    # Check if the playlist is empty
    playlist_tracks = playlist_data[0][0].split(",")
    if not playlist_tracks[0]:
        playlist_tracks = str(track_id)
    else:
        # Check if the track is already in the playlist
        if str(track_id) in playlist_tracks:
            raise HTTPException(
                status_code=400, detail="Track already in playlist")
        # Add the track to the playlist
        playlist_tracks.append(str(track_id))
        playlist_tracks = ",".join(playlist_tracks)
    execute_query(
        f"UPDATE playlists SET Tracks = '{playlist_tracks}' WHERE ID = {playlist_id}")
    return {"message": "Track added to playlist"}
