import asyncio
import random
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

colors = [0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694, 0x9b59b6, 0x71368a, 0xe91e63,
          0xad1457, 0xf1c40f, 0xc27c0e, 0xe67e22, 0x95a5a6, 0x607d8b, 0x99aab5, 0x546e7a, 0x7289da,
          0x99aab5, 0x2c2f33, 0x23272a]

randcolor = random.choice(colors)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="s!help"))


@bot.command()
async def search(ctx, *, song):
    await ctx.send("Searching for lyrics...")
    song = genius.search_song(song)
    embed = discord.Embed(title=song.title, description=song.artist, url=song.url, color=randcolor)
    embed.add_field(name="Lyrics", value=song.lyrics[:1024])

    if len(song.lyrics) >= 2000:
        await ctx.send("Lyrics are too long to send in a message.")
    await ctx.channel.send(embed=embed)


@bot.command()
async def artist(ctx, *, singer):
    await ctx.send("Searching for the artist and getting data. This may take up to 30 seconds...")
    try:
        async with ctx.typing():
            artist = genius.search_artist(singer, max_songs=3)
            embed = discord.Embed(title=artist.name, url=artist.url, color=randcolor)
            embed.add_field(name="Top 3 Songs",
                            value=artist.songs[0].title + "\n" + artist.songs[1].title + "\n" + artist.songs[2].title)
            embed.set_image(url=artist.image_url)
            await ctx.channel.send(embed=embed)
    except Exception as e:
        await ctx.channel.send("Something went wrong with the response. Try another artist or try again later.")


@bot.command()
async def album(ctx, *, song):
    await ctx.send("Searching for album...")
    song = genius.search_album(song)
    tracks = []
    length = len(song.tracks)

    try:
        for i in range(length):
            tracks.append(song.tracks[i].song.title)

        async with ctx.typing():
            embed = discord.Embed(title=f"{song.name} by {song.artist.name}",
                                  description=f"Release Date: {song.release_date_components.day}/{song.release_date_components.month}/{song.release_date_components.year}",
                                  url=song.url,
                                  color=randcolor)
            embed.add_field(name="Songs", value="\n".join(tracks))
            embed.set_image(url=song.cover_art_url)
            await ctx.channel.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.channel.send("Something went wrong with the response. Try another artist or try again later.")


bot.run(DISCORD_TOKEN)
