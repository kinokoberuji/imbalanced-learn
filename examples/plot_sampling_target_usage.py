"""
======================================================================
Usage of the ``sampling_target`` parameter for the different algorithm
======================================================================

This example shows the different usage of the parameter ``sampling_target`` for
the different family of samplers (i.e. over-sampling, under-sampling. or
cleaning methods).

"""

# Authors: Guillaume Lemaitre <g.lemaitre58@gmail.com>
# License: MIT

from collections import Counter

import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris

from imblearn.datasets import make_imbalance

from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.under_sampling import TomekLinks

print(__doc__)


def plot_pie(y):
    target_stats = Counter(y)
    labels = list(target_stats.keys())
    sizes = list(target_stats.values())
    explode = tuple([0.1] * len(target_stats))

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, shadow=True,
           autopct='%1.1f%%')
    ax.axis('equal')


###############################################################################
# Creation of an imbalanced data set from a balanced data set
###############################################################################

###############################################################################
# We will show how to use the parameter ``sampling_target`` when dealing with
# the ``make_imbalance`` function. For this function, this parameter accepts
# both dictionary and callable. When using a dictionary, each key will
# correspond to the class of interest and the corresponding value will be the
# number of samples desired in this class.

iris = load_iris()

print('Information of the original iris data set: \n {}'.format(
    Counter(iris.target)))
plot_pie(iris.target)

sampling_target = {0: 10, 1: 20, 2: 30}
X, y = make_imbalance(iris.data, iris.target, sampling_target=sampling_target)

print('Information of the iris data set after making it'
      ' imbalanced using a dict: \n sampling_target={} \n y: {}'
      .format(sampling_target, Counter(y)))
plot_pie(y)

###############################################################################
# You might required more flexibility and require your own heuristic to
# determine the number of samples by class and you can define your own callable
# as follow. In this case we will define a function which will use a float
# multiplier to define the number of samples per class.


def ratio_multiplier(y):
    multiplier = {0: 0.5, 1: 0.7, 2: 0.95}
    target_stats = Counter(y)
    for key, value in target_stats.items():
        target_stats[key] = int(value * multiplier[key])
    return target_stats


X, y = make_imbalance(iris.data, iris.target, sampling_target=ratio_multiplier)

print('Information of the iris data set after making it'
      ' imbalanced using a callable: \n sampling_target={} \n y: {}'
      .format(sampling_target, Counter(y)))
plot_pie(y)

###############################################################################
# Using ``sampling_target`` in resampling algorithm
###############################################################################

###############################################################################
# ``sampling_target`` has a ``float``
# ...................................
#
# ``sampling_target`` can be given a ``float``. For **under-sampling
# methods**, it corresponds to the ratio :math:`\\alpha_{us}` defined by
# :math:`N_{rM} = \\alpha_{us} \\times N_{m}` where :math:`N_{rM}` and
# :math:`N_{m}` are the number of samples in the majority class after
# resampling and the number of samples in the minority class, respectively.

# select only 2 classes since the ratio make sense in this case
binary_mask = np.bitwise_or(y == 0, y == 2)
binary_y = y[binary_mask]
binary_X = X[binary_mask]

sampling_target = 0.8

rus = RandomUnderSampler(sampling_target=sampling_target)
X_res, y_res = rus.fit_sample(binary_X, binary_y)
print('Information of the iris data set after making it '
      'balanced using a float and an under-sampling method: \n '
      'sampling_target={} \n y: {}'
      .format(sampling_target, Counter(y_res)))
plot_pie(y_res)

###############################################################################
# For **over-sampling methods**, it correspond to the ratio
# :math:`\\alpha_{os}` defined by :math:`N_{rm} = \\alpha_{os} \\times N_{m}`
# where :math:`N_{rm}` and :math:`N_{M}` are the number of samples in the
# minority class after resampling and the number of samples in the majority
# class, respectively.

ros = RandomOverSampler(sampling_target=sampling_target)
X_res, y_res = ros.fit_sample(binary_X, binary_y)
print('Information of the iris data set after making it '
      'balanced using a float and an over-sampling method: \n '
      'sampling_target={} \n y: {}'
      .format(sampling_target, Counter(y_res)))
plot_pie(y_res)

###############################################################################
# ``sampling_target`` has a ``str``
# .................................
#
# ``sampling_target`` can be given as a string which specify the class targeted
# by the resampling. With under- and over-sampling, the number of samples will
# be equalized.

sampling_target = 'not minority'

rus = RandomUnderSampler(sampling_target=sampling_target)
X_res, y_res = rus.fit_sample(X, y)
print('Information of the iris data set after making it '
      'balanced by under-sampling: \n sampling_target={} \n y: {}'
      .format(sampling_target, Counter(y_res)))
plot_pie(y_res)

sampling_target = 'not majority'

ros = RandomOverSampler(sampling_target=sampling_target)
X_res, y_res = ros.fit_sample(X, y)
print('Information of the iris data set after making it '
      'balanced by over-sampling: \n sampling_target={} \n y: {}'
      .format(sampling_target, Counter(y_res)))
plot_pie(y_res)

###############################################################################
# With **cleaning method**, the number of samples in each class will not be
# equalized even if targeted.

sampling_target = 'not minority'
tl = TomekLinks(sampling_target)
X_res, y_res = tl.fit_sample(X, y)
print('Information of the iris data set after making it '
      'balanced by cleaning sampling: \n sampling_target={} \n y: {}'
      .format(sampling_target, Counter(y_res)))
plot_pie(y_res)

###############################################################################
# ``sampling_target`` has a ``dict``
# .................................
#
# When ``sampling_target`` is a ``dict``, the keys correspond to the targeted
# classes. The values correspond to the desired number of samples for each
# targeted class. This is working for both **under- and over-sampling**
# algorithms but not for the **cleaning algorithms**. Use a ``list`` instead.


sampling_target = {0: 10, 1: 15, 2: 20}

rus = RandomUnderSampler(sampling_target=sampling_target)
X_res, y_res = rus.fit_sample(X, y)
print('Information of the iris data set after making it '
      'balanced by under-sampling: \n sampling_target={} \n y: {}'
      .format(sampling_target, Counter(y_res)))
plot_pie(y_res)

sampling_target = {0: 25, 1: 35, 2: 47}

ros = RandomOverSampler(sampling_target=sampling_target)
X_res, y_res = ros.fit_sample(X, y)
print('Information of the iris data set after making it '
      'balanced by over-sampling: \n sampling_target={} \n y: {}'
      .format(sampling_target, Counter(y_res)))
plot_pie(y_res)

###############################################################################
# ``sampling_target`` has a ``list``
# ..................................
#
# When ``sampling_target`` is a ``list``, the list contains the targeted
# classes. It is used only for **cleaning methods** and raise an error
# otherwise.

sampling_target = [0, 1, 2]
tl = TomekLinks(sampling_target=sampling_target)
X_res, y_res = tl.fit_sample(X, y)
print('Information of the iris data set after making it '
      'balanced by cleaning sampling: \n sampling_target={} \n y: {}'
      .format(sampling_target, Counter(y_res)))
plot_pie(y_res)

###############################################################################
# ``sampling_target`` has a callable
# ..................................
#
# When callable, function taking ``y`` and returns a ``dict``. The keys
# correspond to the targeted classes. The values correspond to the desired
# number of samples for each class.


def ratio_multiplier(y):
    multiplier = {1: 0.7, 2: 0.95}
    target_stats = Counter(y)
    for key, value in target_stats.items():
        if key in multiplier:
            target_stats[key] = int(value * multiplier[key])
    return target_stats


X_res, y_res = (RandomUnderSampler(sampling_target=ratio_multiplier)
                .fit_sample(X, y))

print('Information of the iris data set after balancing using a callable'
      ' mode:\n ratio={} \n y: {}'.format(sampling_target, Counter(y_res)))
plot_pie(y_res)

plt.show()
