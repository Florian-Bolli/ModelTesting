from contextlib import suppress
from tensorflow.python.eager.monitoring import Buckets
from racing.car import Car
from racing.track import Track
from mppi_mpc.car_controller import CarController
from constants import *
from globals import *
import matplotlib.pyplot as plt
import numpy as np
import shapely.geometry as geom


from tqdm import trange


track = Track()
car = Car(track)

truth_controller = CarController(track=track, predictor="odeint")
euler_controller = CarController(track=track, predictor="euler")
nn_controller_1 = CarController(track=track, predictor="nn", model_name="Dense-128-128-128-128-invariant-10")
nn_controller_2 = CarController(track=track, predictor="nn", model_name="Dense-128-128-128-128-small")

# list of x1,x2,x3,x4,x5,x6,x7,u1,u2
validation_data = np.loadtxt('ExperimentRecordings/Dataset-1/Test/Test.csv{}'.format(""), delimiter=',', skiprows=5)
validation_data = validation_data[:100] #limit data


np.set_printoptions(precision=5, suppress = True)

def evaluate_step_predictions():
    euler_errors = []
    nn1_errors = []
    nn2_errors = []

    for line in validation_data:
        initial_state = line[1:8]
        control_input = line[8:10]

        res_0 = truth_controller.simulate_step(initial_state, control_input)
        res_1 = euler_controller.simulate_step(initial_state, control_input)
        res_2 = nn_controller_1.simulate_step(initial_state, control_input)
        res_3 = nn_controller_2.simulate_step(initial_state, control_input)


        # error_1 = np.square(res_1 - res_0)
        # error_2 = np.square(res_2 - res_0)
        # error_3 = np.square(res_3 - res_0)

        error_1 = np.abs(res_1 - res_0)
        error_2 = np.abs(res_2 - res_0)
        error_3 = np.abs(res_3 - res_0)

        
        euler_errors.append(error_1)
        nn1_errors.append(error_2)
        nn2_errors.append(error_3)

    euler_errors = np.array(euler_errors)
    nn1_errors = np.array(nn1_errors)
    nn2_errors = np.array(nn2_errors)

    euler_error_mean = np.mean(euler_errors, axis=0)
    nn1_error_mean = np.mean(nn1_errors, axis=0)
    nn2_error_mean = np.mean(nn2_errors, axis=0)

    euler_error_min = np.min(euler_errors, axis=0)
    nn1_error_min = np.min(nn1_errors, axis=0)
    nn2_error_min = np.min(nn2_errors, axis=0)

    euler_error_max = np.max(euler_errors, axis=0)
    nn1_error_max = np.max(nn1_errors, axis=0)
    nn2_error_max = np.max(nn2_errors, axis=0)



    print("Euler Step Errors Min:", euler_error_min)
    print("Euler Step Errors Max:", euler_error_max)
    print("Euler Step Errors Mean:", euler_error_mean)
    print("NN1 Step Errors Min:", nn1_error_min)
    print("NN1 Step Errors Max:", nn1_error_max)
    print("NN1 Step Errors Mean:", nn1_error_mean)
    print("NN2 Step Errors Min: ", nn2_error_min)
    print("NN2 Step Errors Max:", nn2_error_max)
    print("NN2 Step Errors mean:", nn2_error_mean)

def evaluate_trajectory_predictions():
    euler_errors = []
    nn1_errors = []
    nn2_errors = []

   

    for i in trange(len(validation_data) - NUMBER_OF_STEPS_PER_TRAJECTORY):
        initial_state = validation_data[i][1:8]
        control_inputs = validation_data[i:i+20, 8:10]

        truth_controller.set_state(initial_state)
        euler_controller.set_state(initial_state)
        nn_controller_1.set_state(initial_state)
        nn_controller_2.set_state(initial_state)

        res_0 = truth_controller.simulate_trajectory(control_inputs)[0]
        res_1 = euler_controller.simulate_trajectory(control_inputs)[0]
        res_2 = nn_controller_1.simulate_trajectory(control_inputs)[0]
        res_3 = nn_controller_2.simulate_trajectory(control_inputs)[0]

        error_1 = 0
        error_2 = 0
        error_3 = 0

        # Accumulated error
        # for i in range(NUMBER_OF_STEPS_PER_TRAJECTORY):
            # error_1 += np.square(res_1[i] - res_0[i])
            # error_2 += np.square(res_2[i] - res_0[i])
            # error_3 += np.square(res_3[i] - res_0[i])

        error_1 = np.abs(res_1[NUMBER_OF_STEPS_PER_TRAJECTORY] - res_0[NUMBER_OF_STEPS_PER_TRAJECTORY])
        error_2 = np.abs(res_2[NUMBER_OF_STEPS_PER_TRAJECTORY] - res_0[NUMBER_OF_STEPS_PER_TRAJECTORY])
        error_3 = np.abs(res_3[NUMBER_OF_STEPS_PER_TRAJECTORY] - res_0[NUMBER_OF_STEPS_PER_TRAJECTORY])

        euler_errors.append(error_1)
        nn1_errors.append(error_2)
        nn2_errors.append(error_3)

    euler_errors = np.array(euler_errors)
    nn1_errors = np.array(nn1_errors)
    nn2_errors = np.array(nn2_errors)

    euler_error_mean = np.mean(euler_errors, axis=0)
    nn1_error_mean = np.mean(nn1_errors, axis=0)
    nn2_error_mean = np.mean(nn2_errors, axis=0)

    euler_error_min = np.min(euler_errors, axis=0)
    nn1_error_min = np.min(nn1_errors, axis=0)
    nn2_error_min = np.min(nn2_errors, axis=0)


    euler_error_max = np.max(euler_errors, axis=0)
    nn1_error_max = np.max(nn1_errors, axis=0)
    nn2_error_max = np.max(nn2_errors, axis=0)



    print("Euler Trajectory Errors Min:", euler_error_min)
    print("Euler Trajectory Errors Max:", euler_error_max)
    print("Euler Trajectory Errors Mean:", euler_error_mean)
    print("NN1 Trajectory Errors Min:", nn1_error_min)
    print("NN1 Trajectory Errors Max:", nn1_error_max)
    print("NN1 Trajectory Errors Mean:", nn1_error_mean)
    print("NN2 Trajectory Errors Min: ", nn2_error_min)
    print("NN2 Trajectory Errors Max:", nn2_error_max)
    print("NN2 Trajectory Errors mean:", nn2_error_mean)




def evaluate_distance_cost():
    np.set_printoptions(precision=5, suppress = True)

    # data is saved as list of x1,x2,x3,x4,x5,x6,x7,u1,u2

    positions_euler = np.loadtxt('ExperimentRecordings/euler.csv{}'.format(""), delimiter=',', skiprows=5)[:,1:3]
    positions_nn_1 = np.loadtxt('ExperimentRecordings/nn-large.csv{}'.format(""), delimiter=',', skiprows=5)[:,1:3]
    positions_nn_2 = np.loadtxt('ExperimentRecordings/nn-small.csv{}'.format(""), delimiter=',', skiprows=5)[:,1:3]

    positions_euler = geom.LineString(positions_euler)

    distances_1 = []
    for i in range(1,len(positions_nn_1)):
        point = geom.Point(positions_nn_1[i])
        distance = positions_euler.distance(point)
        distances_1.append(distance)

    print("NN1 Mean: ", np.mean(distances_1))
    print("NN1 Min: ", np.min(distances_1))
    print("NN1 Max: ", np.max(distances_1))



    distances_2 = []
    for i in range(1,len(positions_nn_2)):
        point = geom.Point(positions_nn_2[i])
        distance = positions_euler.distance(point)
        distances_2.append(distance)

    print("NN2 Mean: ", np.mean(distances_2))
    print("NN2 Min: ", np.min(distances_2))
    print("NN2 Max: ", np.max(distances_2))


if __name__ == "__main__":

    # evaluate_step_predictions()
    # evaluate_trajectory_predictions()
    evaluate_distance_cost()