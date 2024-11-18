import config as ini
import discord
from discord.ext import commands
import module.mod_control_db as db

# 既存のクラス
class Posted:
    def __init__(self,
                ch_name,         # チャンネル名
                ch_id,           # チャンネルID
                post_id,         # 投稿ID
                author_name,     # 投稿主名
                author_id,       # 投稿主ID
                ):
        self.ch_name = ch_name
        self.ch_id = ch_id
        self.post_id = post_id
        self.author_name = author_name
        self.author_id = author_id
    def __str__(self):
        return (f"Posted class updated.\n"
                f"ch_name={self.ch_name},\n"
                f"ch_id={self.ch_id},\n"
                f"post_id={self.post_id},\n"
                f"author_name={self.author_name},\n"
                f"author_id={self.author_id}\n"
                f"--------------------------------------------------------")

class Reacted:
    def __init__(self,
                ch_name,                    # チャンネル名
                ch_id,                      # チャンネルID
                reacted_user_name,          # リアクションしたユーザー名
                reacted_user_id,            # リアクションしたユーザーID
                post_id,                    # 投稿ID
                post_author_user_name,      # 投稿主ユーザー名
                post_author_user_id,        # 投稿主ユーザーID
                all_reacted_users,          # これまでにリアクションしたユーザー名とIDの配列
                ):
        self.ch_name = ch_name
        self.ch_id = ch_id
        self.reacted_user_name = reacted_user_name
        self.reacted_user_id = reacted_user_id
        self.post_id = post_id
        self.post_author_user_name = post_author_user_name
        self.post_author_user_id = post_author_user_id
        self.all_reacted_users = all_reacted_users
    def __str__(self):
        return (f"Reacted class updated.\n"
                f"ch_name={self.ch_name},\n"
                f"ch_id={self.ch_id},\n"
                f"reacted_user_name={self.reacted_user_name},\n"
                f"reacted_user_id={self.reacted_user_id},\n"
                f"post_id={self.post_id},\n"
                f"post_author_user_name={self.post_author_user_name},\n"
                f"post_author_user_id={self.post_author_user_id},\n"
                f"all_reacted_users={self.all_reacted_users}\n"
                f"--------------------------------------------------------")

class Deleted:
    def __init__(self,
                post_id,                    # 投稿ID
                ):
        self.post_id = post_id
    def __str__(self):
        return (f"Deleted class updated.\n"
                f"post_id={self.post_id}\n"
                f"--------------------------------------------------------")


# Bot初期設定
intents = discord.Intents.default()
intents.members = True
intents.messages = True  # メッセージの内容を取得するためのインテント
intents.reactions = True  # リアクションの内容を取得するためのインテント
bot = commands.Bot(command_prefix='!', intents=intents)
print('bot初期設定OK')


@bot.event
# Bot起動イベント
async def on_ready():
    # プレイ中のステータスを設定
    activity = discord.Game(name="般若心経ロワイヤル")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Botログインしました。ユーザー名：" + str(bot.user))


@bot.event
async def on_raw_reaction_add(payload):
    print("on_raw_reaction_add")

    # 反応があったメッセージの情報を取得
    channel = bot.get_channel(payload.channel_id)  # チャンネル情報を取得
    message = await channel.fetch_message(payload.message_id)  # メッセージ情報を取得
    user = bot.get_user(payload.user_id)  # 反応したユーザーを取得
    author = message.author  # 投稿したユーザーを取得

    # リアクションしたユーザーと投稿したユーザー名、メッセージ情報を格納する
    reacted_users = []
    async for reaction_user in message.reactions[0].users():  # メッセージに付いたリアクションのユーザーを取得
        reacted_users.append({'id': reaction_user.id, 'name': reaction_user.name})

    # reactedクラスへ
    reacted = Reacted(
        ch_name=channel.name,
        ch_id=channel.id,
        reacted_user_name=user.name,
        reacted_user_id=user.id,
        post_id=message.id,
        post_author_user_name=author.name,
        post_author_user_id=author.id,
        all_reacted_users=reacted_users
    )

    print(reacted)
    #リアクションがあったらtbl_userdataを見る


@bot.event
async def on_message(message):
    # Bot自身のメッセージは無視
    if message.author == bot.user:
        return

    print("on_message")
    #postedクラスへ
    posted = Posted(
        ch_name=message.channel.name,
        ch_id=message.channel.id,
        post_id=message.id,
        author_name=message.author.name,
        author_id=message.author.id
    )
    print(posted)
    # 投稿をしたらtbl_userdataにユーザーレコードがあるか見る　なければ作る　あればpost_count +1


@bot.event
# メッセージ削除イベント
async def on_message_delete(message):
    print("on_message_delete")
    # deletedクラスへ
    deleted = Deleted(post_id=message.id)
    print(deleted)



bot.run(ini.ini.server.mother_bot_token)

