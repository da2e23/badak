import asyncio
from asyncore import loop
import aiohttp
import requests
import discord

def get_my_link(list,slug):
    list.append(f"https://opensea.io/collection/{slug}")
    return list

async def get_own_floorprice(project):
    url = f"https://api.opensea.io/api/v1/collection/{project}?format=json"
    response = requests.request("GET", url)
    floor_price_num = response.json()['collection']['stats']['floor_price']
    return floor_price_num
# async def get_own_floorprice(url):
#         data = requests.request("GET", url).json()['collection']['stats']['floor_price']
#         return data
async def call(urls):
    futures = [asyncio.ensure_future(get_own_floorprice(url)) for url in urls]
                                                           # 태스크(퓨처) 객체를 리스트로 만듦
    result = await asyncio.gather(*futures)                # 결과를 한꺼번에 가져옴
    print(result)