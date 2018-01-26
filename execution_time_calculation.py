# method 1: using time()
from time import time
def factorial(n):
    num = 1
    while n >= 1:
        num = num * n
        n = n - 1
    return num

t0 = time()
factorial(10**5)
print('Elapsed time :', time() - t0)


# method 2: using timeit()
import timeit
def factorial(n):
    num = 1
    while n >= 1:
        num = num * n
        n = n - 1
    return num

t0 = timeit.default_timer()
factorial(10**5)
print('Elapsed time :', timeit.default_timer() - t0)


#method 3: using cprofile()
import cProfile
def factorial(n):
    num = 1
    while n >= 1:
        num = num * n
        n = n - 1
    return num

cProfile.run('factorial(10**5)')

#method 4: simple method
import time
start = time.clock() 
s = 'geeks'
U = []
for c in s:
    U.append(c.upper())
print U
elapsed = time.clock()
e1 = elapsed - start
print "Time spent in function is: ", e1
