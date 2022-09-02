import discord
from discord.ext import commands
import lyricsgenius as genius
import os
from dotenv import load_dotenv


load_dotenv()


DISCORD_TOKEN = os.getenv('DISCORDTOKEN')
genius = genius.Genius(os.getenv('GENIUSTOKEN'))
genius.remove_section_headers = True


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='s!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="s!help"))

@bot.command()
async def search(ctx, *, song):
    await ctx.send("Searching for lyrics...")
    song = genius.search_song(song)
    embed = discord.Embed(title=song.title, description=song.artist, color=0x00ff00)
    embed.add_field(name="Lyrics", value=song.lyrics[:1024])

    if len(song.lyrics) >= 2000:
        await ctx.send("Lyrics are too long to send in a message.")
        await ctx.send(embed=embed)
    await ctx.channel.send(embed=embed)

@bot.command()
async def artist(ctx, *, singer):
    await ctx.send("Searching for the artist and getting data. This may take up to 30 seconds...")
    try:
        artist = genius.search_artist(singer, max_songs=3)
        embed = discord.Embed(title=artist.name, url=artist.url, color=0x00ff00)

        embed.add_field(name="Top 3 Songs", value=artist.songs[0].title + "\n" + artist.songs[1].title + "\n" + artist.songs[2].title)
        embed.set_image(url=artist.image_url)
        await ctx.channel.send(embed=embed)
    except TypeError:
        await ctx.channel.send("Something went wrong with the response. Try another artist or try again later.")


@bot.command()
async def album(ctx, *, song):
    song = genius.search_album(song)
    await ctx.send("Searching for lyrics...")
    embed = discord.Embed(title=song.title, description=song.artist, color=0x00ff00)
    embed.add_field(name="Lyrics", value=song.lyrics[:1024])

    if len(song.lyrics) >= 2000:
        await ctx.send("Lyrics are too long to send in a message.")
        await ctx.send(embed=embed)
    await ctx.channel.send(embed=embed)



bot.run(DISCORD_TOKEN)