# SongBPM for Home Assistant

A custom Home Assistant integration that tracks your currently playing media and automatically fetches the track's BPM (Beats Per Minute) in real-time using the GetSongKEY API. 

*Note: This project was inspired by the abandoned `myTselection/SongBPM` repository, but has been completely rebuilt from scratch to use modern Home Assistant UI configuration and the reliable GetSongKEY REST API.*

## Features
* **Real-time Tracking:** Instantly pulls the BPM when your track changes.
* **Graceful Fallback:** Drops to `0 BPM` when the music is paused, stopped, or if a niche track isn't found in the database.
* **UI Configurable:** No YAML required! Setup your media player and API key directly through the Home Assistant Devices & Services menu.

## Prerequisites
Before installing, you need a free API key from GetSongKEY:
1. Go to [getsongkey.com/api](https://getsongkey.com/api)
2. Fill out the quick form to instantly receive your free API Key.

## Installation 

**Method 1: HACS (Recommended)**
1. Open HACS in your Home Assistant instance.
2. Click the three dots in the top right corner and select **Custom repositories**.
3. Add the URL to this repository and select **Integration** as the category.
4. Click **Download** and restart Home Assistant.

**Method 2: Manual**
1. Download this repository.
2. Copy the `custom_components/songbpm` folder into your Home Assistant `config/custom_components` directory.
3. Restart Home Assistant.

## Configuration
1. Go to **Settings** -> **Devices & Services**.
2. Click **Add Integration** and search for **SongBPM**.
3. Enter your GetSongKEY API Key and select the media player you want to track from the dropdown menu.
4. Play a song! Your new `sensor.songbpm` entity will instantly update with the current tempo.
