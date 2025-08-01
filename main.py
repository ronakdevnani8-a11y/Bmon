import os
import discord
from discord.ext import commands
from yt_dlp import YoutubeDL

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

queues = {}

@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")

@bot.command(name="yap")
async def play(ctx, *, query):
    vc = ctx.author.voice
    if not vc:
        await ctx.send("❌ You must be in a voice channel to play music.")
        return

    voice_channel = vc.channel
    if ctx.guild.id not in queues:
        queues[ctx.guild.id] = []

    queues[ctx.guild.id].append((ctx, query))
    if len(queues[ctx.guild.id]) > 1:
        await ctx.send("🎶 Queued...")
        return

    await join_and_play(ctx, voice_channel)

async def join_and_play(ctx, voice_channel):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice_client:
        voice_client = await voice_channel.connect()

    while queues[ctx.guild.id]:
        ctx, query = queues[ctx.guild.id][0]
        await ctx.send("🔍 Searching...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'cookiefile': 'youtube_cookies.txt',
}

        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)['entries'][0]
            url = info['url']
            title = info['title']
            duration = round(info.get('duration', 0) / 60, 2)

        source = await discord.FFmpegOpusAudio.from_probe(url)
        voice_client.play(source)
        embed = discord.Embed(title="🎵 Now Playing", description=title, color=0x00ff00)
        embed.add_field(name="Requested by", value=ctx.author.mention)
        embed.add_field(name="Duration", value=f"{duration} min")
        await ctx.send(embed=embed)

        while voice_client.is_playing():
            await discord.utils.sleep_until(discord.utils.utcnow() + discord.utils.timedelta(seconds=1))
        queues[ctx.guild.id].pop(0)

    await voice_client.disconnect()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
bot.run(TOKEN)
