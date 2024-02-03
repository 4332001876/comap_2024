
# Analytic Hierarchy Process
def AHP(matrix):
    # Step 1: Normalize the matrix
    n = len(matrix)
    for i in range(n):
        s = sum(matrix[i])
        for j in range(n):
            matrix[i][j] /= s

    # Step 2: Calculate the weight vector
    w = [0] * n
    for i in range(n):
        w[i] = sum(matrix[j][i] for j in range(n)) / n

    # Step 3: Calculate the consistency ratio
    lambda_max = sum(matrix[i][j] * w[j] for i in range(n) for j in range(n))
    consistency_index = (lambda_max - n) / (n - 1)
    random_index = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
    consistency_ratio = consistency_index / random_index[n - 1]

    return w, consistency_ratio