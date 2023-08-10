from matrice import Matrice
import timeit

m=Matrice([[1, 2, 3], [0, 1, 4], [5, 6, 0]])
print(m.transpose().comatrice()*(1/m.det()))
print(m.inverse())