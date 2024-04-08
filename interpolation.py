import numpy as np
from scipy.interpolate import CubicSpline

def interpolate_lin(X, Y, new_size):
    # X, Y are old arrays, we rescale it to new_size
    # returns new X and Y with size = new_size
    X, Y = np.array(X), np.array(Y)
    argsX = X.argsort()
    X = X[argsX]
    Y = Y[argsX]
    old_size = X.shape[0]
    
    new_X = np.linspace(X.min(), X.max(), new_size)
    new_Y = np.zeros_like(new_X)
    new_Y[0] = Y[0]
    for j in range(len(new_X)):
        for i in range(old_size-1):
            if new_X[j] > X[i] and new_X[j] <= X[i+1]:
                new_Y[j] = Y[i] + (new_X[j] - X[i])*(Y[i+1]-Y[i])/(X[i+1]-X[i])
    new_Y[-1] = Y[-1]
    return new_X, new_Y

def average(Y, width):
    Yav = np.zeros_like(Y)
    for i in range(width):
        Yav[i] = np.mean(Y[:i+1])
    for i in range(width, Yav.shape[0]-width):
        Yav[i] = np.mean(Y[i-width:i+width])
    for i in range(Yav.shape[0]-width, Yav.shape[0]):
        Yav[i] = np.mean(Y[i:])
    return Yav

def interpolate_lin_av(X, Y, new_size, av_width):
    # X, Y are old arrays, we rescale it to new_size
    # awerages Y along 2*av_width+1 points
    # returns new X and Y with size = new_size
    X, Y = np.array(X), np.array(Y)
    argsX = X.argsort()
    X = X[argsX]
    Y = Y[argsX]
    old_size = X.shape[0]
    
    Y = average(Y, av_width)
    
    new_X = np.linspace(X.min(), X.max(), new_size)
    new_Y = np.zeros_like(new_X)
    new_Y[0] = Y[0]
    for j in range(len(new_X)):
        for i in range(old_size-1):
            if new_X[j] > X[i] and new_X[j] <= X[i+1]:
                new_Y[j] = Y[i] + (new_X[j] - X[i])*(Y[i+1]-Y[i])/(X[i+1]-X[i])
    new_Y[-1] = Y[-1]
    return new_X, new_Y

def interpolate_spline(X, Y, new_size):
    # X, Y are old arrays, we rescale it to new_size
    # returns new X and Y with size = new_size
    X, Y = np.array(X), np.array(Y)
    argsX = X.argsort()
    X = X[argsX]
    Y = Y[argsX]
    
    cs = CubicSpline(X, Y)
    
    new_X = np.linspace(X.min(), X.max(), new_size)
    new_Y = cs(new_X)
    
    return new_X, new_Y