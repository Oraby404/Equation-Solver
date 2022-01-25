import numpy
import re


class Methods:

    def __init__(self, n, es, max_iterations, str, X=None):

        mylist = [0] * (len(str))

        for i in range(len(str)):
            mylist[i] = re.split("[xyzb]", str[i])

        # ---------------------------added----------------------------

        A = numpy.array(mylist)
        A = numpy.delete(A, -1, axis=1)
        for iy, ix in numpy.ndindex(A.shape):
            A[iy][ix] = eval(A[iy, ix])
        A = numpy.asarray(A, dtype=numpy.float64, order='C')

        B = A[:, -1]
        B = B[numpy.newaxis].T

        self.A = A
        self.B = B

        # A , B and X are from the text file
        self.order = n - 1  # starts from  0
        # ARRAY OF EQUATIONS PARSE IT TO GET A B ARRAYS
        # ARRAY OF INIT
        self.X = X

        self.equations_matrix = numpy.concatenate((self.A, self.B), axis=1)
        self.solutions = numpy.zeros(n)
        self.max_iterations = max_iterations
        self.es = es
        self.ea = 0

        ###############################################################################

    def parse(self, str):
        self.str = str

        mylist = [0] * (len(str))
        for i in range(len(str)):
            mylist[i] = re.split("[xyzb]", str[i])

        newList = [0] * (len(mylist))
        for l in range(len(mylist)):
            newList[l] = mylist[l][3]
        return mylist, newList

    def gauss_elimination(self):
        # forward elimination
        # for every unknown ( a , b ,c ...)
        for k in range(0, self.order):
            # for each equation
            for i in range(k + 1, self.order + 1):
                mul_factor = self.equations_matrix[i, k] / self.equations_matrix[k, k]
                # for every element in this equation
                for j in range(k + 1, self.order + 2):
                    # start with j = 0 in case you want to get an upper triangular matrix
                    self.equations_matrix[i, j] = self.equations_matrix[i, j] - (
                            mul_factor * self.equations_matrix[k, j])

        # backward elimination
        n = self.order
        self.solutions[n] = self.equations_matrix[n, n + 1] / self.equations_matrix[n, n]
        # for each equation
        for i in range(n - 1, -1, -1):
            sum_a = self.equations_matrix[i, n + 1]  # b of i
            for j in range(i + 1, n + 1):
                sum_a = sum_a - (self.equations_matrix[i, j] * self.solutions[j])
            self.solutions[i] = sum_a / self.equations_matrix[i, i]

    ###############################################################################

    def lu_decomposition(self):
        # decompose
        # for every unknown ( a , b ,c ...)
        for k in range(0, self.order):
            # for each equation
            for i in range(k + 1, self.order + 1):
                mul_factor = self.A[i, k] / self.A[k, k]
                self.A[i, k] = mul_factor  # L is the lower triangular matrix in A (instead of zeroes to save space)
                # for every element in this equation
                for j in range(k + 1, self.order + 1):
                    self.A[i, j] = self.A[i, j] - (mul_factor * self.A[k, j])

        # forward elimination
        # Convert B into D
        n = self.order
        for i in range(1, n + 1):
            sum_a = self.B[i]
            for j in range(0, i):
                sum_a = sum_a - (self.A[i, j] * self.B[j])
            self.B[i] = sum_a

        # backward elimination
        self.solutions[n] = self.B[n] / self.A[n, n]
        # for each equation
        for i in range(n - 1, -1, -1):
            sum_a = 0
            for j in range(i + 1, n + 1):
                sum_a = sum_a + (self.A[i, j] * self.solutions[j])
            self.solutions[i] = (self.B[i] - sum_a) / self.A[i, i]

    ###############################################################################

    # it
    def gauss_jordan(self):
        # forward elimination
        # for every unknown ( a , b ,c ...) plus B
        for k in range(0, self.order + 1):
            # normalize
            self.equations_matrix[k] /= self.equations_matrix[k, k]
            #  print(self.equations_matrix[k])

            # for each equation
            for i in range(0, self.order + 1):
                if i != k:
                    mul_factor = self.equations_matrix[i, k]
                    # for every element in this equation
                    for j in range(k + 1, self.order + 2):
                        # start with j = 0 in case you want to get an identity matrix on the left
                        self.equations_matrix[i, j] = self.equations_matrix[i, j] - (
                                mul_factor * self.equations_matrix[k, j])

        for b in range(0, self.order + 1):
            self.solutions[b] = self.equations_matrix[b, self.order + 1]

    ###############################################################################

    def gauss_seidel(self):

        for iteration in range(1, self.max_iterations + 1):
            # for every unknown (x1 , x2 , x3 ...)
            for i in range(0, self.order + 1):
                # sum of the terms
                sum_x = self.B[i]
                for j in range(0, self.order + 1):
                    if i != j:
                        sum_x = sum_x - (self.A[i, j] * self.X[j])
                self.X[i] = sum_x / self.A[i, i]

    ###############################################################################


# str = ["3x+2y+1z-6b", "2x+3y+0z-7b", "0x+0y+2z-4b"]
str = ["2x+1y+4z+1b", "1x+2y+3z+1.5b", "4x-1y+2z+2b"]
# str = ['a+b+c', '5a+66b+2c', '6a-2d+4v']
my_method = Methods(3, 0.001, 10, str)
# my_method.A = A
# my_method.B = B

my_method.gauss_elimination()
print(my_method.solutions)

# my_method.lu_decomposition()
# print(my_method.solutions)


# my_method.gauss_jordan()
# print(my_method.solutions)

# my_method.gauss_seidel()
# print(my_method.X)
