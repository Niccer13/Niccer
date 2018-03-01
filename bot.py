# lobo by Niccer

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import chalk
from datetime import datetime, date, time
import safygiphy
import io
import requests
import random



startup_extensions = ["Music"]
g = safygiphy.Giphy()
bot = commands.Bot(command_prefix='#')
testmsgid = None
testmsguser = None
awaitmsg = None
botmsg = None




@bot.event
async def on_ready():
    print("Ready")
    print("I am running on " + bot.user.name)
    print ("with the ID: " + bot.user.id)
    await bot.change_presence(game=discord.Game(name="Woyer"))

@bot.event
async def on_member_join(member):
    await bot.send_message(discord.Object(id="216945205759180800"), "Vitaj na servery, {}".format(member.mention))

@bot.event
async def on_member_remove(member):
    await bot.send_message(discord.Object(id="216945205759180800"), "{} opustil server".format(member.mention))

class Main_Commands():
    def __init__(self, bot):
        self.bot = bot

@bot.command(pass_context=True)
async def skap(ctx):
    await bot.say("ty skap")

@bot.command(pass_context=True)
async def nohy(ctx):
    await bot.say("Jakub nemá nohy")
   
@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find: ", color=0x00ff00)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(title="{}'s info".format(ctx.message.server.name), description="Here's what I could find: ", color=0x00ffff)
    embed.add_field(name="Server Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="Server ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def thetime(ctx):
    embed = discord.Embed(title="", description="", color=0xff0000)
    embed.add_field(name="Date", value=datetime.now().strftime("%Y-%m-%d"))
    embed.add_field(name="Time", value=datetime.now().strftime("%H:%M:%S"))
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def gif(ctx):
        gif_tag = ctx.message.content[5:]
        rgif = g.random(tag=str(gif_tag))
        response = requests.get(
         str(rgif.get("data", []).get('image_original_url')), stream=True
        )
        await bot.send_file(ctx.message.channel, io.BytesIO(response.raw.read()), filename='video.gif')

@bot.command(pass_context=True)
async def coinflip(ctx):
    choice = random.randint(1,2)
    if choice == 1:
        await bot.add_reaction(ctx.message, "🔴")
    else:
        await bot.add_reaction(ctx.message, "🔵")

@bot.command(pass_context=True)
async def status(ctx):
    game = ctx.message.content[8:]
    await bot.change_presence(game=discord.Game(name=game))
    await bot.send_message(ctx.message.channel, "Current Status: " + game)

@bot.command(pass_context=True)
async def kick(ctx, user: discord.Member):
    if "218765419228561409" in [role.id for role in ctx.message.author.roles]: 
        await bot.say("{} has been kicked out of the server!".format(user.name))
        await bot.kick(user)
    else:
        await bot.say("You don't have permission for this command")

@bot.command(pass_context=True)
async def ban(ctx, user: discord.Member):
    if "218765419228561409" in [role.id for role in ctx.message.author.roles]:
        await bot.say("{} has been banned from the server!".format(user.name))
        await bot.ban(user, delete_message_days=7)
    else:
        await bot.say("You don't have permission for this command")

@bot.command(pass_context=True)
async def unban(ctx):
    ban_list = await bot.get_bans(ctx.message.server)


    await bot.say("Ban list:\n{}".format("\n".join([user.name for user in ban_list])))

    if not ban_list:
        await bot.say("Ban list is empty.")
        return
    if "218765419228561409" in [role.id for role in ctx.message.author.roles]:
        try:
            await bot.unban(ctx.message.server, ban_list[-1])
            await bot.say("Unbanned user: `{}`".format(ban_list[-1].name))
        except discord.Forbidden:
            await bot.say("I do not have permission to unban.")
            return
        except discord.HTTPException:
            await bot.say("Unban failed.")
            return
    else:
        await bot.say("You don't have permission for this command")

@bot.command(pass_context = True)
async def clear(ctx, number):
    number = int(ctx.message.content[7:])
    counter = 0
    if "218765419228561409" in [role.id for role in ctx.message.author.roles]:
        async for x in bot.logs_from(ctx.message.channel, limit = number):
            if counter < number:
                await bot.delete_message(x)
                counter += 1
    else:
        await bot.say("You don't have permission for this command")

            
             

@bot.command(pass_context=True)
async def poll(ctx):

    global botmsg  
    botmsg = ctx.message.content[6:]

    global awaitmsg
    awaitmsg = await bot.say(botmsg)
    await bot.add_reaction(awaitmsg, "✅")
    await bot.add_reaction(awaitmsg, "❎")
    await bot.add_reaction(awaitmsg, "🤷")

    global testmsgid
    testmsgid = awaitmsg.id


@bot.event
async def on_reaction_add(reaction, user):
    msg = reaction.message
    chat = reaction.message.channel


    if reaction.emoji == "✅" and reaction.count == 3 and msg.id == testmsgid:
        await bot.send_message(chat, botmsg + " - Áno")
        await bot.delete_message(awaitmsg)
    if reaction.emoji == "❎" and reaction.count == 3 and msg.id == testmsgid:
        await bot.send_message(chat, botmsg + " - Nie")
        await bot.delete_message(awaitmsg)
   






if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = "{}: {}".format(type(e).__name__, e)
            print("Failed to load extension {}\n{}".format(extension, exc))







bot.run("NDE3ODI1MTQzMzA2MzIxOTQw.DXcy8Q.YPXp_s-RSFe4Plx-B-o9Ak3hCj8")
