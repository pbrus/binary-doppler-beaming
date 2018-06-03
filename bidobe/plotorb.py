import matplotlib.pyplot as plt


def plot_projected_orbits(orbit1, orbit2, xunit="m", yunit="m", filename=None):
    """
    Plot orbits of a binary system projected on the sky. Position
    expressed in XY coordinate system.

    Parameters
    ----------
    orbit1, orbit2 : numpy.array(shape=(*,2), dtype=float)
        Array represents x, y position of an object
        in the binary system.
    xunit, yunit : str
        String which is x/y's label on an image.
        Default set in meters.
    filename : str
        The name of a file where the image will be saved to.
        It should have the .eps extenstion. If None the image
        will be only displayed on a screen.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.grid(color='gray', linestyle='--', linewidth=0.2)
    plt.xlabel('x (' + xunit + ')')
    plt.ylabel('y (' + yunit + ')')
    plt.title('Binary system')
    orbit = choose_greater_orbit(orbit1, orbit2)
    arrow_length = calculate_arrow_length(orbit)
    xran, yran = choose_xy_ranges(orbit, arrow_length)
    plt.arrow(0, 0, arrow_length, 0, head_width=0.05*arrow_length,
        head_length=0.1*arrow_length, fc='black', width=0.001*arrow_length)
    plt.arrow(0, 0, 0, arrow_length, head_width=0.05*arrow_length,
        head_length=0.1*arrow_length, fc='black', width=0.001*arrow_length)
    ax.set_xlim(xran)
    ax.set_ylim(yran)
    ax.annotate("W", (arrow_length, 0.05*arrow_length))
    ax.annotate("N", (0.05*arrow_length, arrow_length))
    plt.plot(orbit1[:,0], orbit1[:,1], 'r-', linewidth=0.5)
    plt.plot(orbit2[:,0], orbit2[:,1], 'b-', linewidth=0.5)
    plt.tight_layout()

    if filename:
        fig.savefig(filename, format="eps", bbox_inches=None)
    else:
        plt.show()

def choose_greater_orbit(orbit1, orbit2):
    x1_min = orbit1[:,0].min()
    x1_max = orbit1[:,0].max()
    x2_min = orbit2[:,0].min()
    x2_max = orbit2[:,0].max()

    if (x1_max - x1_min) > (x2_max - x2_min):
        return orbit1
    else:
        return orbit2

def calculate_arrow_length(orbit):
    arrow_length_scale = 0.2
    x_min = orbit[:,0].min()
    x_max = orbit[:,0].max()
    y_min = orbit[:,1].min()
    y_max = orbit[:,1].max()

    minimum, maximum = choose_greater_range(x_min, x_max, y_min, y_max)
    arrow_length = arrow_length_scale*(maximum - minimum)

    return arrow_length

def choose_xy_ranges(orbit, arrow_length):
    x_min = orbit[:,0].min()
    x_max = orbit[:,0].max()
    y_min = orbit[:,1].min()
    y_max = orbit[:,1].max()

    minimum, maximum = choose_greater_range(x_min, x_max, y_min, y_max)
    margin = 0.1*(maximum - minimum)

    if arrow_length > x_max:
        x_max = 1.2*arrow_length
    if arrow_length > y_max:
        y_max = 1.2*arrow_length

    return (x_min - margin, x_max + margin), (y_min - margin, y_max + margin)

def choose_greater_range(first_min, first_max, second_min, second_max):

    if (first_max - first_min) > (second_max - second_min):
        return first_min, first_max
    else:
        return second_min, second_max


def plot_radial_velocities(time, velocity1, velocity2,
                           xunit="s", yunit="m/s", filename=None):
    """
    Plot radial velocities of a binary system.

    Parameters
    ----------
    time : 1D numpy.array(dtype=float)
        Array represents time.
    velocity1, velocity2 : 1D numpy.array(dtype=float)
        Array represents radial velocity of each object.
    xunit : str
        String which is x's label on the image.
        Default set in seconds.
    yunit : str
        String which is y's label on the image.
        Default set in meters per second.
    filename : str
        The name of a file where the image will be saved to.
        It should have the .eps extenstion. If None the image
        will be only displayed on a screen.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(color='gray', linestyle='--', linewidth=0.2)
    plt.xlabel('Time (' + xunit + ')')
    plt.ylabel(r'$V_{rad}$' + ' (' + yunit + ')')
    plt.title('Radial velocities')
    plt.plot(time, velocity1, 'r-', linewidth=0.5)
    plt.plot(time, velocity2, 'b-', linewidth=0.5)
    plt.tight_layout()

    if filename:
        fig.savefig(filename, format="eps", bbox_inches=None)
    else:
        plt.show()


def plot_light_curve(time, magnitude, xunit="s", filename=None):
    """
    Plot light curve caused by the doppler beaming in a binary system.

    Parameters
    ----------
    time : 1D numpy.array(dtype=float)
        Array represents time.
    magnitude : 1D numpy.array(dtype=float)
        Array represents magnitude of the binary system.
    xunit : str
        String which is x's label on the image.
        Default set in seconds.
    filename : str
        The name of a file where the image will be saved to.
        It should have the .eps extenstion. If None the image
        will be only displayed on a screen.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(color='gray', linestyle='--', linewidth=0.2)
    plt.xlabel('Time (' + xunit + ')')
    plt.ylabel('Brightness (mag)')
    plt.title('Light curve')
    plt.gca().invert_yaxis()
    plt.plot(time, magnitude, 'g-', linewidth=0.5)
    plt.tight_layout()

    if filename:
        fig.savefig(filename, format="eps", bbox_inches=None)
    else:
        plt.show()
