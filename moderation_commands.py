import discord
from discord.ext import commands
from main import fun_fact, color, link, bot_proprietary, error
import random

def setup(bot):
    bot.add_cog(ModerationCommands(bot))

class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def banid(self, ctx):
        await ctx.message.delete()
        banned_user = await ctx.guild.bans()
        embed = discord.Embed(title="ID des utilisateurs bannis", url=link, color=color["gray"])
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/3283-pepe-banned.png")
        list = ""
        for i in banned_user:
            list += f"{i.user.name} --> `{i.user.id}`\n"
        if list == "":
            list = "Il n'y en a pas"
        embed.add_field(name="Liste des id des utilisateurs bannis", value=list, inline=True)
        embed.set_footer(text=random.choice(fun_fact))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.check(bot_proprietary)
    async def private(self, ctx):
        embed = discord.Embed(title="**Commande privée**", url=link, color=color["black_blue"])
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/9897-verified.gif")
        embed.add_field(name="Privée", value="Eh oui, seulement le proprietaire du bot peut utiliser cette commande !",)
        embed.set_footer(text="Je suis d'accord avec toi cela ne sert à rien, mais bon...", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, number: int):
        await ctx.message.delete()
        messages = await ctx.channel.history(limit=number + 1).flatten()
        for message in messages:
            await message.delete()
        embed = discord.Embed(title="**Message(s) supprimé(s)**", url=link, color=color["red"])
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/6414-robut-trash.png")
        embed.add_field(name="Nombre de message(s) supprimé(s)",
                        value=f"**{number}** message(s) ont bien été supprimé !")
        embed.set_footer(text=random.choice(fun_fact))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, username: discord.User, *, reason="*Aucune raison n'a été donné !*"):
        await ctx.message.delete()
        await ctx.guild.kick(username, reason=reason)
        embed = discord.Embed(title="**Exclusion**", description="Un modérateur a frappé !", url=link,
                              color=color["red"])
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/4542-xmas-hammer-ban.png")
        embed.add_field(name="Membre exclu", value=username.name, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.set_footer(text=random.choice(fun_fact))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, username: discord.User, *, reason="*Aucune raison n'a été donné !*"):
        await ctx.message.delete()
        await ctx.guild.ban(username, reason=reason)
        embed = discord.Embed(title="**Banissement**", description="Un modérateur a frappé !", url=link,
                              color=color["red"])
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://emoji.gg/assets/emoji/6623_banhammer.png")
        embed.add_field(name="Membre banni", value=username.name, inline=True)
        embed.add_field(name="Raison", value=reason, inline=True)
        embed.set_footer(text=random.choice(fun_fact))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unban(self, ctx, user, *, reason="*Aucune raison n'a été donné !*"):
        name, id = user.split("#")
        banned_user = await ctx.guild.bans()
        for i in banned_user:
            if i.user.name == name and i.user.discriminator == id:
                await ctx.guild.unban(i.user, reason=reason)
                await ctx.message.delete()
                embed = discord.Embed(title="**Dé-Bannissement**", description="Un modérateur a réfléchis !", url=link,
                                      color=color["blue"])
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url="https://emoji.gg/assets/emoji/7191_unban_hammer.png")
                embed.add_field(name="Membre dé-banni", value=name, inline=True)
                embed.add_field(name="Raison", value=reason, inline=True)
                embed.set_footer(text=random.choice(fun_fact))
                await ctx.send(embed=embed)
                return
        await ctx.send(embed=error(ctx.author.name, ctx.author.avatar_url, description_error="L'utilisateur recherché n'est pas dans la liste des bannis du serveur !"))

