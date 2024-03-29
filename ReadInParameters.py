#### BIT CLUNKY STILL :/ need more loops and not to repeat stuff e.g. always reusing room T

import pandas as pd
import numpy as np
from functions import *

cell_length=0.5 #cm from spreadsheet 

def  CompositeMaterialSurface(surface_data, materials_data,room):
    #internal section
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]
    N_cells_internal=int(surface_data.iloc[3,1]/cell_length)
    THcond_internal=np.full((1, N_cells_internal), material.loc[:,'Thermal conductivity'].to_numpy())
    densityC_internal=np.full((1, N_cells_internal), material.loc[:,'DensityC'].to_numpy())
    HTC_internal=material.loc[:,'HTCconv'].to_numpy()
    #external section
    external_type=surface_data.iloc[4,1]
    material=materials_data.loc[materials_data['Material'] == external_type]
    N_cells_external=int(surface_data.iloc[5,1]/cell_length)
    THcond_external=np.full((1, N_cells_external), material.loc[:,'Thermal conductivity'].to_numpy())
    densityC_external=np.full((1,N_cells_external), material.loc[:,'DensityC'].to_numpy())
    #append arrays
    THcond=np.append(THcond_internal,THcond_external)
    densityC=np.append(densityC_internal,densityC_external)
    N_cells=1+N_cells_internal+N_cells_external
    #N_cells is +1 to account for the last cell being set to zero and cell data being at the inward side of the cell
    thickness=(surface_data.iloc[3,1]+surface_data.iloc[5,1])/100 #total thickness convert to m
    surface=output_surface_parameters(THcond[0:N_cells-1],HTC_internal,densityC[0:N_cells-1],thickness,surface_data.iloc[1,1],N_cells,room.T_room,surface_data.iloc[6,1])
    return surface

def Internals(surface_data, materials_data,room): #we can treat internals as just normal surface class
    #internal section
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]
    N_cells=int(surface_data.iloc[3,1]/cell_length)
    THcond=material.loc[:,'Thermal conductivity'].to_numpy()
    densityC=material.loc[:,'DensityC'].to_numpy()
    thickness=(surface_data.iloc[3,1])/100 #total thickness convert to m
    internal=output_surface_parameters(THcond,material.loc[:,'HTCconv'].to_numpy(),densityC,thickness,surface_data.iloc[1,1],N_cells,room.T_room,surface_data.iloc[4,1])
    return internal

def HotSpot(surface_data,materials_data,room):
    #internal section
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]
    N_cells_internal=int(surface_data.iloc[3,1]/cell_length)
    THcond_internal=np.full((1, N_cells_internal), material.loc[:,'Thermal conductivity'].to_numpy())
    densityC_internal=np.full((1, N_cells_internal), material.loc[:,'DensityC'].to_numpy())
    #external section
    external_type=surface_data.iloc[4,1]
    material=materials_data.loc[materials_data['Material'] == external_type]
    N_cells_external=int(surface_data.iloc[5,1]/cell_length)
    THcond_external=np.full((1, N_cells_external), material.loc[:,'Thermal conductivity'].to_numpy())
    densityC_external=np.full((1,N_cells_external), material.loc[:,'DensityC'].to_numpy())
    #append arrays
    THcond=np.append(THcond_internal,THcond_external)
    densityC=np.append(densityC_internal,densityC_external)
    N_cells=N_cells_internal+N_cells_external
    thickness=(surface_data.iloc[3,1]+surface_data.iloc[5,1])/100 #total thickness convert to m
    hotspot=hotspot_parameters(THcond[0:N_cells-1],material.loc[:,'HTCconv'].to_numpy(),densityC[0:N_cells-1],thickness,surface_data.iloc[1,1],N_cells,room.T_room,surface_data.iloc[6,1])
    return hotspot

def WindowsSurface(surface_data,materials_data,room):
    #SOMETHING WIERD WITH WINDOWS
    #single glazing
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]
    thickness=surface_data.iloc[5,1]/100
    N_cells=int(100*thickness/cell_length)
    #print(N_cells)
    window=output_surface_parameters(material.loc[:,'Thermal conductivity'].to_numpy(),material.loc[:,'HTCconv'].to_numpy(), material.loc[:,'DensityC'].to_numpy(),thickness,surface_data.iloc[1,1],N_cells,room.T_room,surface_data.iloc[4,1])
    return window

def ReadInParameters(filename):
    data = pd.read_excel(filename, sheet_name='Input')
    materials_data= pd.read_excel(filename, sheet_name='Materials')

#//////////// upper room /////////////////////
    #T_room,Qin,volume,densityC,U,airchanges_per_hour):
    upper_data=data.iloc[:7,:6]
    upper_data_parameters_room=upper_data.iloc[:7,1:2].to_numpy()
    upper=room_parameters(*upper_data_parameters_room)
    # do composite surfaces
    surface_data=data.iloc[7:14,:2]
    roof_upper=CompositeMaterialSurface(surface_data, materials_data,upper)
    surface_data=data.iloc[7:14,2:4]
    wall_upper=CompositeMaterialSurface(surface_data, materials_data,upper)
    ## Windows
    surface_data=data.iloc[7:14,4:6]
    windows_upper=WindowsSurface(surface_data,materials_data,upper)
        #HOTSPOT
    surface_data=data.iloc[0:7,4:6]
    hotspot_upper=HotSpot(surface_data,materials_data,upper)
    #internals
    surface_data=data.iloc[0:7,2:4]
    internals_upper=Internals(surface_data,materials_data,upper)

    output_surface_array_upper=[roof_upper,wall_upper,windows_upper]

#//////////// middle room /////////////////////
    middle_data=data.iloc[18:25,:6]
    middle_data_parameters_room=middle_data.iloc[:7,1:2].to_numpy()
    middle=room_parameters(*middle_data_parameters_room)
# do composite surfaces
    surface_data=data.iloc[25:32,:2]
    roof_middle=CompositeMaterialSurface(surface_data, materials_data,middle)
    surface_data=data.iloc[25:32,2:4]
    wall_middle=CompositeMaterialSurface(surface_data, materials_data,middle)
    ## windows
    surface_data=data.iloc[25:32,4:6]
    windows_middle=WindowsSurface(surface_data,materials_data,middle)
    #HOTSPOT
    surface_data=data.iloc[18:32,4:6]
    hotspot_middle=HotSpot(surface_data,materials_data,middle)
    #internals
    surface_data=data.iloc[18:25,2:4]
    internals_middle=Internals(surface_data,materials_data,middle)

    output_surface_array_middle=[roof_middle,wall_middle,windows_middle]

#//////////// lower room /////////////////////
    lower_data=data.iloc[36:43,:6]
    lower_data_parameters_room=lower_data.iloc[:7,1:2].to_numpy()
    lower=room_parameters(*lower_data_parameters_room)
#do composite surfaces
    surface_data=data.iloc[43:50,:2]
    roof_lower=CompositeMaterialSurface(surface_data, materials_data,lower)
    surface_data=data.iloc[43:50,2:4]
    wall_lower=CompositeMaterialSurface(surface_data, materials_data,lower)
    surface_data=data.iloc[43:50,4:6]
    floor=CompositeMaterialSurface(surface_data, materials_data,lower)
    ## windows
    surface_data=data.iloc[43:49,6:8]
    windows_lower=WindowsSurface(surface_data,materials_data,lower)
    output_surface_array_lower=[roof_lower,wall_lower,floor,windows_lower]
    #HOTSPOT
    surface_data=data.iloc[36:43,4:6]
    hotspot_lower=HotSpot(surface_data,materials_data,lower)
    #internals
    surface_data=data.iloc[36:43,2:4]
    internals_lower=Internals(surface_data,materials_data,lower)
    
# target temp settings
    temperature_data=data.iloc[:4,7:10]
    T_target=temperature_data.iloc[1,1]
    T_exterior=temperature_data.iloc[0,1]
    
    hotspots=[hotspot_upper,hotspot_middle,hotspot_lower]
    internals=[internals_upper,internals_middle,internals_lower]
    rooms=[upper,middle,lower]
    output_surfaces=[output_surface_array_upper,output_surface_array_middle,output_surface_array_lower]
    
    return [rooms,output_surfaces,T_target,T_exterior,hotspots,internals]