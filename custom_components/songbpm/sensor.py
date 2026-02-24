import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.const import CONF_API_KEY

from .const import DOMAIN
from .utils import ComponentSession

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up SongBPM sensor based on a config entry."""
    # Get the media player and API key you selected in the setup menu
    media_player_id = entry.data.get("media_player") or entry.options.get("media_player")
    api_key = entry.data.get(CONF_API_KEY) or entry.options.get(CONF_API_KEY)
    
    if not media_player_id:
        _LOGGER.error("No media player configured for SongBPM")
        return
        
    if not api_key:
        _LOGGER.error("No API key configured for SongBPM")
        return
        
    sensor = SongBPMSensor(entry, media_player_id, api_key)
    async_add_entities([sensor], True)

class SongBPMSensor(SensorEntity):
    """Representation of the SongBPM sensor."""

    def __init__(self, entry, media_player_id, api_key):
        self._entry = entry
        self._media_player_id = media_player_id
        self._attr_name = f"SongBPM"
        self._attr_unique_id = f"{entry.entry_id}_bpm"
        self._attr_native_value = 0
        self._attr_native_unit_of_measurement = "BPM"
        self._attr_icon = "mdi:metronome"
        # Hand the API key over to our session manager
        self._session = ComponentSession(api_key)
        self._last_song = None

    async def async_added_to_hass(self):
        """Run when entity is added to Home Assistant."""
        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [self._media_player_id], self._async_media_player_changed
            )
        )

    async def _async_media_player_changed(self, event):
        """Handle media player state changes."""
        new_state = event.data.get("new_state")
        
        # If the player is paused, idle, off, or unavailable, drop BPM to 0
        if new_state is None or new_state.state != "playing":
            self._attr_native_value = 0
            self._last_song = None  # Clear the last song so it triggers again when unpaused
            self.async_write_ha_state()
            return

        artist = new_state.attributes.get("media_artist")
        title = new_state.attributes.get("media_title")

        # If a song is playing but missing ID3 tags, drop BPM to 0
        if not artist or not title:
            self._attr_native_value = 0
            self.async_write_ha_state()
            return

        current_song = f"{artist} - {title}"
        
        # Don't waste network calls if the song hasn't changed
        if current_song == self._last_song:
            return 

        self._last_song = current_song
        _LOGGER.debug(f"New song detected: {current_song}. Fetching BPM...")

        # Run the API fetcher
        bpm = await self._session.getSongBpm(title, artist)
        
        # If a BPM is found, use it. Otherwise, drop to 0.
        if bpm:
            self._attr_native_value = bpm
        else:
            self._attr_native_value = 0
            
        self.async_write_ha_state()
