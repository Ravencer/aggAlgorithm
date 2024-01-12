import numpy as np

def arrangeAlgorithm(matQ, matR, uniqElements, k=3, v=3, newNodes={}, currentNode=0, currentElem=''):
    
    if(len(uniqElements) < 1):
        return newNodes
    print(2)
    if(newNodes == {}):
        maxElem = chooseMax(matQ)
        newNodes['node' + str(currentNode)] = [maxElem]
        return arrangeAlgorithm(matQ, matR, uniqElements, k, v, newNodes, currentNode, maxElem)
    if(len((newNodes['node' + str(currentNode)])) < k):
        
        if(len((newNodes['node' + str(currentNode)])) < 1):
            maxElem = chooseMax(matQ)
            newNodes['node' + str(currentNode)] = maxElem
            return arrangeAlgorithm(matQ, matR, uniqElements, k, v, newNodes, currentNode, maxElem)
        # Находим дизъюнкции элементов с выбранным ранее
        disjunctions = []
        disj = []
        for row in matQ[1:]:
            if(row[0] != currentElem):
                disj = list((np.logical_or(row[1:], list(filter(lambda x: x[0] == currentElem, matQ))[0][1:])*1))
                print()
                disj.insert(0, row[0])
                disjunctions.append(disj)
        if len(disjunctions) == 0:
                if(len(matQ[1:]) < 2):
                    return newNodes
                newUniqElem = []
                newMatQ = []
                for elem in uniqElements:
                    if((elem not in (newNodes['node' + str(currentNode)]))):
                        newUniqElem.append(elem)
                for row in matQ:
                        if(row[0] not in (newNodes['node' + str(currentNode)]) and row[0] != currentElem):
                            newMatQ.append(row)
                currentNode = currentNode+1
                maxElem = chooseMax(newMatQ)
                newNodes['node' + str(currentNode)] = [maxElem]
                return arrangeAlgorithm(newMatQ, matR, newUniqElem, k, v, newNodes, currentNode, maxElem)
        # Находим те элементы, у которых дизъюнкция минимальна
        newDisj = []
        minDisj = sum(min(disjunctions, key=lambda x: sum(x[1:]))[1:])
        for row in disjunctions:
            # Проверяем, не нарушит ли элемент условие по значению v
            if(sum(row[1:]) == minDisj and sum(row[1:]) <= v):
                newDisj.append(row)
        if len(newDisj) == 0:
                newUniqElem = []
                newMatQ = []
                for elem in uniqElements:
                    if((elem not in (newNodes['node' + str(currentNode)]))):
                        newUniqElem.append(elem)
                for row in matQ:
                        if(row[0] not in (newNodes['node' + str(currentNode)]) and row[0] != currentElem):
                            newMatQ.append(row)
                currentNode = currentNode+1
                maxElem = chooseMax(newMatQ)
                newNodes['node' + str(currentNode)] = [maxElem]
                return arrangeAlgorithm(newMatQ, matR, newUniqElem, k, v, newNodes, currentNode, maxElem)
        conjunction = []
        conj = []
        # Находим конъюнкцию элементов с заранее выбранным
        for row in matQ[1:]:
            if(row[0] != currentElem and any(row[0] in elements for elements in newDisj)):
                conj = list((np.logical_and(row[1:], list(filter(lambda x: x[0] == currentElem, matQ))[0][1:])*1))
                conj.insert(0, row[0])
                conjunction.append(conj)
        # Находим элемент с максимальной конъюнкцией и включаем в узел
        maxConj = (max(conjunction, key=lambda x: sum(x[1:]))[0])
        elemDisj = list(filter(lambda x: x[0] == maxConj, disjunctions))[0][1:]
        elemDisj.insert(0, 'currElements')
        newNodes['node' + str(currentNode)].append(maxConj)
        newMatrix = []
        for row in matQ:
            if(row[0] not in newNodes['node' + str(currentNode)] and row[0] != currentElem):
                newMatrix.append(row)
        newMatrix.append(elemDisj)
        return arrangeAlgorithm(newMatrix, matR, uniqElements, k, v, newNodes, currentNode, currentElem='currElements')
        
             
    else:
        if(matQ[1:][0][0] == 'currElements'):
           return newNodes
        newUniqElem = []
        newMatQ = []
        for elem in uniqElements:
            if((elem not in (newNodes['node' + str(currentNode)]))):
                newUniqElem.append(elem)
        
        for row in matQ:
                if(row[0] not in (newNodes['node' + str(currentNode)]) and row[0] != currentElem):
                    newMatQ.append(row)
        currentNode = currentNode+1
        maxElem = chooseMax(newMatQ)
        newNodes['node' + str(currentNode)] = [maxElem]
        return arrangeAlgorithm(newMatQ, matR, newUniqElem, k, v, newNodes, currentNode, maxElem)
    
    return newNodes


def chooseMax(matrix):
    # Пропускаем первую строку матрицы
    elements_data = matrix[1:]
    
    
    # Ищем элемент с максимальной суммой значений 
    max_degree_element = max(elements_data, key=lambda x: sum(x[1:]))
    
    # Возвращаем название элемента с максимальной вершиной
    return max_degree_element[0]


    




