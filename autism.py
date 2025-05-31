# Author: Warren Tan
# Date Created: 14/12/2024
# Date Modified: 22/05/2025

import re
import json
from dataclasses import dataclass, field, asdict
from typing import List

# path to data
dataPath = "latest.json"

global pokedex
global moves
global cpMultipliers
global typeChart

def main():
    defender = getPokemon("Rillaboom")

    

    # get max pokemon from txt file
    with open("availableMax.txt", 'r', encoding="utf-16") as f:
        pokemonStr = [line.strip("\n") for line in f]
        maxAttackers = [getPokemon(string) for string in pokemonStr]

    # get Gmax pokemon from txt file
    with open("availableGMax.txt", 'r', encoding="utf-16") as f:
        pokemonStr = []
        for line in f:
            lineArr = line.strip("\n").split(",")
            GmaxPokemonInfo = lineArr[0], lineArr[1]
            pokemonStr.append(GmaxPokemonInfo)

        GmaxAttackers = [getPokemon(GmaxPokemonInfo[0]) for GmaxPokemonInfo in pokemonStr]

        for index, attacker in enumerate(GmaxAttackers):
            attacker.gmaxType = pokemonStr[index][1]

    # calculate damage and store
    finalDamagesDict = {}

    # Dmax Attackers
    for attacker in maxAttackers:
        for moveStr in attacker.fastMoves:
            attackerMove = Move(name=moveStr, type=getMove(moveStr).type, power=350)
            pokemonName, pokemonDamage, moveType = attacker.calculateDamage(attackerMove, defender, printOut = False)
            finalDamagesDict["Dmax", pokemonName, moveType] = pokemonDamage

        for moveStr in attacker.eliteFastMove:
            attackerMove = Move(name=moveStr, type=getMove(moveStr).type, power=350)
            pokemonName, pokemonDamage, moveType = attacker.calculateDamage(attackerMove, defender, printOut = False)
            if ("Dmax",pokemonName, moveType) not in finalDamagesDict:
                finalDamagesDict["Dmax", pokemonName, moveType + "*"] = pokemonDamage

    # Gmax Attackers
    for attacker in GmaxAttackers:
        if attacker.gmaxType != "typeless":
            attackerMove = Move(name="GmaxMove", type=(f"POKEMON_TYPE_{attacker.gmaxType}".upper()), power=450)
            pokemonName, pokemonDamage, moveType = attacker.calculateDamage(attackerMove, defender, printOut = False)
            finalDamagesDict["Gmax", pokemonName, moveType] = pokemonDamage
    
    # convert dictionary to sorted array and print
    finalDamagesSorted = sorted(finalDamagesDict.items(), key=lambda x: x[1], reverse=True)
    print(f"Max,Name,Damage,Type")
    for item in finalDamagesSorted:
        key, pokemonDamage = item
        maxType, pokemonName, moveType = key
        print(f"{maxType},{pokemonName.capitalize()},{pokemonDamage},{moveType.replace('POKEMON_TYPE_', '').capitalize()}")


@dataclass
class Pokemon:

    id: int = 0
    name: str = "missingNo"
    type: str = "typeless"
    type2: str = "None"
    stamina: int = 0
    attack: int = 0
    defense: int = 0
    gmaxType: str = "typeless"

    fastMoves: List[str] = field(default_factory=list)
    eliteFastMove: List[str] = field(default_factory=list)
    chargedMoves: List[str] = field(default_factory=list)
    eliteChargedMove: List[str] = field(default_factory=list)

    damage: int = None

    def calculateDamage(self, move, other = None, level : int = 20, iv : int = 10, otherLevel : int = 52, printOut = True):

        # default to 0 defense
        if other is None:
            other = Pokemon()

        actualAttack = (self.attack * cpMultipliers[level - 1]) + iv

        # Tier 6 max raids have a CP multiplier of ~8.5x = ~level 52
        # raid boss attack/defense IVs are always maxed
        actualDefense = (other.defense * cpMultipliers[otherLevel - 1]) + 15

        # STAB
        sameTypeAttackBonus = (1.2 if ((move.type == self.type) | (move.type == self.type2)) else 1)
        
        # supereffective
        supereffectiveType1 = (1 if other.type == "typeless" else getTypeMatchup(move.type, other.type))
        supereffectiveType2 = (1 if other.type2 == "" else getTypeMatchup(move.type, other.type2))
        supereffective = supereffectiveType1 * supereffectiveType2

        modifier = sameTypeAttackBonus * supereffective

        self.damage = int(((0.5 * move.power * (actualAttack/actualDefense) * modifier) // 1) + 1)

        if printOut:
            print(f"{self.name},{self.damage},{move.type.replace('POKEMON_TYPE_', '').capitalize()}")

        return self.name, self.damage, move.type

    def __str__(self):
        output = ""
        for key, value in asdict(self).items():
            if key not in {"fastMoves", "eliteFastMove", "chargedMoves", "eliteChargedMove"}:
                output += f"{value},"
            else:
                for move in value:
                    output += f"{move} "
                output += f","

        return output
    
    def keys(self):
        output = ""
        for key, _ in asdict(self).items():
            output += f"{key},"
        return output

    def __gt__(self, other):
        return self.damage > other.damage
    
    def __lt__(self, other):
        return self.damage < other.damage
    
    def __eq__(self, other):
        return self.damage == other.damage

@dataclass
class Move:

    name: str = ""
    type: str = "None"
    power: int = -1
    energy: int = -1

    def __str__(self):
        output = ""
        for key, value in asdict(self).items():
            output += f"{value},"

        return output
    
    def keys(self):
        output = ""
        for key, _ in asdict(self).items():
            output += f"{key},"
        return output

    def __gt__(self, other):
        return self.name > other.name
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __eq__(self, other):
        return self.name == other.name

# creates table
def createPokemonTable(filePath : str):
    # create table
    table = []

    # regex for pokemon
    pokemonPattern = re.compile(r"V\d{4}_POKEMON_[A-Z0-9]+$")

    # check all data in filePath
    with open(filePath, 'r') as f:
        for entry in json.load(f):
            templateId = entry.get("templateId")
            
            # compare to regex pattern
            if pokemonPattern.match(templateId):
                
                # obtain data
                pokemonSettings = entry.get("data", {}).get("pokemonSettings", {})

                pokemonId = int(entry.get("templateId", "")[1:5].lstrip("0"))
                pokemonName = pokemonSettings.get("pokemonId", "")

                pokemonType = pokemonSettings.get("type", "")
                pokemonType2 = pokemonSettings.get("type2", "")

                stats = pokemonSettings.get("stats", {})
                baseStamina = int(stats.get("baseStamina", 0))
                baseAttack = int(stats.get("baseAttack", 0))
                baseDefense = int(stats.get("baseDefense", 0))

                quickMoves = pokemonSettings.get("quickMoves", [])
                eliteQuickMove = pokemonSettings.get("eliteQuickMove", [])
                cinematicMoves = pokemonSettings.get("cinematicMoves", [])
                eliteCinematicMove = pokemonSettings.get("eliteCinematicMove", [])


                newEntry = Pokemon(id = pokemonId, name=pokemonName, type=pokemonType, type2=pokemonType2, stamina=baseStamina, attack=baseAttack, defense=baseDefense, fastMoves=quickMoves, eliteFastMove=eliteQuickMove, chargedMoves=cinematicMoves, eliteChargedMove=eliteCinematicMove)
                
                table.append(newEntry)

    return table

def createMoveTable(filePath : str):
    # create table
    table = []

    # regex for moves
    movePattern = re.compile(r"COMBAT_V\d{4}_MOVE_[A-Z0-9_]+")

    # check all data in filePath
    with open(filePath, 'r') as f:
        for entry in json.load(f):
            templateId = entry.get("templateId")
            
            # compare to regex pattern
            if movePattern.match(templateId):
                
                # obtain data
                combatMove = entry.get("data", {}).get("combatMove", {})

                uniqueId = str(combatMove.get("uniqueId", "")).replace("_FAST", "")
                type = combatMove.get("type", "")
                
                power = float(combatMove.get("power", 0))
                energyDelta = int(combatMove.get("energyDelta", 0))

                newEntry = Move(name=uniqueId, type=type, power=power, energy=energyDelta)
                
                table.append(newEntry)

    return table

def createCPTable(filePath : str):
    # check all data in filePath
    with open(filePath, 'r') as f:
        for entry in json.load(f):
            templateId = entry.get("templateId")
            
            # compare to regex pattern
            if templateId == "PLAYER_LEVEL_SETTINGS":
                
                # obtain data
                multipliers = entry.get("data", {}).get("playerLevel", {}).get("cpMultiplier", {})
                return multipliers

    print(f"Table could not be found")
    return None

def createTypeTable(filePath : str):
    # create table
    table = []

    # regex for types
    # ex: "POKEMON_TYPE_NORMAL"
    movePattern = re.compile(r"POKEMON_TYPE_[A-Z0-9_]+")

    # check all data in filePath
    with open(filePath, 'r') as f:
        for entry in json.load(f):
            templateId = entry.get("templateId")
            
            # compare to regex pattern
            if movePattern.match(templateId):
                
                # obtain data
                # name = entry.get("templateId")
                attackScalar = entry.get("data", {}).get("typeEffective", {}).get("attackScalar", [])

                table.append(attackScalar)

    return table

# get data from table
def getPokemon(query, col : str = "name"):
    if isinstance(query, str):
        query = query.upper()

    for index, data in enumerate(pokedex):
        if getattr(data, col, None) == query:
            return pokedex[index]
    
    print(f"'{query}' not found in col: {col}")
    return None

def getMove(query, col : str = "name"):
    if isinstance(query, str):
        query = query.upper().replace("_FAST", "")

    for index, data in enumerate(moves):
        if getattr(data, col, None) == query:
            return moves[index]
    
    print(f"'{query}' not found in col: {col}")
    return None

def getTypeMatchup(attackerType, defenderType):
    attackingIndicies = ["normal","fighting","flying","poison","ground","rock",
                         "bug","ghost","steel","fire","water","grass",
                         "electric","psychic","ice","dragon","dark","fairy"]
    attackingIndicies.sort()
    
    defendingIndicies = ["normal","fighting","flying","poison","ground","rock",
                         "bug","ghost","steel","fire","water","grass",
                         "electric","psychic","ice","dragon","dark","fairy"]

    attackingIndex = attackingIndicies.index(attackerType.replace("POKEMON_TYPE_", "").lower())
    defendingIndex = defendingIndicies.index(defenderType.replace("POKEMON_TYPE_", "").lower())
    
    return typeChart[attackingIndex][defendingIndex]
    
# print table
def printTypeTable():
    print()

    # defendingTypes = ["normal","fighting","flying","poison","ground","rock",
    #                   "bug","ghost","steel","fire","water","grass",
    #                   "electric","psychic","ice","dragon","dark","fairy"]
    
    # for defendingType in defendingTypes:
    #     print(defendingType, end=",")
    # print()

    # for row in typeChart:
    #     typing = row[0]
    #     chart = row[1]
        
    #     print(typing, end=",")
    #     for scalar in chart:
    #         print(scalar, end=",")
    #     print()

# build table of pokemon
pokedex = createPokemonTable(dataPath)

# build table of moves
moves = createMoveTable(dataPath)
moves.sort()

# build cp multipliers table
cpMultipliers = createCPTable(dataPath)

# build type table
typeChart = createTypeTable(dataPath)

if __name__ == "__main__":
    main()