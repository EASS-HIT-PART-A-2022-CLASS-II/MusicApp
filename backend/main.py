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
    # Check if track already exists
    exists_query = f"SELECT * FROM tracks WHERE ID={track.id}"
    if execute_read_query(exists_query):
        raise HTTPException(status_code=409, detail="Track already exists")
    # Insert the new track into the tracks table
    insert_query = f"INSERT INTO tracks (TrackName, Artist, Album, Genre, Duration) VALUES ('{track.name}', '{track.artist}', '{track.album}', '{track.genre}', {track.duration})"
    execute_query(insert_query)
    return track

# Delete a specific track
@app.delete("/tracks/{track_id}")
def delete_track(track_id: int):
    # Check if the track is found in any of the playlists
    playlists = execute_read_query(
        f"SELECT ID FROM playlists WHERE Tracks LIKE '%{track_id}%'")
    # Delete the track from all playlists that contain it
    for playlist in playlists:
        execute_query(
            f"UPDATE playlists SET Tracks = replace(Tracks, '{track_id}', '') WHERE ID = {playlist['ID']}")
    # Delete the track itself
    execute_query(f"DELETE FROM tracks WHERE ID = {track_id}")
    return {"message": "Track deleted"}


# Create a new playlist
@app.post("/playlists")
def create_playlist(playlist: Playlist):
    # Check if all track ids exist in tracks table
    for track_id in playlist.tracks:
        result = execute_read_query(f"SELECT ID FROM tracks WHERE ID={track_id}")
        if not result:
            raise HTTPException(
                status_code=404, detail=f"Track with id {track_id} not found")
    # Check if playlist already exists
    result = execute_read_query(f"SELECT ID FROM playlists WHERE ID={playlist.id}")
    if result:
        raise HTTPException(status_code=409, detail="Playlist already exists")
    # Create the playlist in the playlists table
    query = f"INSERT INTO playlists (ID, PlaylistName, Tracks) VALUES ({playlist.id}, '{playlist.name}', '{playlist.tracks}')"
    execute_query(query)
    return playlist


# Read a specific playlist
@app.get("/playlists/{playlist_id}")
def read_playlist(playlist_id: int):
    # Fetch the playlist from the database
    query = f"SELECT * FROM playlists WHERE ID={playlist_id}"
    result = execute_read_query(query)
    if result:
        # Return the playlist as a Playlist object
        return Playlist(**result[0])
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
    # Check if the track is in the playlist
    query = f"SELECT * FROM playlists WHERE ID={playlist_id} AND Tracks LIKE '%,{track_id},%' OR Tracks LIKE '{track_id},%' OR Tracks LIKE '%,{track_id}'"
    result = execute_read_query(query)
    if not result:
        raise HTTPException(
            status_code=404, detail="Track not found in playlist")
    execute_query(
        f"UPDATE playlists SET Tracks = REPLACE(tracks, ',{track_id}', '') WHERE ID = {playlist_id}")
    return {"message": "Track removed from playlist"}


# Add a new track to playlist
@app.post("/playlists/{playlist_id}/tracks/{track_id}")
def add_track_to_playlist(playlist_id: int, track_id: int):
    # Check if the playlist exists
    query = f"SELECT * FROM playlists WHERE ID={playlist_id}"
    result = execute_read_query(query, conn)
    if not result:
        raise HTTPException(status_code=404, detail="Playlist not found")
    # Check if the track exists
    query = f"SELECT * FROM Tracks WHERE ID={track_id}"
    result = execute_read_query(query)
    if not result:
        raise HTTPException(status_code=404, detail="Track not found")
    # Check if the track is already in the playlist
    query = f"SELECT * FROM playlists WHERE ID={playlist_id} AND Tracks LIKE '%{track_id}%'"
    result = execute_read_query(query)
    if result:
        raise HTTPException(
            status_code=409, detail="Track already in playlist")
    # Add the track to the playlist
    query = f"UPDATE playlists SET Tracks=CONCAT(Tracks, ',{track_id}') WHERE ID={playlist_id}"
    execute_query(query)
    return {"message": "Track added to playlist"}
