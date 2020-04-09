from datetime import datetime
from config import TOKEN
import discord
from discord.ext import commands
from exelworker import add_info, create_table


client = commands.Bot(command_prefix="!")

now_id = 1


@client.event
async def on_ready():
    print(client.user, "has connected")


states = {}


@client.command("start", pass_context=True)
async def start(ctx):
    user = ctx.author
    if user in states:
        await user.send("Бот уже запомнил вас, вы можете начать поиск собеседника при помощи команы !find")
    else:
        states[user] = [0, user, None, None]
        await user.send("Вы были добавлены в базу бота, для справки напишите !info")


@client.command("find", pass_context=True)
async def find(ctx):
    global now_id
    user = ctx.author
    if user not in states:
        await user.send("Вы были добавлены в базу бота.")
        states[user] = [1, user, None, None]
    if states[user][0] == 2:
        await user.send("Если вы хотите остановитиь диалог напишите !stop.")
        return
    states[user] = [1, user, None, None]
    await user.send("Поиск начат.")
    for other in states:
        if other != user and states[other][0] == 1:
            states[user][0] = 2
            states[user][2] = states[other][1]
            states[user][3] = now_id
            states[other][3] = now_id
            now_id += 1
            states[other][0] = 2
            states[other][2] = states[user][1]
            await user.send("Собеседник найден, можете общаться.")
            await other.send("Собеседник найден, можете общаться.")
            create_table(states[user][3])


@client.command("stop", pass_context=True)
async def stop(ctx):
    user = ctx.author
    state = states[user]
    if state[0] == 0:
        await user.send("Вы ещё не начали поиск, для поиска напишите !find")
    elif state[0] == 1:
        states[user][0] = 0
        await user.send("Поиск остановлен.")
    else:
        other = states[user][2]
        states[user][0] = 0
        states[user][2] = None
        states[other][0] = 0
        states[other][2] = None
        dialog_id = states[user][3]
        states[user][3] = None
        states[other][3] = None
        await user.send(f"Диалог окончен, вы вышли из поиска. id диаолга: {dialog_id}")
        await other.send(f"Собеседник вышел из беседы, поиск остановлен. id диаолга: {dialog_id}")


@client.command("info", pass_context=True)
async def info(ctx):
    user = ctx.author
    await user.send("Напишите !start, чтобы бот запомнил вас.")
    await user.send("Напишите !find, чтобы начать поиск собеседника.")
    await user.send("Напишите !stop, чтобы закончить поиск или диалог.")
    await user.send("Напишите !info, чтобы открыть справку.")


@client.event
async def on_message(message):
    user = message.author
    if user == client.user:
        return
    await client.process_commands(message)
    if message.content.startswith("!"):
        return
    if user not in states:
        await user.send("Бот ещё не запомнил вас, для справки напишите !info")
    else:
        if states[user][0] == 0 or states[user][0] == 1:
            await user.send("Вы не можете общаться вне диалога.")
        else:
            other = states[user][2]
            dialog_id = states[user][3]
            add_info(str(user), message.content, states[user][3])
            await other.send(message.content)


client.run(TOKEN)
