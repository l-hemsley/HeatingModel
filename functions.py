import numpy as np


def calculate_Qout_convective(HTC,area_cell,T1,T2):
    Qout=HTC*area_cell*(T1-T2)
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
    return Qout

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

def do_surfaces_in_room(output_surface_array,T_room,t_step):
    Qout_room_total=0
    for output_surface in output_surface_array:
        #calculate Qout for room/surface boundary - CONVECTIVE
        Qout_room_to_surface=calculate_Qout_convective(output_surface.HTC,output_surface.area,T_room,output_surface.T_array[0])
        #Qin_rad_to_surface=calculate_Qout_radiative(output_surface.HTC,output_surface.area,T_room,output_surface.T_array[0])
        Qout_room_total=Qout_room_total+Qout_room_to_surface  
        #calculate Qout/Qin for interior of surface
        output_surface.Qout_array=calculate_Qout_conductive_surface(output_surface)
        Qin_xarray=np.append(Qout_room_to_surface,output_surface.Qout_array[0:output_surface.N_cells-2])
        #update surface interior temperatures
        output_surface.T_array=output_surface.T_array+np.append(calculate_Tchange_surface(output_surface,t_step,Qin_xarray),[0])

    return [Qout_room_total,output_surface_array]

class output_surface_parameters:
    #class related to the input parameters on the DMD
    def __init__(self,THcond,HTC,densityC,thickness,area,N_cells,initial_T):
        self.THcond = THcond
        self.HTC= HTC
        self.densityC= densityC
        self.thickness =thickness
        self.area=area
        self.N_cells=N_cells
        self.initial_T=initial_T
        self.cell_length=self.thickness/self.N_cells
        self.volume_cell=self.cell_length*self.area
        self.T_array=np.full([self.N_cells ],self.initial_T )
        self.Qout_array=np.full([self.N_cells ],0 )
     
    
