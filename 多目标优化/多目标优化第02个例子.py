# Mar 1, 2022
# Modified by Dr. XU
from pyomo.environ import *
from pyomo.opt import SolverFactory
import numpy as np
import numpy.linalg as la

## -------------------------------- ##

np.set_printoptions(precision = 2)

mat_input = np.array([[ 5, 0.7, 100],
                      [ 10, 0.6, 80 ],
                      [ 3 , 0.5, 127],
                      [ 4, 1, 90] ])

## -------------------------------- ##
def _norm_matrix( mat ):
    '''
    L2 norm
    '''
    mat_tmp = mat

    # number of columns
    _N = len( mat[0] )

    for j in range( _N ):
        _norm = la.norm(mat[:,j])
        mat_tmp[:,j]  = mat[:,j] / _norm

    return mat_tmp
## -------------------------------- ##

mat_new = _norm_matrix( mat_input )

print('-------------------------')
print('The new matrix is ')
print(mat_new)
print('-------------------------')

## -------------------------------- ##


N = 4
I = range(1, N+1)
M = 2 # number of multi-objections
J = range(1, M+1)
# 注意大小写
m = ConcreteModel()

# m.x = Var(I, domain=NonNegativeReals)
m.x = Var(I, domain=NonNegativeIntegers)
m.y = Var(J, domain=NonNegativeReals)
m.z = Var( domain=NonNegativeReals)
# Reals, PositiveReals, NonNegativeReals
# Integers,  PositiveIntegers, NegativeIntegers
# Binary

m.con01 = Constraint(expr= 0.41*m.x[1] + 0.82*m.x[2] + 0.24 * m.x[3] +  0.33 * m.x[4] <= 20 )

# m.con02 = Constraint(expr=100* m.x[1] + 80*m.x[2] + 127 * m.x[3] + 90 * m.x[4] >= 293 )
# m.con03 = Constraint(expr=0.5 * m.x[1] + 0.4 *m.x[2] + 0.63 * m.x[3] + 0.45 * m.x[4] >= 40 )


m.con04 = Constraint(expr = m.y[1] == 41.41- ( 0.48*m.x[1] + 0.41*m.x[2] + 0.35 * m.x[3] + 0.69 * m.x[4]) )
m.con05 = Constraint(expr = m.y[2] == 52.29- ( 0.5 * m.x[1] + 0.4 *m.x[2] + 0.63 * m.x[3] + 0.45 * m.x[4]) )
m.con06 = Constraint( expr = 0.65 * m.y[1] <= m.z)
m.con07 = Constraint( expr = 0.35 * m.y[2] <= m.z)

m.obj = Objective(expr= m.z , sense = minimize)

# m.obj = Objective(expr= 0.5 * m.x[1] + 0.4 *m.x[2] + 0.63 * m.x[3] + 0.45 * m.x[4], sense = maximize)
# m.obj = Objective(expr= 0.48*m.x[1] + 0.41*m.x[2] + 0.35 * m.x[3] + 0.69 * m.x[4], sense = maximize)
# m.obj = Objective(expr= 0.7*(0.48*m.x[1] + 0.41*m.x[2] + 0.35 * m.x[3] + 0.69 * m.x[4] ) + 0.3* (0.5 * m.x[1] + 0.4 *m.x[2] + 0.63 * m.x[3] + 0.45 * m.x[4] ), sense = maximize)
# m.obj = Objective(expr= 0.65*( 41.41 - (0.48*m.x[1] + 0.41*m.x[2] + 0.35 * m.x[3] + 0.69 * m.x[4] )) + 0.35* ( 52.29  - (0.5 * m.x[1] + 0.4 *m.x[2] + 0.63 * m.x[3] + 0.45 * m.x[4] )), sense = minimize)
# m.obj = Objective(expr= 0.65*( 41.41 - (0.48*m.x[1] + 0.41*m.x[2] + 0.35 * m.x[3] + 0.69 * m.x[4] ))**2  + 0.35* ( 52.29  - (0.5 * m.x[1] + 0.4 *m.x[2] + 0.63 * m.x[3] + 0.45 * m.x[4] ))**2, sense = minimize)

# m.obj = Objective(expr= 0.65*m.y[1] + 0.35*m.y[2] , sense = minimize)

# opt = SolverFactory('cplex', executable='/Applications/CPLEX_Studio201/cplex/bin/x86-64_osx/cplex')
opt = SolverFactory('glpk')
# opt = SolverFactory('mosek')
# opt = SolverFactory('gurobi')
# opt.options['NonConvex'] = 2
opt.solve(m, tee=True)
m.pprint()

m.display()

print('---------------------------')
print( f'The objective is {value(m.obj)}' )
print('---------------------------')