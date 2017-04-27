# playlist-maker
A web app that lets you make a Spotify playlist with songs by artists who are similar to your favorite artist.
Check out some of the <a href="https://open.spotify.com/user/codesue">playlists I've made with Playlist Maker</a>.

Required: <a href="http://flask.pocoo.org/">flask</a>, <a href="https://spotipy.readthedocs.io/en/latest/">spotipy</a>

Usage: edit the following in app.py then run <code>python app.py</code>
```python
SPOTIPY_CLIENT_ID="your-spotify-client-id"
SPOTIPY_CLIENT_SECRET="your-spotify-client-secret"
SPOTIPY_REDIRECT_URI="your-app-redirect-url"
username = ""
```
Alternatively, you can set your app credentials as environment variables. If so, you don't need to pass them to <code>util.prompt_for_user_token</code>.

Homepage:
<img src="https://github.com/codesue/playlist-maker/blob/master/screenshots/playlist_maker_index.png" alt="screenshot of Playlist Maker homepage" />

Example results page:
<img src="https://github.com/codesue/playlist-maker/blob/master/screenshots/playlist_maker_madonna.png" alt="screenshot of Playlist Maker Madonna results" />

Website uses Story theme by <a href="https://html5up.net/">HTML5UP</a>, an <a href="https://unsplash.com/@alicemoore?photo=E--AUpYXbjM">Alice Moore</a> image from Unsplash, and content from Spotify. 
