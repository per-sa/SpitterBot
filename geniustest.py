
import lyricsgenius as genius
import os
from dotenv import load_dotenv


load_dotenv()



genius = genius.Genius(os.getenv('GENIUSTOKEN'))
genius.remove_section_headers = True

artist = genius.search_artist("Andy Shauf", max_songs=2, sort="title")
print(artist.image_url)




