import numpy as np
from scipy.optimize import linprog

c = np.array([40,90])
a = np.array([[9,7],[7,20]])
b = np.array([[56],[70]])
x1_bond = [0,None]
x2_bond = [0,None]
res = linprog(-c,A_ub=a,b_ub=b,bounds=(x1_bond,x2_bond),method='simplex')


# prog1
import pulp
my_lp_problem = pulp.LpProblem("My LP Problem", pulp.LpMaximize)
x = pulp.LpVariable('x', lowBound=0, cat='Continuous')  # cat = Integer / Binary
y = pulp.LpVariable('y', lowBound=2, cat='Continuous')

# 目标函数
my_lp_problem += 4 * x + 3 * y, "Z"

# Constraints
my_lp_problem += 2 * y <= 25 - x
my_lp_problem += 4 * y >= 2 * x - 8
my_lp_problem += y <= 2 * x - 5

my_lp_problem.solve()

for variable in my_lp_problem.variables():
    print ("{} = {}".format(variable.name, variable.varValue))
print(pulp.value(my_lp_problem.objective))

# prog2
my_lp_problem = pulp.LpProblem("My LP Problem", pulp.LpMaximize)
x1 = pulp.LpVariable('x1',lowBound=0,cat='Integer')
x2 = pulp.LpVariable('x2',lowBound=0,cat='Integer')

my_lp_problem += 4 * x1 + 90 * x2, "Z"

my_lp_problem += 9 * x1 + 7 * x2 <= 56
my_lp_problem += 7 * x1 + 20 * x2 <= 70

my_lp_problem.solve()

for variable in my_lp_problem.variables():
    print ("{} = {}".format(variable.name, variable.varValue))

print(pulp.value(my_lp_problem.objective))

