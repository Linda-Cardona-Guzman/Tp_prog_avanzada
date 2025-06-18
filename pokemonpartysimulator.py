import requests

class pokemon_trainer:
    def __init__(self, name, trainer_id:int, trainerclass, trainerparty, pokedex):
        self._trainer_id = trainer_id
        self._name = name
        self._trainerclass = trainerclass
        self._trainerparty = trainerparty
        self._pokedex = pokedex
        self._badges = 0
        self._money = 0
        

    def trainercard(self):
        return f"""----------------------------------------
{self._name}
ID: {self._trainer_id}
Trainer Class: {self._trainerclass}
Badges: {self._badges}
Money: {self._money}P¥
----------------------------------------
"""

    def see_party(self):
        return self._trainerparty.show_party()
    
    def see_a_pokemon(self):
        return self._trainerparty.select_a_pokemon()
    
    def see_a_pokedex_entry(self, pokemon):
        a, b = self._pokedex.see_pokemon_entry(pokemon)
        return a, b

    def add_pokemon_to_party(self, pokemon):
        return self._trainerparty.add_pokemon(pokemon)
    
    def take_pokemon_from_party(self, pokemon):
        return self._trainerparty.take_off_pokemon(pokemon)

class pokedex:
    class pokedex_entry:
        def __init__(self, pokemon):
            poke = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon._species}/')
            self._info = poke.json()

            self._pokedexid = self._info["id"]
            self._species = self._info["species"]["name"]
            self._height = self._info["height"]
            self._weight = self._info["weight"]

            self._types = ""
            for i in range(len(self._info["types"])):
                self._types += f"({self._info["types"][i]["type"]["name"]})"

            self._abilities = self._info["abilities"]


        def show_info(self):
            print(f"""Pokedex Number: {self._pokedexid}
Species: {self._species}
Type/s: {self._types}
Height: {self._height}
Weight: {self._weight}
""")

        def show_abilities(self):
            for i in self._abilities:
                print(f"Ability name: {i["ability"]["name"]} (Is it a hidden Ability?: {i["is_hidden"]})")
            

    #---------------------------------------------------------------
    #mainclass ------------------------------------------
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(pokedex, cls).__new__(cls)
        else:
            print("a")
        return cls._instance

    def see_pokemon_entry(self, pokemon):
        a = self.pokedex_entry(pokemon)
        info = a.show_info()
        abilities = a.show_abilities()
        return info, abilities 


class pokemon:
    def __init__(self, species_name, level, nickname=None):
        poke = requests.get(f'https://pokeapi.co/api/v2/pokemon/{species_name}/')
        self._info = poke.json()
        self._stats = self._info["stats"]

        self._nickname = self._info["name"] if nickname is None else nickname[:10]
        self._species = self._info["species"]["name"]
        self._level = level
        self._maxhp = self._stats[0]["base_stat"]
        self._current_hp = self._maxhp
    
    def get_species(self):
        return self._species
    def get_nickname(self):
        return self._nickname
    def get_level(self):
        return self._level
    def get_hp(self):
        return self._current_hp, self._maxhp

    def fainted(self):
        return self._current_hp > 0
    
    def show_stats(self):
        hp, mhp = self.get_hp()
        print(f"\n{self.get_nickname()} / {self.get_species()}")
        print(f"LVL: {self.get_level()}")
        print(f"HP: {hp}/{mhp}")
        for i in self._stats[1:]:
            print(f"{i["stat"]["name"]}: {i["base_stat"]}")


class party:
    class _Node:
        def __init__(self, _data, _next = None):
            self._data = _data
            self._next = _next

    def __init__(self):
        self._first_pkmn = None
        self._size = 0
        
    def add_pokemon(self, pokemon):
        pokemon = self._Node(pokemon)
        

        if self._size >= 6:
            return "The pokémon party is full."
        
        currpoke = self._first_pkmn

        if self._first_pkmn is None:
            self._first_pkmn = pokemon
        else:    
            while currpoke._next is not None:
                currpoke = currpoke._next
        
            currpoke._next = pokemon

        
        self._size += 1

    
    def take_off_pokemon(self, pokemon):
        if self._size <= 1:
            return "You need at least 1 Pokémon in your party."
        
        prevpoke = self._first_pkmn
        currentpoke = self._first_pkmn._next

        while currentpoke is not None:
            if currentpoke._data.get_species() == pokemon or currentpoke._data.get_nickname() == pokemon:
                prevpoke._next = currentpoke._next
            elif prevpoke._data.get_species() == pokemon or prevpoke._data.get_nickname() == pokemon:
                self._first_pkmn = currentpoke

            currentpoke = currentpoke._next
            prevpoke = prevpoke._next

    def select_a_pokemon(self):
        self.show_party()
        opt = int(input("Select a pokémon(1-6): "))
        while (opt > 6 or opt <= 0) or opt > self._size:
            opt = int(input("Select a pokémon(1-6): "))
        
        currpoke = self._first_pkmn
        num = 1

        while currpoke is not None and num <= opt:
            if num == opt:
                return currpoke._data.show_stats()
            currpoke = currpoke._next
            num+= 1
        
        

    
    def show_party(self):
        if self._size == 0:
            return "You don't have Pokemon in your Party."

        print("\nPokémon Party")
        currentpoke = self._first_pkmn
        for i in range(1, 7):
            if currentpoke is not None:
                pkdata = currentpoke._data
                pk_name = pkdata.get_nickname()
                lvl = pkdata.get_level()
                hp, mxhp = pkdata.get_hp()
                print(f"slot {i}: {pk_name.ljust(15)}Lv: {lvl:<3} HP: {hp}/{mxhp}")
                currentpoke = currentpoke._next
            else:
                print(f"slot {i}: {None}")
