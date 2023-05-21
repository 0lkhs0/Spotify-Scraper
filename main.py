# import libraries

import lyricsgenius
from dotenv import load_dotenv
import os
import base64
import requests
from requests import post, get, Timeout
import csv
import json

# load env for tokens
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
genius_token = os.getenv("GENIUS_TOKEN")

# function to get spotify access token


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# function to get headers for gets


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# function to get track id from song name


def get_track_id(token, song_name):
    url = "https://api.spotify.com/v1/search/"
    headers = get_auth_header(token)

    query = f"?q={song_name}&type=track&limit=5"
    query_url = url + query

    result = get(query_url, headers=headers)
    json_result = result.json()
    if len(json_result) == 0:
        return None

    track_items = json_result["tracks"]["items"]
    track_ids = [item["id"] for item in track_items]
    return track_ids

# function to get track data


def get_track_data(token, track_ids):
    track_data_list = []

    for i, track_id in enumerate(track_ids):
        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        headers = get_auth_header(token)

        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        track_data = {
            "name": json_result["name"],
            "artist": json_result["artists"][0]["name"],
            "album": json_result["album"]["name"],
            "release_date": json_result["album"]["release_date"],
            "duration_ms": json_result["duration_ms"],
            "popularity": json_result["popularity"]
        }

        track_data_list.append(track_data)
        print(f"{i+1}. {track_data['name']} - {track_data['artist']}")
    print("0. Exit\n")
    return track_data_list

# function to select track


def selector(data):
    selected = None
    while selected is None:
        try:
            choice = int(input("Select the correct choice... "))
            if 1 <= choice <= 5:
                selected = data[choice-1]
            elif choice == 0:
                return None
            else:
                print("Invalid Choice! Please try again... ")
        except ValueError:
            print("Invalid input! Please try again... ")
    return selected

# function to save track data into csv


def save_track_data_csv(data):
    cwd = os.getcwd()
    file_path = os.path.join(cwd, "track_data.csv")

    if data == None:
        return None
    if not os.path.isfile(file_path):
        with open(file_path, "w") as f:
            writer = csv.DictWriter(
                f, fieldnames=["name", "album", "artist", "duration_ms", "release_date", "popularity"])
            writer.writeheader()

    with open(file_path, "a", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["name", "album", "artist", "duration_ms", "release_date", "popularity"])
        writer.writerow(data)

    print("Track data successfully added into csv!\n")

# get lyrics function


def get_lyrics(song_name, artist_name):
    genius = lyricsgenius.Genius(genius_token, timeout=100000)
    song = genius.search_song(song_name, artist_name)

    if song:
        lyrics = song.lyrics
        return lyrics

    return None

# function to save lyrics to csv


def save_lyrcis_csv(song_name, artist_name, lyrics):
    cwd = os.getcwd()
    file_path = os.path.join(cwd, "lyrics_data.csv")

    data = {
        "Song Name": song_name,
        "Artist Name": artist_name,
        "Lyrics": lyrics
    }

    file_exists = True if os.path.isfile(file_path) else False

    with open(file_path, "a", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["Song Name", "Artist Name", "Lyrics"])

        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

    print("Lyrics saved to CSV successfully! \n")

# function to get album ids


def get_album_ids(token, album_name, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q=album:{album_name} artist:{artist_name}&type=album&limit=5"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_results = result.json()

    if len(json_results) == 0:
        return None

    album_items = json_results["albums"]["items"]

    album_ids = [item["id"] for item in album_items]
    return album_ids

# function to get album data


def get_album_data(token, album_ids):
    album_data_list = []

    for i, album_id in enumerate(album_ids):
        url = f"https://api.spotify.com/v1/albums/{album_id}"
        headers = get_auth_header(token)

        result = get(url, headers=headers)
        json_result = json.loads(result.content)

        album_data = {
            "id": album_id,
            "name": json_result["name"],
            "artist": json_result["artists"][0]["name"],
            "release_date": json_result["release_date"],
            "total_tracks": json_result["total_tracks"],
            "popularity": json_result["popularity"],
            "genres": json_result["genres"],
            "external_urls": json_result["external_urls"]["spotify"]
        }
        album_data_list.append(album_data)
        print(
            f"{i+1}. {album_data['name']} - {album_data['artist']} - {album_data['release_date']}")
        print("")
        return album_data_list

# function to save album data to csv


def save_album_data(album_data):
    cwd = os.getcwd()
    file_path = os.path.join(cwd, "albums_data.csv")

    header = ["Name", "Artist", "Release Date",
              "Total Tracks", "Popularity", "Genres", "external URL"]

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if f.tell() == 0:
            writer.writerow(header)

        writer.writerow([
            album_data["name"],
            album_data["artist"],
            album_data["release_date"],
            album_data["total_tracks"],
            album_data["popularity"],
            ", ".join(album_data["genres"]),
            album_data["external_urls"]
        ])

    print("Album data saved to CSV successfully!")

# function to get album's tracks


def get_album_tracks(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_results = json.loads(result.content)

    track_ids = [track["id"] for track in json_results["items"]]
    return track_ids

# function to get album's track data


def get_album_track_data(token, track_ids):
    album_track_data_list = []
    for i, track_id in enumerate(track_ids):
        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        headers = get_auth_header(token)

        result = get(url, headers=headers)
        json_result = json.loads(result.content)
        track_data = {
            "name": json_result["name"],
            "artist": json_result["artists"][0]["name"],
            "album": json_result["album"]["name"],
            "release_date": json_result["album"]["release_date"],
            "duration_ms": json_result["duration_ms"],
            "popularity": json_result["popularity"]
        }
        album_track_data_list.append(track_data)
        print(f"{i+1}. {track_data['name']} - {track_data['artist']}")

    return album_track_data_list

# function to save the album's tracks and lyrics


def save_album_tracks_lyrics(track, album_name, lyrics):
    cwd = os.getcwd()
    file_path = os.path.join(cwd, "albums_tracks_lyrics.csv")

    header = ["Name", "Artist", "Album", "Popularity", "Duration", "Lyrics"]
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if f.tell() == 0:
            writer.writerow(header)

        writer.writerow([
            track["name"],
            track["artist"],
            album_name,
            track["popularity"],
            track["duration_ms"],
            lyrics
        ])
    print("Album track data and lyrics saved to CSV successfully!\n")

# function to get artist_id


def get_artist_data(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=5"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        return None

    artist_names = [artist["name"] for artist in json_result]
    for i, name in enumerate(artist_names):
        print(f"{i+1}. {name}")

    selected = selector(json_result)
    return selected
# function to save artist data


def save_artist_data(artist_data):
    cwd = os.getcwd()
    file_path = os.path.join(cwd, "albums_tracks_lyrics.csv")

    header = ["Name", "Popularity", "Followers", "Genre", "URL"]
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if f.tell() == 0:
            writer.writerow(header)
        writer.writerow([
            artist_data["name"],
            artist_data["popularity"],
            artist_data["followers"]["total"],
            artist_data["genres"],
            artist_data["external_urls"]["spotify"]
        ])

    print("Artist data saved to CSV successfully!\n")


# function to get all of artist's tracks
def get_all_artist_tracks(token, artist_name, artist_id):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=track&limit=50"

    all_tracks = []

    while True:
        result = get(url + query, headers=headers)
        json_result = json.loads(result.content)

        tracks = json_result.get("tracks", {}).get("items", [])

        artist_tracks = [track for track in tracks if any(
            artist["id"] == artist_id for artist in track.get("artists", []))
        ]

        all_tracks.extend(artist_tracks)

        if "next" in json_result.get("tracks", {}):
            url = json_result["tracks"]["next"]
        else:
            break

    if all_tracks:
        for i, track in enumerate(all_tracks):
            print(f"{i+1}. {track['name']}")
    else:
        print("No tracks found for the given artist.")
    return all_tracks

# function to save artist's tracks and lyrics


def save_artist_track_lyrics(track_data, artist_name, lyrics):
    cwd = os.getcwd()
    file_path = os.path.join(cwd, f"{artist_name}_tracks_lyrics.csv")

    header = ["Name", "Artist", "Album", "Popularity", "Duration", "Lyrics"]

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if f.tell() == 0:
            writer.writerow(header)

        writer.writerow([
            track_data["name"],
            artist_name,
            track_data["album"]["name"],
            track_data["popularity"],
            track_data["duration_ms"],
            lyrics
        ])
    print("Artist track data and lyrics saved to CSV successfully!\n")

# function to scrape playlist


def scrape_playlist_data(token, playlist_uri):
    # Extract the user ID and playlist ID from the URI
    _, user_id, playlist_id = playlist_uri.split(':')

    url = f"https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_results = result.json()

    track_data_list = []

    if "items" in json_results:
        for item in json_results["items"]:
            track = item["track"]
            track_data = {
                "Name": track["name"],
                "Artist": track["artists"][0]["name"],
                "Album": track["album"]["name"],
                "Release Date": track["album"]["release_date"],
                "Popularity": track["popularity"],
                "Duration": track["duration_ms"],
                "URL": track["external_urls"]["spotify"]
            }
            track_data_list.append(track_data)

    return track_data_list

# function to save playlist data to csv


def save_playlist_data(track_data, lyrics):
    cwd = os.getcwd()
    file_path = os.path.join(cwd, "playlist_data.csv")

    header = ["Name", "Artist", "Album",
              "Release date", "Popularity", "Duration", "URL"]

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if f.tell() == 0:
            writer.writerow(header)

        writer.writerow([
            track_data["Name"],
            track_data["Artist"],
            track_data["Album"],
            track_data["Release Date"],
            track_data["Popularity"],
            track_data["Duration"],
            track_data["URL"],
            lyrics
        ])
    print("Playlist track data and lyrics saved to CSV successfully!\n")

# menu function


def menu():
    print("")
    print("SPOTIFY SCRAPER \n")
    print("Getting token... \n")
    token = get_token()
    print("Token obtained successfully... \n")

    while True:
        print("SPOTIFY SCRAPER \n")
        print("Select an option... \n")
        print("[1] --- Scrape tracks's data")
        print("[2] --- Scrape tracks's lyrics")
        print("[3] --- Scrape album's data")
        print("[4] --- Scrape album's tracks and lyrics")
        print("[5] --- Scrape artist's data")
        print("[6] --- Scrape artist's tracks")
        print("[7] --- Scrape a playlist")
        print("[8] --- Quit\n")

        choice = int(input("Please enter your option... :"))
        if choice == 1:
            while True:
                song_name = input(
                    "Please enter the name of the song...  \nEnter 0 to exit\n")

                try:
                    x = int(song_name)
                    if x == 0:
                        break
                except ValueError:
                    pass
                track_ids = get_track_id(token, song_name)
                track_data_list = get_track_data(token, track_ids)
                selected_track_data = selector(track_data_list)
                save_track_data_csv(selected_track_data)
                pass

        if choice == 2:
            while True:
                song_name = input(
                    "Please enter the name of the song...  \nEnter 0 to exit\n")
                try:
                    x = int(song_name)
                    if x == 0:
                        break
                except ValueError:
                    pass
                artist_name = input(
                    "Please enter the name of the artist... \n")

                lyrics = get_lyrics(song_name, artist_name)
                save_lyrcis_csv(song_name, artist_name, lyrics)
                pass

        if choice == 3:
            while True:
                album_name = input(
                    "Please enter the name of the album... \nEnter 0 to exit \n")
                try:
                    x = int(album_name)
                    if x == 0:
                        break
                except ValueError:
                    pass
                artist_name = input(
                    "Please enter the name of the artist... \n")
                album_ids = get_album_ids(token, album_name, artist_name)
                album_data = get_album_data(token, album_ids)
                selected_album = selector(album_data)
                save_album_data(selected_album)
                pass

        if choice == 4:
            while True:
                album_name = input(
                    "Please enter the name of the album... \nEnter 0 to exit \n")
                try:
                    x = int(album_name)
                    if x == 0:
                        break
                except ValueError:
                    pass
                artist_name = input("Please enter the name of the artist...")
                album_ids = get_album_ids(token, album_name, artist_name)
                album_data = get_album_data(token, album_ids)
                selected = selector(album_data)
                track_ids = get_album_tracks(token, selected["id"])
                track_data_list = get_album_track_data(token, track_ids)

                for track in track_data_list:
                    lyrics = get_lyrics(track["name"], artist_name)
                    save_album_tracks_lyrics(track, album_name, lyrics)

                pass

        if choice == 5:
            while True:
                artist_name = input("Please enter an artist's name...")
                try:
                    x = int(album_name)
                    if x == 0:
                        break
                except ValueError:
                    pass
                artist_data = get_artist_data(token, artist_name)
                artist_name = artist_data["name"]
                save_artist_data(artist_data)

            pass

        if choice == 6:
            artist_name = input("Please enter artist's name...")
            artist_data = get_artist_data(token, artist_name)
            artist_id = artist_data["id"]
            artist_name = artist_data["name"]
            tracks = get_all_artist_tracks(token, artist_name, artist_id)
            for track in tracks:
                lyrics = get_lyrics(track["name"], artist_name)
                save_artist_track_lyrics(track, artist_name, lyrics)

            pass

        if choice == 7:
            playlist_uri = input("Please enter the playlist URI...")
            tracks = scrape_playlist_data(token, playlist_uri)
            for track in tracks:
                lyrics = get_lyrics(track["Name"], track["Artist"])
                save_playlist_data(track, lyrics)
            pass
        elif choice == 8:
            print("Quitting... ")
            break

        else:
            print("Invalid choice! Please try again\n")


if __name__ == '__main__':
    menu()
