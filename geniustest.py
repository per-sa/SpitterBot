
import lyricsgenius as genius
import os
from dotenv import load_dotenv


load_dotenv()



genius = genius.Genius(os.getenv('GENIUSTOKEN'))
genius.remove_section_headers = True

artist = genius.search_album("come over when you're sober")
print(artist.url)





