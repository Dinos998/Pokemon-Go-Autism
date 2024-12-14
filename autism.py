# Author: Warren Tan
# Date Created: 14/12/2024
# Date Modified: 14/12/2024

import csv
import math
from pokemon import Pokemon

table = []

def main():
    statsPath = "Pokemon.csv"
    
    createTable(statsPath)

    pokemon1 = findByName("Blastoise")
    pokemon2 = findByName("Kingler")

    
    
    calculateDamage(pokemon1, 350, 15)
    calculateDamage(pokemon2, 250, 10)



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

            if data[0] == 151:
                break

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
        if pokemon.name == name and pokemon.form == form:
            nameFound = True
            returnPokemon = pokemon
            break

    if not nameFound:
        raise ValueError("Name not found")

    return returnPokemon

def findByNum(num : str):
    nameFound = False
    for pokemon in table:
        if pokemon.id == num:
            nameFound = True
            returnPokemon = pokemon
            break

    if not nameFound:
        raise ValueError("Name not found")
    
    return returnPokemon

def calculateDamage(pokemon : Pokemon, basePower : int, atkIV : int = 10):
    actualAttack = pokemon.attack + atkIV
    actualDamage =  int(((0.5 * basePower * actualAttack) // 1) + 1)
    
    print(f"%-10s does {actualDamage} damage with a {basePower} power move." % pokemon.name)
    return actualDamage
 
if __name__ == "__main__":
    main()