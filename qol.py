from common import bot
from datetime import datetime
import discord
import random
from discord.ui import Select, View


@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(710062946281193523)
    if(len(message.content) == 0):
        display = message.attachments[0]
    else:
        display = message.content

    embed = discord.Embed(
        title=display,
        description=message.created_at,
        color=discord.Colour.green()
    )

    embed.add_field(
        name=message.author.name,
        value='',
        inline=True
    )

    await channel.send(embed=embed)
    


@bot.event
async def on_message_edit(before, after):
    if(before.author.id == 896157997309497354):
        return
    
    embed = discord.Embed(
        title="Before: "+before.content,
        description="After: "+after.content,
        color=discord.Colour.green()
    )

    embed.add_field(
        name=before.author.name,
        value='',
        inline=True
    )

    channel = bot.get_channel(710062946281193523)
    await channel.send(embed=embed)



@bot.command()
async def rewind(message,arg):
    channel = bot.get_channel(message.channel.id)
    datetime_str = arg + ' 00:00:00'
    try:
        datetime_object = datetime.strptime(datetime_str, '%d/%m/%y %H:%M:%S')

        messageAtDate = []
        async for message in channel.history(after=datetime_object):
            messageAtDate = message
            break
        
        oldmessage = await message.channel.fetch_message(messageAtDate.id)

        await oldmessage.reply("Gotchu.")
    except:
        await message.reply("It needs to be in dd/mm/yy form.")


@bot.command()
async def rm(message):
    channel = bot.get_channel(message.channel.id)

    allmes = []
    #get get user response and say if guess was right or wrong
    year = int(str(datetime.today().year)[-2:])
    #datetime_str = '03/15/20 00:00:00'
    done = "done"
    while(done == "done"):
        try:
            randomYear = random.randint(20, year)
            randomMonth = random.randint(1, 12)
            randomDay = random.randint(1, 30)
            datetime_str = str(randomMonth) + '/' + str(randomDay) + '/' + str(randomYear) + ' 00:00:00'
            datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
            async for message in channel.history(before=datetime_object):
                allmes.append(message)
            
            randoms = random.choice(allmes)
            while(randoms.author.name == "sesh" and randoms.author.name == "friendly neighborhood" and randoms.author.name == "MEE6"):
                randoms = random.choice(allmes)
            
            done = "ok"

            VC = discord.utils.get(message.guild.channels, id=message.channel.id)
            allmembers = []
            for user in VC.members:
                if(user.name != 'sesh' and user.name != 'friendly neighborhood' and user.name != 'MEE6'):
                    allmembers.append(user.name)

            membersOptions = random.sample(allmembers, 3)
            membersOptions.append(randoms.author.name)
            random.shuffle(membersOptions)

            if(len(randoms.content) != 0):
                display = randoms.content
            else:
                display = randoms.attachments[0]

            embed = discord.Embed(
                    title="Message: " + display,
                    description="",
                    color=discord.Colour.green()
                )

            select = Select(
                min_values = 1,
                placeholder = "Who sent it?",
                options=[
                    discord.SelectOption(label=membersOptions[0]),
                    discord.SelectOption(label=membersOptions[1]),
                    discord.SelectOption(label=membersOptions[2]),
                    discord.SelectOption(label=membersOptions[3])
                ]
            )
            wrongPeopleAnswers = []
            correctPeopleAnswers = []
            async def my_callback(interaction):
                if(interaction.user.name in wrongPeopleAnswers or interaction.user.name in correctPeopleAnswers):
                    pass
                elif (select.values[0] == randoms.author.name):
                    correctPeopleAnswers.append(interaction.user.name)
                    embed = discord.Embed(
                        title="Message: " + display,
                        description="Guessed correct:"+ str(correctPeopleAnswers),
                        color=discord.Colour.green()
                    )
                    embed.add_field(name="", value="Guessed incorrect:"+ str(wrongPeopleAnswers))
                    await interaction.response.edit_message(embed=embed)
                    #await interaction.response.send_message(f"{select.values[0]} is correct")
                else:
                    wrongPeopleAnswers.append(interaction.user.name)
                    embed = discord.Embed(
                        title="Message: " + display,
                        description="Guessed correct:"+ str(correctPeopleAnswers),
                        color=discord.Colour.green()
                    )
                    embed.add_field(name="", value="Guessed incorrect:"+ str(wrongPeopleAnswers))
                    await interaction.response.edit_message(embed=embed)
            select.callback = my_callback
            view = View()
            view.add_item(select)
            await message.channel.send(embed=embed, view=view)
            # await message.channel.send(randoms.content)
        except:
            pass