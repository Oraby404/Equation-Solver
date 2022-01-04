import numpy


class Methods:

    def __init__(self, n, es, max_iterations):
        self.order = n - 1  # starts from  0

        # A , B and X are from the text file

        # self.A = numpy.zeros((n, n))
        self.A = numpy.array([[3, -0.1, -0.2], [0.1, 7, -0.3], [0.3, -0.2, 10]], dtype='float64')
        # self.B = numpy.zeros((n, 1))
        self.B = numpy.array([[7.85], [-19.3], [71.4]], dtype='float64')
        # initial values for gauss seidel
        self.X = numpy.zeros(n, dtype='float64')

        self.equations_matrix = numpy.concatenate((self.A, self.B), axis=1)
        self.solutions = numpy.zeros(n)
        self.max_iterations = max_iterations
        self.es = es
        self.ea = 0

        ###############################################################################

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


my_method = Methods(3, 0.001, 10)

# my_method.gauss_elimination()
# print(my_method.solutions)

# my_method.lu_decomposition()
# print(my_method.solutions)

# my_method.gauss_jordan()
# print(my_method.solutions)

my_method.gauss_seidel()
print(my_method.X)
