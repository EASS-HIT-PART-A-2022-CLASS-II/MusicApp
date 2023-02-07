import streamlit as st
import requests

st.title("Welcome to MusicApp")
read_write = st.radio("Read, write, or remove data?",
                      ("Read", "Write", "Remove"))

if read_write == "Read":
    # Read data section
    st.header("Read track/playlist info")
    id_input = st.text_input("Enter an ID:")
    data_type = st.radio("Select data type:", ("Track", "Playlist"))
    if st.button("Get data"):
        if data_type == "Track":
            try:
                data = requests.get(
                    f"http://backend:8080/tracks/{id_input}").json()
                st.write("Track data:", data)
            except requests.exceptions.HTTPError as err:
                st.error(err)

        elif data_type == "Playlist":
            try:
                data = requests.get(
                    f"http://backend:8080/playlists/{id_input}").json()
                st.write("Playlist data:", data)
            except requests.exceptions.HTTPError as err:
                st.error(err)

elif read_write == "Write":
    # Write data section
    write_type = st.radio("Write track, playlist or a track to a playlist?",
                          ("Track", "Playlist", "Track to Playlist"))
    if write_type == "Track":
        # Add a section for adding new tracks
        st.header("Add a new track")
        # Removed id option - AUTO_INCREMENT in db
        # track_id = st.number_input("ID:")
        track_id = 0 #needed for the json obj, but it doesn't read it
        track_name = st.text_input("Name:")
        track_artist = st.text_input("Artist:")
        track_album = st.text_input("Album:")
        track_genre = st.text_input("Genre:")
        track_duration = st.number_input("Duration (in seconds):")
        if st.button("Add track"):
            track_data = {
                "id": track_id,
                "name": track_name,
                "artist": track_artist,
                "album": track_album,
                "genre": track_genre,
                "duration": track_duration
            }
            response = requests.post(
                "http://backend:8080/tracks", json=track_data)
            if response.status_code == 200:
                st.write("Track data:", response.json())
                st.success("Track added successfully!")
            else:
                st.error("Error adding track.")

    elif write_type == "Playlist":
        # Add a section for adding new playlists
        st.header("Add a new playlist")
        playlist_id = 0
        playlist_name = st.text_input("Name:")
        playlist_tracks = st.text_input("Tracks IDs(comma-separated):")
        if st.button("Add playlist"):
            playlist_data = {
                "id": playlist_id,
                "name": playlist_name,
                "tracks": playlist_tracks.split(",")
            }
            response = requests.post(
                "http://backend:8080/playlists", json=playlist_data)
            if response.status_code == 200:
                st.write("Playlist data:", response.json())
                st.success("Playlist added successfully!")
            elif response.status_code == 404:
                st.error("Error adding playlist. One or more track IDs may not exist.")
            elif response.status_code == 409:
                st.error(
                    "Playlist's ID already exists")
            else:
                st.error("Error adding playlist.")

    elif write_type == "Track to Playlist":
        # Add a section for adding new track to a playlist
        st.header("Add a track to playlist")
        playlist_id = int(st.number_input("Playlist ID:"))
        track_id = int(st.number_input("Track ID:"))
        if st.button("Add track to playlist"):
            response = requests.patch(
                f"http://backend:8080/playlists/{playlist_id}/tracks/{track_id}")
        
            # response = requests.patch(
            #     f"http://backend:8080/playlists/{playlist_id}/tracks", json={"track_id": track_id})
            # response = requests.patch(
            #     f"http://backend:8080/playlists/{playlist_id}/tracks", json={"playlist_id": playlist_id, "track_id": track_id})
            # response = requests.patch(
            #     "http://backend:8080/playlists/tracks",
            #     json={"playlist_id": playlist_id, "track_id": track_id}
            # )
            if response.status_code == 200:
                st.success("Track added to playlist successfully!")
            elif response.status_code == 404:
                st.error(
                    "Error adding track to playlist. Playlist not exist.")
            elif response.status_code == 407:
                st.error(
                    "Error adding track to playlist. Track not exist.")
            elif response.status_code == 400:
                st.error(
                    "Error adding track to playlist. Track already in playlist.")
            else:
                st.error("Error adding track to playlist.")

   
elif read_write == "Remove":
    # Remove data section
    remove_type = st.radio("Remove track, playlist or a track from a playlist?",
                           ("Track", "Playlist", "Track from Playlist"))

    if remove_type == "Track":
        # Add a section for removing tracks
        st.header("Remove a track")
        track_id = st.number_input("ID:")
        if st.button("Remove track"):
            track_id = int(track_id)
            response = requests.delete(f"http://backend:8080/tracks/{track_id}")
            if response.status_code == 200:
                st.success("Track removed successfully!")
            else:
                st.error("Error removing track.")

    elif remove_type == "Playlist":
        # Add a section for removing playlists
        st.header("Remove a playlist")
        playlist_id = st.number_input("ID:")
        if st.button("Remove playlist"):
            playlist_id = int(playlist_id)
            response = requests.delete(
                f"http://backend:8080/playlists/{playlist_id}")
            if response.status_code == 200:
                st.success("Playlist removed successfully!")
            else:
                st.error("Error removing playlist.")

    elif remove_type == "Track from Playlist":
        # Remove track from playlist section
        st.header("Remove a track from a playlist")
        playlist_id = int(st.number_input("Enter playlist ID:"))
        track_id = int(st.number_input("Enter track ID:"))

        if st.button("Remove track"):
            response = requests.delete(
                f"http://backend:8080/playlists/{playlist_id}/tracks/{track_id}")
            if response.status_code == 200:
                st.success("Track removed from playlist successfully!")
            else:
                st.error("Error removing track from playlist.")



