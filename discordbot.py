import discord 
import os
from discord.ext import tasks
from datetime import timedelta
import datetime
import random
import re
import asyncio
import sys
from func import diceroll
import traceback 

#トークン
TOKEN = os.environ['DISCORD_BOT_TOKEN']

#チャンネルID
CHANNEL_ID = 613341065365291010  #top
CHANNEL_ID2 = 694053188013391882 #testlog
CHANNEL_ID3 = 624496341124513793 #omikuji
CHANNEL_ID4 = 694053188013391882 #ID取得
CHANNEL_ID5 = 613343508153106443
CHANNEL_IDother = 661705202424086547

lot_channel_id = 643070878652825601 #ここにコマンドを送るチャンネルID
lot_result_channel_id1 = 613346390092939275 #class-saxony
lot_result_channel_id2 = 613346614085419040 #class-crimean
lot_result_channel_id3 = 613346718624251944 #class-rusviet
lot_result_channel_id4 = 613346798383267841 #class-nordic

master_owner_id = 459936557432963103 or 436078064292855818
great_owner_id = 459936557432963103
my_bot_id = 511397857887125539
ksi_ver = '6.0.1'
discord_py_ver = '3.7.3'
ssr_tuti = 636400089396543526
ssr_ch = 638239968140984330

omikuji_vip = ["459936557432963103","0"]

# 接続に必要なオブジェクトを生成
client = discord.Client()

#起動メッセージ
@client.event
async def on_ready():
    print(client.user.name)  # ボットの名前
    print(client.user.id)  # ボットのID
    print(discord.__version__)  # discord.pyのバージョン
    print('----------------')
    print('Hello World,リマインドbotプログラム「project-RRN」、起動しました')
    channel = client.get_channel(CHANNEL_ID2)
    await channel.send(f'名前:{client.user.name}')  # ボットの名前
    await channel.send(f'ID:{client.user.id}')  # ボットのID
    await channel.send(f'Discord ver:{discord.__version__}')  # discord.pyのバージョン
    await channel.send('----------------')
    await channel.send('状態：BOT再起動しました。')   
    await client.change_presence(status=discord.Status.idle,activity=discord.Game(name=f'ギルド専属ナビ|Ping:{client.ws.latency * 1000:.0f}ms'))
    
@client.event
async def on_voice_state_update(member, before, after):
    if not member.guild.id == 613341065365291008:
        return
    if member.guild.id == 613341065365291008 and (before.channel != after.channel):
        now = datetime.utcnow() + timedelta(hours=9)
        alert_channel = client.get_channel(676378599158317056)
        if before.channel is None: 
            msg = f'{now:%m/%d-%H:%M} に {member.name} が {after.channel.name} に参加しました。'
            await alert_channel.send(msg)
        elif after.channel is None: 
            msg = f'{now:%m/%d-%H:%M} に {member.name} が {before.channel.name} から退出しました。'
            await alert_channel.send(msg)

    if before.channel != after.channel:
        # before.channelとafter.channelが異なるなら入退室
        if after.channel and len(after.channel.members) == 1:
            # もし、ボイスチャットが開始されたら
            await client.get_channel(CHANNEL_ID).send(f"{member.name}さんが通話を開始しました。\n場所：<#{after.channel.id}>(←クリックすると直接入れます)")

        if before.channel and len(before.channel.members) == 0:
            # もし、ボイスチャットが終了したら
            await client.get_channel(CHANNEL_ID).send(f"{member.name}さんが通話を終了しました。\n場所：{before.channel.name}")

@client.event
async def on_message(message):
    """メッセージを処理"""
    if message.author.id == my_bot_id:
        return
#おみくじ
    if message.content == "おみくじ":
        if message.channel.id == CHANNEL_ID3 or CHANNEL_IDother:
            # Embedを使ったメッセージ送信 と ランダムで要素を選択
            embed = discord.Embed(title="おみくじ", description=f"{message.author.mention}さんの今日の運勢は！",
                                  color=0x2ECC69)
            embed.set_thumbnail(url=message.author.avatar_url)
            prob = random.random()
            if message.author.id in omikuji_vip: 
                vipwari = 2
                prob = prob/vipwari
            if prob < 0.01:
                omokuji = "大吉"
            elif prob < 0.1:
                omokuji = "中吉"
            elif prob < 0.2:
                omokuji = "小吉"
            elif prob < 0.3:
                omokuji = "吉"
            elif prob < 0.4:
                omokuji = "半吉"
            elif prob < 0.5:
                omokuji = "末吉"
            elif prob < 0.6:
                omokuji = "末小吉"
            elif prob < 0.7:
                omokuji = "末凶"
            elif prob < 0.8:
                omokuji = "凶"
            elif prob < 0.99:
                omokuji = "小凶"
            else:
                omokuji = "大凶"
            
            embed.add_field(name="[運勢] ", value=omokuji, inline=False)
            await message.channel.send(embed=embed)
            #client.get_channel(CHANNEL_ID3)
        
    if message.content == 'ヘルプ':
        page_count = 0 #ヘルプの現在表示しているページ数
        page_content_list = [">>> **リリナコマンド一覧(ページ1)**\n\n**何時？**：今の時間を教えてくれます！(何時何分何秒)\n**何日？**：何日か教えてくれます！(何月何日)\n\n➡絵文字を押すと次のページへ",
            ">>> **リリナコマンド一覧(ページ2)**\n\n**!dc XdY**：Y面のダイスをX回振ります！\n**coin**：コイントスを行います。\n**スロット**：あなたは大当たりを引けるのか!？\n\n➡絵文字で次のページ\n⬅絵文字で前のページ",
            ">>> **リリナコマンド一覧(ページ3)**\n\n以下のコマンドは<#624496341124513793>で使えます。\n\n**おみくじ**or**御神籤**：おみくじが引けます！\n**運勢**：貴方の運勢は！\n\n➡絵文字で次のページ\n⬅絵文字で前のページ",
            ">>> **リリナコマンド一覧(ページ4)**\n\n以下のコマンドは__管理者権限__が必要\n**ステータス**：この鯖のステータスです。\n\n➡絵文字で次のページ\n⬅絵文字で前のページ",
            ">>> **このBOT詳細情報(ページ5)**\n\nBOT名前：" + f"{client.user.name}" + "\nBOT ID：" + f"{client.user.id}" + "\nDiscordバージョン：" + f"{discord.__version__}" + "\nDiscord.pyバージョン：" + discord_py_ver + "\n開発バージョン：" + ksi_ver + "\n開発者：<@459936557432963103>\n\n⬅絵文字で前のページ"] #ヘルプの各ページ内容] #ヘルプの各ページ内容
        
        send_message = await message.channel.send(page_content_list[0]) #最初のページ投稿
        await send_message.add_reaction("➡")

        def help_react_check(reaction,user):
            '''
            ヘルプに対する、ヘルプリクエスト者本人からのリアクションかをチェックする
            '''
            emoji = str(reaction.emoji)
            if reaction.message.id != send_message.id:
                return 0
            if emoji == "➡" or emoji == "⬅":
                if user != message.author:
                    return 0
                else:
                    return 1

        while not client.is_closed():
            try:
                reaction,user = await client.wait_for('reaction_add',check=help_react_check,timeout=60.0)
            except asyncio.TimeoutError:
                msg_end = '\n stop'
                await send_message.edit(content=page_content_list[page_count] + msg_end)
                return #時間制限が来たら、それ以降は処理しない
            else:
                emoji = str(reaction.emoji)
                if emoji == "➡" and page_count < 4:
                    page_count += 1
                if emoji == "⬅" and page_count > 0:
                    page_count -= 1

                await send_message.clear_reactions() #事前に消去する
                await send_message.edit(content=page_content_list[page_count])

                if page_count == 0:
                    await send_message.add_reaction("➡")
                elif page_count == 1:
                    await send_message.add_reaction("⬅")
                    await send_message.add_reaction("➡")
                elif page_count == 2:
                    await send_message.add_reaction("⬅")
                    await send_message.add_reaction("➡")
                elif page_count == 3:
                    await send_message.add_reaction("⬅")
                    await send_message.add_reaction("➡")
                elif page_count == 4:
                    await send_message.add_reaction("⬅")
                    #各ページごとに必要なリアクション

    if message.content == 'ヘルプクラス' or message.content == 'クラスヘルプ':
        page_count = 0 #ヘルプの現在表示しているページ数
        page_content_list = [">>> **クラス一覧(ページ0)**\n\nこちらはクラスについての一覧です。\n\n目次\n<@&613345307861844011>についてはページ1\n<@&613345394033819649>についてはページ2\n<@&613345488166715392>についてはページ3\n<@&613345547344150538>についてはページ4\n\n総クラスリーダー：<@475909877018132500>\n\n各一覧の見方\nクラス名：クラス名\n特徴：クラスの特徴\nクラスリーダー：クラスリーダー\nコマンド：<#643070878652825601>で入力\n\n➡絵文字を押すとクラス説明へ",
            ">>> **クラス一覧(ページ1)**\n\nクラス名：<@&613345307861844011>(ザクセン)\n特徴：PS向上\nクラスリーダー：<@329673969806475275>\nコマンド：赤\n\n➡絵文字で次のクラス\n⬅絵文字で前の説明",
            ">>> **クラス一覧(ページ2)**\n\nクラス名：<@&613345394033819649>(クリミア)\n特徴：エンジョイ\nクラスリーダー：<@602460316806152192>と<@539430524020719628>\nコマンド：黄\n\n➡絵文字で次のクラス\n⬅絵文字で前のクラス",
            ">>> **クラス一覧(ページ3)**\n\nクラス名：<@&613345488166715392>(ロズヴィエルト)\n特徴：初心者\nクラスリーダー：<@493093867973902357>\nコマンド：緑\n\n➡絵文字で次のクラス\n⬅絵文字で前のクラス",
            ">>> **クラス一覧(ページ4)**\n\nクラス名：<@&613345547344150538>(ノルデック)\n特徴：配信OK\nクラスリーダー：<@540121769454075904>\nコマンド：青\n\n⬅絵文字で前のクラス"] #ヘルプの各ページ内容
        
        send_message = await message.channel.send(page_content_list[0]) #最初のページ投稿
        await send_message.add_reaction("➡")

        def help_react_check(reaction,user):
            '''
            ヘルプに対する、ヘルプリクエスト者本人からのリアクションかをチェックする
            '''
            emoji = str(reaction.emoji)
            if reaction.message.id != send_message.id:
                return 0
            if emoji == "➡" or emoji == "⬅":
                if user != message.author:
                    return 0
                else:
                    return 1

        while not client.is_closed():
            try:
                reaction,user = await client.wait_for('reaction_add',check=help_react_check,timeout=60.0)
            except asyncio.TimeoutError:
                msg_end = '\n stop'
                await send_message.edit(content=page_content_list[page_count] + msg_end)
                return #時間制限が来たら、それ以降は処理しない
            else:
                emoji = str(reaction.emoji)
                if emoji == "➡" and page_count < 4:
                    page_count += 1
                if emoji == "⬅" and page_count > 0:
                    page_count -= 1

                await send_message.clear_reactions() #事前に消去する
                await send_message.edit(content=page_content_list[page_count])

                if page_count == 0:
                    await send_message.add_reaction("➡")
                elif page_count == 1:
                    await send_message.add_reaction("⬅")
                    await send_message.add_reaction("➡")
                elif page_count == 2:
                    await send_message.add_reaction("⬅")
                    await send_message.add_reaction("➡")
                elif page_count == 3:
                    await send_message.add_reaction("⬅")
                    await send_message.add_reaction("➡")
                elif page_count == 4:
                    await send_message.add_reaction("⬅")
                    #各ページごとに必要なリアクション

    if message.content.startswith("スロット"): 
        suroto=random.choice(('０', '１', '２', '３', '４', '５', '６', '７', '８', '９'))
        suroto1=random.choice(('０', '１', '２', '３', '４', '５', '６', '７', '８', '９'))
        suroto2=random.choice(('０', '１', '２', '３', '４', '５', '６', '７', '８', '９'))
        await asyncio.sleep(0.1)
        my_message = await message.channel.send('スロット結果がここに表示されます！')
        await asyncio.sleep(3)
        await my_message.edit(content='？|？|？')
        await asyncio.sleep(1)
        await my_message.edit(content=suroto + '|？|？')
        await asyncio.sleep(1)
        await my_message.edit(content=suroto + '|' + suroto1 + '|？')
        await asyncio.sleep(1)
        await my_message.edit(content=suroto + '|' + suroto1 + '|' + suroto2)
        if suroto == suroto1 == suroto2:
            await my_message.edit(content=suroto + '|' + suroto1 + '|' + suroto2 + '\n 結果：大当たり！！')
        elif suroto == suroto1 or suroto == suroto2 or suroto1 == suroto2:
            await my_message.edit(content=suroto + '|' + suroto1 + '|' + suroto2 + '\n 結果：リーチ！')
        else:
            await my_message.edit(content=suroto + '|' + suroto1 + '|' + suroto2 + '\n 結果：ハズレ')

    if message.content == 'coin sn1' or message.content == 'coin sn2':
        if message.author.id == great_owner_id:
            coin=random.choice(('●', '○'))
            if message.content == 'coin sn1':
                my_message = await message.channel.send('コイントスをします！')
                await asyncio.sleep(3)
                await my_message.edit(content='定義：○は表、●は裏')
                await asyncio.sleep(3)
                coinp = 0
                while coinp < 6:
                    await my_message.edit(content='抽選中：○```定義：○は表、●は裏```')
                    await asyncio.sleep(0.5)
                    await my_message.edit(content='抽選中：●```定義：○は表、●は裏```')
                    await asyncio.sleep(0.5)
                    coinp += 1
                await my_message.edit(content='抽選中：　```定義：○は表、●は裏```')
                await asyncio.sleep(2)
                await my_message.edit(content='　結果：' + coin + '```定義：○は表、●は裏 \n adid:sn1```')
                return
            elif message.content == 'coin sn2':
                my_message = await message.channel.send('コイントスをします！')
                await asyncio.sleep(3)
                await my_message.edit(content='定義：●は表、○は裏')
                await asyncio.sleep(3)
                coinp = 0
                while coinp < 6:
                    await my_message.edit(content='抽選中：○```定義：●は表、○は裏```')
                    await asyncio.sleep(0.5)
                    await my_message.edit(content='抽選中：●```定義：●は表、○は裏```')
                    await asyncio.sleep(0.5)
                    coinp += 1
                await my_message.edit(content='抽選中：　```定義：●は表、○は裏```')
                await asyncio.sleep(2)
                await my_message.edit(content='　結果：'+ coin + '```定義：●は表、○は裏 \n adid:sn2```')
                return
        await message.channel.send('Error:You cannot use this command')  
        return

    if message.content == 'coin':
        coin=random.choice(('●', '○'))
        coin1=random.choice(('1', '2'))
        await asyncio.sleep(0.1)
        if coin1 == '1':
            my_message = await message.channel.send('コイントスをします！')
            await asyncio.sleep(3)
            await my_message.edit(content='定義：○は表、●は裏')
            await asyncio.sleep(3)
            coinp = 0
            while coinp < 6:
                await my_message.edit(content='抽選中：○```定義：○は表、●は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：●```定義：○は表、●は裏```')
                await asyncio.sleep(0.5)
                coinp += 1
            await my_message.edit(content='抽選中：　```定義：○は表、●は裏```')
            await asyncio.sleep(2)
            await my_message.edit(content='　結果：' + coin + '```定義：○は表、●は裏 \n adid:sn' + coin1 + '```')
            
            return
        elif coin1 == '2':
            my_message = await message.channel.send('コイントスをします！')
            await asyncio.sleep(3)
            await my_message.edit(content='定義：●は表、○は裏')
            await asyncio.sleep(3)
            coinp = 0
            while coinp < 6:
                await my_message.edit(content='抽選中：○```定義：●は表、○は裏```')
                await asyncio.sleep(0.5)
                await my_message.edit(content='抽選中：●```定義：●は表、○は裏```')
                await asyncio.sleep(0.5)
                coinp += 1
            await my_message.edit(content='抽選中：　```定義：●は表、○は裏```')
            await asyncio.sleep(2)
            await my_message.edit(content='　結果：'+ coin + '```定義：●は表、○は裏 \n adid:sn' + coin1 + '```')
            
            return
        await message.channel.send('Error')
           
#運勢
    if message.content == '運勢':
        if message.channel.id == CHANNEL_ID3 or CHANNEL_IDother:
            prob = random.random()
    
            if prob < 0.3:
                await message.channel.send('凶です……外出を控えることをオススメします')
           
            elif prob < 0.65:
                await message.channel.send('吉です！何かいい事があるかもですね！')
        
            elif prob < 0.71:
                await message.channel.send('末吉……どれくらい運がいいんでしょうね？•́ω•̀)?')
        
            elif prob < 0.76:
                await message.channel.send('半吉は吉の半分、つまり運がいいのです！')
        
            elif prob < 0.80:
                await message.channel.send('小吉ですね！ちょっと優しくされるかも？')
        
            elif prob < 0.83:
                await message.channel.send('吉の中で1番当たっても微妙に感じられる……つまり末吉なのです( ´･ω･`)')
       
            elif prob <= 1.0:
                await message.channel.send('おめでとうございます！大吉ですよ！(๑>∀<๑)♥')   
        

    if message.content == '御神籤':
        if message.channel.id == CHANNEL_ID3 or CHANNEL_IDother:
            await asyncio.sleep(0.1)
            prob = random.random()
    
            if prob < 0.02: #大凶
                await message.channel.send('https://cdn.discordapp.com/attachments/649413089778728970/655056313637666816/20191213233945.jpg')
        
            elif prob < 0.10: #凶
                await message.channel.send('https://cdn.discordapp.com/attachments/649413089778728970/655055945659056134/20191213233816.jpg')
        
            elif prob < 0.35: #吉
                await message.channel.send('https://cdn.discordapp.com/attachments/649413089778728970/655055610441891840/20191213233638.jpg')
        
            elif prob < 0.55: #半吉
                await message.channel.send('https://cdn.discordapp.com/attachments/649413089778728970/655054936773754890/20191213233418.jpg')
        
            elif prob < 0.75: #小吉
                await message.channel.send('https://cdn.discordapp.com/attachments/649413089778728970/655054736638345238/20191213233326.jpg')
        
            elif prob < 0.95: #末吉
                await message.channel.send('https://cdn.discordapp.com/attachments/649413089778728970/655054481956012046/20191213233205.jpg')
       
            elif prob <= 1.0: #大吉
                await message.channel.send('https://cdn.discordapp.com/attachments/649413089778728970/655051678499995651/20191213232052.jpg')   
        
    if message.content.startswith("!dc"):
        # 入力された内容を受け取る
        say = message.content 

        # [!dc ]部分を消し、AdBのdで区切ってリスト化する
        order = say.strip('!dc ')
        cnt, mx = list(map(int, order.split('d'))) # さいころの個数と面数
        dice = diceroll(cnt, mx) # 和を計算する関数(後述)
        await message.channel.send(dice[cnt])
        del dice[cnt]

        # さいころの目の総和の内訳を表示する
        await message.channel.send(dice)

    if message.content == 'ステータス':
        if message.author.guild_permissions.administrator:
            embed = discord.Embed(title="この鯖のステータス",description="Embed式")
            embed.add_field(name="サーバー名",value=f'{message.guild.name}',inline=False)
            embed.add_field(name="現オーナー名",value=f'{message.guild.owner}',inline=False)
            guild = message.guild
            member_count = sum(1 for member in guild.members if not member.bot) 
            bot_count = sum(1 for member in guild.members if member.bot) 
            all_count = (member_count) + (bot_count)
            embed.add_field(name="総人数",value=f'{all_count}',inline=False)
            embed.add_field(name="ユーザ数",value=f'{member_count}')
            embed.add_field(name="BOT数",value=f'{bot_count}')
            embed.add_field(name="テキストチャンネル数",value=f'{len(message.guild.text_channels)}個',inline=False)
            embed.add_field(name="ボイスチャンネル数",value=f'{len(message.guild.voice_channels)}個',inline=False)
            embed.set_thumbnail(url=message.guild.icon_url)
            await message.channel.send(embed=embed)

    if message.author.bot:  # ボットのメッセージをハネる
        return 

    if client.user in message.mentions: # 話しかけられたかの判定
        hensin = random.choice(('よんだ？', 'なにー？', 'たべちゃうぞー！', 'がおー！', 'よろしくね', '！？'))
        reply = f'{message.author.mention} さん' + hensin + '```\n 私の機能が分からなかったら「ヘルプ」と打ってね☆```' #返信メッセージの作成
        await message.channel.send(reply) # 返信メッセージを送信

    if message.content.startswith("赤"): #から始まるメッセージ
        #指定したチャンネルとメッセージを送ったチャンネルが同じIDなら実行
        if message.channel.id == lot_channel_id:
            role1 = discord.utils.get(message.guild.roles, name='class SAXONY')
            await message.author.add_roles(role1)
            role0 = discord.utils.get(message.guild.roles, name='class ticket')
            await message.author.remove_roles(role0)
            dm = await message.author.create_dm()
            await dm.send(f"{message.author.mention}さん! \n 「class-SAXONY」に参加しました。")
            await client.get_channel(lot_result_channel_id1).send(f'{message.author.mention} さんが参加しました！')
        if not message.channel.id == lot_channel_id:
            await message.delete()

    if message.content.startswith("黄"): #から始まるメッセージ
        #指定したチャンネルとメッセージを送ったチャンネルが同じIDなら実行
        if message.channel.id == lot_channel_id:
            role2 = discord.utils.get(message.guild.roles, name='class CRIMEAN')
            await message.author.add_roles(role2)
            role0 = discord.utils.get(message.guild.roles, name='class ticket')
            await message.author.remove_roles(role0)
            dm = await message.author.create_dm()
            await dm.send(f"{message.author.mention}さん！ \n 「class-CRIMEAN」に参加しました。")
            await client.get_channel(lot_result_channel_id2).send(f'{message.author.mention} さんが参加しました！')
        if not message.channel.id == lot_channel_id:
            await message.delete()

    if message.content.startswith("緑"): #から始まるメッセージ
        #指定したチャンネルとメッセージを送ったチャンネルが同じIDなら実行
        if message.channel.id == lot_channel_id:
            role3 = discord.utils.get(message.guild.roles, name='class RUSVIET')
            await message.author.add_roles(role3)
            role0 = discord.utils.get(message.guild.roles, name='class ticket')
            await message.author.remove_roles(role0)
            dm = await message.author.create_dm()
            await dm.send(f"{message.author.mention}さん! \n 「class-RUSVIET」に参加しました。")
            await client.get_channel(lot_result_channel_id3).send(f'{message.author.mention} さんが参加しました！')
        if not message.channel.id == lot_channel_id:
            await message.delete()

    if message.content.startswith("青"): #から始まるメッセージ
        #指定したチャンネルとメッセージを送ったチャンネルが同じIDなら実行
        if message.channel.id == lot_channel_id:
            role4 = discord.utils.get(message.guild.roles, name='class NORDIC')
            await message.author.add_roles(role4)
            role0 = discord.utils.get(message.guild.roles, name='class ticket')
            await message.author.remove_roles(role0)
            dm = await message.author.create_dm()
            await dm.send(f"{message.author.mention}さん! \n 「class NORDIC」に参加しました。")
            await client.get_channel(lot_result_channel_id4).send(f"{message.author.mention} さんが参加しました！")
        if not message.channel.id == lot_channel_id:
            await message.delete()

    now = datetime.datetime.now().strftime('%H')
    if now == '01':
        morning_txt = 'おはようです。ですが、まだ1:00ですよ。'
        evening_txt = 'おやすみなさい。良い夢見て下さいね。'
    elif now == '02':
        morning_txt = 'おはようです。ですが、まだ2:00ですよ。'
        evening_txt = 'おやすみなさい。良い夢見て下さいね。'
    elif now == '03':
        morning_txt = 'おはようです。ですが、まだ3:00ですよ。'
        evening_txt = 'おやすみなさい。夜更かしはあまり良くないですよ。'
    elif now == '04':
        morning_txt = 'おはようです。早起きは良いことです。'
        evening_txt = 'おやすみなさい。健康のため、もう少し早く寝ましょう。'
    elif now == '05':
        morning_txt = 'おはようです。早起きは良いことです。'
        evening_txt = 'おやすみなさい。もう5:00ですよ。'
    elif now == '06':
        morning_txt = 'おはようです。早起きは良いことです。'
        evening_txt = 'おやすみなさい。もう6:00ですよ。'
    elif now == '07':
        morning_txt = 'おはようです。良い朝ですね。'
        evening_txt = 'おやすみなさい。もう朝です。もっと早く眠れるようにしましょう。'
    elif now == '08':
        morning_txt = 'おはようです。朝食は何でしょう。パンかな。ご飯かな。'
        evening_txt = 'おやすみなさい。次の日が休みであっても、早く寝ましょう。'
    elif now == '09':
        morning_txt = 'おはようです。今日も一日頑張りましょう。'
        evening_txt = 'おやすみなさい。昼夜逆転生活はあまり良くありません。'
    elif now == '10':
        morning_txt = 'おはようです。今日も一日頑張りましょう。'
        evening_txt = 'おやすみなさい。この時間は起きていられるよう、早寝早起きを習慣付けましょう。'
    elif now == '11':
        morning_txt = 'おそようです。もう少し早く起きられるように頑張りましょう。'
        evening_txt = 'おやすみなさい。昼寝には少し早いようです。'
    elif now == '12':
        morning_txt = 'おそよーです。もうお昼ですよ。'
        evening_txt = 'おやすみなさい。軽い昼寝は20分程度がオススメです。'
    elif now == '13':
        morning_txt = 'おはようです。残り半日も頑張りましょう。'
        evening_txt = 'おやすみなさい。長めの昼寝は90分程度がオススメです。'
    elif now == '14':
        morning_txt = 'おはようです。14:00です。'
        evening_txt = 'おやすみなさい。長く寝過ぎないように。'
    elif now == '15':
        morning_txt = 'おはようです。今日のおやつは何かな？'
        evening_txt = 'おやすみなさい。長く寝過ぎないように。'
    elif now == '16':
        morning_txt = 'おはようです。長く寝過ぎるのは体には良くありません。'
        evening_txt = 'おやすみなさい。寝るにはまだ早いような気がします。'
    elif now == '17':
        morning_txt = 'おはようです。もう17:00ですよ。'
        evening_txt = 'おやすみなさい。まだ寝るには早いような気がします。'
    elif now == '18':
        morning_txt = 'おはようです。もう18:00。夕食時です。'
        evening_txt = 'おやすみなさい。まだまだ寝るには早いような気がします。'
    elif now == '19':
        morning_txt = 'おはようです。もう19:00。一日が終わりに近づいていますよ。'
        evening_txt = 'おやすみなさい。早寝は良いことです。'
    elif now == '20':
        morning_txt = 'おはようです。20:00です。これから夜がはじまります。'
        evening_txt = 'おやすみなさい。良い夢を見て下さい。'
    elif now == '21':
        morning_txt = 'おはようです。もう夜ですよ。今の生活を改めましょう。'
        evening_txt = 'おやすみなさい。良い夢を見ることを願っています。'
    elif now == '22':
        morning_txt = 'おはようです。まもなく日付が変わります。'
        evening_txt = 'おやすみなさい。明日も良い一日になるように。'
    elif now == '23':
        morning_txt = 'おはようです。まもなく日付が変わりますよ。'
        evening_txt = 'おやすみなさい。明日も頑張りましょう。'
    else:
        morning_txt = 'おはようです。起きるには早すぎます。'
        evening_txt = 'おやすみなさい。日付が変わりました。'
    
    if message.content.startswith("おはよ"): #から始まるメッセージ
        #指定したチャンネルとメッセージを送ったチャンネルが同じIDなら実行
        if message.author.id == master_owner_id:
            await message.channel.send('おはようございます！マスターさん！今日も一日頑張って下さい！') 
        if not message.author.id == master_owner_id:
            await message.channel.send(f"{message.author.mention} さん。{morning_txt}") 

    if message.content.startswith("おやす"): #から始まるメッセージ
        #指定したチャンネルとメッセージを送ったチャンネルが同じIDなら実行
        if message.author.id == master_owner_id:
            await message.channel.send('おやすみなさい！マスターさん！今日も一日お疲れさまでした！') 
        if not message.author.id == master_owner_id:
            await message.channel.send(f"{message.author.mention} さん。{evening_txt}") 

#年月日
    if message.content == '何日？':
        date = datetime.datetime.now()
        await message.channel.send(f'今日は{date.year}年{date.month}月{date.day}日です！')    
    if message.content == '何時？':
        date = datetime.datetime.now()
        await message.channel.send(f'今は{date.hour}時{date.minute}分{date.second}秒だよ！')
    if message.content == '時計':
        weekdays = datetime.date.today().weekday()
        if weekdays == 0:
            weekday_name = "月曜日"
        elif weekdays == 1:
            weekday_name = "火曜日"
        elif weekdays == 2:
            weekday_name = "水曜日"
        elif weekdays == 3:
            weekday_name = "木曜日"
        elif weekdays == 4:
            weekday_name = "金曜日"
        elif weekdays == 5:
            weekday_name = "土曜日"
        elif weekdays == 6:
            weekday_name = "日曜日"
        else:
            weekday_name = "エラー"
        date = datetime.datetime.now()
        embed = discord.Embed(title="時計", description="TimeZone(Japan)",color=random.choice((0,0x1abc9c,0x11806a,0x2ecc71,0x1f8b4c,0x3498db,0x206694,0x9b59b6,0x71368a,0xe91e63,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0x95a5a6,0x607d8b,0x979c9f,0x546e7a,0x7289da,0x99aab5)))
        embed.add_field(name="日付", value=f'{date.year}年{date.month}月{date.day}日{weekday_name}', inline=False)
        embed.add_field(name="時間", value=f'{date.hour}時{date.minute}分{date.second}秒', inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/688986679956340804/690461569854996490/180half_f.gif")
        await message.channel.send(embed=embed)
        
    if message.content == '!restart': 
        if message.author.id == great_owner_id:
            await message.channel.send('再起動します')
            await asyncio.sleep(0.5)
            await client.logout()  
            os.execv(sys.executable,[sys.executable, os.path.join(sys.path[0], __file__)] + sys.argv[1:])  
        if not message.author.id == great_owner_id:
            await message.channel.send('貴方にこのコマンドの使用権限はありません')   

@client.event
async def on_member_join(member):
    if member.guild.id == CHANNEL_ID:
        injoin = f'{member.mention} さん！いらっしゃい！ \n 私は <@511397857887125539> です！ \n 私について分からないことがありましたら、「ヘルプ」と打ってね☆'
        await client.get_channel(CHANNEL_ID4).send(member.name)
        await client.get_channel(CHANNEL_ID4).send(member.id)
        await client.get_channel(CHANNEL_ID).send(injoin)
                 
# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.datetime.now().strftime('%H:%M')
    if now == '09:00':
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('９：００です！おはようございます！今日も一日頑張りましょう！')  
    elif now == '23:00':
        channel = client.get_channel(CHANNEL_ID)
        await channel.send('２３：００です！おやすみなさい！以降のメンションはお控え下さい。') 
#ループ処理実行
loop.start()

client.run(TOKEN)

#リリナ
#ver 6.0.1
