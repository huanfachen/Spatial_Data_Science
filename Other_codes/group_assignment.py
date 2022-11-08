# Author: Huanfa Chen
# Last update: 8 Nov, 2022
# This code splits K students into groups of n_group_size and a few groups of n_group_size - 1 (if K is not divisible by n_group_size)
# Most groups will have four students. There will likely be some groups of 3 if the number of students is not divisible by 4

import numpy as np
import pandas as pd
import scipy.optimize
# require scipy > 1.9

# problem settings - can be custom to your problem
# K
n_student = 116 
n_group_size = 4
# random seed to guarantee reproducibility
random_seed = 1023

# get the number of groups of size n_group_size and the number of groups of size n_group_size-1
# this is a integer programming problem
# maximise a
# s.t. 
# n_group_size * a + (n_group_size - 1) * b = n_student 
# a >= 0
# b >= 0
# a,b is integer

c = [-1, 0]
A = [[n_group_size, n_group_size-1]]
b = [n_student]
x0_bounds = (0, None)
x1_bounds = (0, None)
res = scipy.optimize.linprog(
    c, A_eq=A, b_eq=b, bounds=(x0_bounds, x1_bounds),
    integrality=[1, 1],
    options={"disp": True})

number_group_full_size, number_group_one_less = int(res.x[0]), int(res.x[1])

list_group_number = np.concatenate(
    [np.repeat(np.arange(number_group_full_size), n_group_size),
     np.repeat(np.arange(number_group_full_size, number_group_full_size + number_group_one_less), n_group_size - 1)
    ]
)

# generate random number
np.random.seed(random_seed)
# randomisation
np.random.shuffle(list_group_number)

# validation
unique, counts = np.unique(list_group_number, return_counts=True)
assert np.min(unique) == 0
assert np.min(counts) >= n_group_size - 1
assert np.max(counts) == n_group_size

# print the output. Can be combined with other datasets
print("The random group assignment")
print(list_group_number)