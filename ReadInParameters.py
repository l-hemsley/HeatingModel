####this is a nightmare and needs lots of tidying!


import pandas as pd
import numpy as np
from functions import *

def  CompositeMaterials(surface_data,material):
    N_cells_internal=int(surface_data.iloc[3,1]/0.5)
    THcond_internal=np.full((1, N_cells_internal), material.loc[:,'Thermal conductivity'].to_numpy())
    densityC_internal=np.full((1, N_cells_internal), material.loc[:,'DensityC'].to_numpy())

    N_cells_external=int(surface_data.iloc[5,1]/0.5)
    THcond_external=np.full((1, N_cells_external), material.loc[:,'Thermal conductivity'].to_numpy())
    densityC_external=np.full((1,N_cells_external), material.loc[:,'DensityC'].to_numpy())
    THcond=np.append(THcond_internal,THcond_external)
    densityC=np.append(densityC_internal,densityC_external)
    N_cells=N_cells_internal+N_cells_external
    thickness=(surface_data.iloc[3,1]+surface_data.iloc[5,1])/100 #convert to m
    return  THcond[0:N_cells-1],densityC[0:N_cells-1],N_cells, thickness

def ReadInParameters(filename):
    data = pd.read_excel(filename, sheet_name='Input')
    materials_data= pd.read_excel(filename, sheet_name='Materials')

    #//////////// middle room /////////////////////
    #T_room,Qin,volume,densityC,U,airchanges_per_hour):
    upper_data=data.iloc[:13,:6]
    #upper room
    upper_data_parameters_room=upper_data.iloc[:7,1:2].to_numpy()
    upper=room_parameters(*upper_data_parameters_room)

    surface_data=data.iloc[7:13,:2]
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]

    [THcond,densityC,N_cells,thickness]=CompositeMaterials(surface_data,material)
    roof_upper=output_surface_parameters(THcond,material.loc[:,'HTCconv'].to_numpy(),densityC,thickness,surface_data.iloc[1,1],N_cells,upper_data_parameters_room[0])
    ##
    surface_data=data.iloc[7:13,2:4]
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]

    [THcond,densityC,N_cells,thickness]=CompositeMaterials(surface_data,material)
    wall_upper=output_surface_parameters(THcond,material.loc[:,'HTCconv'].to_numpy(),densityC,thickness,surface_data.iloc[1,1],N_cells,upper_data_parameters_room[0])


    ## Windows
    surface_data=data.iloc[7:13,4:6]
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]

    N_cells_internal=1
    THcond=np.full((1, N_cells_internal), material.loc[:,'Thermal conductivity'].to_numpy())
    densityC=np.full((1, N_cells_internal), material.loc[:,'DensityC'].to_numpy())
    thickness=0.01 #1cm for windows
    windows_upper=output_surface_parameters(THcond,material.loc[:,'HTCconv'].to_numpy(),densityC,thickness,surface_data.iloc[1,1],N_cells_internal,upper_data_parameters_room[0])

    output_surface_array_upper=[roof_upper,wall_upper,windows_upper]

#//////////// middle room /////////////////////
    middle_data=data.iloc[18:32,:6]
    middle_data_parameters_room=middle_data.iloc[:7,1:2].to_numpy()
    middle=room_parameters(*middle_data_parameters_room)

    surface_data=data.iloc[25:31,:2]
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]

    [THcond,densityC,N_cells,thickness]=CompositeMaterials(surface_data,material)
    roof_middle=output_surface_parameters(THcond,material.loc[:,'HTCconv'].to_numpy(),densityC,thickness,surface_data.iloc[1,1],N_cells,upper_data_parameters_room[0])

    ##
    surface_data=data.iloc[25:31,2:4]
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]

    [THcond,densityC,N_cells,thickness]=CompositeMaterials(surface_data,material)
    wall_middle=output_surface_parameters(THcond,material.loc[:,'HTCconv'].to_numpy(),densityC,thickness,surface_data.iloc[1,1],N_cells,upper_data_parameters_room[0])

    ## windows
    surface_data=data.iloc[25:31,4:6]
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]

    N_cells_internal=1
    THcond=np.full((1, N_cells_internal), material.loc[:,'Thermal conductivity'].to_numpy())
    densityC=np.full((1, N_cells_internal), material.loc[:,'DensityC'].to_numpy())
    thickness=0.01
    windows_middle=output_surface_parameters(THcond,material.loc[:,'HTCconv'].to_numpy(),densityC,thickness,surface_data.iloc[1,1],N_cells_internal,middle_data_parameters_room[0])

    output_surface_array_middle=[roof_middle,wall_middle,windows_middle]

    #T_room,Qin,volume,densityC,U,airchanges_per_hour):
    #//////////// lower room /////////////////////
    lower_data=data.iloc[36:51,:6]

    lower_data_parameters_room=lower_data.iloc[:7,1:2].to_numpy()
    lower=room_parameters(*lower_data_parameters_room)

    surface_data=data.iloc[43:49,:2]
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]

    [THcond,densityC,N_cells,thickness]=CompositeMaterials(surface_data,material)
    roof_lower=output_surface_parameters(THcond,material.loc[:,'HTCconv'].to_numpy(),densityC,thickness,surface_data.iloc[1,1],N_cells,upper_data_parameters_room[0])
    
    surface_data=data.iloc[43:49,2:4]
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]

    [THcond,densityC,N_cells,thickness]=CompositeMaterials(surface_data,material)
    wall_lower=output_surface_parameters(THcond,material.loc[:,'HTCconv'].to_numpy(),densityC,thickness,surface_data.iloc[1,1],N_cells,upper_data_parameters_room[0])

    ##
    surface_data=data.iloc[43:49,4:6]
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]

    [THcond,densityC,N_cells,thickness]=CompositeMaterials(surface_data,material)

    floor=output_surface_parameters(THcond,material.loc[:,'HTCconv'].to_numpy(),densityC,thickness,surface_data.iloc[1,1],N_cells,upper_data_parameters_room[0])

    ## windows
    surface_data=data.iloc[43:49,6:8]
    internal_type=surface_data.iloc[2,1]
    material=materials_data.loc[materials_data['Material'] == internal_type]

    N_cells_internal=1
    THcond=np.full((1, N_cells_internal), material.loc[:,'Thermal conductivity'].to_numpy())
    densityC=np.full((1, N_cells_internal), material.loc[:,'DensityC'].to_numpy())
    thickness=0.01
    windows_lower=output_surface_parameters(THcond,material.loc[:,'HTCconv'].to_numpy(),densityC,thickness,surface_data.iloc[1,1],N_cells_internal,upper_data_parameters_room[0])

    output_surface_array_lower=[roof_lower,wall_lower,floor,windows_lower]

    temperature_data=data.iloc[:4,7:10]
    T_target=temperature_data.iloc[1,1]
    T_exterior=temperature_data.iloc[0,1]
    target_level=temperature_data.iloc[2,1]

    
    return [lower,middle,upper,output_surface_array_lower,output_surface_array_middle,output_surface_array_upper,T_target,T_exterior,target_level]