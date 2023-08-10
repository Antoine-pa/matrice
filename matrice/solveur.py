from matrice import Matrice

class Solveur:
    def __init__(self):
        self._var = ("x", "y", "z", "u", "v", "w")
        n = input("nombre d'inconnues : ")
        assert n.isdigit()
        n = int(n)
        if n > 6:
            print("trop d'inconnues")
            return False
        print("équations de type "+" + ".join([chr(97+nb)+self._var[nb] for nb in range(n)]) + " = r")
        lA = [[0]*n for _ in range(n)]
        lR = [[0] for _ in range(n)]
        print()
        for eq in range(len(lA)):
            print(f"équation n°{eq+1} :")
            for coef in range(len(lA[eq])):
                c = input(f"coef de {self._var[coef]}: ")
                try:
                    c = float(c)
                    if c%1==0:
                        c=int(c)
                except:
                    print(f"{c} n'est pas un nombre")
                    return False
                lA[eq][coef] = c
            r = input("résultat : ")
            try:
                r=float(r)
                if r%1==0:
                    r=int(r)
            except:
                print(f"{r} n'est pas un nombre")
                return False
            lR[eq][0] = r
            self.print_eq(lA, lR, eq, n)
            print()
            
        self.MA = Matrice(lA)
        self.MR = Matrice(lR)
        self.print_result()
        
        
    def solve(self):
        return self.MA.inverse()*self.MR
    
    def print_result(self):
        r = self.solve()
        if not r:
            print("Aucune solution")
            return
        print("\n".join([f"{self._var[nb]}={r.matrice[nb][0]}" for nb in range(len(r.matrice))]))
    
    
    def print_eq(self, lA, lR, eq, n):
        print("".join([f"{'+' if (lA[eq][nb] > 0 and nb !=0) else ''}"+(str(lA[eq][nb]) if abs(lA[eq][nb]) != 1 else ("-" if lA[eq][nb] == -1 else ""))+self._var[nb] for nb in range(n)]) + "=" + str(lR[eq][0]))