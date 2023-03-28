import numpy as np


def calculate_Qout_convective(HTconv,area_cell,T1,T2):
    Qout=HTconv*area_cell*(T1-T2)
    return Qout

def calculate_Qout_conductive(THcond,area_cell,T1,T2,length_cell):
    Qout=THcond*area_cell*(T1-T2)/length_cell
    return Qout

def calculate_Qout_conductive_surface(output_surface):
    N_cells=np.size(output_surface.T_array)
    THcond=output_surface.THcond
    area=output_surface.area
    T1=output_surface.T_array[0:output_surface.N_cells-1]
    T2=output_surface.T_array[1:output_surface.N_cells]
    cell_length=output_surface.cell_length
    Qout=THcond*area*(T1-T2)/cell_length
    # does this account for radiant heat loss from the outer surface
    # Qout=HTconv*area*(T1-T2) + (5.67*10**-8)*0.9*area*(T1**4-T2**4)
    return Qout

#def calculate_Qout_radiative_surface(sigma_epsilon,area_cell,T1,T2):
#    Qout=sigma_epsilon*area_cell*(T1**4-T2**4)
#    return Qout

#this is defining the heat out of the radiator system into the room
#def calculate_Qout_watersystem(Qrating,T1,T2,Tdesign):
#    #ignore radiative heat and assume T2 = 20degC
#    Qout=Qrating(T1-20)/(Tdesign-20)
#    return Qout

#this is defining the energy needed to provide the heat to the water system
#def calculate_Energy_in(Qin_watersystem,heat_generator_efficiency):
#    #ignore radiative heat and assume T2 = zero, so ratio of heat to rated heat is just T1/Tdesign
#    Qout=Qrating(T1/Tdesign)
#    return Qout

#this is defining the thermal inertia of the radiator system
#def calculate_Tchange_watersystem(Qin,Qout,t_step,thermal_inertia):
#    DT=(Qin-Qout)*t_step/thermal_inertia
#    return DT

def calculate_Tchange(Qin,Qout,t_step,densityC,volume_cell):
    DT=(Qin-Qout)*t_step/(densityC*volume_cell)
    return DT

def calculate_Tchange_surface(output_surface,t_step,Qin):
    N_cells=np.size(output_surface.T_array)
    Qout=output_surface.Qout_array
    densityC=output_surface.densityC
    volume_cell=output_surface.volume_cell
    DT=(Qin-Qout)*t_step/(densityC*volume_cell)
    return DT

def do_surfaces_in_room(output_surface_array,T_room,t_step,T_exterior):
    Qout_room_total=0
    for output_surface in output_surface_array:
        #calculate Qout for room/surface boundary - CONVECTIVE
        Qout_room_to_surface=calculate_Qout_convective(output_surface.HTconv,output_surface.area,T_room,output_surface.T_array[0])
        #Qin_rad_to_surface=calculate_Qout_radiative(output_surface.HTconv,output_surface.area,T_room,output_surface.T_array[0])
        Qout_room_total=Qout_room_total+Qout_room_to_surface  
        #calculate Qout/Qin for interior of surface
        output_surface.Qout_array=calculate_Qout_conductive_surface(output_surface)
        Qin_xarray=np.append(Qout_room_to_surface+output_surface.Qrad,output_surface.Qout_array[0:output_surface.N_cells-2])
        #update surface interior temperatures
        output_surface.T_array=output_surface.T_array+np.append(calculate_Tchange_surface(output_surface,t_step,Qin_xarray),[0])
        output_surface.T_array[-1]=T_exterior

    return [Qout_room_total,output_surface_array]

def do_internals_in_room(internal,T_room,t_step,T_exterior):
    #treats internals as normal surface but no Qout on last (exterior cells Q out=0)
     #calculate Qout for room/surface boundary - CONVECTIVE
    Qout_room_to_internal=calculate_Qout_convective(internal.HTconv,internal.area,T_room,internal.T_array[0])
    internal.Qout_array=np.append(calculate_Qout_conductive_surface(internal),0)
    Qin_xarray=np.append(Qout_room_to_internal+internal.Qrad,internal.Qout_array[0:internal.N_cells-1])
        #update surface interior temperatures
    internal.T_array=internal.T_array+calculate_Tchange_surface(internal,t_step,Qin_xarray)
    return [Qout_room_to_internal,internal]

def do_hotspots_in_room(hotspot,t_step,T_exterior):
    #treat hotspot like composite surface except for extra fixed varibale 'airbyhotspot' which takes the place of T_room
    #calculate Qout for room/surface boundary, which then is subtracted from the Q in to the room 
    Qout_room_to_hotspot=calculate_Qout_convective(hotspot.HTconv,hotspot.area,hotspot.airbyhotspot,hotspot.T_array[0])
    hotspot.Qout_array=calculate_Qout_conductive_surface(hotspot)
    Qin_xarray=np.append(Qout_room_to_hotspot,hotspot.Qout_array[0:hotspot.N_cells-2])
    #update surface interior temperatures
    hotspot.T_array=hotspot.T_array+np.append(calculate_Tchange_surface(hotspot,t_step,Qin_xarray),[0])
    hotspot.T_array[-1]=T_exterior
    return Qout_room_to_hotspot

class hotspot_parameters:
    #class related to the input parameters on the DMD
    def __init__(self,THcond,HTconv,densityC,thickness,area,N_cells,initial_T,airbyhotspot):
        self.HTconv= HTconv
        self.area=area
        self.THcond = THcond  #can be array for multi material
        self.HTconv= HTconv
        self.densityC= densityC # array for multi material
        self.thickness =thickness #this is TOTAL THICKNESS
        self.area=area
        self.N_cells=N_cells
        self.initial_T=initial_T
        self.cell_length=self.thickness/self.N_cells
        self.volume_cell=self.cell_length*self.area
        self.T_array=np.full([self.N_cells ],self.initial_T )
        self.Qout_array=np.full([self.N_cells ],0 )
        self.airbyhotspot=airbyhotspot

class output_surface_parameters:
    #class related to the input parameters on the DMD
    def __init__(self,THcond,HTconv,densityC,thickness,area,N_cells,initial_T,radiant_heat):
        self.THcond = THcond  #can be array for multi material
        self.HTconv= HTconv
        self.densityC= densityC # array for multi material
        self.thickness =thickness #this is TOTAL THICKNESS
        self.area=area
        self.N_cells=N_cells
        self.initial_T=initial_T
        self.cell_length=self.thickness/self.N_cells
        self.volume_cell=self.cell_length*self.area
        self.T_array=np.full([self.N_cells ],self.initial_T )
        self.Qout_array=np.full([self.N_cells ],0 )
        self.Qrad_max=radiant_heat
        self.Qrad=self.Qrad_max
 #       self.sigma_epsilon=(5.67*10**-8)*0.9
     
    
class room_parameters:
    #class related to the input parameters on the DMD
    def __init__(self,T_room,Qin,volume,densityC,U,airchanges_per_hour,area):
        self.T_room=T_room
        self.Qin_max=Qin
        self.Qin=Qin
        self.volume=volume
        self.densityC=densityC
        self.U=U # this is for conductive heat to the lower level??
        self.airchanges_per_hour=airchanges_per_hour
        self.area=area
    
#class watersystem_parameters:
#    #class related to the input parameters on the DMD
#    def __init__(self,T_waterststem,Qin,volume,densityC,U,airchanges_per_hour,area):
#        self.T_watersystem=T_watersystem
#        self.Qin_max=Qin
#        self.Qin_watersystem=Qin_watersystem
#        self.thermal_inertia=thermal_inertia
#        self.Qrating=Qrating
#        self.Tdesign=Tdesign
#        self.heat_generator_efficiency=heat_generator_efficiency