from common import bot
from datetime import datetime
import discord
import random
from discord.ui import Select, View
from dotenv import load_dotenv
import os


@bot.command()
async def rm(message):
    load_dotenv()
    MAIN_CHAT_ID = os.getenv('MAIN_CHAT_ID')
    NORMAL_CHAT_ID = os.getenv('NORMAL_CHAT_ID')
    if message.channel.id == int(NORMAL_CHAT_ID):
        return
    
    target_channel_id = int(MAIN_CHAT_ID)
    channel = bot.get_channel(target_channel_id)

    allmes = []
    year = int(str(datetime.today().year)[-2:])
    done = "done"

    while done == "done":
        try:
            randomYear = random.randint(20, year)
            randomMonth = random.randint(1, 12)
            randomDay = random.randint(1, 30)
            datetime_str = f"{randomMonth}/{randomDay}/{randomYear} 00:00:00"
            datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')

            async for msg in channel.history(before=datetime_object):
                allmes.append(msg)

            randoms = random.choice(allmes)
            while randoms.author.name in ["sesh", "friendly neighborhood", "MEE6"]:
                randoms = random.choice(allmes)

            done = "ok"

            VC = discord.utils.get(message.guild.channels, id=message.channel.id)
            allmembers = [user.name for user in VC.members if user.name not in ["sesh", "friendly neighborhood", "MEE6"]]

            membersOptions = random.sample(allmembers, min(3, len(allmembers))) + [randoms.author.name]
            random.shuffle(membersOptions)

            display = randoms.content if randoms.content else randoms.attachments[0].url

            embed = discord.Embed(
                title="Message: " + display,
                color=discord.Colour.green()
            )

            select = Select(
                min_values=1,
                placeholder="Who sent it?",
                options=[discord.SelectOption(label=name) for name in membersOptions]
            )

            wrongPeopleAnswers = []
            correctPeopleAnswers = []

            async def my_callback(interaction):
                if interaction.user.name in wrongPeopleAnswers or interaction.user.name in correctPeopleAnswers:
                    return
                elif select.values[0] == randoms.author.name:
                    correctPeopleAnswers.append(interaction.user.name)
                    embed.description = "Guessed correct: " + str(correctPeopleAnswers)
                    embed.add_field(name="", value="Guessed incorrect: " + str(wrongPeopleAnswers))
                    await interaction.response.edit_message(embed=embed)
                else:
                    wrongPeopleAnswers.append(interaction.user.name)
                    embed.description = "Guessed correct: " + str(correctPeopleAnswers)
                    embed.add_field(name="", value="Guessed incorrect: " + str(wrongPeopleAnswers))
                    await interaction.response.edit_message(embed=embed)

            select.callback = my_callback
            view = View()
            view.add_item(select)
            await message.channel.send(embed=embed, view=view)

        except Exception as e:
            await message.channel.send("Ran into an error, try again.")