class Matrice:
    def __init__(self, t):
        self.matrice = t

    def __str__(self):
        ret = ""
        matrice_str = []
        for line in self.matrice:
            matrice_str.append(list(map(str, line)))

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

    def dimension(self):
        return (len(self.matrice), len(self.matrice[0]))

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            t2 = [[] for _ in range(len(self.matrice))]
            for i in range(len(self.matrice)):
                for el in self.matrice[i]:
                    t2[i].append(el*other)
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

    def det(self):
        assert len(self.matrice) == len(self.matrice[1])
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
            return s
        else:
            return self.matrice[0][0] * self.matrice[1][1] - self.matrice[0][1] * self.matrice[1][0]
        
    def l_empty(self, x = None, y = None):
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
        self.matrice = l
        return self
    
    def adj(self):
        l = self.l_empty()
        for y in range(len(self.matrice)):
            for x in range(len(self.matrice[0])):
                l_mineure = self.l_empty(-1, -1)
                for line in range(len(self.matrice)):
                    for el in range(len(self.matrice[0])):
                        if line != y and el != x:
                            if line < y:
                                if el < x:
                                    l_mineure[line][el] = self.matrice[line][el]
                                else:
                                    l_mineure[line][el-1] = self.matrice[line][el]
                            else:
                                if el < x:
                                    l_mineure[line+1][el] = self.matrice[line][el]
                                else:
                                    l_mineure[line+1][el-1] = self.matrice[line][el]
                    
                print(l_mineure)

m = Matrice([[1, 2, 3], [3, 4, 5]])
m2 = Matrice([[5, 6], [7, 8], [1, 2]])
"""
print(m)
print(m2)
print(m*m2)
print(m2*m)
"""
m3 = Matrice([[1, 2, 3], [0, 1, 4], [5, 6, 0]])
print(m3.transpose())
print(m3.adj())
