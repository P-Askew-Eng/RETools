# latitude and longitude to OSGB
# derived from Annex C of 'A guide to coordinate systems in Great Britain' v2.3 Ordnance Survey
#get input and covert to radians
from math import * #radians,sin,cos,tan,sqrt
lat=float(raw_input('Enter latitude [ decimal degrees] '))
lon=float(raw_input('Enter Longitude [decimal degrees] '))
phi =radians(lat)
lmbda=radians(lon)
#define constants - Appendix A

#airy 1830 ellipsoid constants
a=float(6377563.396)
b=float(6356256.909)
e_squared=float(((a**2)-(b**2))/(a**2))
print ('e squared '), e_squared
#National Grid constants
F0=float(0.9996012717)
phi0=float(radians(49))
lambda0=float(radians(-2))
E0=float(400000)
N0=float(-100000)

#start computations equations C1 to C5
n=(a-b)/(a+b)
#print ('n '),n
v=a*F0/(sqrt(1-(e_squared*(sin(phi)**2))))#discrepancy between OS guide and Os spreadsheet used spreadsheet formula here
#print ('nu '),v
rho=a*F0*(1-e_squared)*((1-(e_squared*sin(phi)*sin(phi)))**(-1.5))
#print ('rho '), rho
eta_2=float((v/rho)-1)
#print ('eta squared '),eta_2
M=b*F0*(
((1+n+((5/4)*(n**2))+((5/4)*(n**3)))*(phi-phi0))
-(((3*n)+(3*(n**2))+((21/8)*(n**3)))*(sin(phi-phi0))*(cos(phi+phi0)))
+((((15/8)*(n**2))+((15/8)*(n**3)))*(sin(2*(phi-phi0)))*(cos(2*(phi+phi0))))
-(((35/24)*(n**3))*(sin(3*(phi-phi0)))*(cos(3*(phi+phi0))))
) # this seems to deviate from the OS example leading to an error of 1.8 metres in Northing - can't trace it yet so is it rounding?
print ('M '), M
I=M+N0
#print ('I '),I
II=(v/2)*(sin(phi))*(cos(phi))
#print ('II '),II
III=(v/24)*sin(phi)*((cos(phi))**3)*(5-((tan(phi))**2)+(9*eta_2))
#print ('III '),III
IIIA=(v/720)*sin(phi)*((cos(phi))**5)*(61-(58*(tan(phi))**2)+((tan(phi))**4))
#print ('IIIA '),IIIA
IV=v*cos(phi)
#print ('IV '),IV
V=(v/6)*(cos(phi))**3*((v/rho)-((tan(phi))**2))
#print ('V '),V
VI=(v/120)*((cos(phi))**5)*(5-(18*((tan(phi))**2))+((tan(phi))**4)+(14*eta_2)-(58*((tan(phi))**2)*eta_2))
#print ('VI '),VI
N=I+II*((lmbda-lambda0)**2)+III*((lmbda-lambda0)**4)+IIIA*((lmbda-lambda0)**6)
E=E0+IV*(lmbda-lambda0)+V*((lmbda-lambda0)**3)+VI*((lmbda-lambda0)**5)
# phew! time to output
print ('easting'),E
print ('northing'),N
