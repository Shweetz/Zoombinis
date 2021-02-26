
import itertools
import operator
import time

zombs = [
    "1111",
    "2222",
    "3333",
    "4444",
    "5555",
    "1234",
    "2345",
    "5432",
    "4321",
    "2534",
    "2142",
    "3115",
    "4531",
    "4125",
    "1133",
    "4344"
    ]
"""
zombs = [
    "1111",
    "1112",
    "1113",
    "1114",
    "1115",
    "1121",
    "1122",
    "1123",
    "1124",
    "1125",
    "1131",
    "1132",
    "1133",
    "1134",
    "1135",
    "1141"
    ]
"""
zombs_test_1 = [
    "1422",
    "5141",
    "2514",
    "4312",
    "5232",
    "5442",
    "2234",
    "2355", # 8
    "2122",
    "1253",
    "1515",
    "5332",
    "2121",
    "2231",
    "5144",
    "3413",
    ]


final_order = [0] * 16

##########   1      2       3      4        5
HAIR = 0 # spike, pony,   bowl,  bald,   hat
EYES = 1 # normal,one,    sleepy,glasses,sunglasses
NOSE = 2 # green, orange, red,   purple, blue
FEET = 3 # feet,  rollers,spring,bike,   helico
ATTS = [HAIR, EYES, NOSE, FEET]
    
def percent(n, total):
    return int(n / total * 10000) / 100

def str_att(att):
    if att == 0:
        return "HAIR"
    elif att == 1:
        return "EYES"
    elif att == 2:
        return "NOSE"
    elif att == 3:
        return "FEET"
    
    print(f"ERROR str_att: att={att}")

def print_list(p_list):
    lig = "["
    for n in p_list:
        if n == 0:
            lig += str(n).rjust(4)
        else:
            lig += str(n.code).rjust(4)
        lig += ", "
    lig = lig[:-2] + "]"
    print(lig)
    lig = "["
    for n in p_list:
        if n == 0:
            lig += str(n).rjust(4)
        else:
            lig += str(n.value).rjust(4)
        lig += ", "
    lig = lig[:-2] + "]"
    print(lig)
    
class Group:
    def __init__(self, zombs):
        self.zombs = []
        for z in zombs:
            self.zombs.append(Zombini(z))
        
        self.reset()
        
    def reset(self):
        for z in self.zombs:
            z.reset()
            
        self.total_perm_tried = 0
        self.total_perm_poss = 0
            
    def g_sort(self, att_1, order_1, att_2, order_2):
        for z in self.zombs:
            z.value = 0
            z.value += order_1.index(z.code[att_1]) * 10 + 10
            z.value += order_2.index(z.code[att_2]) *  1 +  1
#             print(z.value)
        
#         print()
        self.zombs.sort(key=operator.attrgetter("value"), reverse=True)
        
        self.total_perm_tried += 1
        
#         if self.total_perm_tried % 10000 == 0:
#             print(f"Trying permutations: {self.total_perm_tried}/172800")
        
        # Check if sorting works
        for i, code in enumerate(final_order):
            if code != 0:
                
#                 if o.value != self.zombs[i].value:
#                     print(f"{i} {o.value} {self.zombs[i].value}")
#                     return False

                for z in self.zombs:
                    if z.code == code:
                        if z.value != self.zombs[i].value:
                            return False
                
#         print_list(final_order)
#         print_list(self.zombs)
#         print()
        
#         print(f"poss {att_1} {order_1} {att_2} {order_2}")
        for i in range(len(self.zombs)):
            for z in self.zombs:
                if z.value == self.zombs[i].value:
                    if final_order == [0] * 16:
                        z.add_poss(i)
                        
                    else:                        
                        if final_order[i] == 0:
                            if z.code not in final_order:
                                z.add_poss(i)
                                
                        elif final_order[i] == z.code:
                            z.add_poss(i)
                        
        
        self.total_perm_poss += 1
        return True
    
    def g_print(self):
        self.zombs.sort(key=operator.attrgetter("code"))
        
        print()
        
        # Poss total
#         lig = "rank".rjust(4)
#         for i in range(1, len(self.zombs) + 1):
#             lig += " " + str(i).rjust(5)
#         print(lig)
#         
#         for z in self.zombs:
#             lig = z.code
#             for n in z.nb_poss:
#                 lig += " " + str(n).rjust(5)
#             print(lig)
#         print()
        
        # Poss proba
        lig = "rank"
        for i in range(1, len(self.zombs) + 1):
            lig += " " + str(i).rjust(5)
        print(lig)
        
        for z in self.zombs:
            lig = z.code
            for n in z.nb_poss:
                p = percent(n, g.total_perm_poss)
                lig += " " + str(p).rjust(5)
            print(lig)
        print()
        
        print(f"self.total_perm_tried={self.total_perm_tried}")
        print(f"self.total_perm_poss={self.total_perm_poss}")
        
    def best(self):
        p_best = 0
        z_best = 0
        r_best = 0
        
        for z in self.zombs:
            for r, n in enumerate(z.nb_poss):
                p = percent(n, g.total_perm_poss)
                if final_order[r] == 0 and p > p_best:
                    p_best = p
                    z_best = z
                    r_best = r
        
        return p_best, z_best, r_best
        
class Zombini:
    def __init__(self, zomb):
        self.code = zomb
#         self.hair = zomb[HAIR]
#         self.eyes = zomb[EYES]
#         self.nose = zomb[NOSE]
#         self.feet = zomb[FEET]
#         self.value = 0
        self.reset()
    
    def reset(self):
        self.nb_poss = [0] * len(zombs)
        
    def add_poss(self, i):
        self.nb_poss[i] += 1
        
    def __str__(self):
        return "55"

def solve(g):
    while 0 in final_order:
        
        g.reset()
        
        begin = time.time()
#         print(f"Trying permutations: 0/172800")
        
        
        for att1 in ATTS:
            for att2 in ATTS:
                if att1 != att2:                    
                    atts_poss = False
                    
                    for combo1 in itertools.permutations("12345"):
                        for combo2 in itertools.permutations("12345"):
                            
                            if g.g_sort(att1, combo1, att2, combo2):
                                atts_poss = True
                                
                    if atts_poss:
                        print(f"{str_att(att1)} {str_att(att2)}: possible")
                    else:
                        print(f"{str_att(att1)} {str_att(att2)}: impossible")
                        
#         for att1 in ATTS:
#             for att2 in ATTS:
#                 if att1 != att2:
# #                     print(f"{att1} {att2}")
#                     g.g_sort(att1, "54321", att2, "12345")
                    
        
        
#         for att2 in ATTS:
#             if HAIR != att2:
#                 g.g_sort(HAIR, "54321", att2, "12345")
        
#         g.g_sort(HAIR, "12345", NOSE, "12345")
                    
        g.g_print()
        duration = time.time() - begin
        print(f"Time = {int(duration * 10) / 10}sec")
        print()
        
        p_best, z_best, r_best = g.best()
        print(f"Best proba={p_best}%, zomb={z_best.code} at rank {r_best + 1} from the left")
        
        z_code = z_best
        z_code = input("zombini code?")
        final_rank = int(input("zombini rank?")) - 1
        final_order[final_rank] = z_code
        print(final_order)
        print()
        
    print("End")
    
if __name__ == "__main__":
    g = Group(zombs)
    g = Group(zombs_test_1)
    
    solve(g)
    