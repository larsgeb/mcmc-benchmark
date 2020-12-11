import numpy as np


def autocorrelation(x):
    result = np.correlate(x - np.mean(x), x - np.mean(x), mode="full")
    return result[int(result.size / 2) :] / np.max(result)


def crosscorrelation(x, y):
    result = np.correlate(x - np.mean(x), y - np.mean(y), mode="full")
    return result[int(result.size / 2) :] / np.max(np.abs(result))
