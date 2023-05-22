# Spotify-Scraper

A Python-based application for scraping data from the Spotify API and Genius lyrics API.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview

Spotify Scraper is a tool that allows you to retrieve various data from the Spotify API, including track information, album details, artist data, and lyrics from the Genius website. It utilizes the Spotify Web API and the LyricsGenius Python library.

With Spotify Scraper, you can:

- Search and scrape track data, including track name, artist, album, popularity, and duration.
- Retrieve lyrics for specific songs.
- Scrape album data, including album name, release date, and track listing.
- Extract artist information, such as name, followers, genres, and top tracks.
- Scrape data from playlists and save track information along with lyrics.

## Features

- Track Data Scraping: Retrieve and save track data, including artist, album, popularity, and duration.
- Lyrics Extraction: Scrape lyrics for specific songs using the Genius lyrics website.
- Album Data Scraping: Retrieve and save album data, including release date and track listing.
- Artist Data Extraction: Extract and store artist information, including name, followers, genres, and top tracks.
- Playlist Scraping: Scrape data from playlists and save track information along with lyrics.

## Installation

1. Clone the repository:

git clone https://github.com/your-username/spotify-scraper.git

2. Install the required dependencies:

3. Obtain Spotify API credentials:

- Create a new application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
- Set the redirect URI as `http://localhost:8000/callback`.

- Note down the client ID and client secret.

4. Configure the application:

- Replace `CLIENT_ID` and `CLIENT_SECRET` in `.env` with your Spotify API credentials.

5. Obtain Genius API credentials:

- Create an account on the [Genius Developer Dashboard](https://genius.com/developers).
- Generate a new API token.
- Replace `GENIUS_TOKEN` with your genius API credentials in `.env` .

## Usage

1. Run the `main.py` file:

2. Choose an option from the menu to scrape different data types (tracks, lyrics, albums, artists, playlists).

3. Follow the prompts to enter the required information (e.g., song name, artist name, album name, playlist URI).

4. View the scraped data, which will be saved to CSV files in the project directory.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or inquiries, please contact Sean (mailto: seannlim2000@gmail.com).
