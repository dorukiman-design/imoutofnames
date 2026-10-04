from datetime import datetime, timedelta

import aiohttp
import random

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.img = None
        self.name = None
        self.hp = random.randint(200, 400)
        self.power = random.randint(30, 60)
        self.last_feed_time  = datetime.now()
        if pokemon_trainer not in self.pokemons:
            self.pokemons[pokemon_trainer] = self

    async def feed(self, feed_interval=60, hp_increase=10):
            current_time = datetime.now()
            delta_time = timedelta(seconds=feed_interval)
            if (current_time - self.last_feed_time) > delta_time:
                self.hp += hp_increase
                self.last_feed_time = current_time
                return f"Pokémon'un sağlığı geri yüklenir. Mevcut sağlık: {self.hp}"
            else:
                return f"Pokémonunuzu şu zaman besleyebilirsiniz: {current_time+delta_time}"



        
    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return f"Pokémonunuzun ismi: {self.name} Pokemonunuzun canı:{self.hp} Pokemonunuzun gücü: {self.power}"

    async def show_img(self):
        # PokeAPI aracılığıyla bir pokémonun adını almak için asenktron metot
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:  #  HTTP oturumu açmak
            async with session.get(url) as response:  # Pokémon verilerini almak için bir GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması
                    img_url = data['sprites']['front_default']  #  Pokémonun URL'sini alma
                    return img_url  # Resmin URL'sini döndürme
                else:
                    return None  # İstek başarısız olursa None döndürür
                
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):  # Düşmanın Wizard veri tipi olup olmadığının kontrol edilmesi (Sihirbaz sınıfının bir örneği midir?) 
            sans = random.randint(1, 5) 
            if sans == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullanıldı!"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"

class Wizard (Pokemon):
    async def feed(self):
        return await super().feed(hp_increase=20)

class Fighter (Pokemon):
    async def attack(self, enemy):
        super_guc = random.randint(5, 15)  
        self.guc += super_guc
        sonuc = await super().attack(enemy)  
        self.guc -= super_guc
        return sonuc + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_guc}"
    async def feed(self):
        return await super().feed(feed_interval=10)
    
    
