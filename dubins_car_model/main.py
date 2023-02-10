import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import math
from Dubins_Car import car

Car = car()

if __name__ == "__main__":
    """
    The code below simulates Dubins Car dynamics and control with 4 different
    linear and angular controls. Since the controls are constant, the animation
    will cause the car to drive in 4 different circles. The gif is saved as 
    Dubins Car 1.
        - positive angular velocity will cause the car to turn left
        - negative angular velocity will cause the car to turn right
    """

    control_inputs = [(2, 0.4), (3, -0.7), (2, 0.4), (3, -0.8)]
    Car.compute_state(control_inputs)

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlim(-15, 10)
    ax.set_ylim(-10, 20)
    plt.title('Dubins Car 1 Simulator') 

    # initialize rectangle and line
    patch = patches.Rectangle((0,0), width=1.50, height=0.75, angle=0, fc='b')
    line, = ax.plot([], [], lw=3)

    def init():
        ax.add_patch(patch)
        line.set_data([], [])
        return patch,

    # animation function 
    def animate(i):
        x = round(Car.xdata[i*20], 2)
        y = round(Car.ydata[i*20], 2)
        theta = round(Car.theta_lst[i*20], 2)
        line.set_data(Car.xdata[:i*20], Car.ydata[:i*20])
        patch.set_xy([x,y])
        patch.set_angle(np.rad2deg(theta))
        return patch,

    # call the animator	 
    anim = FuncAnimation(fig, animate, 
                        init_func=init, 
                        frames=200,
                        interval=50, 
                        blit=True)

    # save the animation as mp4 video file 
    anim.save('Dubins Car 1.gif', writer='pillow', fps=60)

    """
    The code below simulates Dubins Car dynamic and control; however,
    instead of providing constant linear and angular controls, the
    control values increment with time. The results are coil shaped
    patterns. 
    """

    Car.xdata.clear()  # clear x_data for plotting in animation function
    Car.ydata.clear()  # clear y_data for plotting in animation function

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_xlim(-4, 10)
    ax.set_ylim(-2, 9)
    plt.title('Dubins Car 2 Simulator') 

    # initialize rectangle
    patch = patches.Rectangle((0,0), width=0.65, height=0.30, angle=0, fc='b')
    line, = ax.plot([], [], lw=3)

    def init():
        ax.add_patch(patch)
        line.set_data([], [])
        return patch,

    # animation function 
    def animate(i):
        if (i < 50):
            v = 10 + i/2 
            w = 10 + i/5 
            state = Car.step(v, w)
            x = state[0]
            y = state[1]
            theta = state[2]
            line.set_data(Car.xdata[:i], Car.ydata[:i])
            patch.set_xy([x,y])
            patch.set_angle(np.rad2deg(theta))

        elif (i > 50 and i < 100):
            v = 10 + i/10
            w = 5 + i/50
            state = Car.step(v, w)
            x = state[0]
            y = state[1]
            theta = state[2]
            line.set_data(Car.xdata[:i], Car.ydata[:i])
            patch.set_xy([x,y])
            patch.set_angle(np.rad2deg(theta))
        
        elif (i > 100 and i < 150):
            v = 10 + i/10
            w = -10 - i/100
            state = Car.step(v, w)
            x = state[0]
            y = state[1]
            theta = state[2]
            line.set_data(Car.xdata[:i], Car.ydata[:i])
            patch.set_xy([x,y])
            patch.set_angle(np.rad2deg(theta))

        elif (i > 150):
            v = 10 + i/25
            w = -10 + i/25
            state = Car.step(v, w)
            x = state[0]
            y = state[1]
            theta = state[2]
            line.set_data(Car.xdata[:i], Car.ydata[:i])
            patch.set_xy([x,y])
            patch.set_angle(np.rad2deg(theta))

        return patch,

    # call the animator	 
    anim = FuncAnimation(fig, animate, 
                        init_func=init, 
                        frames=200,
                        interval=50, 
                        blit=True)

    # save the animation as mp4 video file 
    anim.save('Dubins Car 2.gif', writer='pillow', fps=60)