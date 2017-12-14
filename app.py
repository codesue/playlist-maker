from flask import Flask, request, render_template, redirect, url_for, Markup
import spotipy
import spotipy.util as util

app = Flask(__name__)

# DO NOT PUBLISH CREDENTIALS!
SPOTIPY_CLIENT_ID = "your-spotify-client-id"
SPOTIPY_CLIENT_SECRET = "your-spotify-client-secret"
SPOTIPY_REDIRECT_URI = "your-app-redirect-url"

scope = "playlist-modify-public"
username = ""

token = util.prompt_for_user_token(username, scope, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
sp = spotipy.Spotify(auth=token)

# Debug logging
import logging
import sys
# Defaults to stdout
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
try: 
	log.info('Logging to console')
except:
	_, ex, _ = sys.exc_info()
	log.error(ex.message)


@app.route("/")
def index():
	return render_template("index.html")
	
@app.route("/your-playlist/")
def show_playlist():
	desired_artist = request.args.get("artist_to_search")
	# Handles no artist entered in form
	if not desired_artist:
		return redirect(url_for("index"))
	
	# Search for artist 
	desired_artist_results = sp.search(q="artist:" + desired_artist, type="artist")	
	# Handle artist not found
	if len(desired_artist_results["artists"]["items"]) == 0:
		return redirect(url_for("artist_not_found"))
	# Get artist info	
	desired_artist_entry = desired_artist_results["artists"]["items"][0]
	artist_name = desired_artist_entry["name"]
	artist_uri = desired_artist_entry["uri"]
	artist_image_url = desired_artist_entry["images"][0]["url"]	
		
	# Get related artists
	related_artists = sp.artist_related_artists(artist_uri)		
		
	# Create Playlist
	playlist_name = "Inspired by " + artist_name
	sp.trace = False
	playlist = sp.user_playlist_create(username, playlist_name)
	playlist_id = playlist["id"]
	
	# Make list of tracks
	list_of_tracks = []
	
	# Add artist top tracks to list of tracks
	# Be mindful of number of tracks b/c API limits
	artist_top_tracks = sp.artist_top_tracks(artist_uri)
	song_count = 0
	for track in artist_top_tracks["tracks"]:
		if song_count < 5:
			list_of_tracks.append(track["id"])
			song_count += 1
	
	# Add related artist tracks to list of tracks
	# Max 10 related artists, Max 5 tracks per artist b/c API limits
	related_artist_count = 0
	related_song_count = 0
	for artist in related_artists["artists"]:
		if related_artist_count < 10:
			related_artist_uri = artist["uri"]
			related_artist_top_tracks = sp.artist_top_tracks(related_artist_uri)
			for track in related_artist_top_tracks["tracks"]:
				if related_song_count < 5:
					list_of_tracks.append(track["id"])
					related_song_count += 1
			related_artist_count += 1
			# Reset related_song_count for next artist
			related_song_count = 0
	
	# Add list of tracks to playlist
	add_tracks_to_playlist = sp.user_playlist_add_tracks(username, playlist_id, list_of_tracks)
		
	# Make playlist iframe href
	playlist_iframe_href = "https://open.spotify.com/embed?uri=spotify:user:" + username + ":playlist:" + playlist_id + "&theme=white"
				
	return render_template("your-playlist/index.html", artist_name=artist_name, artist_image_url=artist_image_url, playlist_iframe_href=playlist_iframe_href)

@app.route("/artist-not-found/")
def artist_not_found():
	return render_template("/artist-not-found/index.html")

@app.errorhandler(404)
def page_not_found(e):
	return render_template("/error-pages/404.html")

if __name__ == "__main__":
	app.debug = True
	app.run()
	
	
