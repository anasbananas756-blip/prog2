""" MA3.py

Student:
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
import numpy as np
import functools as ft
import concurrent.futures as future


def approximate_pi(n): # Ex1
    #n is the number of points
    # Write your code here

    print(n) # Prints n

    nc = 0 # Counter for number of points belonging to circle

    xlst = [] # list for x-coordinates of points outside circle
    ylst = [] # list for y-coordinates of points outside circle

    xc = [] # list for x-coordinates of points belonging to circle
    yc = [] # list for y-coordinates of points belonging to circle
    
    # Instead of using for loop to append, i think i couldve defined
    # the circle condition as a function and then used filter to make 
    # the lists.
    
    for i in range(n): # create n uniformly distr. points in xy-plane
        x = random.uniform(-1,1) # x-coordinate 
        y = random.uniform(-1,1) # y-coordinate
        if x**2 + y**2 <= 1: # Condition for point belonging to circle
            nc +=1 # Adds to the number of points belonging to circle
            xc.append(x) 
            yc.append(y)
        else: # The condition above isnt satisfied, ie the point does not belong to circle
            xlst.append(x)
            ylst.append(y)
             
    plt.scatter(xlst,ylst,marker='.',c='b') # Scatter all points outside circle
    plt.scatter(xc,yc,marker='.',c='red') # Scatter all points belonging to circle

    # Set equally long axes, taken from internet
    plt.xlim(-1, 1) 
    plt.ylim(-1, 1)
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')

    plt.savefig(f'{n} points') # Save image to png
    
    return 4*nc/n # Return approx. of pi

def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere 
    arr = np.random.uniform(-1,1,(d,n)) ** 2 # Generate n U distr. random vectors in d-space
    arr = ft.reduce(lambda x, y: x + y, arr) # Does what np.sum(axis=0) would do since reduce iterates over first axis
    nc = len(list(filter(lambda x : x <= 1, arr))) # Number of points belonging to circle
    return (2**d)*nc/n # V_c / V ≈ n_c / n


def hypersphere_exact(n,d): #Ex2, real value
    # n is the number of points
    # d is the number of dimensions of the sphere 
    return (m.pi**(d/2))/m.gamma(1 + (d/2))


#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=10):
      #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    start = pc()
    with future.ProcessPoolExecutor() as vol:
        results = vol.map(sphere_volume, [n]*np, [d]*np)
    end = pc()
    print(f'Parallell processes using pool executor took {end-start} seconds')
    return sum(results)/np
#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    start = pc()
    with future.ProcessPoolExecutor() as vol:
        results = vol.map(sphere_volume, [n//np]*np, [d]*np)
    end = pc()
    print(f'Parallell processes splitting data using pool executor took {end-start} seconds')
    return sum(results)
    
def main():
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        print(approximate_pi(n))
    
    #Ex2
    n = 100000
    d = 2
    print(sphere_volume(n,d))
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    print(sphere_volume(n,d))
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    #Ex3
    n = 100000
    d = 11
    V = 0 
    start = pc()
    for y in range(10):
        V += sphere_volume(n,d)
    stop = pc()
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print(f'Average volume: {V/10}')
    print("What is parallel time?")
    print(f'Average volume by parallelized computation: {sphere_volume_parallel1(n,d)}')
    '''
    Running the code on the arrhenius linux server, parallel code runs almost 5 times faster
    '''

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")
    print(f'Average volume by parallelized computation: {sphere_volume_parallel2(n,d)}')
    
    

if __name__ == '__main__':
	main()
