import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import math
plt.style.use('seaborn-pastel')

class car:
    def __init__(self):
        # initial position
        self.x = -10
        self.y = -10
        self.theta = 0
        self.delta_t = 0.01
        self.xdata = []
        self.ydata = []
        self.theta_lst = []
        self.pterm_lst = []
        self.iterm_lst = []
        self.dterm_lst = []
        self.output = []

        # PID Control
        self.target = 10
        self.integral = 0
        self.error_last = 0

    def track_line(self):
        # linear velocity is constant
        v = 20

        # angular velocity (steering) controlled with PID loop --> track line
        error = self.target - Car.y  # ex. 10 - 0 = 10 --> positive theta turns left 
        self.integral += error
        derivative = error - self.error_last
        self.error_last = error

        Kp = 0.1
        Ki = 0
        Kd = 0

        pterm = error * Kp
        iterm = Car.integral * Ki
        dterm = derivative * Kd

        w = pterm + iterm + dterm

        # save values for plotting
        self.pterm_lst.append(pterm)
        self.iterm_lst.append(iterm)
        self.dterm_lst.append(dterm)
        self.output.append(w)    

        # compute new state
        x_1 = self.x + ((v*math.cos(self.theta)) * self.delta_t)
        y_1 = self.y + ((v*math.sin(self.theta)) * self.delta_t)
        theta_1 = self.theta + (w * self.delta_t)

        # save state for plotting
        self.xdata.append(x_1)
        self.ydata.append(y_1)
        self.theta_lst.append(theta_1)

        # step the simulatoin
        self.x = x_1
        self.y = y_1
        self.theta = theta_1

if __name__ == "__main__":

    Car = car()

    fig = plt.figure()
    ax = plt.axes(xlim=(-15, 40), ylim=(-40, 40))
    line, = ax.plot([], [], lw=1)
    line_car, = ax.plot([], [], lw=2)
    patch = patches.Rectangle((0,0), width=2, height=0.5, angle=0, fc='g') 

    def init():
        line.set_data([], [])
        line_car.set_data([], [])
        ax.add_patch(patch)
        return patch,

    # animation function 
    def animate(i):
        # TRACK LINE USING PID CONTROL
        x = np.linspace(-15, 40, 100)
        y = 10
        line.set_data(x, y) # plot target line 

        # Function to track line
        Car.track_line()
        # plot the car's path --> inputs are growing lists computed during runtime
        line_car.set_data(Car.xdata, Car.ydata)

        # simulate car as rectangle in animation
        patch.set_xy([Car.x,Car.y])
        patch.set_angle(np.rad2deg(Car.theta))
        return patch,

    plt.title('Initial Position: [-10, -10]') 
    anim = FuncAnimation(fig, animate, init_func=init,
                               frames=300, interval=20, blit=True)

    anim.save('track_line.gif', writer='pillow')