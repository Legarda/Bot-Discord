import discord
import random
import asyncio
from aiohttp import request
from discord import Embed
from discord.ext.commands import BucketType
from discord.ext.commands import command, cooldown
import requests


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('Logorans with API')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!guess'):
            await message.channel.send('Guess a number between 1 and 100.')

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 100)

            try:
                guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send('Sorry, you took too long it was {}.'.format(answer))

            if int(guess.content) == answer:
                await message.channel.send('You are right!')
            else:
                await message.channel.send('Oops. It is actually {}.'.format(answer))

    @command(name="fact")
    @cooldown(3, 60, BucketType.guild)
    async def animal_fact(self, ctx, animal: str):
        if (animal := animal.lower()) in ("dog", "cat", "panda", "fox", "bird", "koala"):
            fact_url = f"https://some-random-api.ml/facts/{animal}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal == 'bird' else animal}"

            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]

                else:
                    image_link = None

            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = Embed(title=f"{animal.title()} fact",
                                  description=data["fact"],
                                  colour=ctx.author.colour)
                    if image_link is not None:
                        embed.set_image(url=image_link)
                    await ctx.send(embed=embed)

                else:
                    await ctx.send(f"API returned a {response.status} status.")

        else:
            await ctx.send("No facts are available for that animal.")

    url = "https://animu.p.rapidapi.com/waifu"

    headers = {
        'auth': "undefined",
        'x-rapidapi-key': "a3a12776b6mshf0d936cf9ee7419p1ecb41jsne2f2be35874a",
        'x-rapidapi-host': "animu.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)


client = MyClient()
client.run('ODQ2NzAyNDIyNDgxOTYxMDEx.YKzXFA.z4EI4GioIoCqqp0oQAJ3XtbToKo')
