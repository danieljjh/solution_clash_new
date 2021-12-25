import math
'''
item_dict: MX: [deltaH+,H2O,["X-","M+"]]
'''
item_dict = {
    "HCl": [1, 0, ["Cl-"]],
    "NaOH": [-1, 0, ["Na+"]],
    "Ca(OH)2": [-2, 0, ["Ca2+"]],
    "CaCO3": [-2, 0, ["CO32-"]],
    "CuSO4.5H2O": [1, 1, ["Cu2+", "Cu2+"]],
    "NH3.H2O": [-0.5, 0, ["NH4+", "NH4+"]],
    "H2S": [0.5, 0, ["HS-", "HS-"]],
    "BaSO4": [0, 0, []],
    "CuSO4": [1, 0, ["Cu2+", "Cu2+"]],
    "H2SO4": [2, 0, ["SO42-"]],
    "AgCl": [0, 0, []],
    "NaCl": [0, 0, ["Na+","Cl-"]],
    "Na2SO3": [-1, 0, ["Na+", "SO32-"]],
    "Na": [-1, -1, ["Na+"]]
}
weak_acid_ions = ["CO32-", "SO32-", "HS-"]
weak_alka = ["CaCO3", "Fe(OH)2", "Zn"]
weak_alka_ions = ["Cu2+", "Fe2+"]
# acid_gas = {
#     "CO32-": 'CO2',
#     "SO32-": "SO2",
#     "HS-": "H2S",
# }
# alka_gas = {
#     "NH4+": "NH3",
# }
# turn_gold = [
#     3, 5, 7, 9, 9, 9, 9, 9, 11, 13, 13, 13, 13, 13, 13, 13, 15, 15, 15, 17
#     ]


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
        self.evalue = []
        self.pH = 7

    def ioni(self, item):
        m = abs(item_dict[item][0])
        if item in weak_alka and (item_dict[item][0] + self.cH < 0) and self.cH > 0:
            for i in item_dict[item][2]:
                ion_add(i, self.cH, self.Ions)
                self.evalue.append(f"电离产生了{i}离子{0.1*self.cH}mol")
            self.cH = 0
        elif self.cH <= 0 and item in weak_alka:
            self.evalue.append("没有用哦！弱碱在中性碱性环境下不可溶。")
        else:   
            self.cH += item_dict[item][0]
            print(item_dict[item][2])
            if len(item_dict[item][2]) == 0:
                self.evalue.append("没有用哦！没有电离出任何东西！")
            for i in item_dict[item][2]:
                ion_add(i, m, self.Ions)
                if item_dict[item][0] == 0:
                    self.evalue.append(f"没有用哦！虽然电离产生了{i}离子，但没有改变pH")
                else:
                    self.evalue.append(f"电离产生了{i}离子{0.1*item_dict[item][0]}mol")
        self.checkDH()
        self.water = self.water + item_dict[item][1]
        self.cal_pH()

    def checkDH(self):
        Ionlist = list(self.Ions.keys())
        if (set(weak_acid_ions) & set(Ionlist)) and (set(weak_alka_ions) & set(Ionlist)):
            alka = list(set(weak_acid_ions) & set(Ionlist))
            acid = list(set(weak_alka_ions) & set(Ionlist))
            for i in range(min(len(alka), len(acid))):
                q = min(self.Ions[alka[i]], self.Ions[acid[i]])
                ion_add(alka[i], -q, self.Ions)
                ion_add(acid[i], -q, self.Ions)
                self.evalue.append(f"{alka[i]}与{acid[i]}产生了沉淀")

    def cal_pH(self):
        if self.cH == 0:
            self.pH = 7
        elif self.cH > 0:
            self.pH = round(-math.log10(0.6 * self.cH / self.water), 3)
        else:
            self.pH = round(14 + math.log10(-0.6 * self.cH / self.water), 3)
    # def checkGas(self):
    #     Ionlist = list(self.Ions.keys())
    #     if (set(acid_gas) & set(Ionlist)) and self.cH > 0:
    #         agas = (set(acid_gas) & set(Ionlist))
    #         for i in agas:
    #             print("1")

    # def check_end(self):
    #     if abs(self.cH) >= self.water:
    #         Gameplay.endgame(self.owner)


# class Gameplay():
#     def __init__(self, turn, curPlayer):
#         self.turn = turn
#         self.curPlayer = curPlayer

#     def nxt_turn(self):
#         self.curPlayer = 1
#         self.turn += 1

#     def nxt_player(self):
#         self.curPlayer = 2

#     def endgame(self):
#         print(self.name, "被打败了！")
