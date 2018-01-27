'''
TODO:
Make this a web-based quiz games
'''

# Q-1
# What is the output of this code?
def fact(x):
  if x == 1:
    return 1
  else:
    return x*fact(x-1)
print(fact(3))
# 6


# Q-2
# What is the output of this code?
def fb(n):
  if n == 0:
    return 0
  if n == 1:
    return 1
  else:
    return(fb(n-1) + fb(n-2))
print(fb(5))
# 5
