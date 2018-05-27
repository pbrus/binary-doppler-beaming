import matplotlib.pyplot as plt


def plot_projected_orbits(orbit1, orbit2):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.grid(color='gray', linestyle='--', linewidth=0.2)
    plt.xlabel('x (AU)')
    plt.ylabel('y (AU)')
    xran, yran = choose_xy_ranges(orbit1, orbit2)
    ax.set_xlim(xran)
    ax.set_ylim(yran)
    dx = ax.get_xticks()[2] - ax.get_xticks()[0]
    dy = ax.get_yticks()[2] - ax.get_yticks()[0]
    plt.arrow(0, 0, dx, 0, head_width=0.05*dx, head_length=0.1*dx, fc='black')
    plt.arrow(0, 0, 0, dy, head_width=0.05*dy, head_length=0.1*dy, fc='black')
    plt.plot(orbit1[:,0], orbit1[:,1], 'r-', linewidth=0.5)
    plt.plot(orbit2[:,0], orbit2[:,1], 'b-', linewidth=0.5)
    plt.show()

def choose_xy_ranges(orbit1, orbit2):
    margin_scale = 0.1
    x1_min = orbit1[:,0].min()
    x1_max = orbit1[:,0].max()
    x2_min = orbit2[:,0].min()
    x2_max = orbit2[:,0].max()
    y1_min = orbit1[:,1].min()
    y1_max = orbit1[:,1].max()
    y2_min = orbit2[:,1].min()
    y2_max = orbit2[:,1].max()
    dx1 = x1_max - x1_min
    dx2 = x2_max - x2_min
    dy1 = y1_max - y1_min
    dy2 = y2_max - y2_min

    if dx1 > dx2:
        return ((x1_min - margin_scale*dx1, x1_max + margin_scale*dx1),
                (y1_min - margin_scale*dy1, y1_max + margin_scale*dy1))
    else:
        return ((x2_min - margin_scale*dx2, x2_max + margin_scale*dx2),
                (y2_min - margin_scale*dy2, y2_max + margin_scale*dy2))
