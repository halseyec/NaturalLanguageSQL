
# Music Database

This database models a simple music service; it tracks artists, albums, songs, and listener playlists.

### Successful Query

**Question:** Which playlists contain songs by Bob Dylan?  
**SQL Query:**
```sql
SELECT p.title
FROM playlist p
JOIN playlist_song ps ON p.playlist_id = ps.playlist_id
JOIN song s ON ps.song_id = s.song_id
JOIN album a ON s.album_id = a.album_id
JOIN artist ar ON a.artist_id = ar.artist_id
WHERE ar.name = 'Bob Dylan';
```
**Result:** Throwback, Throwback  
**Friendly Response:** The songs by Bob Dylan are included in the playlist named "Throwback".

### Unsuccessful Query

**Question:** Which song would you recommend for listener Halsey Curry?  
**SQL Query:**
```sql
SELECT s.title
FROM song s 
JOIN album a ON s.album_id = a.album_id 
JOIN artist ar ON a.artist_id = ar.artist_id 
JOIN listener l ON ar.artist_id = l.listener_id 
WHERE l.name = 'Halsey Curry';
```
**Result:** [('Folsom Prison Blues',), ('Jackson',), ('Book of Love',), ('Thats Alright',), ('Gypsy',)]  
**Friendly Response:** I would recommend the following songs for Halsey Curry: 'Folsom Prison Blues', 'Jackson', 'Book of Love', 'Thats Alright', and 'Gypsy'. I hope they enjoy them!  
**Problem:** The query joined artist and listener on `artist_id = listener_id`, which isn't a valid relationship.

## Barriers and Prompting Strategies

I worked on my own database bot for hours, but the zero-shot prompting wasn't successful.
The struggle with attribute access, invalid joins, and non-existent tables was too much, so I used the sample model. 

### Zero-Shot Prompting

Without any examples it returned the top 3 albums by duration and listed albums released before 1970. 
However, it struggled to find playlists with songs by certain artists or suggest songs for a listener. 
It only handled simple questions consistently.

### Single-Domain Double-Shot Prompting

Having examples benefited more complex questions that used
multiple tables. For example, it identified playlists that contain Bob Dylan’s songs and the artist with the most songs. 
But it also joined tables and grouped incorrectly.
