import math

# define class to store iterative data 
class car:
    def __init__(self):
        # initial conditions
        self.x = 0
        self.y = 0
        self.theta = 0
        self.delta_t = 0.01
        self.xdata = []
        self.ydata = []
        self.theta_lst = []

    # control input linear(v), angular(w) 
    def compute_state(self, control_inputs):
        # for each control input, simulate 1000 time steps of path
        for control in control_inputs:
            for i in range(0, 1000):
                # linear and angular velocity
                v = control[0]
                w = control[1]

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

    def step(self, v, w):
        x_1 = self.x + ((v*math.cos(self.theta)) * self.delta_t)
        y_1 = self.y + ((v*math.sin(self.theta)) * self.delta_t)
        theta_1 = self.theta + (w * self.delta_t)

        self.xdata.append(x_1)
        self.ydata.append(y_1)

        self.x = x_1
        self.y = y_1
        self.theta = theta_1

        return(x_1, y_1, theta_1)