import sys

sys.path.append("../")

from targets import Himmelblau
from helpers import processing
import numpy as np


# Our benchmark is run using the following tuning parameters:
#
# Identity mass matrix
# Step lenght 0.1, slightly randomized
# No adaptive step length
# Number of steps 10, slightly randomized


initial_model = np.zeros((2, 1))
number_of_proposals = 10000

# Your sampling routine here -----------------------------------------------------------

# ...

# --------------------------------------------------------------------------------------


# Below find our implementation. Our software is not included --------------------------
# import hmc_tomography


# # For our code, every target is wrapped in a class
# class Himmelblau_cls(hmc_tomography.Distributions._AbstractDistribution):
#     dimensions = 2

#     def __init__(self, temperature=100):
#         self.temperature = temperature

#     def misfit(self, m):
#         return Himmelblau.misfit(m, temperature=self.temperature)

#     def gradient(self, m):
#         return Himmelblau.gradient(m, temperature=self.temperature)


# Our HMC sampling

# h5_filename = "basic_hmc/himmelblau_1_samples_basic_hmc.h5"

# hmc_tomography.Samplers.HMC().sample(
#     h5_filename,
#     Himmelblau_cls(),
#     proposals=number_of_proposals,
#     stepsize=0.1,
#     amount_of_steps=10,
#     autotuning=True,
#     initial_model=initial_model,
#     overwrite_existing_file=True,
# )

# with hmc_tomography.Samples(h5_filename, burn_in=0) as samples_h5:
#     samples = samples_h5.numpy[:-1, :]  # Strip misfit from array
#     misfits = samples_h5.misfits

# np.save("basic_hmc/himmelblau_1_samples_basic_hmc.npy", samples)
# np.save("basic_hmc/himmelblau_1_misfits_basic_hmc.npy", misfits)

# Our Metropolis-Hastings sampling

# h5_filename = "basic_rwmh/himmelblau_1_samples_basic_rwmh.h5"

# hmc_tomography.Samplers.RWMH().sample(
#     h5_filename,
#     Himmelblau_cls(),
#     proposals=number_of_proposals
#     * 20,  # MH is about 20x faster than HMC with 10 steps
#     stepsize=0.4,
#     autotuning=False,
#     online_thinning=20,
#     initial_model=initial_model,
#     overwrite_existing_file=True,
# )

# with hmc_tomography.Samples(h5_filename, burn_in=0) as samples_h5:
#     samples = samples_h5.numpy[:-1, :]  # Strip misfit from array
#     misfits = samples_h5.misfits

# np.save("basic_rwmh/himmelblau_1_samples_basic_rwmh.npy", samples)
# np.save("basic_rwmh/himmelblau_1_misfits_basic_rwmh.npy", misfits)

# --------------------------------------------------------------------------------------


# Make sure samples is a 2xnumber_of_proposals array of your samples.
samples = np.load("auto_hmc/himmelblau_1_samples_auto_hmc.npy")
misfits = np.load("auto_hmc/himmelblau_1_misfits_auto_hmc.npy")

import matplotlib.pyplot as plt

plt.figure(figsize=(6, 8))
plt.tight_layout()
plt.subplots_adjust(wspace=0.0, hspace=0.0)

hist1d_1_axis = plt.subplot(4, 2, 1)
hist2d_axis = plt.subplot(4, 2, 3)
hist1d_2_axis = plt.subplot(4, 2, 4)

misfit_axis = plt.subplot(4, 1, 4)

m0lower, m0upper, m1lower, m1upper = -6, 6, -6, 6

hist1d_1_axis.hist(samples[0, :], range=(m0lower, m0upper), bins=50)
hist1d_2_axis.hist(
    samples[1, :], range=(m1lower, m1upper), orientation="horizontal", bins=50
)

hist1d_1_axis.set_yticklabels([])
hist1d_1_axis.set_xticklabels([])
hist1d_2_axis.set_yticklabels([])
hist1d_2_axis.set_xticklabels([])
hist1d_2_axis.set_xlabel("Relative density")
hist1d_1_axis.set_ylabel("Relative density")

hist2d_axis.hist2d(
    samples[0, :],
    samples[1, :],
    range=[[m0lower, m0upper], [m1lower, m1upper]],
    bins=50,
)

hist2d_axis.set_xlabel("Dimension 0")
hist2d_axis.set_ylabel("Dimension 1")

misfit_axis.plot(misfits)
misfit_axis.set_ylabel("Misfit value")
misfit_axis.set_xlabel("Iteration")

plt.show()

samples_1 = np.load("basic_rwmh/himmelblau_1_samples_basic_rwmh.npy")
samples_2 = np.load("basic_hmc/himmelblau_1_samples_basic_hmc.npy")
samples_3 = np.load("auto_rwmh/himmelblau_1_samples_auto_rwmh.npy")
samples_4 = np.load("auto_hmc/himmelblau_1_samples_auto_hmc.npy")

plt.figure()

autocor_1 = processing.autocorrelation(samples_1[0, :])
autocor_2 = processing.autocorrelation(samples_2[0, :])
autocor_3 = processing.autocorrelation(samples_3[0, :])
autocor_4 = processing.autocorrelation(samples_4[0, :])

# The *20 is to correct for online thinning.
plt.plot(np.arange(10000), autocor_1, label="basic rwmh")
plt.plot(np.arange(10000) * 20, autocor_2, label="basic hmc")
plt.plot(np.arange(10000), autocor_3, label="autotuned rwmh")
plt.plot(np.arange(10000) * 20, autocor_4, label="autotuned hmc")

plt.xlim([0, 5e3])

plt.xlabel("Sample delay")
plt.ylabel("Autocorrelation")
plt.legend()

plt.show()
