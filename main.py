from discord.ext import commands
import discord
import asyncio
import random
import json
import os

client = commands.Bot(command_prefix='!', help_command=None)
os.chdir("/home/ontheverge/Desktop/")

@client.event
async def on_ready():
    print("I'm ready!")

    channel = client.get_channel(818451410521817099)
    await channel.send("Ready! :smile:")


@client.command()
@commands.has_role('Admin')
async def clear(ctx, amount="5"):
    if amount != "all":
        amount = int(amount)

    if amount == "all":
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=amount + 1)


@client.command()
@commands.has_role('Admin')
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.channel.send(f'Banned {member}!')
    if reason == None:
        await member.send("***You've been banned for breaking a rule.***")
    else:
        await member.send(f"**You've been banned for: {reason}**")


@client.command()
@commands.has_role('Admin')
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.channel.send(f'Kicked {member}!')
    if reason == None:
        await member.send("***You've been kicked for breaking rules.***")
    else:
        await member.send(f"You've been kicked for: **{reason}**.")


async def get_bank_data():
    with open("mainbank.json", "r") as bank_file:
        users = json.load(bank_file)
        return users


@client.command()
async def balance(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author

    wallet_amount = users[str(user.id)]["wallet"]
    bank_amount = users[str(user.id)]["bank"]
    all_time = users[str(user.id)]["all time"]

    em = discord.Embed(title=f"{ctx.author.name}'s balance", colour=discord.Color.red())
    em.add_field(name="Wallet", value=wallet_amount)
    em.add_field(name="Bank balance", value=bank_amount)
    em.add_field(name="All Time", value=all_time)
    await ctx.send(embed=em)


@client.command()
async def bal(ctx):
    await balance(ctx)


@client.command()
async def beg(ctx):
    await open_account(ctx.author)

    earnings = random.randint(1, 3)

    await ctx.send(f"Someone gave you {earnings} coins!")

    await update_bank(ctx.author, earnings)
    await update_bank(ctx.author, earnings, "all time")


@client.command()
async def withdraw(ctx, amount=None):
    await open_account(ctx.author)

    amount = amount.lower()

    users = await get_bank_data()
    user = ctx.author

    if amount == "all":
        bank_all = users[str(user.id)]["bank"]
        await update_bank(ctx.author, bank_all)
        await update_bank(ctx.author, -1 * bank_all, "bank")
        await ctx.send("Withdrew all!")
    else:
        if amount == None:
            await ctx.send("Please enter an amount!")
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[1]:
            print(bal[1])
            await ctx.send("You don't have that much money!")
            return
        if amount < 0:
            await ctx.send("Amount must be positive")
            return

        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1 * amount, "bank")

        await ctx.send(f"You withdrew {amount} coins!")


@client.command()
async def deposit(ctx, amount=None):
    await open_account(ctx.author)

    amount = amount.lower()

    users = await get_bank_data()
    user = ctx.author

    if amount == "all":
        wallet_all = users[str(user.id)]["wallet"]
        await update_bank(ctx.author, -1 * wallet_all)
        await update_bank(ctx.author, wallet_all, "bank")
        await ctx.send("Deposited all!")
    else:
        if amount == None:
            await ctx.send("Please enter an amount!")
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[0]:
            print(bal[1])
            await ctx.send("You don't have that much money!")
            return
        if amount < 0:
            await ctx.send("Amount must be positive")
            return

        await update_bank(ctx.author, -1 * amount)
        await update_bank(ctx.author, amount, "bank")
        await ctx.send(f"You deposited {amount} coins!")


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["times_needed_for_promo"] = 2
        users[str(user.id)]["times_worked"] = 0
        users[str(user.id)]["work_pay"] = 2
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["warns"] = 0
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["times_worked"] = 0
        users[str(user.id)]["all time"] = 0
        users[str(user.id)]["pi_4s"] = 0
        users[str(user.id)]["vr_headsets"] = 0
        users[str(user.id)]["computers"] = 0
        users[str(user.id)]["tablets"] = 0
        users[str(user.id)]["cars"] = 0
        users[str(user.id)]["watches"] = 0
        users[str(user.id)]["houses"] = 0

    with open("mainbank.json", "w") as bank_file:
        json.dump(users, bank_file)

    print("done")

    return True


@client.command()
async def work(ctx):
    users = await get_bank_data()
    user = ctx.author

    work_pay = users[str(user.id)]["work_pay"]

    await update_bank(ctx.author, work_pay)
    await update_bank(ctx.author, work_pay, "all time")
    await update_bank(ctx.author, 1, "times_worked")
    await ctx.send(f"You gained: {work_pay}!")


async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as bank_file:
        json.dump(users, bank_file)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"], users[str(user.id)]["pi_4s"],
           users[str(user.id)]["vr_headsets"], users[str(user.id)]["computers"], users[str(user.id)]["tablets"],
           users[str(user.id)]["cars"], users[str(user.id)]["watches"], users[str(user.id)]["houses"],
           users[str(user.id)]["warns"]]
    return bal


@client.command()
async def shop(ctx, mode="None", *, item="None"):
    mode = mode.lower()
    item = item.lower()

    users = await get_bank_data()
    user = ctx.author

    wallet = users[str(user.id)]["wallet"]

    pi_4 = users[str(user.id)]["pi_4s"]
    vr_headsets = users[str(user.id)]["vr_headsets"]
    computers = users[str(user.id)]["computers"]
    tablets = users[str(user.id)]["tablets"]
    cars = users[str(user.id)]["cars"]
    watches = users[str(user.id)]["watches"]
    houses = users[str(user.id)]["houses"]
    print(houses)

    if item == "none":
        shop_em = discord.Embed(title="Shop", colour=discord.Color.red())
        shop_em.add_field(name="Pi 4", value="62")
        shop_em.add_field(name="VR", value="400")
        shop_em.add_field(name="Computer", value="500")
        shop_em.add_field(name="Tablet", value="700")
        shop_em.add_field(name="Car", value="19,000")
        shop_em.add_field(name="Watch", value="35,000")
        shop_em.add_field(name="House", value="450,000")
        await ctx.send(embed=shop_em)
    if mode == "buy":
        if item == "pi 4":
            if 62 > wallet:
                await ctx.send("Sorry, this action requires: 62")
            else:
                print(wallet)
                await update_bank(ctx.author, -1 * 62)
                await update_bank(ctx.author, 1, "pi_4s")
                await ctx.send("You bought a Pi 4!")
        if item == "vr":
            if 400 > wallet:
                await ctx.send("Sorry, this action requires: 400")
            else:
                await update_bank(ctx.author, -1 * 400)
                await update_bank(ctx.author, 1, "vr_headsets")
                await ctx.send("You bought a VR headset!")
        if item == "computer":
            if 500 > wallet:
                await ctx.send("Sorry, this action requires: 500")
            else:
                await update_bank(ctx.author, -1 * 500)
                await update_bank(ctx.author, 1, "computers")
                await ctx.send("You bought a computer!")
        if item == "tablet":
            if 700 > wallet:
                await ctx.send("Sorry, this action requires: 700")
            else:
                await update_bank(ctx.author, -1 * 700)
                await update_bank(ctx.author, 1, "tablets")
                await ctx.send("You bought a tablet!")
        if item == "car":
            if 19000 > wallet:
                await ctx.send("Sorry, this action requires: 19000")
            else:
                await update_bank(ctx.author, -1 * 19000)
                await update_bank(ctx.author, 1, "cars")
                await ctx.send("You bought a car!")
        if item == "watch":
            if 35000 > wallet:
                await ctx.send("Sorry, this action requires: 35000")
            else:
                await update_bank(ctx.author, -1 * 35000)
                await update_bank(ctx.author, 1, "watches")
                await ctx.send("You bought a watch!")
        if item == "house":
            if 450000 > wallet:
                await ctx.send("Sorry, this action requires: 450000")
            else:
                await update_bank(ctx.author, -1 * 450000)
                await update_bank(ctx.author, 1, "houses")
                await ctx.send("You bought a house!")
    elif mode == "sell":
        if item == "pi 4":
            if pi_4 > 0:
                await update_bank(ctx.author, 62)
                await update_bank(ctx.author, -1, "pi_4s")
                await ctx.send("You sold a Pi 4!")
            else:
                await ctx.send("Sorry, you have to own a pi 4 to sell one!")
        if item == "vr":
            if vr_headsets > 0:
                await update_bank(ctx.author, 400)
                await update_bank(ctx.author, -1, "vr_headsets")
                await ctx.send("You sold a VR Headset!")
            else:
                await ctx.send("Sorry, you have to own a vr headset to sell one!")
        if item == "computer":
            if computers > 0:
                await update_bank(ctx.author, 500)
                await update_bank(ctx.author, -1, "computers")
                await ctx.send("You sold a computer!")
            else:
                await ctx.send("Sorry, you have to own a computer to sell one!")
        if item == "tablet":
            if tablets > 0:
                await update_bank(ctx.author, 700)
                await update_bank(ctx.author, -1, "tablets")
                await ctx.send("You sold a tablet!")
            else:
                await ctx.send("Sorry, you have to own a tablet to sell one!")
        if item == "car":
            if cars > 0:
                await update_bank(ctx.author, 19000)
                await update_bank(ctx.author, -1, "cars")
                await ctx.send("You sold a car!")
            else:
                await ctx.send("Sorry, you have to own a car to sell one!")
        if item == "watch":
            if watches > 0:
                await update_bank(ctx.author, 35000)
                await update_bank(ctx.author, -1, "watches")
                await ctx.send("You sold a watch!")
            else:
                await ctx.send("Sorry, you have to own a watch to sell one!")
        if item == "house":
            print(houses)
            if houses > 0:
                await update_bank(ctx.author, 450000)
                await update_bank(ctx.author, -1, "houses")
                await ctx.send("You sold a house!")
            else:
                await ctx.send("Sorry, you have to own a house to sell one!")


@client.command()
async def possesions(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    users = await get_bank_data()
    user = member

    pi_4 = users[str(user.id)]["pi_4s"]
    vr = users[str(user.id)]["vr_headsets"]
    computers = users[str(user.id)]["computers"]
    tablets = users[str(user.id)]["tablets"]
    cars = users[str(user.id)]["cars"]
    watches = users[str(user.id)]["watches"]
    houses = users[str(user.id)]["houses"]

    possesions_embed = discord.Embed(title=f"{ctx.author.name}'s possesions", colour=discord.Colour.red())
    possesions_embed.add_field(name=f"Pi 4s", value=pi_4)
    possesions_embed.add_field(name=f"VR Headsets", value=vr)
    possesions_embed.add_field(name=f"Computers", value=computers)
    possesions_embed.add_field(name=f"Tablets", value=tablets)
    possesions_embed.add_field(name=f"Cars", value=cars)
    possesions_embed.add_field(name=f"Watches", value=watches)
    possesions_embed.add_field(name=f"Houses", value=houses)
    await ctx.send(embed=possesions_embed)


@client.command()
@commands.has_role('Money Giver')
async def varchange(ctx, member: discord.Member = None, amount=0, *, location="wallet"):
    if member == None:
        member = ctx.author

    if amount == 0:
        await ctx.send("Please enter an amount")
        return

    await update_bank(ctx.author, amount, location)

    await ctx.send(f"Sent {amount} to {member}'s {location}")


@client.command()
async def workinfo(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    users = await get_bank_data()
    user = ctx.author

    times_worked = users[str(user.id)]["times_worked"]
    times_needed_for_promo = users[str(user.id)]["times_needed_for_promo"]
    work_pay = users[str(user.id)]["work_pay"]
    work_embed = discord.Embed(title=f"{member}'s work panel", colour=discord.Colour.red())
    work_embed.add_field(name="Times worked", value=times_worked)
    work_embed.add_field(name="Work pay", value=work_pay)
    work_embed.add_field(name="Times needed for promo", value=times_needed_for_promo)
    await ctx.send(embed=work_embed)


@client.command()
async def reqpromo(ctx):
    users = await get_bank_data()
    user = ctx.author

    times_needed_for_promo = users[str(user.id)]["times_needed_for_promo"]
    times_worked = users[str(user.id)]["times_worked"]

    if users[str(user.id)]["times_worked"] >= times_needed_for_promo:
        await update_bank(user, -1 * times_needed_for_promo, "times_worked")
        await update_bank(user, 1, "times_needed_for_promo")
        await update_bank(user, 1, "work_pay")
        await ctx.send(f"Good job! You will get 1 extra every time you work from now on! :smile:")
    else:
        await ctx.send(
            f"Sorry, you need to work for as you've only worked {times_worked}, however, you need to work {times_needed_for_promo} times. :frowning:")


@client.command()
async def help(ctx, mode="general"):
    if mode == "general":
        help_embed = discord.Embed(title="Help Menu", colour=discord.Colour.red())
        help_embed.add_field(name="Shop", value="!shop buy\n!shop sell\n!possesions")
        help_embed.add_field(name="Balance", value="!balance\n!bal\n")
        help_embed.add_field(name="Admin", value="!varchange\n!ban\n!kick\n!clear\n")
        help_embed.add_field(name="Work", value="!work\n!workinfo\n!beg")
        help_embed.add_field(name="Management", value="!deposit\n!withdraw")
        help_embed.add_field(name="Games", value="!eightball\n!coinflip")
        help_embed.add_field(name="Administration", value="!suggestion\n!report")
        help_embed.add_field(name="Promotion", value="!reqpromo")
        await ctx.send(embed=help_embed)


@client.command()
async def reset_data(ctx):
    users = await get_bank_data()
    user = ctx.author

    wallet = users[str(user.id)]["wallet"]
    bank = users[str(user.id)]["bank"]
    all_time = users[str(user.id)]["all time"]
    times_needed_for_promo = users[str(user.id)]["times_needed_for_promo"]
    times_worked = users[str(user.id)]["times_worked"]
    work_pay = users[str(user.id)]["work_pay"]
    pi_4s = users[str(user.id)]["pi_4s"]
    vr_headsets = users[str(user.id)]["vr_headsets"]
    computers = users[str(user.id)]["computers"]
    tablets = users[str(user.id)]["tablets"]
    cars = users[str(user.id)]["cars"]
    watches = users[str(user.id)]["watches"]
    house = users[str(user.id)]["houses"]

    await update_bank(user, -1 * wallet)
    await update_bank(user, -1 * bank, "bank")
    await update_bank(user, -1 * all_time, "all time")
    await update_bank(user, -1 * times_needed_for_promo + 2, "times_needed_for_promo")
    await update_bank(user, -1 * times_worked, "times_worked")
    await update_bank(user, -1 * work_pay + 2, "work_pay")
    await update_bank(user, -1 * pi_4s, "pi_4s")
    await update_bank(user, -1 * vr_headsets, "vr_headsets")
    await update_bank(user, -1 * computers, "computers")
    await update_bank(user, -1 * tablets, "tablets")
    await update_bank(user, -1 * cars, "cars")
    await update_bank(user, -1 * watches, "watches")
    await update_bank(user, -1 * house, "houses")


@client.command()
async def eightball(ctx, *, question="um"):
    if question == "um":
        ctx.send("Please enter a question")
        return

    random_answers = [
        "nope", "never in your life", "uh hu sure",
        "um try again", "idk", "um I'm an 8 ball not a magician *ppspspspstt*, Oh... right",
        "Haha yeah", "just like baby potatos grow", "yas"
    ]

    random_answer = random.randint(0, 8)

    await ctx.send(f"The answer to: {question} is: {random_answers[random_answer]}")


@client.command()
async def coinflip(ctx):
    if random.randint(0, 1) == 0:
        await ctx.send(":coin: \n:arrow_up:")
    else:
        await ctx.send(":coin: \n:arrow_down:")


@client.command()
async def suggestion(ctx, *, suggestion):
    target = await client.fetch_user(611631045091131533)
    await target.send(suggestion)


# Report

@client.command()
async def report(ctx, member: discord.Member, *, issue="None"):
    if issue == "None":
        ctx.send("Please enter an issue!")
        return

    target = await client.fetch_user(611631045091131533)
    await target.send(f"{member} was reported by {ctx.author} for: {issue}")


@client.command()
async def warn(ctx, member: discord.Member = "None", *, issue="None"):
    if member == "none":
        ctx.send("No no you didn't put a person!")
        return

    users = await get_bank_data()
    user = member

    await update_bank(ctx.author, 1, "warns")
    await ctx.send(users[str(user.id)]["warns"])


client.run(token)