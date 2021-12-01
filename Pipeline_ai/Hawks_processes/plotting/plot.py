import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats
from tqdm.notebook import tqdm
from scipy import integrate

coef_Tmax = 1.1


def plot_cascade(cascade, Tmax=None):
    plt.stem(cascade[:, 0] / 60.0, cascade[:, 1], use_line_collection=True)
    plt.yscale("log")
    if Tmax is not None:
        plt.xlim(None, Tmax / 60)
    plt.xlabel("time (min)")
    plt.ylabel("magnitude (log)")


def counting_process(cascade, T=None):
    """
    Returns a 2D-array N such that N(:,0) contains time samples t and N(:,1) contains images by point process N(t)

    cascade -- 2D-array containing samples of the point process as returned by simulate_exp_hawkes_process
    T       -- 1D array containing time samples whose value N(t) has to be computed (if None defines T to cover the full cascade)
    """

    tks = cascade[:, 0]
    if T is None:
        Tmax = tks[-1] * coef_Tmax
        T = np.linspace(0, Tmax)
    N = np.zeros((len(T), 2))
    N[:, 0] = T
    for tk in tks:
        N[T >= tk, 1] += 1
    return N


def cond_intensity(params, history, T):
    """
    Returns a numpy 2D-array containing the conditional intensity of an exponential Hawkes process
    (first column is time, second is mapped intensity)

    params   -- parameter tuple (p,beta) of the Hawkes process
    history  -- (n,2) numpy array containing marked time points (t_i,m_i)
    T        -- 1D-array containing the input times for which the intensity must be computed
    """

    p, beta = params
    I = np.zeros((len(T), 2))
    I[:, 0] = T

    # For every marked point,
    for ti, mi in history:
        # Get all time indexes whose time is greater than ti
        J = T >= ti
        # Update the intensity for all times larger thanti
        I[J, 1] += mi * np.exp(-beta * (T[J] - ti))

    # Don't forget to multiply by p*beta
    I[:, 1] *= p * beta
    return I


def draw_intensity(params, history, Tmax=None, label=""):
    """
    Draws an intensity plot along the history

    params   -- parameter tuple (p,beta) of the Hawkes process
    history  -- (n,2) numpy array containing marked time points (t_i,m_i)
    Tmax     -- upper bound of the plot interval
    label    -- legend label
    """

    if Tmax is None:
        Tmax = history[-1, 0] * coef_Tmax
    T = np.linspace(-10.0, Tmax, 1000)
    I = cond_intensity(params, history, T)
    plt.plot(I[:, 0] / 60.0, I[:, 1], label=label)
    plt.plot(history[:, 0] / 60, np.zeros(len(history)), "o", color="red")
    plt.title("Process intensity")
    plt.xlabel("Time (min)")


def cumul_intensity(cond_intensity):
    """
    Returns a 2D array containing the cumulative intensity such that first column is time
    and second is mapped cumulative intensity up to given time.

    cond_intensity -- 2D-array as returned by cond_intensity function
    """

    T = cond_intensity[:, 0]
    I = cond_intensity[:, 1]

    C = np.empty_like(cond_intensity)
    C[:, 0] = T
    C[:, 1] = integrate.cumtrapz(I, T, initial=0)

    return C


def draw_cumul_intensity(params, history, Tmax=None, label=""):
    if Tmax is None:
        Tmax = history[-1, 0] * coef_Tmax
    T = np.linspace(-10.0, Tmax, 1000)
    I = cond_intensity(params, history, T)
    cumul = cumul_intensity(I)
    plt.plot(cumul[:, 0] / 60.0, cumul[:, 1], label=label)
    plt.xlabel("Time (min)")


def plot_predictions(estimator, params, cascade, alpha, mu):
    # Compute the predictions according to the estimator
    est_preds, est_LLs, est_params = predictions_from_estimator(
        estimator, cascade, alpha, mu
    )

    # Compute the predictions according to the true parameters
    preds = predictions(params, cascade, alpha, mu)

    # Compute the counting process
    N = counting_process(cascade)

    plt.plot(est_preds[:, 0] / 60, est_preds[:, 1], label="est")
    plt.plot(preds[:, 0] / 60, preds[:, 1], label="pred")
    plt.plot(N[:, 0] / 60, N[:, 1], label="N")
    plt.plot(cascade[:, 0] / 60, np.zeros(len(cascade)), "o", color="red")
    plt.ylim([0, N[-1, 1] * 3])
    plt.legend()

    return est_preds, est_LLs, est_params