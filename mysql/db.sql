CREATE DATABASE IF NOT EXISTS db;
USE db;

CREATE TABLE tracks (
    ID int NOT NULL AUTO_INCREMENT,
    TrackName varchar(100) NOT NULL,
    Artist varchar(100) NOT NULL,
    Album varchar(100) NOT NULL,
    Genre varchar(100) NOT NULL,
    Duration int NOT NULL,
    PRIMARY KEY (ID)
);

INSERT INTO tracks (TrackName, Artist, Album, Genre, Duration)
VALUES ("Track 1", "Artist 1", "Album 1", "Genre 1", 120),
       ("Track 2", "Artist 2", "Album 2", "Genre 2", 213),
       ("Track 3", "Artist 3", "Album 3", "Genre 3", 420),
       ("Track 4", "Artist 4", "Album 4", "Genre 4", 445),
       ("Track 5", "Artist 5", "Album 5", "Genre 5", 231);

CREATE TABLE playlists (
    ID int NOT NULL AUTO_INCREMENT,
    PlaylistName varchar(100) NOT NULL,
    Tracks varchar(255) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO playlists (PlaylistName, Tracks)
VALUES ("Playlist 1", "1,2,3"),
       ("Playlist 2", "4"),
       ("Playlist 3", "5");
