import numpy as np
import matplotlib.pyplot as plt

from . import sub_utils_plot as su

def show_truss_init_3D(nodes_coor: np.ndarray, elements_connect: np.ndarray, title: str = 'Initial truss\nClose to continue', color: str='k') -> plt.axes:
    """show the loaded truss

    Args:
        nodes_coor (np.ndarray): 2D ndarray of nodes coordinates
        elements_connect (np.ndarray): 2D ndarray of elements connectivities
        title (str, optional): title of the plot. Defaults to 'Initial truss\nClose to continue'
        color (str, optional): color of the truss
        
    Return:
        ax (plt.axes): used axis
    """
    h = 5
    r = 4/3
    
    fig = plt.figure(figsize=(h*r, h))
    ax = fig.add_subplot(projection='3d')
    ax.grid()
    for nodes_connected in elements_connect:
        x_plot = nodes_coor[nodes_connected, 0]
        y_plot = nodes_coor[nodes_connected, 1]
        z_plot = nodes_coor[nodes_connected, 2]
        ax.plot(x_plot, y_plot, z_plot, '-o', lw=2, markersize=5, color=color)

    ax.axis('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title(title)
    return ax

def show_add_BC(ax:plt.axes, restricted_dof: list, nodes_coor: np.ndarray, loads_vector: np.ndarray) -> plt.axes:
    """illustrate all Boundary Conditions by completing axis 'ax'

    Args:
        ax (plt.axes): axis with init truss to complete
        restricted_dof (list): list of degree of freedom restricted to 0
        nodes_coor (np.ndarray): 2D ndarray of nodes coordinates
        loads_vector (np.ndarray): 2D array of the load components for each node

    Returns:
        ax (plt.axes): used axis
    """
    # get main dimension
    lim = [ax.get_xlim(), ax.get_ylim(), ax.get_zlim()]
    size_lim = [item[1]-item[0] for item in lim]
    s = np.min(size_lim)/20                             # triangle drawing parameter
    
    components = ['x', 'y', 'z']
    for index_dof in restricted_dof:
        nb_node = int(index_dof/3)
        coor = nodes_coor[nb_node, :]
        idx_comp = index_dof % len(components)
        
        if components[idx_comp] == 'x':
            ax = su.plot_3D_BC_x(ax, coor, s)
        if components[idx_comp] == 'y':
            ax = su.plot_3D_BC_y(ax, coor, s)
        if components[idx_comp] == 'z':
            ax = su.plot_3D_BC_z(ax, coor, s)
    
    s = 5*s                                             # arrow drawing parameter
    for load_info in loads_vector:
        coor = nodes_coor[int(load_info[0]), :]
        ax = su.plot_3D_load(ax, coor, load_info[1:], s)    
    return ax

def show_add_deformed(ax: plt.axes, nodes_coor: np.ndarray, shaped_nodal_displacements: np.ndarray, elements_connect: np.ndarray, scaling: float = 10, stress: np.ndarray = None) -> plt.axes:
    """Add to axe 'ax' the deformed truss

    Args:
        ax (plt.axes): axis to complete
        nodes_coor (np.ndarray): 2D ndarray of nodes coordinates
        shaped_nodal_displacements (np.ndarray): 2D ndarray of all nodal displacements
        elements_connect (np.ndarray): 2D ndarray of elements connectivities
        scaling (float, optinal): scaling of nodal displacements. Defaults to 10.
        stress (np.ndarray, optional): stress value for each element. Defaults to None

    Returns:
        plt.axes: used axis
    """
    deformed_truss = nodes_coor + scaling*shaped_nodal_displacements
    
    if stress is not None:
        norm_stress = 3*stress/np.max(np.abs(stress))
        for index, nodes_connected in enumerate(elements_connect):
            x_plot = deformed_truss[nodes_connected, 0]
            y_plot = deformed_truss[nodes_connected, 1]
            z_plot = deformed_truss[nodes_connected, 2]
            if stress[index] > 0:
                ax.plot(x_plot, y_plot, z_plot, color='g', lw=norm_stress[index], marker='o', markersize=7)
            else:
                ax.plot(x_plot, y_plot, z_plot, color='r', lw=norm_stress[index], marker='o', markersize=7)
        print('\nColor code:')
        print('    |- red -> compression')
        print('    |- green -> tension\n')
    else:
        for nodes_connected in elements_connect:
            x_plot = deformed_truss[nodes_connected, 0]
            y_plot = deformed_truss[nodes_connected, 1]
            z_plot = deformed_truss[nodes_connected, 2]
            ax.plot(x_plot, y_plot, z_plot, '--ok', lw=1, markersize=7)
    
    return ax