class Matrice:
    """
    une classe permettant de représenter une matrice et d'effectuer des cacluls dessus.
    attributs:
        matrice: un tableau de nombres (liste de liste)
    méthodes spéciales:
        __repr__(): renvoie la représentation de la matrice
        __eq__(other): compare other à la matrice et renvoie vrai si elles sont identiques
        __ne__(other): inverse de __eq__
        __mul__(other), __rmul__(other): renvoie la multiplication de la matrice par une autre matrice ou un nombre sous forme d'un nouvel objet
        __imul__(other): affecte la multiplication entre other et la matrice
        __add__(other), __radd__(other): appelle _calc pour faire l'addition et renvoie son résultat
        __iadd__(other): affecte l'addition entre other et la matrice
        __sub__(other), __rsub__(other): appelle _calc pour faire la soustraction et renvoie son résultat
        __isub__(other): affecte la soustraction entre other et la matrice
        __pow__(other): renvoie la matrice puissance other
        __ipow__(other): affecte la puissance other de la matrice à la matrice
        __getitem__(key): récupère la valeur dans la matrice aux coordonnées du tuple key composé de x et y
        __setitem__(key, value): change la valeur aux coordonnées key par value
        __contains__(value): regarde si value est dans la matrice
        __len__(): renvoie le nombre d'éléments dans la matrice
        __hash__(): renvoie le hash de la matrice
    méthodes:
        adjacente(), adj(): renvoie la matrice adjacente de la matrice sous forme d'un nouvel objet
        comatrice(): renvoie la comatrice de la matrice sous forme d'un nouvel objet
        det(): renvoie le déterminant de la matrice si elle est carrée
        dimension(): renvoie les dimensions de la matrice sous forme de tuple
        inverse(), inv(): renvoie la matrice inverse si elle est inversible osus forme d'un nouvel objet
        transpose(): renvoie la matrice transposée de la matrice sous forme d'un nouvel objet
        l_empty(x, y): renvoie un tableau vide dimension de la matrice + x et y
    méthodes privées:
        _calc(other, op): renvoie l'addition ou la soustraction en fonction de op entre la matrice et other sous forme d'un nouvel objet
    """
    def __init__(self, tab: list):
        for l in tab:
            for el in l:
                if not isinstance(el, int) and not isinstance(el, float):
                    raise ValueError("The list does not only contain numbers.")
        self.matrice = tab
        self.adj = self.adjacente
        self.inv = self.inverse

    def __repr__(self):
        """
        Méthode spéciale pqui permet d'afficher la matrice.
        """
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
    
    def __eq__(self, other) -> bool:
        """
        Méthode spéciale permettant la comparaison entre la matrice et un élément.
        """
        return isinstance(other, Matrice) and self.matrice == other.matrice
    
    def __ne__(self, other) -> bool:
        """
        Méthode spéciale permettant la comparaison entre la matrice et un élément.
        """
        return not self.__eq__(other)

    def __mul__(self, other):
        """
        Méthode spéciale qui gère la multiplication entre la matrice et une autre matrice ou un nombre
        """
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
                raise ArithmeticError("dimensions not compatible")
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
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __imul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        """
        Méthode spécialer permettant d'additionner deux matrices ensemble.
        """
        return self._calc(other, "+")
    
    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self._calc(other, "-")

    def __rsub__(self, other):
        return self.__sub__(other)
    
    def __isub__(self, other):
        return self.__sub__(other)
    
    def __pow__(self, other):
        if not isinstance(other, int):
            raise ValueError("Value is not integer.")
        if other == 0:
            return self.identite()
        elif other > 0:
            m = self.copy()
            for _ in range(other-1):
                m *= self
            return m
        else:
            m1 = self.copy().inverse()
            m = m1.copy()
            for _ in range(abs(other) - 1):
                m *= m1
            return m
    
    def __rpow__(self, other):
        raise ArithmeticError("Invalid operation.")
        return

    def __ipow__(self, other):
        return self.__pow__(other)
    
    def __getitem__(self, key: tuple):
        if len(key) != 2 or not isinstance(key[0], int) or not isinstance(key[1], int):
            raise ValueError("Incorect key.")
        return self.matrice[key[1]][key[0]]
    
    def __setitem__(self, key: tuple, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise ValueError("Incorect value.")
        if len(key) != 2 or not isinstance(key[0], int) or not isinstance(key[1], int):
            raise ValueError("Incorect key.")
        self.matrice[key[1]][key[0]] = value
    
    def __contains__(self, other):
        if not isinstance(other, int) and not isinstance(other, float):
            return False
        for l in self.matrice:
            if other in l:
                return True
        return False
    
    def __len__(self):
        return len(self.matrice[0]) * len(self.matrice)
    
    def __hash__(self):
        return hash((tuple(l) for l in self.matrice))

    def adjacente(self):
        """
        Méthode permettant de renvoyer la matrice adjacente de la matrice.
        """
        matrice = self.comatrice()
        for y in range(len(matrice.matrice)):
            for x in range(len(matrice.matrice[0])):
                matrice.matrice[x][y] *= (-1)**(x+y)
        return matrice
    
    def comatrice(self):
        """
        Méthode renvoyant la comatrice de la matrice
        """
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
        
    def copy(self):
        return Matrice(self.matrice)

    def det(self) -> int:
        """
        Méthode permettant d'obtenir le déterminant de la matrice
        """
        if not len(self.matrice) == len(self.matrice[0]):
            raise ArithmeticError("non square matrix")
        if len(self.matrice) > 3:
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
        elif len(self.matrice) == len(self.matrice[0]) == 3: #sarrus
            p = [self.matrice[0][0] * self.matrice[1][1] * self.matrice[2][2], 
                 self.matrice[1][0] * self.matrice[2][1] * self.matrice[0][2],
                 self.matrice[2][0] * self.matrice[0][1] * self.matrice[1][2]
            ]
            n = [self.matrice[0][0] * self.matrice[1][2] * self.matrice[2][1], 
                 self.matrice[1][0] * self.matrice[0][1] * self.matrice[2][2],
                 self.matrice[2][0] * self.matrice[1][1] * self.matrice[0][2]
            ]
            return sum(p)-sum(n)
        elif len(self.matrice) == len(self.matrice[0]) == 1:
            return self.matrice[0][0]
        else:
            return self.matrice[0][0] * self.matrice[1][1] - self.matrice[0][1] * self.matrice[1][0]

    def dimension(self) -> tuple:
        """
        Méthode qui renvoie les dimensions de la matrice
        """
        return (len(self.matrice), len(self.matrice[0]))
    
    def dot(self, other):
        if not isinstance(other, Matrice):
            raise ValueError("Invalid parameter.")
        if self.dimension() != other.dimension() or 1 not in self.dimension():
            raise ArithmeticError("Invalid size")
        return self.transpose() * other
    
    def identite(self):
        """
        Méthode permettant de renvoyer une matrice identitée de même taille que la matrice
        """
        if not self.is_squared():
            raise ArithmeticError("Non squared matrix.")
        l = []
        for y in range(len(self.matrice)):
            l.append([])
            for x in range(len(self.matrice[0])):
                if x == y:
                    l[y].append(1)
                else:
                    l[y].append(0)
        return Matrice(l)
    
    def inverse(self):
        """
        Méthode permettant de renvoyer la matrice inverse de la Matrice
        """
        d = self.det()
        if d == 0:
            raise ArithmeticError("non-invertible matrix")
        return self.adj()*(1/d)
    
    def is_squared(self) -> bool:
        d = self.dimension()
        return d[0] == d[1]
        
    def l_empty(self, x: int = 0, y: int = 0) -> list:
        """
        Méthode renvoyant un tableau vide de mêmes dimensions que la matrice plus les dimensions données en paramètres.
        """
        x += len(self.matrice[0])
        y += len(self.matrice)
        return [[0]*x for _ in range(y)]
        
    def transpose(self):
        """
        Methode renvoyant la matrice transposée de la matrice
        """
        return Matrice(list(map(list, zip(*self.matrice))))

#    def 
    def _calc(self, other, op):
        """
        Méthode privée permetant d'additionner ou soustraire une matrice à une autre
        """
        if not isinstance(other, Matrice):
            raise ValueError("bad argument")
        d1 = self.dimension()
        d2 = other.dimension()
        if d1 != d2:
            raise ArithmeticError("dimensions not compatible")
        t2 = [[0 for _ in range(d1[1])] for _ in range(d1[0])]
        for i in range(len(self.matrice)):
            for i2 in range(len(self.matrice[i])):
                if op == "+":
                    t2[i][i2] = self.matrice[i][i2] + other.matrice[i][i2]
                else:
                    t2[i][i2] = self.matrice[i][i2] - other.matrice[i][i2]
        return Matrice(t2)
    