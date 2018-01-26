'''
Given the lengths for each side on a triangle, find all three angles of the triangle
https://py.checkio.org/mission/triangle-angles/
'''
import math

#solution 1
def checkio(a, b, c):
    try:
        a2, b2 = [round(math.degrees(math.acos((x**2 + c**2 - y**2) / (2*x*c)))) for (x,y) in [(b,a),(a,b)]]
        if a2 == 0: raise ValueError
        c2 = 180-a2-b2
        return sorted([a2,b2,c2])
    except ValueError:
        return [0]*3

#solution 2
# return sorted([round(math.degrees(math.acos((y**2+z**2-x**2)/(2*y*z)))) if all([x+y>z,y+z>x,z+x>y]) else 0 for (x,y,z) in [(a,b,c),(b,c,a),(c,a,b)]])

if __name__ == '__main__':
    assert checkio(4, 4, 4) == [60, 60, 60], "All sides are equal"
    assert checkio(3, 4, 5) == [37, 53, 90], "Egyptian triangle"
    assert checkio(2, 2, 5) == [0, 0, 0], "It's can not be a triangle"
    assert checkio(10, 20, 30) == [0, 0, 0], "It's can not be a triangle"