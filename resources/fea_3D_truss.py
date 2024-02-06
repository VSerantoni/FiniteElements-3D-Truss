import numpy as np
import matplotlib.pyplot as plt

from . import utils as ut
from . import utils_plot as up

class FeaTruss3D():
    
    def __init__(self, NodesCoorPath: str, ElementsConnectPath: str, show: bool = False) -> None:
        """Finite Element Analysis -> init

        Args:
            NodesCoorPath (str): path towards nodes coordinates
            ElementsConnectPath (str): path towards elements connections
            show (bool, optional): plot the init truss
        """
        # input parameters
        self.nodes_path = NodesCoorPath
        self.elements_path = ElementsConnectPath
        
        # load all
        self.nodes_coor = ut.load_nodes_coor(self.nodes_path)
        self.elements_connect = ut.load_elements_connect(self.elements_path)
        
        self.nbNodes = self.nodes_coor.shape[0]
        self.nbElements = self.elements_connect.shape[0]
        self.nb_dof = 3*self.nbNodes
        
        if show:
            _ = up.show_truss_init_3D(self.nodes_coor, self.elements_connect)
            plt.show()
    
    def set_BC(self, restrictedDof_path: str, allLoads_path: str, show_BC: bool = True):
        """set parameters for the boundary conditions

        Args:
            restrictedDof_path (str): path towards the bool list of all restricted degree of freedom
            allLoads_path (str): path towards the list of all projected for each node
            show_BC (bool, optional): plot the init truss with restricted dof and imposed load. Defaults to True.
        """
        # list of index DoF restricted to 0
        self.restricted_dof = ut.load_restricted_dof(restrictedDof_path)
        
        # list of loads for each DoF
        self.loads_on_dof, self.loads_vector = ut.load_loads(allLoads_path, self.nb_dof)
        
        if show_BC:
            ax = up.show_truss_init_3D(self.nodes_coor, self.elements_connect)
            _ = up.show_add_BC(ax, self.restricted_dof, self.nodes_coor, self.loads_vector)
            plt.show()
        
    def eval_stiffness(self, Young: float, CrossSectionPath: str) -> None:
        """evaluate the global stiffness matrix

        Args:
            Young (float): the Young's modulus
            CrossSectionPath (str): path towards elements sections
        """
        self.young = Young
        self.cross_sections = ut.load_cross_section(CrossSectionPath)
        
        # get the stiffness matrix
        self.Kg = np.zeros([self.nb_dof, self.nb_dof])    

        # loop on each element
        for index, nodes_connected in enumerate(self.elements_connect):
            area = self.cross_sections[index]
            lx, ly, lz, Le = ut.get_angle_Le(self.nodes_coor[nodes_connected])
            
            # Stiffness matrix for this element
            Ke = ut.stiffness_3D_truss(self.young, area, lx, ly, lz, Le)
            
            # Placing Ke inside Kg to construct it
            elementDof = np.array([[nodes_connected[0]*3, nodes_connected[0]*3+1, nodes_connected[0]*3+2, nodes_connected[1]*3, nodes_connected[1]*3+1, nodes_connected[1]*3+2]])
            self.Kg[elementDof, elementDof.T] += Ke
        
    def solve(self) -> None:
        """evaluate the nodal displacement using the relation Kg.U = F
        """
        not_restricted_dof = np.setdiff1d(np.arange(self.nb_dof), self.restricted_dof)
        
        partial_displacements = np.linalg.solve(self.Kg[not_restricted_dof[:,np.newaxis], not_restricted_dof], self.loads_on_dof[not_restricted_dof])
        self.nodal_displacements = np.zeros([self.nb_dof])
        self.nodal_displacements[not_restricted_dof] = partial_displacements
        
        self.shaped_nodal_displacements = self.nodal_displacements.reshape((self.nbNodes, 3))
        print('\nnodal dispalcements:')
        print(f'{self.shaped_nodal_displacements}\n')
        
    def eval_reactions(self) -> None:
        """evaluate nodal reactions
        """
        self.reactions = self.Kg@self.nodal_displacements
        self.reactions[np.abs(self.reactions) < 1e-10] = 0
        
        self.shaped_reactions = self.reactions.reshape((self.nbNodes, 3))
        print('\nnodal reactions:')
        print(f'{self.shaped_reactions}\n')
    
    def eval_stress(self, show_stress: bool = False) -> None:
        """evaluate the normal stress on each element
        
        Args:
            show_stress (bool, optional): showing illustration of stress values. Defaults to False
        """
        self.sigma = np.zeros(self.nbElements)
        for index, nodes_connected in enumerate(self.elements_connect):
            lx, ly, lz, Le = ut.get_angle_Le(self.nodes_coor[nodes_connected])
            # stress
            elementDof = np.array([[nodes_connected[0]*3, nodes_connected[0]*3+1, nodes_connected[0]*3+2, nodes_connected[1]*3, nodes_connected[1]*3+1, nodes_connected[1]*3+2]])            
            self.sigma[index] = self.young/Le * np.array([[-lx, -ly, -lz, lx, ly, lz]])@self.nodal_displacements[elementDof].T
        
        print('\nstress on each element:')
        print(f'{self.sigma[np.newaxis].T}\n')
        
    def show_deformed(self, compare_init: bool = True, colored_stress: bool = True) -> None:
        
        # scaling factor to increase displayed deformation => 10% of max coordinate        
        scaling = (0.1*np.max(np.abs(self.nodes_coor)))/np.max(np.abs(self.shaped_nodal_displacements))
        
        title = f'Deformed truss\nscaling factor: {scaling:.2f}'
        if compare_init:
            ax = up.show_truss_init_3D(self.nodes_coor, self.elements_connect, title=title, color='gray')            
        else:
            scaling = 1
            h = 5
            r = 4/3
            
            fig = plt.figure(figsize=(h*r, h))
            ax = fig.add_subplot(projection='3d')
            ax.grid()
            ax.set_title(title)
        
        if colored_stress:
            ax = up.show_add_deformed(ax, self.nodes_coor, self.shaped_nodal_displacements, self.elements_connect, scaling, self.sigma)
        else:
            ax = up.show_add_deformed(ax, self.nodes_coor, self.shaped_nodal_displacements, self.elements_connect, scaling)
        ax.axis('equal')
        plt.show()