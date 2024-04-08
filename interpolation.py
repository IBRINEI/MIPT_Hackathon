import numpy as np

def interpolate(X, Y, new_size):
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