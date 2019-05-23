"""
Save to file, plot or animate on the screen:
  1. orbits of a binary system projected on the sky
  2. radial velocities of each component of the binary system
  3. a light curve caused by the doppler beaming

"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


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
    figure = _projected_orbits(orbit1, orbit2, xunit, yunit)
    _display_or_save_figure(figure, filename)


def animate_projected_orbits(orbit1, orbit2, xunit="m", yunit="m"):
    """
    Animate orbiting objects of a binary system projected on the sky.
    Position expressed in XY coordinate system.

    Parameters
    ----------
    orbit1, orbit2 : numpy.array(shape=(*,2), dtype=float)
        Array represents x, y position of an object
        in the binary system.
    xunit, yunit : str
        String which is x/y's label on an image.
        Default set in meters.
    """
    figure = _projected_orbits(orbit1, orbit2, xunit, yunit)
    animation = _anim_projected_orbits(figure, orbit1, orbit2)
    _display_or_save_figure(figure, None)


def _projected_orbits(orbit1, orbit2, xunit, yunit):
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.set_aspect('equal')
    ax.grid(color='gray', linestyle='--', linewidth=0.2)
    plt.xlabel('x (' + xunit + ')')
    plt.ylabel('y (' + yunit + ')')
    plt.title('Binary system')
    init_xran, init_yran = _choose_orbits_ranges(orbit1, orbit2)
    arrow_length = _calculate_arrow_length(init_xran, init_yran)
    xran, yran = _choose_xy_ranges(init_xran, init_yran, arrow_length)
    plt.arrow(0, 0, arrow_length, 0, head_width=0.05*arrow_length,
              head_length=0.1*arrow_length, fc='black',
              width=0.001*arrow_length)
    plt.arrow(0, 0, 0, arrow_length, head_width=0.05*arrow_length,
              head_length=0.1*arrow_length, fc='black',
              width=0.001*arrow_length)
    ax.set_xlim(xran)
    ax.set_ylim(yran)
    ax.annotate("W", (arrow_length, 0.05*arrow_length))
    ax.annotate("N", (0.05*arrow_length, arrow_length))
    plt.plot(orbit1[:, 0], orbit1[:, 1], 'r-', linewidth=0.5)
    plt.plot(orbit2[:, 0], orbit2[:, 1], 'b-', linewidth=0.5)
    plt.tight_layout()

    return figure


def _anim_projected_orbits(figure, orbit1, orbit2):
    line, = plt.plot(orbit1[:, 0], orbit1[:, 1], 'ko', animated=True)

    def _update_positions(i):
        x1 = orbit1[:, 0][i]
        y1 = orbit1[:, 1][i]
        x2 = orbit2[:, 0][i]
        y2 = orbit2[:, 1][i]
        line.set_data((x1, x2), (y1, y2))

        return line,

    animation = FuncAnimation(figure, _update_positions,
                              frames=range(len(orbit1)), interval=1, blit=True)

    return animation


def _choose_orbits_ranges(orbit1, orbit2):
    x_min = min(orbit1[:, 0].min(), orbit2[:, 0].min())
    x_max = max(orbit1[:, 0].max(), orbit2[:, 0].max())
    y_min = min(orbit1[:, 1].min(), orbit2[:, 1].min())
    y_max = max(orbit1[:, 1].max(), orbit2[:, 1].max())

    return (x_min, x_max), (y_min, y_max)


def _calculate_arrow_length(xran, yran):
    arrow_length_scale = 0.2
    x_min = xran[0]
    x_max = xran[1]
    y_min = yran[0]
    y_max = yran[1]

    minimum, maximum = _choose_greater_range(x_min, x_max, y_min, y_max)
    arrow_length = arrow_length_scale*(maximum - minimum)

    return arrow_length


def _choose_xy_ranges(xran, yran, arrow_length):
    x_min = xran[0]
    x_max = xran[1]
    y_min = yran[0]
    y_max = yran[1]

    minimum, maximum = _choose_greater_range(x_min, x_max, y_min, y_max)
    margin = 0.1*(maximum - minimum)

    if arrow_length > x_max:
        x_max = 1.2*arrow_length
    if arrow_length > y_max:
        y_max = 1.2*arrow_length

    return (x_min - margin, x_max + margin), (y_min - margin, y_max + margin)


def _choose_greater_range(first_min, first_max, second_min, second_max):

    if (first_max - first_min) > (second_max - second_min):
        return first_min, first_max
    else:
        return second_min, second_max


def _display_or_save_figure(figure, filename=None):
    if filename:
        figure.savefig(filename, format="eps", bbox_inches=None)
    else:
        plt.show()


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
    figure = _radial_velocities(time, velocity1, velocity2, xunit, yunit)
    _display_or_save_figure(figure, filename)


def animate_radial_velocities(time, velocity1, velocity2,
                              xunit="s", yunit="m/s"):
    """
    Animate radial velocities of a binary system.

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
    """
    figure = _radial_velocities(time, velocity1, velocity2, xunit, yunit)
    animation = _anim_radial_velocities(figure, time, velocity1, velocity2)
    _display_or_save_figure(figure, None)


def _radial_velocities(time, velocity1, velocity2, xunit="s", yunit="m/s"):
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.grid(color='gray', linestyle='--', linewidth=0.2)
    plt.xlabel('Time (' + xunit + ')')
    plt.ylabel(r'$V_{rad}$' + ' (' + yunit + ')')
    plt.title('Radial velocities')
    plt.plot(time, velocity1, 'r-', linewidth=0.5)
    plt.plot(time, velocity2, 'b-', linewidth=0.5)
    plt.tight_layout()

    return figure


def _anim_radial_velocities(figure, time, velocity1, velocity2):
    line, = plt.plot(time, velocity1, 'ko', animated=True)

    def _current_velocities(i):
        t = time[i]
        v1 = velocity1[i]
        v2 = velocity2[i]
        line.set_data((t, t), (v1, v2))

        return line,

    animation = FuncAnimation(figure, _current_velocities,
                              frames=range(len(time)), interval=1, blit=True)

    return animation


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
    figure = _light_curve(time, magnitude, xunit)
    _display_or_save_figure(figure, filename)


def animate_light_curve(time, magnitude, xunit="s"):
    """
    Animate light curve caused by the doppler beaming in a binary system.

    Parameters
    ----------
    time : 1D numpy.array(dtype=float)
        Array represents time.
    magnitude : 1D numpy.array(dtype=float)
        Array represents magnitude of the binary system.
    xunit : str
        String which is x's label on the image.
        Default set in seconds.
    """
    figure = _light_curve(time, magnitude, xunit)
    animation = _anim_light_curve(figure, time, magnitude)
    _display_or_save_figure(figure, None)


def _light_curve(time, magnitude, xunit):
    figure = plt.figure()
    ax = figure.add_subplot(111)
    ax.grid(color='gray', linestyle='--', linewidth=0.2)
    plt.xlabel('Time (' + xunit + ')')
    plt.ylabel('Brightness (mag)')
    plt.title('Light curve')
    plt.gca().invert_yaxis()
    plt.plot(time, magnitude, 'g-', linewidth=0.5)
    plt.tight_layout()

    return figure


def _anim_light_curve(figure, time, magnitude):
    line, = plt.plot(time, magnitude, 'ko', animated=True)

    def _current_magnitude(i):
        t = time[i]
        mag = magnitude[i]
        line.set_data(t, mag)

        return line,

    animation = FuncAnimation(figure, _current_magnitude,
                              frames=range(len(time)), interval=1, blit=True)

    return animation
