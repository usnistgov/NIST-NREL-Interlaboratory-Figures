import numpy as np
from matplotlib import pylab
from itertools import cycle

def make_basis():
    """
    Make the basis vectors for transforming 3D data to 2D.
    """
    # this could be changed to change the direction of the plots
    start_angle = 90.0
    basis = np.array([[np.cos(2.0*_*np.pi/3.0 + start_angle*np.pi/180),
                       np.sin(2.0*_*np.pi/3.0 + start_angle*np.pi/180)] for _ in range(3)])
    return basis
    
    
def transform(data,basis):
    """
    Transform 3D ratio data into a 2D ternary format.
    
    The rows of the data must some all be positive real numbers and sum to 1.
    
    :param data: An N x 3 numpy array of data to transform.
    :param basis: The basis vectors, generated from make_basis
    
    """
    t_data = np.dot((data.T / data.sum(-1)).T,basis)
    return t_data
        

def setup_plot(ax, side_labels=None, grid_values=None, **kwargs):
    """
    Setup the plot by making the outer border, making grid lines, and labeling the sides.
    
    :param ax: A matplotlib axes handle for where the plotting will take place
    :param side_labels: A list of strings for labeling the sides. The order of the labels must be the same order
    as the data. Default: ["1","2","3"]
    :param grid_values: A list or numpy array of values between 0 and 1 to put grid lines at, for all sides. Default: [0.2, 0.4, 0.6, 0.8]
    
    The kwargs can be:
        label_offset: A factor for offsetting the side labels (default: 0.2)
        tick_offset: A factor for offsetting the tick labels (default: 0.2)
        label_args: a dictionary of formatting arguments passed to ax.text() for the side labels
        tick_args: a dictionary of formatting arguments passed to ax.text() for the tick labels
        edge_args: a dictionary of formatting arguments passed to pylab.plot() for the triangle edge lines.
        grid_args: a dictionary of formatting arguments passed to the grid line plotting
    """
    if side_labels is None: side_labels = ["1","2","3"]
    if grid_values is None: grid_values = [0.2, 0.4, 0.6, 0.8]
    basis = make_basis()
    pts = []
    # for each coordinate, for each grid
    for i in range(3):
        not_i = [x for x in range(3) if x != i]
        for j in grid_values:
            d = 1-j
            pt1 = [0,0,0]
            pt2 = [0,0,0]
            pt1[i] = j
            pt2[i] = j
            pt1[not_i[0]] = d
            pt2[not_i[1]] = d
            pts.append(pt1)
            pts.append(pt2)
    # transform those
    pts_tr = transform(np.array(pts),basis)
    # manage inputs
    label_offset = kwargs.get('label_offset',0.5)
    tick_offset = kwargs.get('tick_offset',0.2)
    label_args = {'ha':'center','va':'center','fontsize':16}
    label_args.update(kwargs.get('label_args',{}))
    tick_args = {'fontsize':14}
    tick_args.update(kwargs.get('tick_args',{}))
    tick_rotations = [0, -60, 60]
    # plot the text first 
    basis_pts = np.vstack((basis,basis[0,:]))
    for i,l in enumerate(side_labels):
        if i >= 3:
            break
        a = basis_pts[i]
        b = basis_pts[i+1]
        x = (a[0]-b[0])*0.5 + b[0]
        y = (a[1]-b[1])*0.5 + b[1]
        angle = 180*np.arctan(y/x)/np.pi + 90
        if angle > 90 and angle <= 270:
            angle = np.mod(angle + 180,360)
        ax.text(x*(1 + label_offset), y*(1 + label_offset), l, rotation=angle, **label_args)
        if True:
            ha = "right" if i == 0 else "left"
            va = "center" if i == 0 else ("top" if i == 1 else "bottom")
            for d in grid_values:
                x = (a[0]-b[0])*d + b[0] - (.02 if i == 0 else 0)
                y = (a[1]-b[1])*d + b[1]
                #s = "%.2f"%d if i == 0 else " %.1f"%d
                s = " %.1f"%d
                ax.text(x,y,s,rotation=tick_rotations[i],ha=ha,va=va,**tick_args)
    # plot the edges
    edge_args = {'c':'black','lw':2,'linestyle':'-'}
    edge_args.update(kwargs.get('edge_args',{}))
    for i in range(3):
        ax.plot([basis_pts[i][0],basis_pts[i+1][0]],[basis_pts[i][1],basis_pts[i+1][1]],**edge_args)
    # plot grid
    grid_args = {'c':'black','lw':0.5}
    grid_args.update(kwargs.get('grid_args',{}))
    val_cycle = cycle(grid_values)
    linestyles = ['-','--','-.']
    n_grid = len(grid_values)*1.0
    for i in range(0,len(pts_tr),2):
        gn = int(np.floor((i/2)/n_grid))
        xs = [pts_tr[i][0],pts_tr[i+1][0]]
        ys = [pts_tr[i][1],pts_tr[i+1][1]]
        grid_args['linestyle'] = linestyles[gn]
        ax.plot(xs,ys,**grid_args)
        
    # Clear normal matplotlib axes graphics.
    ax.set_xticks(())
    ax.set_yticks(())
    ax.set_frame_on(False)
    pylab.axis('equal')

