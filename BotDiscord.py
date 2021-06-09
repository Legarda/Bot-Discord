import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('Legoran`s Готовий до роботи')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Bot Loaded")

        self.role_message_id = 846791849183019058
        self.emoji_to_role = {
            discord.PartialEmoji(name='🔴'): 846777021203480600,
            discord.PartialEmoji(name='🟡'): 846777073405394965,
            discord.PartialEmoji(name='🟢'): 846777118167269406,
            discord.PartialEmoji(name='🟣'): 846776976580673567,
            discord.PartialEmoji(name='🔵'): 846776863153061968,
        }

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji."""

        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:

            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:

            return

        role = guild.get_role(role_id)
        if role is None:

            return

        try:

            await payload.member.add_roles(role)
        except discord.HTTPException:

            pass

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji."""

        if payload.message_id != self.role_message_id:
            return

        guild = self.get_guild(payload.guild_id)
        if guild is None:

            return

        try:
            role_id = self.emoji_to_role[payload.emoji]
        except KeyError:

            return

        role = guild.get_role(role_id)
        if role is None:

            return


        member = guild.get_member(payload.user_id)
        if member is None:

            return

        try:

            await member.remove_roles(role)
        except discord.HTTPException:
            pass


intents = discord.Intents.default()
intents.members = True

client = MyClient(intents=intents)
client.run('ODQ2NzAyNDIyNDgxOTYxMDEx.YKzXFA.z4EI4GioIoCqqp0oQAJ3XtbToKo')
