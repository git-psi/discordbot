import asyncio
import discord
from main import color, pseudo_createur, fun_fact, error, link
from discord.ext import commands
import random
#from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_components import *
#from discord_slash.utils.manage_commands import create_option,

def setup(bot):
    bot.add_cog(HelpCommand(bot))

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_commands = "> `_play` -> Fait jouer une musique aléatoire depuis la liste définie.\n" \
                            "> `_play` + `url` -> Fait jouer la musique depuis youtube.\n" \
                            "> `_leave` -> Le bot quitte le channel vocal.\n" \
                            "> `_skip` -> Passe à la prochaine musique.\n" \
                            "> `_allsong` -> Permet d'afficher la liste des musiques par défault."

        self.moderation_commands = "> `_private` -> Tu ne peut pas faire cette commande.\n" \
                                 "> `_ban` + `nom du membre` (+ `raison`) -> Ban le membre.\n" \
                                 "> `_unban` + `nom du membre` (+ `raison)` -> Unban le membre.\n" \
                                 "> `_kick` + `nom du membre` (+ `raison`) -> Kick le membre.\n" \
                                 "> `_banid` -> Permet de voir le nom et l'id des membres bannis.\n" \
                                 "> `_clear` + `nombre` -> Efface x message du salon."

        self.basic_commands = "> `_bonjour` -> Le bot envoie un message *bonjour*.\n" \
                              "> `_ping` -> Le bot répond...\n" \
                              "> `_say` + `texte` -> Le bot parle à ta place.\n" \
                              "> `_say` + `texte` -> Comme *_say* avec une écriture chinoise (lisible).\n" \
                              "> `_getinfo` + `membercount` + `name` ou `numberofchannel` -> Le bot revoie le renseignement demandé.\n" \
                              "> `_serverinfo` -> Renvoie les info. du serveur.\n" \
                              "> `_choix` -> Un choix très dure se profile...\n" \
                              "> `_quiz` -> Un quiz assez simple.\n" \
                              "> `_cuisiner` -> Permet de cuisiner un plat (choisi).\n" \
                              "> `_mp` + `texte` -> Le bot vous envoie un message privé contenant *texte*.\n" \
                              "> `_user` + `@username` -> Le bot renvoie plusieur info sur l'utilisateur."

        self.slash_basic_commands = "> `/dice` -> Permet de lancer un dé."

        self.slash_moderation_commands = "***Pour l'instant rien***"

        self.slash_music_commands = "***Pour l'instant rien***"


    @commands.command()
    async def help(self, ctx):
        await ctx.message.delete()
        select = create_select(
            options=[
                create_select_option("Commandes slash", value="1"),
                create_select_option("Commandes normales", value="2"),
                create_select_option("Fermer le message", value="3")
            ],
            placeholder="Choisis une option...",
            min_values=1,
            max_values=1
        )
        embed = discord.Embed(title="**Help**", color=color["help"], url=link)
        embed.add_field(name="Choix", value="Choisie quelle option t'interesses.")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        fait_choix = await ctx.send(embed=embed, components=[create_actionrow(select)])

        def check(m):
            return m.author_id == ctx.author.id and m.origin_message.id == fait_choix.id

        choix_ctx = await wait_for_component(self.bot, components=select, check=check)
        await fait_choix.delete()
        if choix_ctx.values[0]=="1":
            embed = discord.Embed(title="**Toutes les commandes**", color=color["help"], url=link)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text="Certaines commandes cachés ne sons pas dans cette liste.")
            embed.set_thumbnail(url="https://s1.qwant.com/thumbr/0x0/b/6/a766c4d880eae6dfe1c92993bab00e3c33f71c1096b1cb9e3f297f2c5e5f70/need-help-png-tap-our-wordpress-experts-for-help-support-266.png?u=https%3A%2F%2Fpluspng.com%2Fimg-png%2Fneed-help-png-tap-our-wordpress-experts-for-help-support-266.png&q=0&b=1&p=0&a=0")
            embed.add_field(name="**__Musique__**", value=self.slash_music_commands)
            embed.add_field(name="**__Moderation__**", value=self.slash_moderation_commands, inline=False)
            embed.add_field(name="**__Basique__**", value=self.slash_basic_commands, inline=False)
        elif choix_ctx.values[0]=="2":
            embed = discord.Embed(title="**Toutes les commandes**", color=color["help"], url=link)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text="Certaines commandes cachés ne sons pas dans cette liste.")
            embed.set_thumbnail(url="https://s1.qwant.com/thumbr/0x0/b/6/a766c4d880eae6dfe1c92993bab00e3c33f71c1096b1cb9e3f297f2c5e5f70/need-help-png-tap-our-wordpress-experts-for-help-support-266.png?u=https%3A%2F%2Fpluspng.com%2Fimg-png%2Fneed-help-png-tap-our-wordpress-experts-for-help-support-266.png&q=0&b=1&p=0&a=0")
            embed.add_field(name="**__Musique__**", value=self.music_commands)
            embed.add_field(name="**__Moderation__**", value=self.moderation_commands, inline=False)
            embed.add_field(name="**__Basique__**", value=self.basic_commands, inline=False)
        else:
            embed = discord.Embed(title="**Annulation**", color=color["help"], url=link, description="💡  La commande a bien été annulée !")
            embed.set_footer(text=random.choice(fun_fact))
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
