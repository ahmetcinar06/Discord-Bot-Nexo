from homework import PC
import discord # discord.py kütüphanesini içe aktar
from discord.ext import commands # Komutlar için gerekli modülü içe aktar
from config import token # Token bilgisini config dosyasından al

# Botun hangi olaylara erişeceğini belirten intents nesnesi oluştur
intents = discord.Intents.default()
# Mesaj içeriğine erişim izni ver
intents.message_content = True

# Botu oluştur, komut ön ekini ve intents'i ayarla
client = commands.Bot(command_prefix='/', intents=intents)
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
        "/about - Bot hakkında bilgi verir.\n"
        "/hello - Merhaba mesajı gönderir.\n"
        "/info - Bot hakkında bilgi verir.\n"
        "/ping - Botun gecikmesini gösterir.\n"
        "/avatar [kullanıcı] - Kullanıcının avatarını gösterir.\n"
        "/kullanici - Adınızı ve ID'nizi gösterir.\n"
        "/sunucu - Sunucu adı ve üye sayısını gösterir.\n"
        "/sunucuinfo - Sunucu oluşturulma tarihi ve bölgesini gösterir.\n"
        "/temizle [miktar] - Mesajları siler. (Varsayılan: 5)\n"
        "/davet - Sunucuya davet linki oluşturur.\n"
        "/rastgele - 2 rastgele sayıyı toplayıp gönderir.\n"
        "/pc_about - PC donanım bilgilerini gösterir.\n"
        "/pc_status - PC kaynak kullanımını gösterir.\n"
        "/pc_antivirus - Antivirüs taraması yapar.\n"
        "/pc_update - Sistem güncellemesi kontrolü yapar.\n"
        "/pc_processes - Çalışan işlemleri listeler.\n"
        "/tahmin - Sayı tahmin oyunu oynatır.\n"
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
async def pc_antivirus(ctx):
    """Antivirüs taraması yapar."""
    await PC().antivirus_scan_discord(ctx)

@client.command()
async def pc_update(ctx):
    """Sistem güncellemesi kontrolü yapar."""
    await PC().system_update_discord(ctx)

@client.command()
async def pc_processes(ctx):
    """Çalışan işlemleri listeler."""
    await PC().processes(ctx)

@client.command()
async def tahmin(ctx):
    """Sayı tahmin oyunu oynatır."""
    await PC().game(ctx)

# Botu başlatmak için token ile çalıştır
client.run('Your Token Here')

