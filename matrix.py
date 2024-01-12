def matrixQ(data, element_names, node_names):
    nodes = node_names
    unique_elements = element_names
    matrix_q = [[0] * (len(nodes) + 1) for _ in range(len(unique_elements) + 1)]

    for j in range(len(nodes)):
        matrix_q[0][j + 1] = nodes[j]

    for i in range(len(unique_elements)):
        matrix_q[i + 1][0] = unique_elements[i]
    
    for i in range(1, len(matrix_q)):
        for j in range(1, len(matrix_q[0])):
            element = matrix_q[i][0]
            node = matrix_q[0][j]
            if element in data[node]:
                matrix_q[i][j] = 1

    return matrix_q

def matrixR(matrix_q, element_names):
    num_elements = len(element_names)
    matrix_r = [[0] * (num_elements + 1) for _ in range(num_elements + 1)]

    for j in range(len(element_names)):
        matrix_r[0][j + 1] = element_names[j]

    for i in range(len(element_names)):
        matrix_r[i + 1][0] = element_names[i]

    for i in range(1, len(matrix_r)):
        for j in range(1, len(matrix_r[0])):
            if i == j:
                matrix_r[i][j] = -1
            else:
                matrix_r[i][j] = sum(1 for q1, q2 in zip(matrix_q[i][1:], matrix_q[j][1:]) if q1 == 1 and q2 == 1)

    return matrix_r