from matrice import Matrice

class Solveur:
    def __init__(self):
        var = ("x", "y", "z", "u", "v", "w")
        n = input("nombre d'inconnues : ")
        assert n.isdigit()
        n = int(n)
        if n > 6:
            print("trop d'inconnues")
            return False
        print("équations de type "+" + ".join([chr(97+nb)+var[nb] for nb in range(n)]) + " = r")
        lA = [[0]*n for _ in range(n)]
        lR = [[0] for _ in range(n)]
        for eq in range(len(lA)):
            for coef in range(len(lA[eq])+1):
                if coef < len(lA[eq]):
                    c = input(f"coef de {var[coef]}: ")
                    try:
                        c = float(c)
                        if c%1==0:
                            c=int(c)
                    except:
                        print(f"{c} n'est pas un nombre")
                        return False
                    lA[eq][coef] = c
                else:
                    r = input("r")
            
            print("".join([f"{'+' if (lA[eq][nb] > 0 and nb !=0) else ''}"+(str(lA[eq][nb]) if abs(lA[eq][nb]) != 1 else ("-" if lA[eq][nb] == -1 else ""))+var[nb] for nb in range(n)]))
        self.MA = Matrice(lA)
        print(self.MA)
        
        
        
                
                
Solveur()
                
