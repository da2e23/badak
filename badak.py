from email import message
from multiprocessing.connection import wait
from random import choices
import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
import time
# import discord
import nextcord
from spreadsheet import *
from exchangerate import *
from getmyprice import *
from nextcord.ext.menus import button, First, Last
from asyncore import loop
from nextcord.ext import commands,menus
# from discord.commands import Option
from nextcord import Interaction, SlashOption, ChannelType
import os

# bot = commands.Bot(command_prefix = "/",intents=discord.Intents.all())
bot = commands.Bot()
project_list =[]
async def list_search(ctx):
    return sorted([i for i in worksheet.col_values(1) if i.startswith(ctx.value.lower())]) # from your database

#지갑 바닥가 가져오기
async def get_own_floorprice(session,url):
    async with session.get(url) as resp:
        data = await resp.json()
        return data['collection']['stats']['floor_price']
#지갑 바닥가 합계 구하기
class getSum():
    def __init__(self, total_sum):
        self.total_sum = total_sum
    def get_total_sum(self,list):
        self.total_sum = sum(filter(None,list))
gs = getSum(0.0)

#time 변수
class getTime():
    def __init__(self, time):
        self.time = time
    def time_reset(self):
        self.time = 5
    def time_setting(self,g_time):
        self.time = g_time          
time_second = getTime(0)

# async def get_own_floorprice(list,price):
#     for i in list:
#         price.append(requests.request("GET", i).json()['collection']['stats']['floor_price'])
class MyMenuPages(menus.MenuPages, inherit_buttons=False):
    @button(emoji="⏮️", position=First(0))
    async def go_to_first_page(self, payload):
        global time_second
        time_second.time_setting(5)
        await self.show_page(0)

    @button(emoji="⬅️", position=First(1))
    async def go_to_previous_page(self, payload):
        global time_second
        time_second.time_setting(5)
        await self.show_checked_page(self.current_page - 1)

    @button(emoji="➡️", position=Last(1))
    async def go_to_next_page(self, payload):
        global time_second
        time_second.time_setting(5)
        await self.show_checked_page(self.current_page + 1)

    @button(emoji="⏭️", position=Last(2))
    async def go_to_last_page(self, payload):
        global time_second
        time_second.time_setting(5)
        max_pages = self._source.get_max_pages()
        last_page = max(max_pages - 1, 0)
        await self.show_page(last_page)

#discord.ext menus/ nextcord.ext menus
class MySource(menus.ListPageSource):
    async def format_page(self, menu, entries):
        embed = nextcord.Embed(title="Project List" ,description='', color=0xf1c40f)
        for i in entries:
            embed.add_field(name="\u200b", value=f"{i}", inline=False)
        embed.set_footer(text="Honey Bottle🍯 | Badak")
        return embed
class MySource_price(menus.ListPageSource):
    async def format_page(self, menu, entries):
        global gs
        print(gs.total_sum)
        embed = nextcord.Embed(title="What's In my Wallet" 
                              ,description=''
                              , color=0xf1c40f)
        for i in range(len(entries)):
            embed.add_field(name="prject", value=entries[i][0], inline=True)
            embed.add_field(name="floor price", value='     {value}  {token}  '.format(value=str(entries[i][1]), token="ETH"), inline=True)
            embed.add_field(name="opensea", value=f"[link]({entries[i][2]})", inline=True)
        embed.add_field(name="Minimum Estimated Assets", value='     {value}  {token}  '.format(value=round(gs.total_sum,3), token="ETH"), inline=False)
        embed.set_footer(text="Honey Bottle🍯 | Badak")
        return embed
class MySource_item(menus.ListPageSource):
    async def format_page(self, menu, entries):
        print(entries[0])
        print(entries[1])
        embed = nextcord.Embed(title="MY ITEM" 
                              ,description=''
                              , color=0x3498db)
        embed.add_field(name="item", value=entries[0], inline=True)
        embed.set_image(url=entries[1])
        embed.set_footer(text="Honey Bottle🍯 | Badak")
        return embed

@bot.event
async def on_ready():
    print('로그인되었습니다!')
    print(bot.user.name)
    print(bot.user.id)
    print('====================================')

@bot.slash_command(description="Import New Project(프로젝트 추가하기)")
# @discord.ext.commands.bot_has_any_role('Co-Founder')
async def input_project(interaction: nextcord.Interaction,
    project: str = SlashOption(name="project", description="프로젝트 키워드를 입력하세요 (Enter Project Keyword)"), # str 타입으로 입력 받음
    ):
    # print(discord.id)
    print(bot.get_channel(1020470142330749008))
    list = worksheet.col_values(1)
    if project in list:
        embed = discord.Embed(title="Error" ,description=project+'는 이미 존재하는 Project 입니다.', color=0xe67e22)
        embed.set_footer(text="Honey Bottle")
        await interaction.response.send_message(embed=embed) # f-string 사용
        return None
    else: 
        url = "https://api.opensea.io/api/v1/collection/{project}?format=json"
        response = requests.request("GET", url)
        try:    
            project_name  = response.json()['collection']['name']
            worksheet.append_row([project])
            embed = discord.Embed(title=project_name ,description=project_name+'를 추가하였습니다.', color=0x3498db)
            embed.add_field(name="Open Sea", value=f"[link](https://opensea.io/collection/{project})", inline=False)
            embed.set_footer(text="Honey Bottle🍯 | Badak")
            await interaction.response.send_message(embed=embed)
        except KeyError:
            embed = discord.Embed(title="Error" ,description='You enter wrong keyword', color=0xe74c3c)
            await interaction.response.send_message(embed=embed,ephemeral = True)
    # else:
    #     embed = discord.Embed(title="Error" ,description='이곳에서는 입력할 수 없는 명령어 입니다.', color=0x62c1cc)
    #     embed.set_footer(text="Honey Bottle")
    #     await interaction.response.send_message(embed=embed) # f-string 사용
    #     return None

#바닥가 검색
@bot.slash_command(description="Search Floor Price(바닥가 보기)")
async def select_project(interaction: nextcord.Interaction,
    project: str = SlashOption(name="project", description="프로젝트 명을 입력하세요 (Enter Project Name)",autocomplete=True),
    ):
    url = f"https://api.opensea.io/api/v1/collection/{project}?format=json"
    response = requests.request("GET", url)
    try:
        print(">>>>>>>>>>>>>>>>>>>>>>> 바닥가 검색")
        project_name  = response.json()['collection']['name']
        pay_token  = response.json()['collection']['payment_tokens'][0]['symbol']
        usd_price  = response.json()['collection']['payment_tokens'][0]['usd_price']
        if pay_token != "ETH":
            pay_token  = response.json()['collection']['payment_tokens'][1]['symbol']
        floor_price = str(response.json()['collection']['stats']['floor_price'])
        floor_price_num = response.json()['collection']['stats']['floor_price']
        image = response.json()['collection']['featured_image_url']
        if response.json()['collection']['featured_image_url'] is None:
            image = response.json()['collection']['image_url']
        if project == 'the-mars-martians':
            image = response.json()['collection']['image_url']
        if project == 'wade-f-f':
            image = 'https://pbs.twimg.com/profile_banners/1543900980730679298/1660888833/1500x500'
        twitter_id = response.json()['collection']['twitter_username']
        show_fl_price = floor_price+' '+pay_token
        show_usd_price = floor_price_num*usd_price
        show_krw_price = show_usd_price*upbit_get_usd_krw()
        show_jpy_price = show_krw_price/upbit_get_jpy_krw()*100
        embed = discord.Embed(title=project_name ,description='', color=0x3498db)
        embed.add_field(name="Floor Price", value=show_fl_price, inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="USD Price", value='$'+str(format(round(show_usd_price,3),',')), inline=True)
        embed.add_field(name="KRW Price", value=str(format(round(show_krw_price,3),','))+'WON', inline=True)
        embed.add_field(name="JPY Price", value=str(format(round(show_jpy_price,3),','))+'¥', inline=True)
        embed.add_field(name="Open Sea", value=f"[link](https://opensea.io/collection/{project})", inline=True)
        embed.add_field(name="Twitter", value=f"[link](https://twitter.com/{twitter_id})", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.set_footer(text="Honey Bottle🍯 | Badak")
        embed.set_image(url=image)
        await interaction.response.send_message(embed=embed) # f-string 사용
    except KeyError:
        embed = discord.Embed(title="Error" ,description='Wrong Name', color=0xe74c3c)
        await interaction.response.send_message(embed=embed,ephemeral = True)
    except TypeError:
        embed = discord.Embed(title="Error" ,description='There is no such project', color=0xe74c3c)
        await interaction.response.send_message(embed=embed,ephemeral = True)
        
@select_project.on_autocomplete("project")
async def autocomplete_list(interaction: nextcord.Interaction, project: str):
    filtered_project=worksheet.col_values(1)
    if project:
        filtered_project = sorted([i for i in filtered_project if i.startswith(project.lower())])
    temp=''
    for i in range(len(filtered_project)):
        if(len(filtered_project[i])>25):
            temp = filtered_project[0, 24];
            filtered_project[i]=temp
        else:
            temp = filtered_project[i];    
    await interaction.response.send_autocomplete(filtered_project)

                                                         
@bot.slash_command(description="Whole list of project(전체 리스트 보기)")
async def show_all(interaction: nextcord.Interaction):
    list = sorted(worksheet.col_values(1))
    formatter = MySource(list, per_page=8)
    menu = menus.MenuPages(formatter)
    await menu.start(interaction=interaction)
    await interaction.response.send_message("Successful", ephemeral = True)

@bot.slash_command(description="Item's floor price in my wallet(내 지갑 ITEM 바닥가 보기)")
async def my_wallet(interaction: nextcord.Interaction,
    address: str = SlashOption(name="address", description="ETH 지갑주소 입력 (Enter your ETH Wallet Address"),
    ):
    # print(discord.id)
    print(bot.get_channel)
    
    url = f"https://api.opensea.io/api/v1/collections?asset_owner={address}&format=json&limit=300&offset=0"
    response = requests.request("GET", url)
    own_project_list = response.json()
    list_project_name=[]
    list_project_floorprice=[]
    list_project_floorprice_link=[]
    list_project_opensea_slug=[]
    list_project_opensea_link=[]
    try: 
        for i in range(len(own_project_list)):
            list_project_name.append(response.json()[i]['name'])
            list_project_opensea_slug.append(response.json()[i]['slug'])
        for j in range(len(list_project_opensea_slug)):
            get_my_link(list_project_opensea_link,list_project_opensea_slug[j])
        for j in list_project_opensea_slug:
            list_project_floorprice_link.append(f"https://api.opensea.io/api/v1/collection/{j}?format=json")
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in list_project_floorprice_link:
                tasks.append(asyncio.ensure_future(get_own_floorprice(session, url)))
            list_project_floorprice = await asyncio.gather(*tasks)
        global gs
        gs.get_total_sum(list_project_floorprice)
        print(gs.get_total_sum)
        
        print("number of project : "+str(len(list_project_name)))     
        # result = await [requests.request("GET", url).json()['collection']['stats']['floor_price'] for url in list_project_floorprice_link]
        print(list_project_floorprice)
        
        all_data = []
        temp=[]
        for i in range(len(list_project_name)):
            temp.append(list_project_name[i])
            temp.append(list_project_floorprice[i])
            temp.append(list_project_opensea_link[i])
            all_data.append(temp)
            temp = []
        
        formatter = MySource_price(all_data, per_page=7)
        menu = MyMenuPages(formatter,timeout=6.0, delete_message_after=True)
        await menu.start(interaction=interaction)
        await interaction.response.send_message("Successful", ephemeral = True)
        # global time_second
        # message = await ctx.send('5초 후에 삭제됩니다.')
        # for x in range(5,0,-1):# This works well as it should!
        #     await asyncio.sleep(1)
        #     print("time 값 확인 1 : "+str(time_second.time))
        #     if time_second.time ==5:
        #         x = time_second.time
        #     print("time 값 확인 2 : "+str(time_second.time))
        #     content = f'{x}초 후에 삭제됩니다.'
        #     await message.edit(content=content)
    except KeyError:
        embed = discord.Embed(title="Error" ,description='Wrong Address', color=0xe74c3c)
        await interaction.response.send_message(embed=embed,ephemeral = True)
    

# @bot.slash_command(description="Item's floor price in my klaytn wallet (내 지갑 klaytn ITEM 바닥가 보기)")
# async def my_wallet_klaytn(ctx,
#     address: discord.commands.Option(str, "지갑주소 입력"), # str 타입으로 입력 받음
#     ):
#     # print(discord.id)
#     print(bot.get_channel)
    
#     url = f"https://api.opensea.io/v2/assets/klaytn?format=json"
#     querystring = {"asset_owner":address,"order_direction":"desc","limit":"20"}
#     headers = {
#     }
#     response = requests.request("GET", url, headers=headers, params=querystring)
#     own_project_list = response.json()['results']
#     print(own_project_list[0])
#     print('own project num : '+str(len(own_project_list)))
#     list_project_name=[]
#     list_project_floorprice=[]
#     list_project_floorprice_link=[]
#     list_project_opensea_slug=[]
#     list_project_opensea_link=[]
    
#     for i in range(len(own_project_list)):
#         list_project_name.append(own_project_list[i]['name'])
#         list_project_opensea_slug.append(own_project_list[i]['collection']['slug'])
#     for j in range(len(list_project_opensea_slug)):
#         get_my_link(list_project_opensea_link,list_project_opensea_slug[j])
#     for j in list_project_opensea_slug:
#         list_project_floorprice_link.append(f"https://api.opensea.io/api/v1/collection/{j}?format=json")
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for url in list_project_floorprice_link:
#             tasks.append(asyncio.ensure_future(get_own_floorprice(session, url)))
#         list_project_floorprice = await asyncio.gather(*tasks)
#     global gs
#     gs.get_total_sum(list_project_floorprice)
#     print(gs.get_total_sum)
    
#     print("number of project : "+str(len(list_project_name)))     
#     # result = await [requests.request("GET", url).json()['collection']['stats']['floor_price'] for url in list_project_floorprice_link]
#     print(list_project_floorprice)
    
#     all_data = []
#     temp=[]
#     for i in range(len(list_project_name)):
#         temp.append(list_project_name[i])
#         temp.append(list_project_floorprice[i])
#         temp.append(list_project_opensea_link[i])
#         all_data.append(temp)
#         temp = []
    
#     formatter = MySource_price(all_data, per_page=7)
#     menu = menus.MenuPages(formatter,timeout=5.0, delete_message_after=True)
#     await menu.start(ctx)
#     # await ctx.send("수정중")

@bot.slash_command(description="See My Collections(내 컬렉션 보기)")
async def my_item(ctx,
    address: str = SlashOption(name="address", description=" ETH 지갑주소 입력 (Enter your ETH Wallet Address"),  
    ):
    
    url = "https://opensea15.p.rapidapi.com/api/v1/assets?format=json"
    querystring = {"owner":address,"order_direction":"desc","limit":"20"}
    headers = {
        "X-RapidAPI-Key": "d5d5061b60msh9960a0ae1b1e167p1592c2jsnf301f946ab17",
        "X-RapidAPI-Host": "opensea15.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    try: 
        own_item_list = response.json()['assets']
        list_item_name=[]
        list_item_image=[]
        
        for i in range(len(own_item_list)):
            list_item_name.append(response.json()['assets'][i]['name'])
            list_item_image.append(response.json()['assets'][i]['image_url'])

        all_data = []
        temp=[]
        for i in range(len(own_item_list)):
            temp.append(list_item_name[i])
            temp.append(list_item_image[i])
            all_data.append(temp)
            if len(temp) >2:
                temp = []
        # for i in range(len(own_item_list)):
        #     embed.add_field(name="item", value=list_item_name[i], inline=True)
        #     embed.add_field(name="Image", value="\u200b",image = list_item_image[i], inline=True)
        #     embed.add_field(name="\u200b", value="\u200b", inline=True)
        # embed.set_footer(text="Honey Bottle🍯 | Badak")
        # await interaction.response.send_message(embed=embed) # f-string 사용
        formatter = MySource_item(all_data, per_page=1)
        menu = MyMenuPages(formatter,timeout=5.0, delete_message_after=True)
        await menu.start(ctx)
        await interaction.response.send_message("Successful", ephemeral = True)
    # await ApplicationContext.send(content='',ephemeral=True,embeds = menu, delete_after=30)
    except KeyError:
        embed = discord.Embed(title="**!Error" ,description='Wrong Address', color=0xe74c3c)
        await interaction.response.send_message(embed=embed,ephemeral = True)


token=os.environ.get('token')      
port = int(os.environ.get("PORT", 17995))
bot.run(token) # 봇 실행