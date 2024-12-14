# Author: Warren Tan
# Date Created: 14/12/2024
# Date Modified: 14/12/2024

class Pokemon:

    def __init__(self, id : str, name : str, form : str, hp : int, atk : int, defence : int, spAtk : int, spDefence : int, spd : int):
        self.id = id
        self.name = name
        self.form = form
        self.spdMod = self.speedModifier(spd)

        nerfedForms = ["Mega Rayquaza", "Primal Kyogre", "Primal Groudon"]
        if self.form in nerfedForms:
            self.nerf = 0.97
        else:
            self.nerf = 1

        # find atk
        atkHigher, atkLower = ((atk, spAtk) if atk > spAtk else (spAtk, atk))
        self.attack = self.calculateAttack(atkHigher, atkLower)
        # find def
        defHigher, defLower = ((defence, spDefence) if defence > spDefence else (spDefence, defence))
        self.defence = self.calculateDefence(defHigher, defLower)

        self.stamina = self.calculateStamina(hp)


    def speedModifier(self, spd : int):
        return 1 + ((spd - 75)/500)
    
    def calculateAttack(self, atkHigher : int, atkLower : int):
        higher = 7/8 * atkHigher
        lower = 1/8 * atkLower
        scaledAtk = round(2 * (higher + lower))
        return round(scaledAtk * self.spdMod * self.nerf)
    
    def calculateDefence(self, defHigher : int, defLower : int):
        higher = 5/8 * defHigher
        lower = 3/8 * defLower
        scaledDef = round(2 * (higher + lower))
        return round(scaledDef * self.spdMod * self.nerf)
    
    def calculateStamina(self, hp : int):
        return round(((hp * 1.75 + 50)) * self.nerf)
    
    def __str__(self):
        return f"{self.name} stats:\n" \
               f"Attack: {self.attack}\n" \
               f"Defence: {self.defence}\n" \
               f"HP: {self.stamina}"