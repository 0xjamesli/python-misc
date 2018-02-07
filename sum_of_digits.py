'''
Calculates the sum of digits in a given number.
For example, "123" would give 6
'''

import math
def digitSum(n):
 sum = 0
 while (n > 0):
  sum+= n%10
  n = math.floor(n/10)
 return sum

if __name__ == "__main__":
 print(digitSum(123))
