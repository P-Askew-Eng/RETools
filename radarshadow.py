#Simple line of site tool with no terrain
#outputs:
#   distance between two objects given latitude and longitude
#   whether it is likely to be line of sight
#   shadow height
#   shadow width 

#Work out shadow dimensions
from math import *

#Define procedures
def Earthradius(latitude):
    a = 6378137.0
    b = 6359752.3
    latrad = radians(latitude)
    ans = sqrt(((a*a*cos(latrad))**2+(b*b*sin(latrad))**2)/((a*cos(latrad))**2+(b*sin(latrad))**2))
    return ans
    
def haversine(lat1,lon1,lat2,lon2):
    phi1=radians(lat1)
    phi2=radians(lat2)
    delta_phi=radians(lat2-lat1)
    delta_lam=radians(lon2-lon1)
    a=(sin(delta_phi/2)**2)+(cos(phi1)*cos(phi2)*(sin(delta_lam)**2))
    return a
    
# Get inputs nb decimal degrees and no error trapping
rad_lat=float(raw_input('Enter radar latitude: '))
rad_lon=float(raw_input('Enter radar longitude: '))
radar_height=float(raw_input('Enter radar height (m): '))
radar_freq=float(raw_input('Enter radar frequency (GHz): '))
radar_rng=float(raw_input('Enter radar range (m): '))
turb_lat=float(raw_input('Enter turbine latitude: '))
turb_lon=float(raw_input('Enter turbine longitude: '))
turbine_height=float(raw_input('Enter turbine height (m): '))

#Calculations
radius_radar=Earthradius(rad_lat)#calculate earth radius at radar location
radar_wl=300000000/(radar_freq*1000000000)#calculate wavelength of radar

#distance between two positions using haversine function
a=haversine(rad_lat,rad_lon,turb_lat,turb_lon)
c=2*atan2(sqrt(a),sqrt(1-a))
rw_dist=6372.8*c # use this rather than 6371 km or local radius for average earth radius
print('Distance to turbine is '),rw_dist,' kilometres'


#calculate line of sights
radius_turbine=Earthradius(turb_lat)
t_los=sqrt(turbine_height*(2*4/3*radius_turbine+turbine_height))#ie turbine to radio horizon
r_los=sqrt(radar_height*(2*4/3*radius_radar+radar_height)) # ie radar to radio horizon
tot_los=t_los+r_los #ie the maximum distance at whch the two sites can communicate
print('Line of Sight distance between radar and turbine is '),tot_los/1000,' kilometres'
radar_sep=4/3*radius_radar*c # find radar distance between the two sites
print('Radio range between radar and turbine is '),radar_sep/1000,' kilometres'
if radar_sep<=tot_los:
    los=1
    print ('Probably line of sight')
else:
    los=0
    print ('Probably not line of sight')


#Calculate shadow parameters
length_S=0
if los == 1:
    print('Distance    Height    Width')
while length_S+(rw_dist*1000)<=radar_rng:
    if los == 0:
        print('No shadow calculations performed as no line of sight')
        break
    height_S=(((((4/3*radius_radar)+radar_height))*(sin((acos((((((4/3*radius_radar)+radar_height))**2)-((((4/3*radius_radar)+turbine_height))**2)+((sqrt(((((4/3*radius_radar)+radar_height))**2)+((((4/3*radius_radar)+turbine_height))**2)-(2*(((4/3*radius_radar)+radar_height))*(((4/3*radius_radar)+turbine_height))*cos((radar_sep/(4/3*radius_radar))))))**2))/(2*(((4/3*radius_radar)+radar_height))*(sqrt(((((4/3*radius_radar)+radar_height))**2)+((((4/3*radius_radar)+turbine_height))**2)-(2*(((4/3*radius_radar)+radar_height))*(((4/3*radius_radar)+turbine_height))*cos((radar_sep/(4/3*radius_radar)))))))))))/(sin((pi-(acos((((((4/3*radius_radar)+radar_height))**2)-((((4/3*radius_radar)+turbine_height))**2)+((sqrt(((((4/3*radius_radar)+radar_height))**2)+((((4/3*radius_radar)+turbine_height))**2)-(2*(((4/3*radius_radar)+radar_height))*(((4/3*radius_radar)+turbine_height))*cos((radar_sep/(4/3*radius_radar))))))**2))/(2*(((4/3*radius_radar)+radar_height))*(sqrt(((((4/3*radius_radar)+radar_height))**2)+((((4/3*radius_radar)+turbine_height))**2)-(2*(((4/3*radius_radar)+radar_height))*(((4/3*radius_radar)+turbine_height))*cos((radar_sep/(4/3*radius_radar)))))))))-((radar_sep+length_S)/(4/3*radius_radar))))))-(4/3*radius_radar))
    width_S=sqrt((((radar_wl/2)+length_S)**2)-(length_S**2))#half width
    print length_S,height_S,2*width_S
    length_S=length_S+500
