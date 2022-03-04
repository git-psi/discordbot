import discord
from main import musiques, color, pseudo_createur, link, fun_fact, error, searsh_musics, music_name
from discord.ext import commands
import random
import youtube_dl

ytdl = youtube_dl.YoutubeDL()

class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]


def setup(bot):
    bot.add_cog(MusicCommands(bot))

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def play_song(self, client, video):

        client.stop()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(video.stream_url,before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

        def next(_):
            self.play_song(client, Video(random.choice(musiques)))

                #asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)
        client.play(source, after=next)

    @commands.command()
    async def play(self, ctx, url=random.choice(musiques)):
        await ctx.message.delete()

        client = ctx.guild.voice_client

        message = await ctx.send("Je réfléchie...")

        try:
            if client and client.channel:
                guild = ctx.guild
                channel = guild.get_channel(917815824142725154)
                await client.disconnect()
                client = await channel.connect()
                video = Video(url)
                self.play_song(client, video)
            else:
                guild = ctx.guild
                channel = guild.get_channel(917815824142725154)
                client = await channel.connect()
                video = Video(url)
                self.play_song(client, video)
            embed = discord.Embed(title="**Musique**", description="Un utilisateur fait jouer une musique",color=color["music"])
            embed.add_field(name="Musique",value=f"La musique {video.url} va être joué.\n\nPour passer à la prochaine la commande est `_skip`")
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"Pour rajouter une musique à la liste par default, envoyer un MP à {pseudo_createur}")
            embed.set_thumbnail(url="https://emoji.gg/assets/emoji/8066-youtubemusic.png")
            await message.delete()
            await ctx.send(embed=embed)
        except:
            await ctx.send(embed=error(ctx.author.name,ctx.author.avatar_url, "L'url recherché n'est pas valide !"))
            self.play_song(client, Video(random.choice(musiques)))

    @commands.command()
    async def skip(self, ctx):
        await ctx.message.delete()
        client = ctx.guild.voice_client
        client.stop()
        embed = discord.Embed(title="**Skip**", url=link, color=color["green"])
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=random.choice(fun_fact))
        embed.add_field(name="La musique à bien été skipé", value="Tu peut choisir de jouer ta propre musique avec la commande `_play + url youtube de la vidéo`")
        embed.set_thumbnail(url="https://s1.qwant.com/thumbr/0x0/3/3/1f9babf7342e0950827a928350f5d879adcaabc4e04db906d4c5b21f5cfd21/media-skip-forward-8.png?u=https%3A%2F%2Fwww.iconattitude.com%2Ficons%2Fopen_icon_library%2Factions%2Fpng%2F256%2Fmedia-skip-forward-8.png&q=0&b=1&p=0&a=0")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def leave(self, ctx):
        await ctx.message.delete()
        client = ctx.guild.voice_client
        await client.disconnect()

    @commands.command()
    async def allsong(self, ctx):
        await ctx.message.delete()
        embed = discord .Embed(title="**Toutes les musiques *prédéfinis***", description="Ici tu retrouve la liste de toute les musiques.", url=link, color=color["music"])
        embed.set_footer(text=random.choice(fun_fact))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        url, music_name=searsh_musics()
        all_name_partie=""
        num=0
        for i in music_name:
            num+=1
            all_name_partie+=str(f"{num}    --->    {i}")
        embed.add_field(name="Liste", value=all_name_partie)
        await ctx.send(embed=embed)

"""
@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()

@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()
"""