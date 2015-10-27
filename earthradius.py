def Earthradius(latitude):
    from math import sin, cos, radians, sqrt
    a = 6378137.0
    b = 6359752.3
    latrad = radians(latitude)
    ans = sqrt(((a*a*cos(latrad))**2+(b*b*sin(latrad))**2)/((a*cos(latrad))**2+(b*sin(latrad))**2))
    return ans
    
x = raw_input('enter latitude in decimal degrees: ')
x = float(x)
radius = Earthradius(x)
print "Radius of earth at ", x, "degrees is ", radius, "metres"
