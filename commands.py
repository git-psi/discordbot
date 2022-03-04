import asyncio
import discord
from main import color, pseudo_createur, fun_fact, error, link, bonjour_message
from discord.ext import commands
import random
from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_components import *
from discord_slash.utils.manage_commands import create_option, create_choice


def setup(bot):
    bot.add_cog(CommandesBasiques(bot))

class CommandesBasiques(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(":ping_pong:    Pong !")

    @commands.command()
    async def say(self, ctx, *text):
        await ctx.message.delete()
        if " ".join(text) == "":
            await ctx.send(embed=error(ctx.author.name, ctx.author.avatar_url,description_error="La commande necessite comme parametre un **texte**.\nExemple: `_say Je suis un super Bot`"))
        else:
            embed = discord.Embed(color=color["violet"])
            embed.add_field(name="Say", value=" ".join(text), inline=True)
            await ctx.send(embed=embed)

    @commands.command()
    async def chinese(self, ctx, *text):
        await ctx.message.delete()
        if " ".join(text) == "":
            await ctx.send(embed=error(ctx.author.name, ctx.author.avatar_url, description_error="La commande necessite comme parametre un **texte**.\nExemple: `_chinese Je suis un super Bot`"))
        else:
            chinese_char = "丹书匚刀巳下呂廾工丿片乚爪冂口尸Q尺丂丁凵V山乂Y乙"
            chinese_text = []
            for word in text:
                for char in word:
                    if char.isalpha():
                        index = ord(char.lower()) - ord("a")
                        transformed = chinese_char[index]
                        chinese_text.append(transformed)
                    else:
                        chinese_text.append(char)
                chinese_text.append("    ")
            embed = discord.Embed(color=color["violet"])
            embed.add_field(name="Chinese", value="".join(chinese_text), inline=True)
            embed.set_footer(text=random.choice(fun_fact))
            await ctx.send(embed=embed)

    @commands.command()
    async def getinfo(self, ctx, info):
        await ctx.message.delete()
        server = ctx.guild
        if info == "membercount":
            title = "Nombre de personnes sur le serveur"
            text = (f"Il y a **{server.member_count}** personnes sur le serveur")
        elif info == "numberofchannel":
            title = "Nombre se salons sur le serveur"
            text = (f"Il y a **{len(server.voice_channels) + len(server.text_channels)}** salons sur le serveur.")
        elif info == "name":
            title = "Nom du serveur"
            text = (f"Le nom du serveur est **{server.name}**")
        else:
            await ctx.send(embed=error(ctx.author.name, ctx.author.avatar_url,
                                       description_error="Etrange... je ne connais pas ce type de renseignement.\nRéessayer la recherche."))
        embed = discord.Embed(title="**Info**", url=link, color=color["black_blue"])
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/3926-exclamation.png")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name=f"**{title}**", value=text)
        embed.set_footer(text=random.choice(fun_fact))
        await ctx.send(embed=embed)

    @commands.command()
    async def bonjour(self, ctx):
        ctx.message.delete()
        embed = discord.Embed(color=color["black_blue"], title=random.choice(bonjour_message), url=link)
        embed.set_image(url="https://emoji.gg/assets/emoji/8726-chacowoah.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        await ctx.message.delete()
        server: discord.Guild
        server = ctx.guild
        number_of_text_channel = len(server.text_channels)
        number_of_voice_channel = len(server.voice_channels)
        embed = discord.Embed(title="**Info sur le serveur**", url=link, color=color["black_blue"])
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.add_field(name="__Info:__", value=
                        f">>> Nom du serveur >> {server. name}\n"
                        f"Nb se personnes >> {server.member_count}\n"
                        f"Nb de *text channel* >> {number_of_text_channel}\n"
                        f"Nb de *voice channel* >> {number_of_voice_channel}\n"
                        f"Afk channel >> {server.afk_channel}\n"
                        f"Id >> {server.id}\n"
                        f"Date de création >> {server.created_at}\n"
                        f"Nb limite d'emojis >> {server.emoji_limit}\n"
                        f"Taille limite de fichier >> {server.filesize_limit}\n"
                        f"Level de vérification >> {server.verification_level}\n"
                        f"Lien d'invitation >> {server.splash}\n"
                        f"Region >> {server.region}\n")
        embed.set_footer(text=random.choice(fun_fact))
        await ctx.send(embed=embed)

    @commands.command()
    async def choix(self, ctx):
        await ctx.message.delete()
        buttons = [
            create_button(style=ButtonStyle.blue, label="Choisissez moi", custom_id="oui"),
            create_button(style=ButtonStyle.danger, label="SURTOUT PAS MOI", custom_id="non")
        ]
        action_row = create_actionrow(*buttons)
        fait_choix = await ctx.send("Faites votre choix !", components=[action_row])

        def check(n):
            return n.author_id == ctx.author.id and n.origin_message.id == fait_choix.id

        button_ctx = await wait_for_component(self.bot, components=action_row, check=check)
        await fait_choix.delete()
        if button_ctx.custom_id == "oui":
            await ctx.send(content="Bravo !")
        else:
            await ctx.send(content="Tu est mort...")

    @commands.command()
    async def quiz(self, ctx):
        await ctx.message.delete()
        select = create_select(
            options=[
                create_select_option("HahA tRoP mAraNt Lol !", value="1", emoji="😂"),
                create_select_option("...", value="2", emoji="😒"),
                create_select_option("Le qrand amour.", value="3", emoji="💛"),
                create_select_option("Renard.", value="4", emoji="🦊"),
                create_select_option("Panda.", value="5", emoji="🐼")
            ],
            placeholder="Choisis un emoji...",
            min_values=1,
            max_values=1
        )
        fait_choix = await ctx.send("Quel est le meilleur emoji de tous les temps ?",
                                    components=[create_actionrow(select)])

        def check(m):
            return m.author_id == ctx.author.id and m.origin_message.id == fait_choix.id

        choix_ctx = await wait_for_component(self.bot, components=select, check=check)
        if choix_ctx.values[0] == "5":
            await choix_ctx.send("Bonne  réponse ! 🐼")
        else:
            await choix_ctx.send("Mauvaise réponse... ce n'était quand meme pas bien dur.")
        await fait_choix.delete()

    @commands.command()
    async def cuisiner(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="**Cuisine**", url=link, color=color["violet"])
        embed.add_field(name="Plat", value="Quelle plat voulez vous cuisiner ?")
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/7019-pancakeflip.png")
        embed.set_footer(text=random.choice(fun_fact))
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        message = await ctx.send(embed=embed)

        def checkMessage(message):
            return message.author == ctx.message.author and ctx.message.channel == message.channel

        try:
            recette = await self.bot.wait_for("message", timeout=10, check=checkMessage)
            await message.delete()
            await recette.delete()
        except:
            await ctx.send(embed=error(ctx.author.name, ctx.author.avatar_url,
                                       description_error="Vous avez été trop long, la recette a été annulé."))
            await recette.delete()
            await ctx.message.delete()
            return
        buttons = [
            create_button(style=ButtonStyle.green, label="Oui", custom_id="y"),
            create_button(style=ButtonStyle.red, label="Non", custom_id="n")
        ]
        action_row = create_actionrow(*buttons)
        embed = discord.Embed(title="**Commencement de la recette**", color=color["violet"])
        embed.add_field(name="Plat",
                        value=f"La préparation de {recette.content} va commencer...\nVeuillez valider, si c'est que vous voulez faire !")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=random.choice(fun_fact))
        embed.set_thumbnail(url="https://s2.qwant.com/thumbr/0x380/7/6/39f3bd26815dda3b3a73a0a51af1efd5898403ad1aa11ad4b812da476ac93d/valid-512.png?u=https%3A%2F%2Fcdn3.iconfinder.com%2Fdata%2Ficons%2Fsecurity-2-1%2F512%2Fvalid-512.png&q=0&b=1&p=0&a=0")
        message = await ctx.send(embed=embed, components=[action_row])

        def check(m):
            return m.author_id == ctx.author.id and m.origin_message.id == message.id

        choix_yes = False
        try:
            button_ctx = await wait_for_component(self.bot, components=action_row, check=check)
            if button_ctx.custom_id == "y":
                embed = discord.Embed(title="**La recette commence**", color=color["violet"])
                embed.add_field(name="Plat", value=f"La recette de {recette.content} a démarré.")
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text=random.choice(fun_fact))
                plat = await ctx.send(embed=embed)
                await message.delete()
                choix_yes = True
            else:
                embed = discord.Embed(title="**Annulation**", color=color["violet"])
                embed.add_field(name="Plat", value=f"La recette de {recette.content} a été stoppé.")
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text=random.choice(fun_fact))
                await ctx.send(embed=embed)
                await message.delete()
        except:
            await ctx.send("Vous avez été trop long, la recette a été annulé !")
            await message.delete
        if choix_yes:
            await asyncio.sleep(5)
            await plat.delete()
            await asyncio.sleep(15)
            plat = await ctx.send("5")
            await asyncio.sleep(1)
            await plat.delete()
            plat = await ctx.send("4")
            await asyncio.sleep(1)
            await plat.delete()
            plat = await ctx.send("3")
            await asyncio.sleep(1)
            await plat.delete()
            plat = await ctx.send("2")
            await asyncio.sleep(1)
            await plat.delete()
            plat = await ctx.send("1")
            await asyncio.sleep(1)
            await plat.delete()
            plat = await ctx.send("0")
            await asyncio.sleep(1)
            await plat.delete()
            embed = discord.Embed(title="**A table**", color=color["violet"])
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=random.choice(fun_fact))
            embed.add_field(name="Le plat est finis !",
                            value=f"Tu vas maintenant pouvoir déguster ton plat de `{recette.content}` !")
            await ctx.send(embed=embed)

    @commands.command()
    async def mp(self, ctx, *, texte="Coucou !"):
        await ctx.message.delete()
        await ctx.author.send(texte)

    @commands.command()
    async def user(self, ctx, user: discord.User):
        await ctx.message.delete()
        embed = discord.Embed(title=f"Toutes les infos sur {user.name}", description=f"---Tu retrouveras ici toutes les infos sur {user.name}---", color=color["bienvenue"], url=link)
        embed.set_image(url=user.avatar_url)
        embed.add_field(name="__Info:__", value=
        f">>> Nom et discriminateur >> {user.name}#{user.discriminator}\n"
        f"Bot >> {user.bot}\n"
        f"Couleur >> {user.color}\n"
        f"Date de création >> {user.created_at}\n"
        f"Id >> {user.id}\n"
        f"Banniere >> {user.public_flags}\n"
        f"Avatar animé >> {user.is_avatar_animated()}\n")
        embed.set_footer(text=random.choice(fun_fact))
        embed.set_author(name=ctx.author.name, url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

