import logging
import aiohttp
import urllib.parse

_LOGGER = logging.getLogger(__name__)

class ComponentSession:
    """Session manager for SongBPM."""
    def __init__(self, api_key):
        # Save the API key passed from sensor.py
        self.api_key = api_key
        self.headers = {
            "User-Agent": "HomeAssistant/SongBPM"
        }

    async def getSongBpm(self, song_title, artist):
        """Fetch BPM natively using the GetSongKEY REST API."""
        if not self.api_key:
            _LOGGER.error("API Key is missing in utils.py!")
            return None

        # The API requires this specific formatting for highly accurate searches
        search_query = f"song:{song_title} artist:{artist}"
        encoded_query = urllib.parse.quote(search_query)
        
        # The official API endpoint using your custom key
        url = f"https://api.getsong.co/search/?api_key={self.api_key}&type=both&lookup={encoded_query}"

        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url, timeout=10) as response:
                    if response.status != 200:
                        _LOGGER.error("API returned status %s for URL: %s", response.status, url)
                        return None
                    
                    data = await response.json()
                    
                    # The API returns a list of songs in data['search']
                    if 'search' in data and len(data['search']) > 0:
                        # Grab the first (most relevant) result
                        first_result = data['search'][0]
                        if 'tempo' in first_result:
                            bpm = int(first_result['tempo'])
                            _LOGGER.debug(f"Successfully pulled BPM via API: {bpm}")
                            return bpm
                    else:
                        _LOGGER.debug(f"Song not found in database: {search_query}")

        except Exception as e:
            _LOGGER.error("Error fetching BPM for %s: %s", search_query, e)
            
        return None
