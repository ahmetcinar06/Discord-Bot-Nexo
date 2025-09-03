from poke import Pokemon  # Pokemon sınıfını içe aktar
import random
import asyncio   

class Game:
    async def num_guess(self, ctx):
        await ctx.send("Sayı Tahmin Oyununa hoş geldin! 1-10 arasında bir sayı tuttum. 3 tahmin hakkın var.")
        number = random.randint(1, 10)
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

        for guesses in range(3):
            try:
                await ctx.send(f"{3-guesses} hakkın kaldı. Tahminin nedir?")
                guess_msg = await ctx.bot.wait_for('message', check=check, timeout=20.0)
                guess = int(guess_msg.content)

                if guess < number:
                    await ctx.send("Daha yüksek bir sayı dene.")
                elif guess > number:
                    await ctx.send("Daha düşük bir sayı dene.")
                else:
                    points = 3 - guesses
                    Pokemon.pokepoints[ctx.author.name] = Pokemon.pokepoints.get(ctx.author.name, 0) + points
                    await ctx.send(f"🎉 Tebrikler! Doğru sayıyı ({number}) buldun ve {points} PokéPuan kazandın! Mevcut puanın: {Pokemon.pokepoints[ctx.author.name]}")
                    return
            except asyncio.TimeoutError:
                await ctx.send("Süre doldu! Oyunu kaybettin.")
                return

        await ctx.send(f"Maalesef bilemedin. Doğru sayı {number} idi.")

    async def pokemon_trivia(self, ctx):
        await ctx.send("Pokémon Trivia oyununa hoş geldin!")

        questions = [
            {"soru": "Ash'in ilk Pokémon'u hangisidir?", "cevap": "pikachu"},
            {"soru": "Su Pokémon'ları Ateş Pokémon'larına karşı güçlü müdür? (evet/hayır)", "cevap": "evet"},
            {"soru": "Charmander'ın son evrimi nedir?", "cevap": "charizard"},
            {"soru": "Legendary Birds üçlüsünden buz türü olan hangisidir?", "cevap": "articuno"},
            {"soru": "Mewtwo hangi tür Pokémon'dur?", "cevap": "psikik"},
            {"soru": "Pokémon dünyasında en çok bilinen başlangıç Pokémon'u hangisidir?", "cevap": "bulbasaur"},
            {"soru": "Pokémon dünyasında en çok bilinen efsanevi Pokémon hangisidir?", "cevap": "mewtwo"},
            {"soru": "Pokémon dünyasında en çok bilinen su türü Pokémon hangisidir?", "cevap": "squirtle"},
            {"soru": "Pokémon dünyasında en çok bilinen elektrik türü Pokémon hangisidir?", "cevap": "pikachu"},
            {"soru": "Pokémon dünyasında en çok bilinen normal türü Pokémon hangisidir?", "cevap": "eevee"},
            {"soru": "Pokémon dünyasında en çok bilinen uçan türü Pokémon hangisidir?", "cevap": "pidgey"},
            {"soru": "Su Pokémon'ları Ateş Pokémon'larına karşı güçlü müdür? (evet/hayır)", "cevap": "evet"},
            {"soru": "Ash'in ilk Pokémon'u hangisidir?", "cevap": "pikachu"}
        ]
        
        question_data = random.choice(questions)
        await ctx.send(f"Soru: {question_data['soru']}")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await ctx.bot.wait_for('message', check=check, timeout=20.0)
            
            if msg.content.lower() == question_data['cevap']:
                points = 5
                Pokemon.pokepoints[ctx.author.name] = Pokemon.pokepoints.get(ctx.author.name, 0) + points
                await ctx.send(f"🎉 Doğru cevap! {points} PokéPuan kazandın! Mevcut puanın: {Pokemon.pokepoints[ctx.author.name]}")
            else:
                await ctx.send(f"Maalesef yanlış. Doğru cevap: **{question_data['cevap'].capitalize()}**")

        except asyncio.TimeoutError:
            await ctx.send("Süre doldu! Bu sorudan puan kazanamadın.")

    async def pokemon_battle(self, ctx):
        if not Pokemon.pokemons.get(ctx.author.name):
            await ctx.send("Öncelikle bir Pokémon bulmalısın!")
            return

        elif not Pokemon.pokemons[ctx.author.name]._data_fetched:
            await Pokemon.pokemons[ctx.author.name]._fetch_data()
        user_list = []
        for user, pokemon in Pokemon.pokemons.items():
            if user != ctx.author.name:
                user_list.append(f"{user}: {pokemon.name}")
        if not user_list:
            await ctx.send("Savaşacak başka kullanıcı yok!")
            return
        await ctx.send("Pokémon Savaş Oyunu başladı!\nRakipler:")
        await ctx.send("\n".join(user_list))
        await ctx.send("Karşılaşmak istediğin rakibi seç (kullanıcı adı):")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await ctx.bot.wait_for('message', check=check, timeout=30.0)
            opponent = msg.content

            if opponent == ctx.author.name:
                await ctx.send("Kendinle savaşamazsın!")
                return

            if not Pokemon.pokemons.get(opponent):
                await ctx.send("Bu kullanıcıda bir Pokémon yok!")
                return

            await ctx.send(f"{opponent} ile savaşa hazırlan!")
            player_pokemon = Pokemon.pokemons[ctx.author.name]
            opponent_pokemon = Pokemon.pokemons[opponent]
            await ctx.send(f"{opponent}, saldırı geliyor! Savunmak için 10 saniye içinde 'shield' yazmalısın.")
            def defend_check(m):
                return m.author.name == opponent and m.channel == ctx.channel and m.content.lower() == "shield"
            try:
                defend_msg = await ctx.bot.wait_for('message', check=defend_check, timeout=10.0)
                await ctx.send(f"{opponent} savunma yaptı ve saldırıyı engelledi!")
            except Exception:
                # Savunamazsa hasar uygula ve kazanana power ekle
                battle_result = await player_pokemon.attack(opponent_pokemon)
                await ctx.send(battle_result)
                player_pokemon.power += 10
                await ctx.send(f"{ctx.author.name}'in Pokémon'una +10 güç eklendi! Toplam güç: {player_pokemon.power}")
                # Kazananı bildir
                if opponent_pokemon.hp <= 0:
                    await ctx.send(f"Kazanan: {ctx.author.name}!")
                else:
                    await ctx.send(f"Savaş devam ediyor. {opponent} hala ayakta!")
                    # Savaş devam ediyorsa yeni saldırı ve savunma turu başlat
                    while opponent_pokemon.hp > 0 and player_pokemon.hp > 0:
                        await ctx.send(f"{ctx.author.name}, tekrar saldırmak için herhangi bir şey yaz!")
                        def attack_check(m):
                            return m.author.name == ctx.author.name and m.channel == ctx.channel
                        try:
                            await ctx.bot.wait_for('message', check=attack_check, timeout=15.0)
                        except Exception:
                            await ctx.send("Saldırı için süre doldu!")
                            break
                        await ctx.send(f"{opponent}, savunmak için 10 saniye içinde 'shield' yazmalısın.")
                        def defend_check(m):
                            return m.author.name == opponent and m.channel == ctx.channel and m.content.lower() == "shield"
                        try:
                            defend_msg = await ctx.bot.wait_for('message', check=defend_check, timeout=10.0)
                            await ctx.send(f"{opponent} savunma yaptı ve saldırıyı engelledi!")
                        except Exception:
                            battle_result = await player_pokemon.attack(opponent_pokemon)
                            await ctx.send(battle_result)
                            player_pokemon.power += 10
                            await ctx.send(f"{ctx.author.name}'in Pokémon'una +10 güç eklendi! Toplam güç: {player_pokemon.power}")
                        if opponent_pokemon.hp <= 0:
                            await ctx.send(f"Kazanan: {ctx.author.name}!")
                            break
                        elif player_pokemon.hp <= 0:
                            await ctx.send(f"Kazanan: {opponent}!")
                            break
        except asyncio.TimeoutError:
            await ctx.send("Süre doldu! Rakip seçimi yapamadın.")
            return

    async def game(self, ctx):
        await ctx.send("Hangi oyunu oynamak istersin?\n"
                       "1. Sayı Tahmin Oyunu\n"
                       "2. Pokémon Trivia\n"
                       "3. Pokémon Battle v1.0\n"
                       "Lütfen oynamak istediğin oyunun numarasını yaz.")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content in ["1", "2", "3"]

        try:
            choice_msg = await ctx.bot.wait_for('message', check=check, timeout=30.0)
            choice = choice_msg.content

            if choice == "1":
                await self.num_guess(ctx)
            elif choice == "2":
                await self.pokemon_trivia(ctx)
            elif choice == "3":
                await ctx.send("Pokémon Savaş Oyunu için bir tutorial ister misin? (evet/hayır)")
                def tutorial_check(m):
                    return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["evet", "hayır"]

                try:
                    tutorial_msg = await ctx.bot.wait_for('message', check=tutorial_check, timeout=30.0)
                    if tutorial_msg.content.lower() == "evet":
                        await ctx.send("İşte Pokémon Battle için bir tutorial:\n"
                                       "1. Her oyuncunun bir Pokémon'u olmalı.\n"
                                       "2. Oyuncular sırayla saldırı yapar.\n"
                                       "3. Her Pokémon'un HP'si vardır ve saldırılar bu HP'yi azaltır.\n"
                                       "4. Oyuncular savunma yapabilir ve saldırılardan kaçınabilir.\n"
                                       "5. Oyunun amacı rakibin Pokémon'unu yenmektir.\n"
                                       "Bir şey daha var: Bu oyun daha BETA aşamasındadır ve yani sürümler gelebilir.")
                    await self.pokemon_battle(ctx)

                except asyncio.TimeoutError:
                    await ctx.send("Süre doldu! Tutorial isteğini yanıtlayamadın.")

        except asyncio.TimeoutError:
            await ctx.send("Oyun seçimi için süre doldu. Lütfen tekrar dene.")