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

class Kaiju:
    def __init__(self, name):
        self.name=name

    async def godzillaguess(self,ctx):
        await ctx.send("Canavarlar kralı, radyoaktif kertenkele. (bunu da bil bi zahmet)")
        if Kaiju.name is not self.name:
            return f"Yanlış kaiju! Doğru kaiju şuydu: {self.name}"
        else:
            return f"Doğru"
    async def kingkongguess(self,ctx):
        await ctx.send("Kafatası adası, dev goril.")
        if Kaiju.name is not self.name:
            return f"Yanlış kaiju! Doğru kaiju şuydu: {self.name}"
        else:
            return f"Doğru"
    async def mothraguess(self,ctx):
        await ctx.send("Güve kraliçe, ışık saçar.")
        if Kaiju.name is not self.name:
            return f"Yanlış kaiju! Doğru kaiju şuydu: {self.name}"
        else:
            return f"Doğru"
    async def rodanguess(self,ctx):
        await ctx.send("Kendini anka kuşu sanıyor")
        if Kaiju.name is not self.name:
            return f"Yanlış kaiju! Doğru kaiju şuydu: {self.name}"
        else:
            return f"Doğru"
    async def ghidoraguess(self,ctx):
        await ctx.send("Üç kafalı altın uzaylı hidra.")
        if Kaiju.name is not self.name:
            return f"Yanlış kaiju! Doğru kaiju şuydu: {self.name}"
        else:
            return f"Doğru"

    Kaiju1 = Kaiju("Godzilla",)
    Kaiju1.godzillaguess()
    Kaiju2 = Kaiju("King Kong")
    Kaiju2.kingkongguess()
    Kaiju3 = Kaiju("Mothra")
    Kaiju3.mothraguess()
    Kaiju4 = Kaiju("Rodan")
    Kaiju4.rodanguess()
    Kaiju5 = Kaiju("Ghidorah")
    Kaiju5.ghidoraguess()



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

bot.run(token)
