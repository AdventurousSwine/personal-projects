import discord

from discord.ext import commands


class factions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if
        if message.channel.id == 820567515650195477:
            if len(message.attachments) == 0:
                await message.delete()
                channel = self.bot.get_channel(799143830565158932)
                embed = discord.Embed(title=f"Deleted message from {message.author} -  {message.author.id}",
                                      description=message.content, color=discord.Color.dark_magenta(),
                                      timestamp=message.created_at)
                await channel.send(embed=embed)

                try:
                    #await message.author.send("Hey there, I had to remove your message:\n\`\`\`{}\`\`\`\nin Bikini Bottom's Rock Bottom because it did not contain an attachment or image.".format(message.content))
                    pass
                except Exception as ex:
                    pass

                #await message.add_reaction(":star:")
                pass

def setup(bot):
    bot.add_cog(factions(bot))