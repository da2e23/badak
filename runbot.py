import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Bot



client = discord.Client(intents=discord.Intents.all())
shop_caller = ''



@client.event
async def on_ready():
    print('로그인되었습니다!')
    print(client.user.name)
    print(client.user.id)
    print('====================================')
@client.event
async def on_message(message):
    if message.content == '핑':
        await message.channel.send('퐁!')
    if message.content == '꿀':
        await message.channel.send('통!')
    if message.content == '동규니':
        await message.channel.send('는 바보지')
    if message.content == '다애':
        await message.channel.send('는 천재지!')
    if message.content.startswith('!바닥가'):
        global shop_caller
        shop_caller = message.author.name
        print(shop_caller+' : shop caller')
        embed = discord.Embed(title="SHOP BOT",description=shop_caller+"님, 환영합니다. \n 쇼핑목록은 다음과 같습니다", color=0x00aaaa)
        embed.add_field(name="STEP🦶", value="빠르게 이동한다", inline=False)
        embed.add_field(name="STUN⚔️", value="스턴!", inline=False)
        msg = await message.channel.send(embed=embed)
        await msg.add_reaction("🦶") #step
        await msg.add_reaction("⚔️") #stun

@client.event
async def on_reaction_add(reaction, user):
    print(user);
    global shop_caller
    if user.bot == 1: #봇이면 패스
        return None
    if shop_caller not in user.name: #메세지 호출한 사람이 아니면 패스
        print(shop_caller+' : shop caller2')
        await reaction.message.channel.send(user.name + "님, !shop을 입력한 후 사용해주세요.")
        return None
    if str(reaction.emoji) == "🦶":
        await reaction.message.channel.send(user.name + "님이 step 아이템을 구매")
    if str(reaction.emoji) == "⚔️":
        await reaction.message.channel.send(user.name + "님이 stun 아이템을 구매")      
client.run(token)
