import numpy as np

def load_nodes_coor(nodes_path: str) -> np.ndarray:
    """load coordinates of all nodes

    Args:
        nodes_path (str): path towards the file

    Returns:
        nodes_coor (np.ndarray): a 2D ndarray with first column the x coordinate and the second column the y coordinate
    """
    nodes_coor = np.loadtxt(nodes_path, dtype=float, delimiter=' ', skiprows=1)
    return nodes_coor

def load_elements_connect(elements_path: str) -> np.ndarray:
    """load elements connectivity (from nodeA to nodeB)

    Args:
        elements_path (str): path towards the file

    Returns:
        elements_connect (np.ndarray): a 2D ndarray with first column the first node connected to the element and the second the second node
    """
    elements_connect = np.loadtxt(elements_path, dtype=int, delimiter=' ', skiprows=1)
    return elements_connect

def load_cross_section(crossSection_path: str) -> np.ndarray:
    """load all cross section of each element

    Args:
        crossSection_path (str): path towards the file

    Returns:
        np.ndarray: a 1D ndarray with ordered elements cross section
    """
    all_cross_section = np.loadtxt(crossSection_path, dtype=float, delimiter=' ', skiprows=1)
    return all_cross_section

def load_restricted_dof(restrictedDof_path: str) -> np.ndarray:
    """load the details of degree of freedom restricted to 0

    Args:
        restrictedDof_path (str): path towards the details of the restricted degree of freedom

    Returns:
        np.ndarray: 1D ndarray with the index of each restricted degree of freedom
    """
    details_restricted_dof = np.loadtxt(restrictedDof_path, dtype=int, delimiter=' ', skiprows=2)
    
    list_restricted_dof = []
    for i, row in enumerate(details_restricted_dof):
        for j, col in enumerate(row[1:]):
            if col:
                list_restricted_dof.append(3*row[0]+j)
    return np.array(list_restricted_dof)

def load_loads(allLoads_path: str, nb_dof: int) -> np.ndarray:
    """load the details of loads in each degree of freedom

    Args:
        allLoads_path (str): path towards the details of loads
        nb_dof (int): total number of degree of freedom

    Returns:
        np.ndarray: 1D ndarray with the load for each degree of freedom
    """
    details_loads = np.loadtxt(allLoads_path, dtype=float, delimiter=' ', skiprows=2)    

    # if single line, add dimension
    if details_loads.ndim == 1:
        details_loads = details_loads[np.newaxis]
    
    loads_on_dof = np.zeros(nb_dof)
    for i, row in enumerate(details_loads):
        for j, col in enumerate(row[1:]):
            loads_on_dof[int(3*row[0]+j)] = col
            # if col:
            #     loads_on_dof.append(int(3*row[0]+j))
    return loads_on_dof, details_loads

def get_angle_Le(nodes: np.ndarray) -> tuple[float, float, float, float]:
    """get info for element connected to 'nodes'

    Args:
        nodes (np.ndarray): 2D ndarray of the nodes coordinates connected to the element

    Returns:
        tuple[float, float, float, float]: angle_x, angle_y, angle_z and element length
    """
    dx = nodes[1, 0]-nodes[0, 0]
    dy = nodes[1, 1]-nodes[0, 1]
    dz = nodes[1, 2]-nodes[0, 2]
    
    Le = np.sqrt(dx**2+dy**2+dz**2)
    lx = dx/Le
    ly = dy/Le
    lz = dz/Le
    return lx, ly, lz, Le

def stiffness_3D_truss(young: float, cross_section: float, lx: float, ly: float, lz: float, Le: float) -> np.ndarray:
    """generate the stiffness matrix for one element

    Args:
        young (float): Young's modulus
        cross_section (float): section of the element
        lx (float): x angle
        ly (float): y angle
        lz (float): z angle
        Le (float): length of the element

    Returns:
        np.ndarray: the stiffness matrix of the element
    """
    T = np.array([[lx**2, lx*ly, lx*lz], [lx*ly, ly**2, ly*lz], [lx*lz, ly*lz, lz**2]])
    Ke = (young*cross_section)/Le * np.asarray(np.bmat([[T, -T], [-T, T]]))
    return Ke
