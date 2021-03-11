import numpy as np
import simplex_api

class ASM():
    #min 1/2x'Qx+B'x
    #Ax >= C
    def __init__(self,Q,B,A,C,equality_cons_num):
        self.Q = Q
        self.B = B
        self.A = A
        self.C = C
        self.working_set = []
        self.equality_set = []
        self.equality_cons_num = equality_cons_num
        for i in range(0,equality_cons_num):
            self.equality_set.append(i)

    def initial(self,equality_cons_num):
        left = np.zeros((self.A.shape[1],self.A.shape[1]))
        right = np.zeros(self.A.shape[1])
        left[0:equality_cons_num][:] = self.A[0:equality_cons_num][:]
        right[0:equality_cons_num] = self.C[0:equality_cons_num][0]
        left[equality_cons_num:][:] = np.random.rand(self.A.shape[1]-equality_cons_num,self.A.shape[1])
        right[equality_cons_num:] = np.random.rand(self.A.shape[1]-equality_cons_num)
        #print(np.array(left))
        #print(np.array(right))
        try:
            x = np.linalg.solve(left,right)
        except:
            x = self.initial(equality_cons_num)
        return x

    def initial3(self,equality_cons_num):
        #A1 = np.insert(self.A, 0, values=-self.A[0], axis=0)
        #C1 = np.insert(self.C,0,values=-self.C[0],axis=0).T[0]
        target = np.zeros(self.A.shape[1])
        simplex_init = simplex_api.Simplex(-self.A,-self.C.T[0], target, equal=None)
        matrix, ret_matrix, X = simplex_init.solve()
        #print('最优解为'.format(np.round(X[0: len(target)], 4)))
        #print('最优值是'.format(np.round(-ret_matrix[0][0], 4)))
        return X[0: len(target)]

    def KKT(self,right_up,upright,downleft,c):
        size = self.Q.shape[0]
        cons_num = len(self.equality_set+self.working_set)

        KKT_left = np.zeros((size+cons_num,size+cons_num))
        KKT_right = np.zeros(size+cons_num)

        KKT_left[:size,:size] = self.Q
        KKT_left[:size,size:] = -upright.T
        KKT_left[size:,:size] = -downleft
        
        KKT_right[:size] = -right_up
        KKT_right[size:] = c[:, 0]

        #print('KKT_left\n',KKT_left)
        #print('KKT_right\n',KKT_right)

        kkt_lambda = np.linalg.pinv(KKT_left) @ KKT_right
        return kkt_lambda

    def calculate_alpha(self,x,p):
        min_alpha = 1
        new_cons_index = -1
        for i in range(self.equality_cons_num,self.A.shape[0]):
            if i in self.working_set:
                continue
            else:
                ci = self.C[i]
                ai = self.A[i]
                ap = ai @ p
                if ap < 0:
                    temp = (ci - ai @ x)/ap
                    if temp < min_alpha:
                        min_alpha = temp
                        new_cons_index = i
                else:
                    continue
        return min_alpha,new_cons_index


    def solve(self):
        variable_num = self.Q.shape[0]

        self.x = self.initial3(self.equality_cons_num)
        #print('x',self.x)
        #iteration
        self.working_set.append(self.equality_cons_num)
        #print('equality_set',self.equality_set)
        #print('working_set',self.working_set)
        max_iteration = 100
        epilson = 1e-6

        for i in range(0,max_iteration):
            lag_right_up = (self.Q @ self.x + self.B.T)[0] #lagrange乘子右边 上部分
            #print('all',self.equality_set+self.working_set)
            lag_matrix_23 = self.A[self.equality_set+self.working_set] #lagrange乘子左边 右上左下部分
            #print("lag\n",lag_matrix_23)
            #print("working_set",self.working_set)
            c = np.zeros_like( self.C[self.equality_set+self.working_set] )
            #c = np.zeros((len(self.working_set),1))

            _lambda = self.KKT(lag_right_up,lag_matrix_23,lag_matrix_23,c)
            p = _lambda[0:variable_num]
            temp_lambda = _lambda[variable_num:]
            #print("num",variable_num+self.equality_cons_num)
            #print("temp_lambda",temp_lambda)

            if np.linalg.norm(np.abs(p), ord = 1) < epilson:
                if len(temp_lambda) == 0 or temp_lambda.min() >= 0:
                    break
                else:
                    #print('temp_lambda',temp_lambda)
                    index = np.argmin(temp_lambda)
                    #print('index',index)
                    del self.working_set[index]
                    self.working_set.sort()
            else:
                alpha,new_cons = self.calculate_alpha(self.x,p)
                self.x = self.x + alpha * p
                if alpha < 1:
                    if new_cons >= 0:
                        self.working_set.append(new_cons)
                        self.working_set.sort()

def main():
    Q = np.array([ [2.0,0.0], [0.0,2.0]])
    B = np.array([ [-2.0], [-5.0]])
    A = np.array([ [1.0, -2.0],[-1.0, -2.0,],[-1.0, 2.0],[1.0, 0.0],[0.0, 1.0] ])
    C = np.array( [ [-2.0], [-6.0], [-2.0], [3.0], [3.0] ] )
    print(Q)
    print(B)
    print(A)
    print(C)
    asm_test = ASM(Q, B, A, C,1)
    asm_test.solve()
    print("x",asm_test.x)
    print("working_set",asm_test.working_set)

if __name__ == "__main__":
    main()