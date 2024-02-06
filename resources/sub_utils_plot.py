import numpy as np
import matplotlib.pyplot as plt

def plot_3D_BC_x(ax: plt.axes, coor: np.ndarray, s: float) -> plt.axes:
    """plot square box around the node in coor

    Args:
        ax (plt.axes): ax to complete
        coor (np.ndarray): coordinates where to draw
        s (float): size of the box

    Returns:
        ax (plt.axes): ax to return
    """
    x, y, z = coor
    ax.plot([x, x-1.5*s, x-1.5*s, x], [y, y, y, y], [z, z+s, z-s, z], 'g', lw=2)
    return ax

def plot_3D_BC_y(ax: plt.axes, coor: np.ndarray, s: float) -> plt.axes:
    """plot square box around the node in coor

    Args:
        ax (plt.axes): ax to complete
        coor (np.ndarray): coordinates where to draw
        s (float): size of the box

    Returns:
        ax (plt.axes): ax to return
    """
    x, y, z = coor
    ax.plot([x, x+s, x-s, x], [y, y+1.5*s, y+1.5*s, y], [z, z, z, z], 'g', lw=2)
    return ax

def plot_3D_BC_z(ax: plt.axes, coor: np.ndarray, s: float) -> plt.axes:
    """plot square box around the node in coor

    Args:
        ax (plt.axes): ax to complete
        coor (np.ndarray): coordinates where to draw
        s (float): size of the box

    Returns:
        ax (plt.axes): ax to return
    """
    x, y, z = coor
    ax.plot([x, x, x, x], [y, y+s, y-s, y], [z, z-1.5*s, z-1.5*s, z], 'g', lw=2)
    return ax

def plot_3D_load(ax: plt.axes, coor: np.ndarray, load: float, s: float) -> plt.axes:
    """plot arrow in the node coor

    Args:
        ax (plt.axes): ax to complete
        coor (np.ndarray): coordinates where to draw
        load (float): load vector [x, y, z] for the node in 'coor'
        s (float): size of the arrow

    Returns:
        ax (plt.axes): ax to return
    """
    x, y, z = coor
    sign = s*np.sign(load)
    coefs = np.abs(load)/np.max(np.abs(load))
    arrow = sign*coefs
    
    ax.quiver(x, y, z, arrow[0], arrow[1], arrow[2], length=s, color='r')
    return ax
