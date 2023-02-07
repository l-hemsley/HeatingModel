####this is a nightmare and needs lots of tidying! Put in loops please


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
    #input params to surface class
    surface=output_surface_parameters(THcond[0:N_cells-1],material.loc[:,'HTCconv'].to_numpy(),densityC[0:N_cells-1],thickness,surface_data.iloc[1,1],N_cells,room.T_room,surface_data.iloc[6,1])
    return surface

def WindowsSurface(surface_data,materials_data,room):
    #single glazing
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]
    N_cells=20 #not sure about this??
    thickness=surface_data.iloc[5,1]
    window=output_surface_parameters(material.loc[:,'Thermal conductivity'].to_numpy(),material.loc[:,'HTCconv'].to_numpy(), material.loc[:,'DensityC'].to_numpy(),thickness,surface_data.iloc[1,1],N_cells,room.T_room,surface_data.iloc[4,1])
    return window

def ReadInParameters(filename):
    data = pd.read_excel(filename, sheet_name='Input')
    materials_data= pd.read_excel(filename, sheet_name='Materials')

#//////////// upper room /////////////////////
    #T_room,Qin,volume,densityC,U,airchanges_per_hour):
    upper_data=data.iloc[:13,:6]
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

    output_surface_array_upper=[roof_upper,wall_upper,windows_upper]

#//////////// middle room /////////////////////
    middle_data=data.iloc[18:32,:6]
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

    output_surface_array_middle=[roof_middle,wall_middle,windows_middle]

#//////////// lower room /////////////////////
    lower_data=data.iloc[36:51,:6]
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
    
# target temp settings
    temperature_data=data.iloc[:4,7:10]
    T_target=temperature_data.iloc[1,1]
    T_exterior=temperature_data.iloc[0,1]
    target_level=temperature_data.iloc[2,1]

    
    return [lower,middle,upper,output_surface_array_lower,output_surface_array_middle,output_surface_array_upper,T_target,T_exterior,target_level]