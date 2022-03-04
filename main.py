import random
from discord.ext import commands#, tasks
from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_components import *
from discord_slash.utils.manage_commands import create_option, create_choice
import asyncio

def searsh_musics():
    musiques=[]
    music_name=[]
    with open("musics.txt") as file:
        for ligne in file:
            if not ligne=="":
                url, name = ligne.split("#")
                music_name.append(name)
                musiques.append(url)
    return musiques, music_name

musiques, music_name=searsh_musics()


pseudo_createur = "⥊Ψ⥋"
fun_fact = [f"Je suis le Bot de Félix alias {pseudo_createur}.",
            "L'eau mouille.",
            "Lorsque vous volez, vous ne touchez pas le sol.",
            "La terre est ronde.",
            "1267x54 fait... un grand nombre.",
            "Dans la vie, il faut avoir des ambitions, et des capacités.",
            "As-tu déjà entendu parler du coronavirus ?",
            "Bonjour.",
            "Je suis... un Bot, et toi ?",
            "Drole de message, non ?",
            "Qui est-tu ?",
            "Je suis moi même, et toi ?",
            "Ceci est un message...",
            f"Tu est... quelqu' un qui connait le grand {pseudo_createur}.",
            "Pourquoi lis-tu cela ?"]
color = {
    "red": 0xe00000,
    "blue": 0x2460ff,
    "error": 0xae0e0e,
    "black_blue": 0x051881,
    "bienvenue": 0x00a420,
    "gray": 0x767676,
    "violet": 0x870092,
    "jaune": 0xe3e300,
    "music": 0x21c811,
    "green": 0x45e400,
    "help":0x0053c2
}

mp = [
    "Salut !",
    "Bonjour à toi.",
    "Je ne parle pas ta langue mais... bonjour.",
    "Coucou.",
    "Je suis le Bot de Félix.",
    "Belle, journée, n'est-ce pas.",
    "T'as vus je peut te répondre.",
    "rien... toujours rien."
]

intents = discord.Intents.default()
intents.members = True
intents.voice_states =intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
bot = commands.Bot(command_prefix="_", description="Bot de Félix", help_command=None, intents=intents)
bonjour_message = ["Bonjour !", "Coucou !", "Salut !", "Je ne te connais pas...mais bonjour à toi !"]
link = "https://www.qwant.com/?q=nada&client=ext-firefox-sb" True
bot = commands.Bot(command_prefix="_", description="Bot de Félix", help_command=None, intents=intents)
bonjour_message = ["Bonjour !", "Coucou !", "Salut !", "Je ne te connais pas...mais bonjour à toi !"]
link = "https://www.qwant.com/?q=nada&client=ext-firefox-sb"

slash = SlashCommand(bot, sync_commands = True)

def bot_proprietary(ctx):
    return ctx.message.author.id == 813458719413239810

def error(author_name, author_url, description_error, link=link):
    embed = discord.Embed(title="**Erreur**", url=link, color=color["error"])
    embed.set_author(name=author_name, icon_url=author_url)
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/3523-win11-erro-icon.png")
    embed.add_field(name="Erreur", value=description_error)
    embed.set_footer(text=random.choice(fun_fact))
    return embed

def good_channel(ctx):
    return ctx.message.channel.id == 918926762942017588

@bot.event
async def on_command_error(ctx, erreur):
    if isinstance(erreur, commands.CommandNotFound):
        await ctx.send(embed=error(ctx.author.name, ctx.author.avatar_url, "Mmmmmmh, je crois bien que cette commande n'existe pas"))
    if isinstance(erreur, commands.MissingRequiredArgument):
        await ctx.send(embed=error(ctx.author.name,ctx.author.avatar_url,"Il manque un argument."))
    elif isinstance(erreur, commands.MissingPermissions):
        await ctx.send(embed=error(ctx.author.name, ctx.author.avatar_url, "Vous n'avez pas les permissions permettant ceci."))
    elif isinstance(erreur, commands.CheckFailure):
        await ctx.send(embed=error(ctx.author.name,ctx.author.avatar_url,"Il semblerait que vous ne puissiez utiliser cette commande.\nElle est peut être reservé à un salon."))
    elif isinstance(erreur, commands.UserNotFound):
        await ctx.send(embed=error(ctx.author.name, ctx.author.avatar_url, "L'utilisateur recherché n'est pas disponible."))
    elif isinstance(erreur.original, discord.Forbidden):
        await ctx.send(embed=error(ctx.author.name, ctx.author.avatar_url, "Je n'ai pas les permissions permettant ceci..."))

@bot.event
async def on_ready():
    print("Le bot est prêt !")
    await bot.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.playing, name=f"Je suis un bot crée par {pseudo_createur}"))

@bot.event
async def on_message(message):
    if not message.author == bot.user:
        if isinstance(message.channel, discord.DMChannel):
            #guild = bot.get_guild(917815824142725150)
            #channel = guild.get_channel(918926762942017588)
            #embed = discord.Embed(title="Message privée", description="Le bot a reçu un message privée !", color=color["jaune"])
            #embed.set_thumbnail(url="https://emoji.gg/assets/emoji/1653-new.png")
            #embed.add_field(name="Auteur", value=message.author)
            #embed.add_field(name="Message", value=message.content)
            #embed.set_footer(text=random.choice(fun_fact))
            #await channel.send(embed=embed)
            reponse = await message.author.send("...")
            await asyncio.sleep(2)
            await reponse.edit(content=random.choice(mp))
            await bot.process_commands(message)
        else:
            await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    await reaction.message.add_reaction(reaction.emoji)

"""
@bot.event
async def on_message_delete(message):
    await message.channel.send(f"Le message de {message.author} a été supprimé.\n> {message.content}")

@bot.event
async def on_message_edit(after, before):
    await before.channel.send(f"{before.author} a édité un message:\n- Avant:   *{after.content}*\n- Après:   *{before.content}*")
"""


@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(917815824142725153)
    embed = discord.Embed(title="**Bienvenue**", description=f"Bienvenue sur mon serveur !", url=link,
                          color=color["bienvenue"])
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/1463-wave.gif")
    embed.add_field(name="Bonjour !",
                    value=f"Bienvenue à toi,{member.mention} sur mon serveur. Je suis un Bot programmé par Félix.",
                    inline=True)
    embed.set_footer(text="Pour toute information, demander à Félix alias ⥊Ψ⥋#1188")
    await channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    channel = member.guild.get_channel(917815824142725153)
    embed = discord.Embed(title="**Au revoir**", description=f"Un membre a quitté le serveur !", url=link,
                          color=color["bienvenue"])
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/8167-chacosweat.png")
    embed.add_field(name="Une derniere parole !",
                    value=f"Au revoir {member.mention}, nous t'aimions tous (enfin, je crois)...", inline=True)
    embed.set_footer(text=random.choice(fun_fact))
    await channel.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, name = None):
    if name:
        try:
            bot.unload_extension(name)
            await ctx.send(f"Unloading....{name}")
        except:
            pass
        bot.load_extension(name)
        await ctx.send(f"Loading....{name}")

@slash.slash(name="dice",guild_ids=[917815824142725150] , description="Lance un dé", options=[
    create_option(name="tricher", description="Si oui, la réponse sera forcémen 4.", option_type=3, required=True, choices=[create_choice(name="Oui",value="y"), create_choice(name="Non", value="n")]),
    create_option(name="limite_inferieur", description="Le nombre minimal que le dés peut donner(1 par default).", option_type=4, required=False),
    create_option(name="limite_superieur", description="Le nombre maximal que le dés peut donner(6 par default).", option_type=4, required=False)
])
async def dice(ctx, limite_inferieur = 1, limite_superieur = 6, tricher = False):
    m1 = await ctx.send("Je lance le dé...")
    await asyncio.sleep(1)
    if tricher=="n": num = random.randint(limite_inferieur,limite_superieur)
    else: num=4
    await m1.delete()
    embed = discord.Embed(title="**Dé**", url=link, color=color["violet"])
    embed.set_footer(text=random.choice(fun_fact))
    embed.add_field(name="Résultat", value=f"Le résultat est **{num}** !")
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/grey_dice.png")
    await ctx.send(embed=embed)



bot.load_extension("commands")
bot.load_extension("music_commands")
bot.load_extension("moderation_commands")
bot.load_extension("help_command")

bot.run("The token of the bot is here.")
