import numpy as np
np.set_printoptions(precision=4, suppress=True, threshold=np.inf)
class Simplex():
    def __init__(self,a,b,c,equal):
        self.a = a
        self.b = b
        self.c = c
        self.equal = equal
    def get_loose_matrix(self,matrix):
        row, col = matrix.shape
        loose_matrix = np.zeros((row, row + col))
        for i, _ in enumerate(loose_matrix):
            loose_matrix[i, 0: col] = matrix[i]
            loose_matrix[i, col + i] = 1.0  
        return loose_matrix
    def join_matrix(self,a, b, c):
        row, col = a.shape
        s = np.zeros((row + 1, col + 1))
        s[1:, 1:] = a  
        s[1:, 0] = b  
        s[0, 1: len(c) + 1] = c  
        return s
    def pivot_matrix(self,matrix, k, j):
        matrix[k] = matrix[k] / matrix[k][j]
        for i, _ in enumerate(matrix):
            if i != k:
                matrix[i] = matrix[i] - matrix[k] * matrix[i][j]
    def get_base_solution(self,matrix, base_ids):
        X = [0.0] * (matrix.shape[1])  
        for i, _ in enumerate(base_ids):
            X[base_ids[i]] = matrix[i + 1][0]
        return X
    def Laux(self,matrix, base_ids):
        l_matrix = np.copy(matrix)
        l_matrix = np.column_stack((l_matrix, [-1] * l_matrix.shape[0]))
        l_matrix[0, :-1] = 0.0
        l_matrix[0, -1] = 1
        k = l_matrix[1:, 0].argmin() + 1  
        j = l_matrix.shape[1] - 1   
        self.pivot_matrix(l_matrix, k=k, j=j)
        base_ids[k - 1] = j  
        l_matrix = self.simplex(l_matrix, base_ids)
        if l_matrix.shape[1] - 1 in base_ids:
            j = np.where(l_matrix[0, 1:] != 0)[0][0] + 1  
            k = base_ids.index(l_matrix.shape[1] - 1) + 1  
            self.pivot_matrix(l_matrix, k=k, j=j)   
            base_ids[k - 1] = j  
        return l_matrix, base_ids
    def resotr_from_Laux(self,l_matrix, z, base_ids):
        z_ids = np.where(z != 0)[0] - 1  
        restore_matrix = np.copy(l_matrix[:, 0:-1])  
        restore_matrix[0] = z  
        for i, base_v in enumerate(base_ids):
            if base_v in z_ids:
                restore_matrix[0] -= restore_matrix[0, base_v + 1] * restore_matrix[i + 1] 
        return restore_matrix
    def simplex(self,matrix, base_ids):
        matrix = matrix.copy()
        while matrix[0, 1:].min() < 0:
            j = np.where(matrix[0, 1:] < 0)[0][0] + 1
            k = np.array([matrix[i][0] / matrix[i][j] if matrix[i][j] > 0 else 0x7fff for i in range(1, matrix.shape[0])]).argmin() + 1
            if matrix[k][j] <= 0:
                return None, None
            self.pivot_matrix(matrix, k, j) 
            base_ids[k - 1] = j - 1 
        return matrix
    def solve(self):
        loose_matrix = self.get_loose_matrix(self.a)  
        if self.equal is not None:
            loose_matrix = np.insert(loose_matrix, 0, equal, axis=0)
        #print(loose_matrix)
        matrix = self.join_matrix(loose_matrix, self.b, self.c)  
        base_ids = list(range(len(self.c), len(self.b) + len(self.c)))  

        if matrix[:, 0].min() < 0:
            l_matrix, base_ids = self.Laux(matrix, base_ids)  
            if l_matrix is not None:
                matrix = self.resotr_from_Laux(l_matrix, matrix[0], base_ids)  
            else:
                return None, None, None
        ret_matrix = self.simplex(matrix, base_ids)  
        X = self.get_base_solution(ret_matrix, base_ids)  
        if ret_matrix is not None:
            return matrix, ret_matrix, X
        else:
            return None, None, None
if __name__ == '__main__':
    equal = None
    a = np.array([[-2, 5, -1], [1, 3, 1]])
    equal = [1, 1, 1] + [0] * a.shape[0]
    #print(equal)
    b = [7, -10, 12]
    c = [-2, -3, 5]
    simplex_init = Simplex(a, b, c, equal=equal)
    matrix, ret_matrix, X = simplex_init.solve()