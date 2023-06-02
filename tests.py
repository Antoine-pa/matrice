from matrice import Matrice
import timeit

m = Matrice([[1, 1, 2], [3, 4, 5], [6, 7, 8]])
m2=Matrice([[0, 1, 2], [3, 4, 5], [6, 7, 8]])

print(m)
print(m.comatrice())
print(m.comatrice2())

print(timeit.timeit("m.comatrice()", "from __main__ import m", number=10000))