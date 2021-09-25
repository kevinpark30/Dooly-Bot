# import libraries
import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv
import youtube_dl

# number characters for the poll
numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣")

# load in the bot token from the .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# set up the intents for the bot; we want the members intent so the bot can recognize if a member
# joins or leaves a server
intents = discord.Intents.default()
intents.members = True

# create a bot object with the given command prefix and intents
bot = commands.Bot(command_prefix="$", intents=intents)

# EVENT: when the bot connects to Discord
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord")

# EVENT: when the bot recognizes a user joins a guild
@bot.event
async def on_member_join(member):
    try:
        channel = discord.utils.get(bot.get_all_channels(), name="general")
        await channel.send(f"Welcome {member.mention} to the server! It's good to have you here!")
    except:
        print("Channel 'general' not found.")

# BOT_COMMMAND: to roll a number between 1 and the given number
@bot.command(name="roll", help="Rolls a number between 1 and the given number")
async def roll(ctx, max_roll):
    try:
        max_roll = int(max_roll)
    except:
        await ctx.send("You have to supply an integer number.")
    if max_roll <= 0:
        await ctx.send("You have to supply a number greater than or equal to 1.")
    roll = random.choice(range(1, max_roll + 1))
    await ctx.send("Dooly rolled a " + str(roll) + ".")

# BOT_COMMAND: to roll a six-sided die
@bot.command(name="rolldie", help="Rolls a die")
async def rolldie(ctx):
    die = random.choice(range(1, 7))
    await ctx.send("Dooly rolled a " + str(die) + ".")

# BOT_COMMAND: flips a coin
@bot.command(name="coinflip", help="Flips a coin")
async def coinflip(ctx):
    outcomes = ["heads", "tails"]
    await ctx.send("Dooly flipped a ".join(outcomes[random.randint(0,1)]).join("."))

# BOT_COMMAND: create a poll
@bot.command(name="poll", help="Creates a poll with the given question in quotes and options after")
async def poll(ctx, question, *options):
    if len(options) > 9:
        await ctx.send("Poll can only have up to 9 options.")
    else:
        embed = discord.Embed(title="Poll", description=question)

        fields = [("Options", "\n".join([f"{numbers[idx]} {options[idx]}" for idx in range(len(options))]), False), ("Instructions", "React with a vote!", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        
        poll = await ctx.send(embed=embed)

        for reaction in numbers[:len(options)]:
            await poll.add_reaction(reaction)

# BOT_COMMAND: plays the song with the given url of a YouTube video
@bot.command(name="play", help="Plays the song with the given url from YouTube")
async def play(ctx, url: str):
    # get the VoiceState of the user who wrote the message 
    user = ctx.author
    voice_state = user.voice

    # check if the user who typed the command is in a voice channel, the bot will join the user's voice channel and play music only if the user is in a voice channel
    if voice_state == None:
       await ctx.send(f"{user.name} is not in a voice channel.")
    else:
        # check if there is a song file
        song_exists = os.path.isfile("song.webm")
        try:
            # if the song file is there, remove it (we need to play a new song since this event is called)
            if song_exists:
                os.remove("song.webm")
        except:
            # this means that we were trying to remove the song while it was playing
            await ctx.send("Wait till the song ends or use the '$stop' command to end the song.")

        # check if the bot is already connected to a voice channel and join the channel if not
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice_client == None:
            voice_channel = voice_state.channel
            await voice_channel.connect()

        # create youtube_dl options
        youtube_dl_options = {
            'format': '249',
        }

        with youtube_dl.YoutubeDL(youtube_dl_options) as ydl:
            # download the url
            ydl.download([url])
        
        for file in os.listdir("./"):
            # find the file that ends with .webm and rename it to song.webm so that we can find it later
            if file.endswith(".webm"):
                os.rename(file, "song.webm")
                
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice_client.play(discord.FFmpegOpusAudio("song.webm"))

# BOT_COMMAND: makes the bot leave from a voice channel
@bot.command(name="leave", help="Disconnects the bot from a voice channel")
async def leave(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice_client == None:
        await voice_client.disconnect()
    else:
        await ctx.send("Dooly is not connected to a voice channel.")

# BOT_COMMAND: pauses the bot from playing a song
@bot.command(name="pause", help="Pauses the song the bot is playing")
async def pause(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice_client == None:
        if voice_client.is_playing():
            voice_client.pause()
        else:
            await ctx.send("Dooly is not playing music.")
    else:
        await ctx.send("Dooly is not in a voice channel.")

# BOT_COMMAND: resumes the bot from playing a song
@bot.command(name="resume", help="Resumes the song the bot was playing")
async def resume(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice_client == None:
        if voice_client.is_paused():
            voice_client.resume()
        else:
            await ctx.send("Dooly did not pause music.")
    else:
        await ctx.send("Dooly is not in a voice channel.")

# BOT_COMMAND: stops the bot from playing a song
@bot.command(name="stop", help="Stops the song the bot was playing")
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice_client == None:
        voice_client.stop()
    else:
        await ctx.send("Dooly is not in a voice channel.")

# BOT_COMMAND: Dooly tells people to play KEAFFA
@bot.command(name="keaffa", help="Tells everyone to play KEAFFA")
async def keaffa(ctx):
    await ctx.send("are we playing keaffa tonight???")

# BOT_COMMAND: Dooly tells people to play KEAFFA (2)
@bot.command(name="keaffa2", help="Tells everyone to play KEAFFA")
async def keaffa2(ctx):
    await ctx.send("are we KEAFING???")

# BOT_COMMAND: Dooly tells people to play KEAFFA (3)
@bot.command(name="keaffa3", help="Tells everyone to play KEAFFA")
async def keaffa3(ctx):
    await ctx.send("ARE\n"+ "WE\n" + "KEAFING\n" + "TODAY?\n" + "PLEASE\n" + "I DONT WANT TO PLAY TFT")

# BOT_COMMAND: Dooly tells people to play amogus
@bot.command(name="amogus", help="Tells everyone to play amogus")
async def amogus(ctx):
    await ctx.send("AMONG US @8PM\n" + "CANCEL ALLLLLLLL YOUR PLANS\n" + "DONT EVEN THINK ABOUT DOING\n" + "HOMEWORK")

# BOT_COMMAND: Dooly sends doomfingers picture
@bot.command(name="doomfingers", help="sends doomfingers")
async def doomfingers(ctx):
    filepath = os.getcwd() + "\\Pictures\\doomfingers.png"
    await ctx.send(file=discord.File(filepath))

# BOT_COMMAND: Dooly sends maplestory gif
@bot.command(name="maplestory", help="sends maplestory gif")
async def maplestory(ctx):
    filepath = os.getcwd() + "\\Pictures\\maple-story-jon.gif"
    await ctx.send(file=discord.File(filepath))

# BOT_COMMAND: Dooly sends attention picture
@bot.command(name="overwatch", help="Tells everyone to play Overwatch")
async def overwatch(ctx):
    filepath = os.getcwd() + "\\Pictures\\overwatch.png"
    await ctx.send(file=discord.File(filepath))

# BOT_COMMAND: Dooly sends cringe gif
@bot.command(name="cringe", help="Tells someone they are cringe")
async def cringe(ctx):
    filepath = os.getcwd() + "\\Pictures\\cringe.gif"
    await ctx.send(file=discord.File(filepath))

bot.run(TOKEN)