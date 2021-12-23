import numpy as np
'''
item_dict: MX: [deltaH+,H2O,["X-","M+"]]
'''
item_dict = {
    "HCl": [1, 0, []],
    "NaOH": [-1, 0, []],
    "Ca(OH)2": [-2, 0, []],
    "CaCO3": [-2, 0, ["CO32-"]],
    "CuSO4.5H2O": [1, 1, ["Cu2+","Cu2+"]],
    "NH3.H2O": [-0.5, 0, ["NH4+"]],
    "H2S": [0.5, 0, ["HS-"]],
    "BaSO4": [0,0,[]],
    "CuSO4": [1,0,["Cu2+","Cu2+"]],
    "H2SO4": [2,0,["SO42-"]],
    "AgCl": [0,0,[]],
    "NaCl": [0,0,[]]
}
weak_acid_ions = ["CO32-", "SO32-"]
weak_alka = ["CaCO3", "Fe(OH)2"]
weak_alka_ions = ["Cu2+", "Fe2+"]
turn_gold = [
    3, 5, 7, 9, 9, 9, 9, 9, 11, 13, 13, 13, 13, 13, 13, 13, 15, 15, 15, 17
    ]


def ion_add(ion, amount, curIons):
    print(ion, amount)
    if ion not in curIons:
        curIons[ion] = amount
    elif amount == 0 and curIons[ion] == 0:
        curIons.pop(ion)
    else:
        curIons[ion] += amount
    for i in curIons:
        curIons[i] = round(curIons[i], 1)


class Player():
    def __init__(self, name, cComb, gold=0):
        self.name = name
        self.gold = gold
        self.cComb = cComb


class Beaker():
    def __init__(self, cH, water, Ions, owner):
        self.cH = cH
        self.water = water
        self.Ions = Ions
        self.owner = owner

    def ioni(self, item):
        m = np.abs(item_dict[item][0])
        if item in weak_alka and item_dict[item][0]+self.cH < 0:
            for i in item_dict[item][2]:
                ion_add(i, self.cH, self.Ions)
            self.cH = 0
        else:
            self.cH += item_dict[item][0]
            for i in item_dict[item][2]:
                ion_add(i, m, self.Ions)
        self.checkDH()

    def checkDH(self):
        Ionlist = list(self.Ions.keys())
        if (set(weak_acid_ions) & set(Ionlist)) and (set(weak_alka_ions) & set(Ionlist)):
            alka = list(set(weak_acid_ions) & set(Ionlist))
            acid = list(set(weak_alka_ions) & set(Ionlist))
            for i in range(min(len(alka), len(acid))):
                q = min(self.Ions[alka[i]], self.Ions[acid[i]])
                ion_add(alka[i], -q, self.Ions)
                ion_add(acid[i], -q, self.Ions)

    def check_end(self):
        if np.abs(self.cH) >= self.water:
            Gameplay.endgame(self.owner)


class Gameplay():
    def __init__(self, turn, curPlayer):
        self.turn = turn
        self.curPlayer = curPlayer

    def nxt_turn(self):
        self.curPlayer = 1
        self.turn += 1

    def nxt_player(self):
        self.curPlayer = 2

    def endgame(self):
        print(self.name, "被打败了!")

