from matrice import Matrice

m = Matrice([[1, 1, 2], [3, 4, 5], [6, 7, 8]])
m2=Matrice([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
print(m.det())
m[(0, 0)] = 2
print(m.det())