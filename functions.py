import numpy as np

def calculate_Qout_conductive(U,area_cell,T1,T2,length_cell):
    Qout=U*area_cell*(T1-T2)/length_cell
    return Qout

def calculate_Tchange(Qin,Qout,t_step,densityC,volume_cell):
    DT=(Qin-Qout)*t_step/(densityC*volume_cell)
    return DT

def calculate_Qout_convective(HTC,area_cell,T1,T2):
    Qout=HTC*area_cell*(T1-T2)
    return Qout

class output_surface_parameters:
    #class related to the input parameters on the DMD
    def __init__(self,U,HTC,densityC,thickness,area,N_cells,initial_T):
        self.U = U
        self.HTC= HTC
        self.densityC= densityC
        self.thickness =thickness
        self.area=area
        self.N_cells=N_cells
        self.initial_T=initial_T
        self.cell_length=self.thickness/self.N_cells
        self.volume_cell=self.thickness*self.area
        self.T_array=np.full([self.N_cells ],self.initial_T )