INSERT INTO artist (artist_id, name, genre) VALUES
(1, 'Bob Dylan', 'Folk'),
(2, 'Taylor Swift', 'Pop'),
(3, 'The Rolling Stones', 'Rock'),
(4, 'Johnny Cash', 'Country'),
(5, 'Fleetwood Mac', 'Rock');

INSERT INTO album (album_id, title, artist_id, release_year) VALUES
(1, 'Blonde on Blonde', 1, 1966),
(2, 'Red', 2, 2012),
(3, 'Some Girls', 3, 1978),
(4, 'At Folsom Prison', 4, 1968),
(5, 'Mirage', 5, 1982);

INSERT INTO song (song_id, title, album_id, duration) VALUES
(1, 'Rainy Day Women #12 & 35', 1, '04:36'),
(2, 'Visions of Johanna', 1, '07:33'),
(3, 'All Too Well', 2, '05:29'),
(4, 'State of Grace', 2, '04:55'),
(5, 'Miss You', 3, '04:48'),
(6, 'Beast of Burden', 3, '04:17'),
(7, 'Folsom Prison Blues', 4, '02:48'),
(8, 'Jackson', 4, '02:45'),
(9, 'Book of Love', 5, '03:38'),
(10, 'Thats Alright', 5, '03:11'),
(11, 'Gypsy', 5, '04:28');

INSERT INTO listener (listener_id, name, email) VALUES
(1, 'Emmeline Smith', 'emmeline@gmail.com'),
(2, 'Cole Peck', 'cole@gmail.com'),
(3, 'Shandi Haynie', 'shandi@gmail.com'),
(4, 'Halsey Curry', 'halsey@gmail.com');

INSERT INTO playlist (playlist_id, title, listener_id) VALUES
(1, 'Throwback', 1),
(2, 'Running', 2),
(3, 'Night drive', 3),
(4, 'Saturday morning', 4);

INSERT INTO playlist_song (playlist_id, song_id) VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4),
(3, 5),
(3, 6),
(4, 7),
(4, 8),
(4, 9),
(4, 10),
(4, 11);
