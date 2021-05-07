import discord
import youtube_dl
import os
import functools
from discord.ext import commands

client = discord.Client()
client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print("I'm ready...")





#HELP don't work
# @client.command(name='help',pass_context=True)
# async def help(ctx):
#     bot_id = discord.utils.get(client.voice_clients,guild=ctx.guild)
#     channel = discord.utils.get(ctx.guild.text_channels,id=820250499684499476)
#     if ctx.channel.id == channel.id:


#JOIN

@client.command(name='join', pass_context=True)
async def join(ctx):
    bot_id = discord.utils.get(client.voice_clients, guild=ctx.guild)
    channel = discord.utils.get(ctx.guild.text_channels, id=820250499684499476)
    # channel = 820250499684499476                #CHANNEL = "TRACKS"
    # track_channel = discord.utils.get(ctx.guild.text_channels, id= channel)
    if ctx.channel.id == channel.id:
        if bot_id is None or not bot_id.is_connected():
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await ctx.send(f"{ctx.author.mention} Bot is was connected to channel.")
    else:
        await ctx.send(f"{ctx.author.mention} Please use channel `{str(channel).title()}`")
        await ctx.message.delete()


#LEAVE

@client.command(name='leave', pass_context=True)
async def leave(ctx):
    bot_id = discord.utils.get(client.voice_clients, guild=ctx.guild)
    channel = discord.utils.get(ctx.guild.text_channels, id=820250499684499476)               #CHANNEL = "TRACKS"
    if ctx.channel.id == channel.id:
        if bot_id is None or bot_id.is_connected():
            channel = discord.utils.get(client.voice_clients, guild=ctx.guild)
            await channel.disconnect()
        else:
            await ctx.send(f"{ctx.author.mention} Bot is was not connected to channel.")
    else:
        await ctx.send(f"{ctx.author.mention} Please use channel `{str(channel).title()}`")
        await ctx.message.delete()



#PLAY

@client.command(name='play',pass_context = True)
async def play(ctx, url: str):
    bot_id = discord.utils.get(client.voice_clients, guild=ctx.guild)
    channel = discord.utils.get(ctx.guild.text_channels, id=820250499684499476)  # CHANNEL = "TRACKS"
    # track_channel = discord.utils.get(ctx.guild.text_channels, id=channel)

    if ctx.channel.id == channel.id:                                           # channel check
        if bot_id is None or not bot_id.is_connected() and not bot_id.is_playing():
            try:
                channel = ctx.message.author.voice.channel
            except:
                await ctx.send(f"{ctx.author.mention} Please connected to channel")
                return

            ytdl_options = {
                'format': 'bestaudio/best',
                'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
                'restrictfilenames': True,
                'noplaylist': True,
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'logtostderr': False,
                'quiet': True,
                'no_warnings': True,
                'default_search': 'auto',
                'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
                }

            with youtube_dl.YoutubeDL(ytdl_options) as ytdl:
                # ytdl_dl = functools.partial(ytdl.download, [url])
                # await client.loop.run_in_executor(None, ytdl_dl)
                result = ytdl.extract_info(url, download=False)

            vc = await channel.connect()
            vc.play(discord.FFmpegPCMAudio(result['url']))

        else:
            await ctx.send(f"{ctx.author.mention} The bot is already connected to the channel.")
    else:
        await ctx.send(f"{ctx.author.mention} Please use channel `{str(channel).title()}`")
        await ctx.message.delete()



#PAUSE

@client.command(name='pause',pass_context = True)
async def pause(ctx):
    bot_id = discord.utils.get(client.voice_clients, guild=ctx.guild)
    channel = discord.utils.get(ctx.guild.text_channels, id=820250499684499476)
    if ctx.channel.id is channel.id:
        if bot_id is not None and bot_id.is_playing() == True:
            bot_id.pause()
        else:
            if bot_id is None or not bot_id.is_connected() and not bot_id.is_paused():
                await ctx.send(f'{ctx.author.mention} Bot is not connected')
            else:
                await ctx.send(f'{ctx.author.mention} Bot is not playing audio.')




#RESUME

@client.command(name='resume', pass_context=True)
async def resume(ctx):
    bot_id = discord.utils.get(client.voice_clients, guild=ctx.guild)
    channel = discord.utils.get(ctx.guild.text_channels, id=820250499684499476)
    if ctx.channel.id is channel.id:
        if bot_id is not None and bot_id.is_paused() == True:
            bot_id.resume()
        else:
            if bot_id is None or not bot_id.is_connected() and not bot_id.is_playing():
                await ctx.send(f'{ctx.author.mention} Bot is not connected')
            else:
                await ctx.send(f'{ctx.author.mention} Bot is not playing audio.')




#STOP

@client.command(name='stop', pass_context=True)
async def stop(ctx):
    bot_id = discord.utils.get(client.voice_clients,  guild=ctx.guild)
    channel = discord.utils.get(ctx.guild.text_channels, id=820250499684499476)
    if ctx.channel.id is channel.id:
        if bot_id is not None and bot_id.is_playing() == True:
            bot_id.stop()
        else:
            if bot_id is None or not bot_id.is_connected():
                await ctx.send(f'{ctx.author.mention} Bot is not connected')
            else:
                await ctx.send(f'{ctx.author.mention} Bot is not playing audio')




client.run("ODIwMjQ4NzMwOTM0NDQ0MDUz.YEyaKA.TIR27CtAzWZLv6bqoTEuwJnLv8k")