import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from config import settings


# Initialize Firebase
cred = credentials.Certificate("firebase/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=settings['SPOTIFY_CLIENT_ID'], client_secret=settings['SPOTIFY_CLIENT_SECRET'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Read 100 registries from artist_requests collection
artist_requests_ref = db.collection('artist_requests').limit(100)
artist_requests = artist_requests_ref.get()

# Search artists in Spotify API based on strings from artist_requests
for artist_request in artist_requests:
    search_results = sp.search(q=artist_request.get('artist_name'), type='artist')
    artists = search_results['artists']['items']

    # Populate participants collection with artist details
    for artist in artists:
        if artist.get('images') and artist.get('genres'): 
            participant = {
                'category': 'music',
                'detail': artist.get('uri'),
                'image': artist.get('images')[0].get('url'),
                'name': artist.get('name'),
                'genre': artist.get('genres')
            }
            db.collection('participants').add(participant)

    artist_request.reference.delete()
    


