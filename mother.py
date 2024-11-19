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
                f"ch_name       :{self.ch_name},\n"
                f"ch_id         :{self.ch_id},\n"
                f"post_id       :{self.post_id},\n"
                f"author_name   :{self.author_name},\n"
                f"author_id     :{self.author_id}\n"
                f"--------------------------------------------------------")

class Reacted:
    def __init__(self,
                ch_name,                    # チャンネル名
                ch_id,                      # チャンネルID
                reacted_user_name,          # リアクションしたユーザー名
                reacted_user_id,            # リアクションしたユーザーID
                reacted_user_roles,         # リアクションしたユーザーのロール配列
                reacted_emoji_name,         # 絵文字名
                post_id,                    # 投稿ID
                post_author_user_name,      # 投稿主ユーザー名
                post_author_user_id,        # 投稿主ユーザーID
                all_reacted_users,          # これまでにリアクションしたユーザー名とIDの配列
                ):
        self.ch_name = ch_name
        self.ch_id = ch_id
        self.reacted_user_name = reacted_user_name
        self.reacted_user_id = reacted_user_id
        self.reacted_user_roles = reacted_user_roles
        self.reacted_emoji_name = reacted_emoji_name
        self.post_id = post_id
        self.post_author_user_name = post_author_user_name
        self.post_author_user_id = post_author_user_id
        self.all_reacted_users = all_reacted_users
    def __str__(self):
        return (f"Reacted class updated.\n"
                f"ch_name               :{self.ch_name},\n"
                f"ch_id                 :{self.ch_id},\n"
                f"reacted_user_name     :{self.reacted_user_name},\n"
                f"reacted_user_id       :{self.reacted_user_id},\n"
                f"reacted_user_roles    :{self.reacted_user_roles},\n"
                f"reacted_emoji_name    :{self.reacted_emoji_name},\n"
                f"post_id               :{self.post_id},\n"
                f"post_author_user_name :{self.post_author_user_name},\n"
                f"post_author_user_id   :{self.post_author_user_id},\n"
                f"all_reacted_users     :{self.all_reacted_users}\n"
                f"--------------------------------------------------------")

class Deleted:
    def __init__(self,
                post_id,                    # 投稿ID
                ):
        self.post_id = post_id
    def __str__(self):
        return (f"Deleted class updated.\n"
                f"post_id   :{self.post_id}\n"
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
# リアクション追加イベント
async def on_raw_reaction_add(payload):
    print("on_raw_reaction_add")
    # 反応があったメッセージの情報を取得
    channel = bot.get_channel(payload.channel_id)  # チャンネル情報を取得
    message = await channel.fetch_message(payload.message_id)  # メッセージ情報を取得
    user = bot.get_user(payload.user_id)  # 反応したユーザーを取得
    author = message.author  # 投稿したユーザーを取得
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(user.id)
    # リアクションした人の @everyone以外のロール
    role_names = [role.name for role in member.roles if role.name != "@everyone"]
    emoji_name = payload.emoji.name
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
        reacted_user_roles=role_names,
        reacted_emoji_name=emoji_name,
        post_id=message.id,
        post_author_user_name=author.name,
        post_author_user_id=author.id,
        all_reacted_users=reacted_users
    )
    # print(reacted)
    # !処理分岐=======================================================================================================
    # リアクションした人、された人両方のtbl_userdataを見る
    # リアクションした人を見る、無ければ作る
    db.check_userdata_exists(reacted.reacted_user_id,reacted.reacted_user_name)
    # リアクションされた人を見る、無ければ作る
    db.check_userdata_exists(reacted.post_author_user_id,reacted.post_author_user_name)
    # リアクションが連続して同じ投稿かを調べる
    if db.check_dub_reacting(reacted.reacted_user_id,reacted.post_id):
        # 連続リアクションなので無効　削除
        reaction_to_remove = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        if reaction_to_remove:
            await reaction_to_remove.remove(user)
        # !隠しメッセージを返信する
        # !「連続して同じ投稿にリアクションを送ることはできません」
        return
    else:
        # 連続リアクションじゃない
        if reacted.post_id == ini.ini.start_channel.post_id:
            if db.check_first_reacted(reacted.reacted_user_id):
                # 既に初回リアクションボーナス受け取り済みです
                return
            else:
                # 初回リアクションボーナス未受取
                # 初回リアクションボーナス付与
                db.benefit(reacted.reacted_user_id,ini.ini.start_channel.benefit)
                # !メッセージを送る
                # !「初回リアクションボーナス」
                # リアクションした投稿を保持する
                db.upd_user_reacted_post(reacted.reacted_user_id,reacted.post_id)
                return
        else:
            # 初回リアクションボーナスの投稿ではない
            # ロール名と価格を取得
            role_name,price = db.get_purchase_role(reacted.ch_id,reacted.post_id)
            if role_name and price:
                # ロール名と価格が返ってきた=ロール販売の投稿へのリアクション
                # ロール購入できるか残高を確認
                if db.check_payable(reacted.reacted_user_id,price):
                    # 買える！
                    # ロールを持っているかどうかチェック
                    if role_name in reacted.reacted_user_roles:
                        # 持っているので買わない
                        # !隠しメッセージを返信する
                        # !「あなたはすでに（○○）ロールを保持しています」
                        return
                    else:
                        # 持ってないので買う
                        if db.payment(reacted.reacted_user_id,price):
                            # 買えたので付与
                            await member.add_roles(role_name)
                            # !メッセージを送る
                            # !「ロールを付与しました」
                            return
                        else:
                            # なぜか買えなかったので付与しない
                            # !メッセージを送る
                            # !「購入できませんでした。しばらくしてからもう一度試してください」
                            return
                else:
                    # 買えない
                    # !メッセージを送る
                    # !「残高が足りません」
                    return
            else:
                # ロール販売系の投稿へのリアクションではない
                # チャンネルレートを調べる
                rate_active,rate_passive = db.get_channel_rate(reacted.ch_id)
                # 贈与絵文字かどうかを調べる
                # 贈与絵文字の価格 対象外の場合はFalse
                donation_emoji_price = db.check_donation_emoji(emoji_name)
                if donation_emoji_price:
                    price = int(donation_emoji_price)
                    if db.check_payable(reacted.reacted_user_id,price):
                        # 贈れるよ
                        # リアクションしたユーザーは、払う
                        db.payment(reacted.reacted_user_id,price)
                        # !贈与したユーザーにメッセージを送る
                        # リアクションされたユーザーに、付与
                        db.benefit(reacted.post_author_user_id,price)
                        # リアクションした投稿を保持する
                        db.upd_user_reacted_post(reacted.reacted_user_id,reacted.post_id)
                        # !贈与されたユーザーにメッセージを送る
                        return
                    else:
                        # 贈れねーのかよ
                        # !残高不足で贈与できませんでした　とメッセージを送る
                        # 該当絵文字のリアクションのみ削除する
                        reaction_to_remove = discord.utils.get(message.reactions, emoji=payload.emoji.name)
                        if reaction_to_remove:
                            await reaction_to_remove.remove(user)
                        return
                else:
                    # 寄付絵文字じゃない
                    # レートに合わせて付与する
                    db.benefit(reacted.reacted_user_id,rate_active)
                    db.benefit(reacted.post_author_user_id,rate_passive)
                    # リアクションした投稿を保持する
                    db.upd_user_reacted_post(reacted.reacted_user_id,reacted.post_id)
                    return



@bot.event
# 投稿イベント
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

