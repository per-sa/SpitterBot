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
    song = genius.search_song(song)
    await ctx.send("Searching for lyrics...")
    embed = discord.Embed(title=song.title, description=song.artist, color=0x00ff00)
    embed.add_field(name="Lyrics", value=song.lyrics[:1024])

    if len(song.lyrics) >= 2000:
        await ctx.send("Lyrics are too long to send in a message.")
        await ctx.send(embed=embed)
    await ctx.channel.send(embed=embed)

@bot.command()
async def artist(ctx, *, singer):
    artist = genius.search_artist(singer, max_songs=3)
    embed = discord.Embed(title=artist.name, color=0x00ff00)
    embed.add_field(name="descriptions", value="nothing")
    embed.set_image(url=artist.image_url)
    await ctx.channel.send(embed=embed)


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