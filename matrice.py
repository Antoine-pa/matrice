class Matrice:
    """
    une classe permettant de représenter une matrice et d'effectuer des cacluls dessus.
    attributs:
        matrice: un tableau (liste de liste)
    méthodes:
        dimension(): renvoie les dimensions de la matrice sous forme de tuple
        det(): renvoie le déterminant de la matrice si elle est carrée
        transpose(): renvoie la matrice transposée de la matrice sous forme d'un nouvel objet
        comatrice(): renvoie la comatrice de la matrice sous forme d'un nouvel objet
        adj(): renvoie la matrice adjacente de la matrice sous forme d'un nouvel objet
        inverse(): renvoie la matrice inverse si elle est inversible osus forme d'un nouvel objet
        l_empty(x, y): renvoie un tableau vide dimension de la matrice + x et y
    méthodes spéciales:
        __str__(): renvoie la représentation de la matrice
        __mul__(other): renvoie la multiplication de la matrice par une autre matrice ou un nombre si c'est possible sous forme d'un nouvel objet
        _calc(other, op): renvoie l'addition ou la soustraction en fonction de op entre la matrice et other si c'est possible sous forme d'un nouvel objet
        __add__(other): appelle _calc pour faire l'addition et renvoie son résultat
        __sub__(other): appelle _calc pour faire la soustraction et renvoie son résultat
    """
    def __init__(self, t):
        self.matrice = t

    def __str__(self):
        ret = ""
        matrice_str = []
        for line in self.matrice:
            matrice_str.append(list(map(str, line)))
        if len(self.matrice) == 1:
            return "[ " + " ".join([str(self.matrice[0][n]) for n in range(len(self.matrice[0]))]) + " ]\n"+str(self.dimension())+"\n"
        long_col = []
        for i in range(len(self.matrice[0])):
            l = []
            for line in matrice_str:
                l.append(len(line[i]))
            long_col.append(max(l))

        for i in range(len(matrice_str)):
            if i == 0:
                ret += "/ "
            elif i == len(self.matrice)-1:
                ret += "\ "
            else:
                ret += "| "

            for i2 in range(len(matrice_str[i])):
                el = matrice_str[i][i2]
                ret += matrice_str[i][i2]+"  "+" "*(long_col[i2]-len(el))
            ret = ret[:-2]
            if i == 0:
                ret += " \ \n"
            elif i == len(self.matrice)-1:
                ret += " / \n"
            else:
                ret += " | \n"
        return ret[:-2]+"\n"+str(self.dimension())+"\n"

    def dimension(self) -> tuple:
        return (len(self.matrice), len(self.matrice[0]))

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            t2 = [[] for _ in range(len(self.matrice))]
            for i in range(len(self.matrice)):
                for el in self.matrice[i]:
                    r = el*other
                    if r%1==0:
                        r=int(r)
                    t2[i].append(r)
            return Matrice(t2)


        elif isinstance(other, Matrice):
            d1 = self.dimension()
            d2 = other.dimension()
            if not d1[1] == d2[0]:
                raise ValueError("dimensions non compatibles")
            t2 = [[0 for _ in range(d2[1])] for _ in range(d1[0])]
            for i in range(len(t2)):
                for i2 in range(len(t2[i])):
                    el = 0
                    for i3 in range(d1[1]):
                        el += self.matrice[i][i3]*other.matrice[i3][i2]
                    if el%1==0:
                        el = int(el)
                    t2[i][i2] = el
            return Matrice(t2)
        raise ValueError("bad argument")

    def _calc(self, other, op):
        if not isinstance(other, Matrice):
            raise ValueError("bad argument")
        d1 = self.dimension()
        d2 = other.dimension()
        if d1 != d2:
            raise ValueError("dimensions non compatibles")
        t2 = [[0 for _ in range(d1[1])] for _ in range(d1[0])]
        for i in range(len(self.matrice)):
            for i2 in range(len(self.matrice[i])):
                if op == "+":
                    t2[i][i2] = self.matrice[i][i2] + other.matrice[i][i2]
                else:
                    t2[i][i2] = self.matrice[i][i2] - other.matrice[i][i2]
        return Matrice(t2)

    def __add__(self, other):
        return self._calc(other, "+")

    def __sub__(self, other):
        return self._calc(other, "-")

    def det(self) -> int:
        assert len(self.matrice) == len(self.matrice[0])
        if len(self.matrice) > 2:
            s = 0
            for i in range(len(self.matrice)):
                m = [[0]*(len(self.matrice)-1) for _ in range(len(self.matrice)-1)]
                for line in range(len(self.matrice)):
                    for el in range(len(self.matrice)):
                        if line != 0 and el != i:
                            if el < i:
                                m[line-1][el] = self.matrice[line][el]
                            else:
                                m[line-1][el-1] = self.matrice[line][el]
                d = Matrice(m).det()
                if i%2 == 1:
                    s-=self.matrice[0][i]*d
                else:
                    s+=self.matrice[0][i]*d
            if s%1 == 0:
                s=int(s)
            return s
        elif len(self.matrice) == len(self.matrice[0]) == 1:
            return self.matrice[0][0]
        else:
            return self.matrice[0][0] * self.matrice[1][1] - self.matrice[0][1] * self.matrice[1][0]
        
    def l_empty(self, x = None, y = None) -> list:
        if x is None and y is None:
            x = len(self.matrice[0])
            y = len(self.matrice)
        else:
            x += len(self.matrice[0])
            y += len(self.matrice)
        return [[0]*x for _ in range(y)]
        
    def transpose(self):
        l = self.l_empty()
        for y in range(len(self.matrice)):
            for x in range(len(self.matrice[0])):
                l[x][y] = self.matrice[y][x]
        return Matrice(l)
    
    def comatrice(self):
        if len(self.matrice) == len(self.matrice[0]) == 1:
            return Matrice([[1]]) #Id
        matrice = self.transpose()
        l = matrice.l_empty()
        for y in range(len(matrice.matrice)):
            for x in range(len(matrice.matrice[0])):
                l_mineure = matrice.l_empty(-1, -1)
                for line in range(len(matrice.matrice)):
                    for el in range(len(matrice.matrice[0])):
                        if line != y and el != x:
                            if line < y:
                                if el < x:
                                    l_mineure[line][el] = matrice.matrice[line][el]
                                else:
                                    l_mineure[line][el-1] = matrice.matrice[line][el]
                            else:
                                if el < x:
                                    l_mineure[line-1][el] = matrice.matrice[line][el]
                                else:
                                    l_mineure[line-1][el-1] = matrice.matrice[line][el]
                    
                m_mineure=Matrice(l_mineure)
                l[y][x]=m_mineure.det()
        return Matrice(l)
    
    def adj(self):
        matrice = self.comatrice()
        for y in range(len(matrice.matrice)):
            for x in range(len(matrice.matrice[0])):
                matrice.matrice[x][y] *= (-1)**(x+y)
        return matrice
    
    def inverse(self):
        d = self.det()
        if d == 0:
            return False
        return self.adj()*(1/d)
    
print(Matrice([[0, 5, 6]]))
