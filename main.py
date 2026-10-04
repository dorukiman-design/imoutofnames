import discord
from discord.ext import commands
from config import token 
from logic import Pokemon
import random
from logic import Wizard, Fighter
from discord import app_commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True 
bot = commands.Bot(command_prefix='!', intents=intents)


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)



@bot.command()  # Kullanıcı "!start" girdiğinde çağrılacak "start" komutunu tanımlayın
async def start(ctx):
    await ctx.send("merhaba, ben bir chomikim. (?)")

@bot.command()  # Kullanıcının yasaklama haklarına sahip olmasını gerektiren "ban" komutunun tanımlanması
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:  # Komutun yasaklanması gereken kullanıcıyı belirtip belirtmediğinin kontrol edilmesi
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Eşit veya daha yüksek rütbeli bir kullanıcıyı yasaklamak mümkün değildir.")
        else:
            await ctx.guild.ban(member)  # Bir kullanıcıyı sunucudan yasaklama
            await ctx.send(f" Kullanıcı {member.name} banlandı.")
        
        if "https://" in ctx.message.content.lower():
            await ctx.message.delete()
            await ctx.author.ban(reason="onun bir reklam olmadığını sen de ben de biliyoruz.")
            await ctx.send(f"{ctx.author.name} reklam yaptığı için banlandı.")
        else:
            await ctx.send("hata")
    else:
        await ctx.send("Bu komut banlamak istediğiniz kullanıcıyı işaret etmelidir. Örneğin: `!ban @user`")

@ban.error  # "ban" komutu için bir hata işleyicisi/handler tanımlayın
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu çalıştırmak için yeterli izniniz yok.")  # Kullanıcıyı erişim hakları hatası hakkında bilgilendiren bir mesaj gönderme
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Kullanıcı bulunamadı.")  # Belirtilen kullanıcı bulunamazsa bir hata mesajı gönderme


@tree.command(name="info", description="Bot hakkında bilgi verir.")
async def info_command(interaction: discord.Interaction):
    #cevap ver ve botun pingini göster
    ping = round(client.latency * 1000)
    await interaction.response.send_message(f"Bot çalışıyor! Ping: {ping}ms")


@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} olarak giriş yapıldı ve /info komutu yüklendi!')


@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')

@bot.event
async def on_member_join(member):
    # Karşılama mesajı gönderme
    for channel in member.guild.text_channels:
        await channel.send(f' Hoş geldiniz: , {member.mention}!')

@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons.keys():
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
        await ctx.send("Zaten kendi Pokémonunuzu oluşturdunuz!")

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):
            chance = random.randint(1, 5)
            if chance == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullandı!"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"

        
@bot.command()
async def start(ctx):
    await ctx.send("Merhaba, ben bir Pokémon oyun botuyum! Kendi pokemonunuzu oluşturmak için !go yazın")

@bot.command()
async def go(ctx):
    author = ctx.author.name
    if author not in Pokemon.pokemons:
        chance = random.randint(1, 3)
        if chance == 1:
            pokemon = Pokemon(author)
        elif chance == 2:
            pokemon = Wizard(author)
        elif chance == 3:
            pokemon = Fighter(author)
        await ctx.send(await pokemon.info())
        image_url = await pokemon.show_img()
        if image_url:
            embed = discord.Embed()
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Pokémon görüntüsü yüklenemedi.")
    else:
        await ctx.send("Zaten bir Pokémon oluşturdunuz.")

@bot.command()
async def attack(ctx):
    target = ctx.message.mentions[0] if ctx.message.mentions else None
    if target:
        if target.name in Pokemon.pokemons and ctx.author.name in Pokemon.pokemons:
            enemy = Pokemon.pokemons[target.name]
            attacker = Pokemon.pokemons[ctx.author.name]
            result = await attacker.attack(enemy)
            await ctx.send(result)
        else:
            await ctx.send("Savaşmak için her iki katılımcının da Pokémon sahibi olması gerekir!")
    else:
        await ctx.send("Saldırmak istediğiniz kullanıcıyı etiketleyerek belirtin.")
@bot.command()
async def info(ctx):
    if ctx.author.name in Pokemon.pokemons:
        pok = Pokemon.pokemons[ctx.author.name]
        await ctx.send(f'Pokémonunuzun ismi: {pok.name}, Canı: {pok.hp}, Gücü: {pok.power}')

    
@bot.command()
async def feed(ctx):
    author = ctx.author.name
    if author in Pokemon.pokemons:
        pokemon = Pokemon.pokemons[author]
        response = await pokemon.feed()
        await ctx.send(response)
    else:
        await ctx.send("Pokémon'un yok!")


bot.run(token)
