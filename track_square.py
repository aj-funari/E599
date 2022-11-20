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
        self.x = 0
        self.y = 25
        self.theta = 0
        # timestep
        self.delta_t = 0.01
        # save for plotting
        self.xdata = []
        self.ydata = []
        self.theta_lst = []
        self.pterm_lst = []
        self.iterm_lst = []
        self.dterm_lst = []
        self.output = []
        self.x_square = []
        self.y_square = []
        self.lock = 0

        # PID Control 
        self.size = 30  # size of square 
        self.integral = 0
        self.error_last = 0

    def build_sqaure(self):
        # top of square
        x0 = list(np.linspace(0, self.size, 100))
        y0 = list(np.linspace(self.size, self.size, 100))
        # right side of square
        x1 = list(np.linspace(self.size, self.size, 100))
        y1 = list(np.linspace(self.size, 0, 100))
        # bottom of square
        x2 = list(np.linspace(self.size, 0, 100))
        y2 = list(np.linspace(0, 0, 100)) 
        # left side of square
        x3 = list(np.linspace(0, 0, 100))
        y3 = list(np.linspace(0, self.size, 100)) 

        self.x_square = x0 + x1 + x2 + x3
        self.y_square = y0 + y1 + y2 + y3 

    def track_square(self, i):
        # linear velocity is constant
        v = 15

        # sequential lock 
        if self.x < self.size and self.x - self.size < 0:  # track top of sqaure  
            error = self.size - self.y

        elif self.y > 0 and self:  # track right side of square
            self.lock = 1
            error = self.size - self.x

        elif self.x > 0 and self.lock <= 2:  # track bottom of square
            self.lock = 2
            error = -(0 - self.y)
   
        elif self.y < self.size and self.lock <= 3:  # track left side of square
            self.lock = 3
            error = -(0 - self.x)

        # error = self.size - self.y
        self.integral += error
        derivative = error - self.error_last
        self.error_last = error

        Kp = 1
        Ki = 0
        Kd = 30

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
    Car.build_sqaure()

    fig = plt.figure()
    ax = plt.axes(xlim=(-20, 50), ylim=(-20, 50))
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
        # add rectangle to animation 
        line.set_data(Car.x_square, Car.y_square) # plot target line
      
        # line.set_data(x, y)

        # Function to track line
        Car.track_square(i)
        # plot the car's path --> inputs are growing lists computed during runtime
        line_car.set_data(Car.xdata, Car.ydata)

        # simulate car as rectangle in animation
        patch.set_xy([Car.x,Car.y])
        patch.set_angle(np.rad2deg(Car.theta))
        return patch,

    plt.title('Initial Position: [0, 25]') 
    anim = FuncAnimation(fig, animate, init_func=init,
                               frames=1000, interval=20, blit=True)

    anim.save('track_square.gif', writer='pillow')