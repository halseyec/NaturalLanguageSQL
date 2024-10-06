CREATE TABLE artist (
    artist_id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    genre VARCHAR(30)
);

CREATE TABLE album (
    album_id INTEGER PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    artist_id INTEGER,
    release_year INTEGER,
    FOREIGN KEY (artist_id) REFERENCES artist (artist_id)
);

CREATE TABLE song (
    song_id INTEGER PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    album_id INTEGER,
    duration TIME,
    FOREIGN KEY (album_id) REFERENCES album (album_id)
);

CREATE TABLE listener (
    listener_id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) UNIQUE
);

CREATE TABLE playlist (
    playlist_id INTEGER PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    listener_id INTEGER,
    FOREIGN KEY (listener_id) REFERENCES listener (listener_id)
);

CREATE TABLE playlist_song (
    playlist_id INTEGER,
    song_id INTEGER,
    FOREIGN KEY (playlist_id) REFERENCES playlist (playlist_id),
    FOREIGN KEY (song_id) REFERENCES song (song_id)
);
