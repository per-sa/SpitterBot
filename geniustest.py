
import lyricsgenius as genius
import os
from dotenv import load_dotenv


load_dotenv()



genius = genius.Genius(os.getenv('GENIUSTOKEN'))
genius.remove_section_headers = True

artist = genius.search_artist("Lil Peep", max_songs=2, sort="title")
print(artist[0]["alternate_names"])




