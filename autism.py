# Author: Warren Tan
# Date Created: 14/12/2024
# Date Modified: 14/12/2024

import csv
from pokemon import Pokemon

table = []

def main():
    statsPath = "Pokemon.csv"

    createTable(statsPath)

    # pretty sure you have to add every dynamax pokemon manually :/
    Available_Max_Pokemon = [MaxPokemon("Lapras", "Ice", True), 
                             MaxPokemon("Charizard", "Fire", True), 
                             MaxPokemon("Charizard", "Fire, Flying, Dragon*"), 
                             MaxPokemon("Blastoise", "Water", True), 
                             MaxPokemon("Blastoise", "Dark, Water"), 
                             MaxPokemon("Venusaur", "Grass", True),
                             MaxPokemon("Venusaur", "Grass"), 
                             MaxPokemon("Gengar", "Ghost", True), 
                             MaxPokemon("Gengar", "Ghost, Dark"),  
                             MaxPokemon("Toxtricity", "Electric", True), 
                             MaxPokemon("Toxtricity", "Electric, Poison"), 
                             MaxPokemon("Cinderace", "Normal, Fire"), 
                             MaxPokemon("Inteleon", "Normal, Water"), 
                             MaxPokemon("Rillaboom", "Normal, Grass"), 
                             MaxPokemon("Excadrill", "Steel, Ground"), 
                             MaxPokemon("Articuno", "Ice"), 
                             MaxPokemon("Zapdos", "Electric"), 
                             MaxPokemon("Moltres", "Fire, Flying"), 
                             MaxPokemon("Cryogonal", "Ice"), 
                             MaxPokemon("Metagross", "Psychic, Steel"), 
                             MaxPokemon("Greedent", "Normal, Grass, Dark, Ground"), 
                             MaxPokemon("Dubwool", "Normal, Fighting"), 
                             MaxPokemon("Kingler", "Water, Steel"), 
                             MaxPokemon("Machamp", "Steel, Fighting"), 
                             MaxPokemon("Falinks", "Fighting"), 
                             ]

    # while i < len(Available_Max_Pokemon)

    Available_Max_Pokemon.sort(reverse=True)

    print("Available Max Pokemon:")
    print("\033[1mMax    |   Pokemon      |  Damage       |  Type")
    print(f"{7 * '-'}+{16 * '-'}+{15 * '-'}+{20 * '-'}", end="\033[0m\n")
    for pokemon in Available_Max_Pokemon:
        print(pokemon)



class MaxPokemon:

    def __init__(self, identifier, types, isGMax : bool = False):
        self.isGMax = isGMax
        self.types = types

        self.pokemon = findByName(identifier)
        self.damage = calculateDamage(self.pokemon, 450 if isGMax else 350)

    def __str__(self):
        form = f"\033[1m{'G' if self.isGMax else 'D'}\033[0mMax"
        output = f"{form}   |   {self.pokemon.name}\t|  {self.damage} dmg\t|  {self.types}"
        # print(output)
        return output

    def __gt__(self, other):
        return self.damage > other.damage
    
    def __lt__(self, other):
        return self.damage < other.damage
    
    def __eq__(self, other):
        return self.damage == other.damage


    
# creates table of all pokemon and their stats
def createTable(filePath : str):
    with open(filePath, "r") as file:
        csvReader = csv.reader(file)
        for data in csvReader:
            # exclude format line
            if data[0] != "ID":
                # create new entry
                newEntry = Pokemon(data[0], data[1], data[2], int(data[6]), int(data[7]), int(data[8]), int(data[9]), int(data[10]), int(data[11]))
                table.append(newEntry)

def findByName(name : str):
    split = name.find(" ")
    if split != -1:
        form = name[0:split]
        name = name[split + 1:]

        if form == "Mega" or form == "Primal":
            form = f"{form} {name}"
    else:
        form = " "

    nameFound = False
    for pokemon in table:
        if pokemon.name == name and (form == " " or pokemon.form == form):
            nameFound = True
            returnPokemon = pokemon
            break

    if not nameFound:
        raise ValueError(f"Name not found: \"{name}\"")

    return returnPokemon

def findByNum(num : str):
    nameFound = False
    for pokemon in table:
        if pokemon.id == num:
            nameFound = True
            returnPokemon = pokemon
            break

    if not nameFound:
        raise ValueError(f"Num not found: \"{num}\"")
    
    return returnPokemon

def calculateDamage(pokemon : Pokemon, basePower : int, atkIV : int = 10):
    actualAttack = pokemon.attack + atkIV
    actualDamage =  int(((0.5 * basePower * actualAttack) // 1) + 1)

    return actualDamage
 
if __name__ == "__main__":
    main()