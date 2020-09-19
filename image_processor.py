# Import Packages

def rotate_left_90_deg(matrix):
	rows = len(matrix)
	cols = len(matrix[0])
    for x in range(0, int(rows / 2)):           
        for y in range(x, cols-x-1):               
            temp = matrix[x][y]
            matrix[x][y] = matrix[y][cols-1-x]  
            matrix[y][cols-1-x] = matrix[rows-1-x][cols-1-y]
            matrix[rows-1-x][cols-1-y] = matrix[rows-1-y][x] 
            matrix[-1-y][x] = temp

def rotate_right_90_deg(matrix): 
    N = len(A[0]) 
    for i in range(N // 2): 
        for j in range(i, N - i - 1): 
            temp = A[i][j] 
            A[i][j] = A[N - 1 - j][i] 
            A[N - 1 - j][i] = A[N - 1 - i][N - 1 - j] 
            A[N - 1 - i][N - 1 - j] = A[j][N - 1 - i] 
            A[j][N - 1 - i] = temp 