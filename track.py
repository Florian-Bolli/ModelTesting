import math
import numpy as np

from constants import *

M_TO_PIXEL = 0.1

def squared_distance(p1, p2):
    squared_distance = abs(p1[0] - p2[0]) ** 2 + abs(p1[1] - p2[1]) ** 2
    return squared_distance



class Track:

    def __init__(self):
        # self.waypoints_x = 0.1 * np.array(oval_points_x)
        # self.waypoints_y = 0.1 *  np.array(oval_points_y)
        self.waypoints_x = M_TO_PIXEL * np.array(track_2_points_x)
        self.waypoints_y = M_TO_PIXEL *  np.array(track_2_points_y)
        self.waypoints = [[self.waypoints_x[i], self.waypoints_y[i]] for i in range(len(self.waypoints_x))]
        self.initial_position = self.waypoints[0]



    
    def distance_to_track(self, p):
        min_distance = 100000
        waypoint_index = 0
        for i in range(len(self.waypoints_x)):
            waypoint = [self.waypoints_x[i], self.waypoints_y[i]]
            dist = squared_distance(p, waypoint)
            if(dist < min_distance):
                min_distance = dist
                waypoint_index = i
        print("waypoint index", waypoint_index)        
        return math.sqrt(min_distance)

    def get_closest_index(self, p):

        min_distance = 100000
        waypoint_index = 0
        for i in range(len(self.waypoints_x)):
            waypoint = [self.waypoints_x[i], self.waypoints_y[i]]
            dist = squared_distance(p, waypoint)
            if(dist < min_distance):
                min_distance = dist
                waypoint_index = i
        return waypoint_index
    

    def distance_to_waypoint(self, p, waypoint_index):
        waypoint = [self.waypoints_x[waypoint_index], self.waypoints_y[waypoint_index]]
        dist = squared_distance(p, waypoint)
        return math.sqrt(dist)

   

    def draw_track(self):
        plt.scatter(self.waypoints_x,self.waypoints_y)

        interpolation_length = 100
        w_x = self.waypoints_x
        w_y = self.waypoints_y

        plt.savefig("track.png")



