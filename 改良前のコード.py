import discord
from discord.ext import commands

# コマンドプレフィックス
prefix = "spb!"

# ボットのトークンが書いてあるテキストファイル
file_name = "./token.txt"
data = None
try:
    file = open(file_name, encoding="utf-8")
    data = file.read()
    file.close()
except Exception as e:
    print(e)

# 接続に必要なオブジェクトを生成
intents = discord.Intents.all()


# ボットの起動
class MyBot(commands.Bot):

    async def setup_hook(self):
        await bot.tree.sync()


# ボットのプレフィックスとインテントを指定
bot = MyBot(command_prefix=prefix, intents=intents, help_command=None)


@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('----------------')
    print('ログインしました')
    print('----------------')
    print('')
    print('BOT表示名：', bot.user.name)  # Botの名前
    print('BOTのID：', bot.user.id)  # ID
    print('Dicord.pyのバージョン：', discord.__version__)
    servers = len(bot.guilds)
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f'{servers} サーバー | {members} メンバー'
    ))


@bot.hybrid_command(help="Discordとボット間のPingを測定")  # ハイブリッドコマンド
@commands.cooldown(1, 30)
async def ping(ctx):
    raw_ping = bot.latency
    ping = round(raw_ping * 1000)
    await ctx.reply(f"私のPing値は{ping}msです。")


@bot.hybrid_command(help="ボットのコマンドクールタイムの機能をテストできます")  # ハイブリッドコマンド
@commands.cooldown(1, 10)
async def cooldown_test(ctx):
    await ctx.reply("もう一度実行してみると...")


# エラー時処理
@bot.event
async def on_command_error(ctx, err):
    # コマンドクールタイム時処理
    if isinstance(err, commands.CommandOnCooldown):
        print(err)
        import datetime
        import math

        d = datetime.datetime.now()
        tmp = str(err).replace("You are on cooldown. Try again in ", "").replace("s", "").split(".")[0]
        now = d + datetime.timedelta(seconds=int(tmp))
        now_ts = now.timestamp()
        cnt = math.ceil(now_ts)
        print(cnt)
        try:
            await ctx.interaction.response.send_ctx(
                f"レート制限に引っかかっています。\nYou are on cooldown. Try again in <t:{str(cnt)}:R>", ephemeral=True)
        except Exception as e:
            print(e)
            await ctx.reply(f"レート制限に引っかかっています。\nYou are on cooldown. Try again in <t:{str(cnt)}:R>")


bot.run(data)
