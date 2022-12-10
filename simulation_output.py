import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from population_Control import *
class simulation():
    def __init__(self, grid_dimension_x = [-50, 50], grid_dimension_y = [-50, 50], each_squ = [15, 15]):
        self.image = np.ones(((grid_dimension_x[1] - grid_dimension_x[0])*each_squ[0], (grid_dimension_y[1] - grid_dimension_y[0])*each_squ[1], 3), dtype=np.int16)
        self.image[:, :, 0] = 0
        self.image[:, :, 1] = 0
        self.image[:, :, 2] = 0
        
        self.each_squ = each_squ
        self.grid_dimension_x = grid_dimension_x
        self.grid_dimension_y = grid_dimension_y
    def colored_specific_sq(self, x = 0, y = 0):
        neg_x0 = 1
        neg_y0 = 1
        neg_x1 = 1
        neg_y1 = 1
        if x > 0:
            neg_x0 = -1
            neg_x1 = 0
        else:
            neg_x0 = 0
            neg_x1 = 1
        if y > 0:
            neg_y0 = -1
            neg_y1 = 0
        else:
            neg_y0 = 0
            neg_y1 = 1
        for i in np.arange(self.image.shape[0]/2 + x*self.each_squ[0] + neg_x0 * self.each_squ[0], self.image.shape[0]/2 + x*self.each_squ[0] + neg_x1 * self.each_squ[0], 1):
            for j in np.arange(self.image.shape[1]/2 + y*self.each_squ[1] + neg_y0 * self.each_squ[1], self.image.shape[1]/2 + y*self.each_squ[1] + neg_y1 * self.each_squ[1], 1):
                self.image[int(j), int(i), :] = (240, 50, 230)
    def draw_grid(self):
        for i in np.arange(0, self.image.shape[0], self.each_squ[0]):
            cv.line(self.image, [i, 0], [i, self.image.shape[1]], (50, 50, 50), 1)
        for i in np.arange(0, self.image.shape[1], self.each_squ[1]):
            cv.line(self.image, [0, i], [self.image.shape[0], i], (50, 50, 50), 1)
    def draw_arrow(self, x = [-10, 20], y = [-10, 30], color = (255, 0, 0)):
        
        neg_x0 = 1
        neg_y0 = 1
        neg_x1 = 1
        neg_y1 = 1
        if x[0] > 0:
            neg_x0 = -1/2
        else:
            neg_x0 = 1/2
        if y[0] > 0:
            neg_y0 = -1/2
        else:
            neg_y0 = 1/2


        if x[1] > 0:
            neg_x1 = -1/2
        else:
            neg_x1 = 1/2
        if y[1] > 0:
            neg_y1 = -1/2
        else:
            neg_y1 = 1/2

        cv.arrowedLine(self.image, 
        [int(self.image.shape[0]/2 + x[0]*self.each_squ[0] + neg_x0 * self.each_squ[0]), int(self.image.shape[1]/2 + y[0]*self.each_squ[1] + neg_y0 * self.each_squ[1])], 
        [int(self.image.shape[0]/2 + x[1]*self.each_squ[0] + neg_x1 * self.each_squ[0]), int(self.image.shape[1]/2 + y[1]*self.each_squ[1] + neg_y1 * self.each_squ[1])], 
        (int(color[0]), int(color[1]), int(color[2])), 2, cv.LINE_4, 0, 0.025)

# pop_control_obj = pop_control(100)
# pop_control_obj.creat_population_prob1()
# simulation_obj = simulation()
# simulation_obj.draw_grid()
# for i in range(len(pop_control_obj.XYDemand[0][:])):
#     simulation_obj.colored_specific_sq(pop_control_obj.XYDemand[0][i], pop_control_obj.XYDemand[1][i])
# simulation_obj.draw_arrow(x = [pop_control_obj.XYDemand[0][:], pop_control_obj.XYDemand[0][:]], y = [pop_control_obj.XYDemand[1][9], pop_control_obj.XYDemand[1][10]])

# # simulation_obj.draw_arrow(x = [-49, 49], y = [-49, 49])
# # simulation_obj.colored_specific_sq(x = -49, y = -10)
# # # simulation_obj.colored_specific_sq(x = 50, y = 50)
# # simulation_obj.colored_specific_sq(x = -49, y = -49)
# plt.imshow(simulation_obj.image)
# plt.show()