from datetime import datetime
from pc import PC
from game import Game  # Game sınıfını içe aktar
from poke import Pokemon, Fighter, Wizard, delete_pokemon_from_db  # Pokemon ve alt sınıfları içe aktar
from config import token  # Bot tokenini config.py dosyasından al
import discord # discord.py kütüphanesini içe aktar
from discord.ext import commands # Komutlar için gerekli modülü içe aktar
import time
import openai  # pip install openai
import sqlite3

# SQLite veritabanı bağlantısı ve tablo oluşturma
DB_PATH = "bellek.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS sohbet_bellek (
    user_id TEXT,
    role TEXT,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

def bellek_yukle(user_id, limit=5):
    cursor.execute("SELECT role, content FROM sohbet_bellek WHERE user_id=? ORDER BY timestamp DESC LIMIT ?", (str(user_id), limit))
    rows = cursor.fetchall()
    # Son eklenenler başta, OpenAI için ters çevir
    return [{"role": role, "content": content} for role, content in reversed(rows)]

def bellek_ekle(user_id, role, content):
    cursor.execute("INSERT INTO sohbet_bellek (user_id, role, content) VALUES (?, ?, ?)", (str(user_id), role, content))
    conn.commit()

openai.api_key = 'Your-OpenAI-API-Key'  # OpenAI API anahtarınızı buraya girin

# Botun hangi olaylara erişeceğini belirten intents nesnesi oluştur
intents = discord.Intents.default()
intents.members = True  # Botun kullanıcılarla çalışmasına ve onları banlamasına izin verir
# Mesaj içeriğine erişim izni ver
intents.message_content = True

# Botu oluştur, komut ön ekini ve intents'i ayarla
client = commands.Bot(command_prefix='nexo ', intents=intents)
# Varsayılan help komutunu kaldır, kendi help komutumuzu ekleyeceğiz
client.remove_command('help')


# Bot Discord'a başarıyla bağlandığında çalışacak fonksiyon
@client.event
async def on_ready():
    print(f'Giriş yaptı:  {client.user}')  # Botun kullanıcı adı konsola yazdırılır



# Her mesaj gönderildiğinde tetiklenen olay
@client.event
async def on_message(message):
    # Botun kendi mesajlarını dikkate alma
    if message.author == client.user:
        return

    # Reklam veya bağlantı kontrolü
    link_keywords = ["http://", "https://", "www.", ".com", ".net", ".org"]
    if any(keyword in message.content.lower() for keyword in link_keywords):
        try:
            await message.author.ban(reason="Reklam veya bağlantı paylaşıldı.")
            await message.channel.send(f"{message.author.mention} kullanıcısı reklam/bağlantı nedeniyle banlandı!")
        except discord.Forbidden:
            await message.channel.send("Banlama işlemi için yetkim yok!")
        except Exception as e:
            await message.channel.send(f"Banlama sırasında hata oluştu: {str(e)}")
        return  # Banladıktan sonra başka işlem yapma

    # Mesajda ek (attachment) var mı kontrol et
    if message.attachments:
        # Her ek için kontrol et
        for attachment in message.attachments:
            # Eğer ek bir resim dosyası ise (jpg, png, gif vs.)
            resim_uzantilari = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")
            for uzanti in resim_uzantilari:
                if attachment.filename.lower().endswith(uzanti):
                    dosya_turu = uzanti.replace('.', '').upper()
                    await message.channel.send(f"Sanırım bir resim gönderdiniz! Dosya türü: {dosya_turu}")  # Kullanıcıya yanıt ver
                    break
            else:
                continue
            break  # Sadece bir kez yanıt ver

    # Mesaj bir komutla başlıyorsa komutları işle
    if message.content.startswith(client.command_prefix):
        await client.process_commands(message)

# Zeka modu aktif kullanıcıları tutan set
# Zeka modu aktif kullanıcıları tutan set
zeka_modu_aktif = set()

# Kullanıcıya özel sohbet belleği
sohbet_bellek = {}

fighting_users = set()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Zeka modu açma/kapama komutları
    if message.content.lower().startswith("nexo ai"):
        zeka_modu_aktif.add(message.author.id)
        await message.channel.send("AI modu aktif.\nÇıkmak için 'nexo çık' yazın.")
        return

    if message.content.lower().startswith("nexo çık"):
        zeka_modu_aktif.discard(message.author.id)
        await message.channel.send("AI modu kapatıldı.")
        return

    # Zeka modu aktifse prefix olmadan cevap ver
    if message.author.id in zeka_modu_aktif and not message.author.bot:
            # Kullanıcıya ait geçmişi veritabanından al
            history = bellek_yukle(message.author.id, limit=5)
            # Yeni mesajı belleğe ekle
            bellek_ekle(message.author.id, "user", message.content)
            history.append({"role": "user", "content": message.content})

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4.1-mini",
                    messages=history,
                    max_tokens=500
                )
                cevap = response.choices[0].message.content
                # Botun cevabını da belleğe ekle
                bellek_ekle(message.author.id, "assistant", cevap)
                await message.channel.send(cevap)
            except Exception as e:
                await message.channel.send(f"Yanıt alınamadı: {str(e)}")
            return

    # Reklam veya bağlantı kontrolü
    link_keywords = ["http://", "https://", "www.", ".com", ".net", ".org"]
    if any(keyword in message.content.lower() for keyword in link_keywords):
        try:
            await message.author.ban(reason="Reklam veya bağlantı paylaşıldı.")
            await message.channel.send(f"{message.author.mention} kullanıcısı reklam/bağlantı nedeniyle banlandı!")
        except discord.Forbidden:
            await message.channel.send("Banlama işlemi için yetkim yok!")
        except Exception as e:
            await message.channel.send(f"Banlama sırasında hata oluştu: {str(e)}")
        return

    # Mesajda ek (attachment) var mı kontrol et
    if message.attachments:
        for attachment in message.attachments:
            resim_uzantilari = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp")
            for uzanti in resim_uzantilari:
                if attachment.filename.lower().endswith(uzanti):
                    dosya_turu = uzanti.replace('.', '').upper()
                    await message.channel.send(f"Sanırım bir resim gönderdiniz! Dosya türü: {dosya_turu}")
                    break
            else:
                continue
            break

    # Komutları işle
    if message.content.startswith(client.command_prefix):
        await client.process_commands(message)

@client.command()
async def apikota(ctx):
    """OpenAI API token sınırı hakkında bilgi verir."""
    await ctx.send(
        "OpenAI API token kullanım sınırını doğrudan bot üzerinden öğrenmek mümkün değildir.\n"
        "Kota ve kullanım bilgisi için https://platform.openai.com/usage adresini ziyaret edebilirsiniz."
    )

@client.command()
async def version(ctx):
    """Yapay zeka modelinin sürümünü gösterir."""
    await ctx.send("Kullandığım yapay zeka modeli: GPT-4.1-mini")

# Ping komutu: Botun gecikmesini gösterir
@client.command()
async def ping(ctx):
    """Botun gecikmesini gösterir."""
    latency = round(client.latency * 1000)  # Gecikmeyi milisaniye cinsinden hesapla
    await ctx.send(f'Pong! Gecikme: {latency}ms')  # Sonucu kanala gönder

# Avatar komutu: Kullanıcının avatarını gösterir
@client.command()
async def avatar(ctx, member: discord.Member = None):
    """Kullanıcının avatarını gösterir."""
    member = member or ctx.author
    await ctx.send(f'{member.display_name} adlı kullanıcının avatarı: {member.avatar.url}')

# Kullanıcı komutu: Komutu kullanan kişinin adını ve ID'sini gösterir
@client.command()
async def kullanici(ctx):
    """Kullanıcı adını ve ID'sini gösterir."""
    await ctx.send(f'Adınız: {ctx.author.display_name}\nID: {ctx.author.id}')

# Sunucuinfo komutu: Sunucu oluşturulma tarihi ve bölgesini gösterir
@client.command()
async def sunucuinfo(ctx):
    """Sunucu oluşturulma tarihi ve bölgesini gösterir."""
    guild = ctx.guild
    await ctx.send(f'Sunucu oluşturulma tarihi: {guild.created_at.strftime("%d.%m.%Y %H:%M")}\nBölge: {getattr(guild, "region", "Bilinmiyor")}')

# Davet komutu: Sunucuya davet linki oluşturur (izin varsa)
@client.command()
async def davet(ctx):
    """Sunucuya davet linki oluşturur."""
    try:
        invite = await ctx.channel.create_invite(max_age=300)
        await ctx.send(f'Davet linkiniz (5 dakika geçerli): {invite.url}')
    except Exception:
        await ctx.send('Davet linki oluşturulamadı. Yetkiniz olmayabilir.')

# Rastgele komutu: 1-100 arası rastgele sayı gönderir
import random
@client.command()
async def rastgele(ctx):
    """1-100 arası rastgele sayı gönderir."""
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    sayi = num1 + num2  # İki rastgele sayının toplamını gönder
    await ctx.send(f'Rastgele sayıların toplamı: {sayi}')


# Sunucu bilgisi komutu: Sunucu adı ve üye sayısını gösterir
@client.command()
async def sunucu(ctx):
    """Sunucu adı ve üye sayısını gösterir."""
    guild = ctx.guild  # Komutun kullanıldığı sunucu bilgisini al
    await ctx.send(f'Sunucu adı: {guild.name}\nÜye sayısı: {guild.member_count}')  # Bilgileri gönder


# Temizle komutu: Belirtilen kadar mesajı siler
@client.command()
async def temizle(ctx, miktar: int = 5):
    """Belirtilen kadar mesajı siler. (Varsayılan: 5)"""
    deleted = await ctx.channel.purge(limit=miktar+1)  # Komut dahil miktar kadar mesajı sil
    await ctx.send(f'{len(deleted)-1} mesaj silindi.', delete_after=2)  # Sonucu bildir, 2 sn sonra sil


# Hakkında komutu: Bot hakkında bilgi verir
@client.command()
async def about(ctx):
    await ctx.send('Bu discord.py kütüphanesi ile oluşturulmuş echo-bot!')


# Bot hakkında bilgi veren komut
@client.command()
async def info(ctx):
    """Bot hakkında bilgi verir."""
    await ctx.send('Ben bir Discord echo-botuyum! Komutlarım ve özelliklerim hakkında bilgi almak için /help yazabilirsin.')

# Merhaba komutu: Selam mesajı gönderir
@client.command()
async def hello(ctx):
    await ctx.send('Merhaba! Ben bir echo-botum!')




# Yardım komutu: Tüm komutları listeler
@client.command()
async def help(ctx):
    komutlar = (
        "nexo about - Bot hakkında bilgi verir.\n"
        "nexo hello - Merhaba mesajı gönderir.\n"
        "nexo info - Bot hakkında bilgi verir.\n"
        "nexo ping - Botun gecikmesini gösterir.\n"
        "nexo avatar [kullanıcı] - Kullanıcının avatarını gösterir.\n"
        "nexo kullanici - Adınızı ve ID'nizi gösterir.\n"
        "nexo sunucu - Sunucu adı ve üye sayısını gösterir.\n"
        "nexo sunucuinfo - Sunucu oluşturulma tarihi ve bölgesini gösterir.\n"
        "nexo temizle [miktar] - Mesajları siler. (Varsayılan: 5)\n"
        "nexo davet - Sunucuya davet linki oluşturur.\n"
        "nexo rastgele - 2 rastgele sayıyı toplayıp gönderir.\n"
        "nexo pc_about - PC donanım bilgilerini gösterir.\n"
        "nexo pc_status - PC kaynak kullanımını gösterir.\n"
        "nexo antivirus - Antivirüs taraması yapar.\n"
        "nexo update - Sistem güncellemesi kontrolü yapar.\n"
        "nexo processes - Çalışan işlemleri listeler.\n"
        "nexo game - Sayı tahmin oyunu oynatır.\n"
        "nexo roller - Sunucudaki rolleri listeler.\n"
        "nexo dm [mesaj] - Kullanıcıya DM gönderir.\n"
        "nexo aktif - Sunucudaki çevrimiçi üyeleri listeler.\n"
        "nexo uptime - Botun çalışma süresini gösterir.\n"
        "nexo ai - Yapay zeka moduna geçiş yapar.\n"
        "nexo version - Yapay zeka modelinin sürümünü gösterir.\n"
        "nexo apikota - OpenAI API token sınırı hakkında bilgi verir.\n"
        "nexo go - Sizin için rastgele bir Pokémon oluşturur.\n"
        "nexo pokemon - Sahip olduğunuz Pokémon'un bilgilerini gösterir.\n"
        "nexo feed - Pokémon'unuzu besleyerek deneyim kazandırırsınız.\n"
        "nexo evolve - Pokémon'unuzu evrimleştirirsiniz.\n"
        "Eğer bir resim gönderirseniz, bot resim gönderdiğinizi ve dosya türünü size bildirir!\n"
    )
    await ctx.send(f'Benim komutlarım:\n{komutlar}')


# Komutlarda hata oluşursa kullanıcıya bilgi verir
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):  # Eksik argüman hatası
        await ctx.send('Eksik argüman girdiniz!')
    elif isinstance(error, commands.CommandNotFound):  # Komut bulunamadı hatası
        await ctx.send('Böyle bir komut yok!')
        await ctx.send('Komutları görmek için `nexo help` yazabilirsiniz.')
    elif isinstance(error, commands.MissingPermissions):  # Yetki hatası
        await ctx.send('Bu komutu kullanmak için izniniz yok!')
    else:
        await ctx.send(f'Bir hata oluştu: {str(error)}')  # Diğer hatalar


# PC yönetim ve oyun komutları (sadece Discord'a özel async fonksiyonlar)
@client.command()
async def pc_about(ctx):
    """PC donanım bilgilerini gösterir."""
    await PC().about_PC(ctx)

@client.command()
async def pc_status(ctx):
    """PC kaynak kullanımını gösterir."""
    await PC().PC_status_discord(ctx)

@client.command()
async def antivirus(ctx):
    """Antivirüs taraması yapar."""
    await PC().antivirus_scan_discord(ctx)

@client.command()
async def update(ctx):
    """Sistem güncellemesi kontrolü yapar."""
    await PC().system_update_discord(ctx)

@client.command()
async def processes(ctx):
    """Çalışan işlemleri listeler."""
    await PC().processes(ctx)

@client.command()
async def game(ctx):
    """Sayı tahmin oyunu oynatır."""
    await Game().game(ctx)

# Sunucudaki rollerin listesini gösterir
@client.command()
async def roller(ctx):
    """Sunucudaki tüm rolleri listeler."""
    roles = [role.name for role in ctx.guild.roles if role.name != "@everyone"]
    await ctx.send("Sunucudaki roller:\n" + ", ".join(roles) if roles else "Hiç rol yok.")

# Kullanıcıya özel DM mesajı gönderir
@client.command()
async def dm(ctx, *, mesaj: str):
    """Kullanıcıya özel DM mesajı gönderir."""
    try:
        await ctx.author.send(mesaj)
        await ctx.send("DM gönderildi!")
    except Exception:
        await ctx.send("DM gönderilemedi.")

# Sunucudaki aktif üyeleri listeler
@client.command()
async def aktif(ctx):
    """Sunucudaki çevrimiçi üyeleri listeler."""
    aktifler = [m.display_name for m in ctx.guild.members if m.status == discord.Status.online and not m.bot]
    await ctx.send("Çevrimiçi üyeler:\n" + ", ".join(aktifler) if aktifler else "Şu anda kimse çevrimiçi değil.")

# Botun uptime bilgisini gösterir
bot_start_time = time.time()
@client.command()
async def uptime(ctx):
    """Botun ne kadar süredir aktif olduğunu gösterir."""
    elapsed = int(time.time() - bot_start_time)
    saat = elapsed // 3600
    dakika = (elapsed % 3600) // 60
    saniye = elapsed % 60
    await ctx.send(f"Bot {saat} saat, {dakika} dakika, {saniye} saniyedir aktif.")

@client.command()
async def saat(ctx):
    """Sunucudaki saat bilgisini gösterir."""
    await ctx.send(f"Sunucudaki saat: {datetime.now().strftime('%H:%M:%S')}")

@client.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons.keys():
        await ctx.send("Hangi tür Pokémon istiyorsun?\n1. Sıradan\n2. Dövüşçü\n3. Sihirbaz\nYanıt olarak 1, 2 veya 3 yaz.")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content in ["1", "2", "3"]
        try:
            msg = await client.wait_for("message", check=check, timeout=30)
            if msg.content == "2":
                pokemon = Fighter(author)
            elif msg.content == "3":
                pokemon = Wizard(author)
            else:
                pokemon = Pokemon(author)
        except Exception:
            pokemon = Pokemon(author)
        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémonun görüntüsü yüklenemedi!")
    else:
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!\nSahip olduğunuz Pokémon'u silmek için `nexo delete_pokemon` komutunu kullanabilirsiniz.")

@client.command()
async def delete_pokemon(ctx):
    """Kullanıcının Pokémon'unu siler."""
    await ctx.send("Pokémon'u silmek için onay verin. Bu işlem 10 PokéPuan'a mal olacaktır. (evet/hayır)")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["evet", "hayır"]
    try:
        msg = await client.wait_for("message", check=check, timeout=30)
    except TimeoutError:
        await ctx.send("Zaman aşımına uğradı. Pokémon silme işlemi iptal edildi.")
        return
    if msg.content.lower() == "hayır":
        await ctx.send("Pokémon silme işlemi iptal edildi.")
        return
    if msg.content.lower() == "evet":
        author = ctx.author.name
        if author not in Pokemon.pokemons:
            await ctx.send("Silinecek bir Pokémon'un bulunmuyor.")
            return
        if Pokemon.pokepoints.get(author, 0) < 10:
            await ctx.send(f"Yeterli PokéPuan'ın yok! Bu işlem için 10 puan gerekir. Mevcut puanın: {Pokemon.pokepoints.get(author, 0)}")
            await ctx.send(f"Eğer puan kazanmak istersen, `nexo game` komutunu kullanarak oyun oynayabilirsin!")
            return
        # Silme işlemini gerçekleştir
        del Pokemon.pokemons[author]
        Pokemon.pokepoints[author] -= 10
        delete_pokemon_from_db(author)
        await ctx.send(f"{author}, Pokémon'un başarıyla silindi! Kalan PokéPuan'ın: {Pokemon.pokepoints[author]}")

@client.command()
async def pokemon(ctx):
    """Sahip olduğunuz Pokémon'un bilgilerini gösterir."""
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        info_msg = await pokemon.info()
        # Son besleme zamanı
        last_time = getattr(Pokemon, 'last_feed_time', {}).get(author)
        if last_time:
            last_time_str = last_time.strftime('%d.%m.%Y %H:%M')
            info_msg += f"\nSon besleme zamanı: {last_time_str}"
        else:
            info_msg += "\nSon besleme zamanı: Henüz beslenmedi."
        await ctx.send(info_msg)
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémon'un görüntüsü yüklenemedi!")
    else:
        await ctx.send("Henüz bir Pokémon'un yok. `nexo go` komutu ile bir tane alabilirsin.")

@client.command()
async def feed(ctx):
    """Pokémon'unuzu besleyerek deneyim kazandırırsınız (savaşta kullanılamaz)."""
    author = ctx.author.name
    if author in fighting_users:
        await ctx.send("Savaşta besleme yapılamaz!")
        return
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        feed_message, levelup_message = await pokemon.feed()
        await ctx.send(feed_message)
        if levelup_message:
            await ctx.send(levelup_message)
    else:
        await ctx.send("Besleyecek bir Pokémon'un yok. 'nexo go' komutu ile bir tane alabilirsin.")

@client.command()
async def evolve(ctx):
    """Pokémon'unuzu evrimleştirirsiniz (savaşta kullanılamaz)."""
    author = ctx.author.name
    if author in fighting_users:
        await ctx.send("Savaşta evrim yapılamaz!")
        return
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        evolve_message = await pokemon.evolve()
        await ctx.send(evolve_message)
    else:
        await ctx.send("Evrimleştirecek bir Pokémon'un yok. 'nexo go' komutu ile bir tane alabilirsin.")

@client.command()
async def heal(ctx):
    """Pokémon'unuzu iyileştirir (sadece savaşta kullanılabilir)."""
    author = ctx.author.name
    if author not in fighting_users:
        await ctx.send("Heal komutu sadece savaşta kullanılabilir!")
        return
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        heal_message = await pokemon.heal()
        await ctx.send(heal_message)
    else:
        await ctx.send("Henüz bir Pokémon'un yok. 'nexo go' komutu ile bir tane alabilirsin.")

# Botu başlatmak için token ile çalıştır
client.run(token)