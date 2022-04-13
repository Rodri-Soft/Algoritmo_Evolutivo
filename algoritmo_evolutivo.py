from asyncio.windows_events import NULL
from itertools import count
import random
import copy

def attack_evaluation(board, row, col, n):    

    attack_counter = 0             

    for i in range(n):
        if board[row][i] == 1 or board[i][col] == 1:
           
            if ((board[row][i] == 1) and (i != col)):                            
                attack_counter += 1
                break               
            
            if ((board[i][col] == 1) and (i != row)):                    
                attack_counter += 1
                break                                
    
    if row <= col:
        c = col - row
        r = 0
    else:
        r = row - col
        c = 0
    while c < n and r < n:
        
        if ((board[r][c] == 1) and (r != row and c != col )):            
            attack_counter += 1
            break
            
        r += 1
        c += 1    

    
    r = 0
    c = col + row
    if c > n-1:
        r = c - (n-1)
        c = n-1
    
    while c >= 0 and r < n:
        if ((board[r][c] == 1) and (r != row and c != col)):            
            attack_counter += 1
            break
            
        r += 1
        c -= 1

    return attack_counter    
   

def show_board(board):
    for row in board:    
        print(*row)
    print('\n')


def fill(board, n):    

    i=0    
    while i < n:

        queen_positioned = False

        while queen_positioned == False:

            row = random.randint(0, n-1)
            column = random.randint(0, n-1)

            if board[row][column] != 1:
                board[row][column] = 1
                queen_positioned = True
        
        i += 1
    return board


def switch_matrix(vector, n):    
    for i in range(n):
        vector.append([0] * n)
    return vector


def count_attacks(board, n):
    aux_board = copy.deepcopy(board)  

    attacks = 0
    matrix_attacks = 0

    for row in range(n):
        for column in range(n):            
            if(aux_board[row][column] == 1):

                attacks = attack_evaluation(aux_board, row, column, n)
                
                matrix_attacks = matrix_attacks + attacks                         
                aux_board[row][column] = 0
    
    return matrix_attacks


def fathers_selection(population, n, generation):
    
    first_father = 0
    second_father = 0

    board_attack = 0
        
    min_first_attack = n*n
    min_second_attack = n*n

    index_list = []
    
    for i in range(5):

        unique_index = False

        while unique_index == False:

            index = random.randint(0, population-1)        

            if index not in index_list:
               
                board_attack = count_attacks(generation[index], n)
                
                if board_attack <= min_first_attack:

                    if min_first_attack <= min_second_attack:
                        min_second_attack = min_first_attack
                        second_father = first_father

                    min_first_attack = board_attack                                                           
                    first_father = index               
                
                elif board_attack <= min_second_attack:                    
                    min_second_attack = board_attack
                    second_father = index
                
                unique_index = True
                index_list.append(index)
                    
    
    best_fathers = [first_father, second_father]
  
    return best_fathers


def fill_child_with_half(list_half, child):
    for row in list_half:      
        coordinates = row
        child[coordinates[0]][coordinates[1]] = 1
    return child


def generate_child(generation, best_fathers, n):

    child = []
    child = switch_matrix(child, n) 

    # Fill First Half
    counter_first_row = 0
    counter_first_element = 0
    counter_first_half = 0
    
    list_first_half = []
    
    for row in generation[best_fathers[0]]:     
        counter_first_element = 0     
        for element in row:
            
            if counter_first_half == (n/2):
                break
            
            if (element == 1) and (counter_first_half < (n/2)):
                list_first_half.append([counter_first_row, counter_first_element])
                counter_first_half += 1

            counter_first_element += 1
        
        if counter_first_half == (n/2):
            break 
        counter_first_row += 1


    # Fill child with the first half
    child = fill_child_with_half(list_first_half, child)


    # Fill Second Half
    counter_second_element = 0
    counter_second_half = 0

    list_second_half = []

    for i, row in reversed(list(enumerate(generation[best_fathers[1]]))):
        counter_second_element = n-1
        while (counter_second_element >= 0) and (counter_second_half < (n/2)):
            
            if row[counter_second_element] == 1:

                if child[i][counter_second_element] != 1:
                    list_second_half.append([i, counter_second_element])
                    counter_second_half += 1
                                   
            counter_second_element -= 1

        if counter_second_half == (n/2):
            break


    # Fill Child With the Second Half
    child = fill_child_with_half(list_second_half, child)    

    return child


def mutate_child(child, n):
    

    mutate_board = []
    mutate_board = switch_matrix(mutate_board, n)  

    queen_number = random.randint(1, n)
    queens_counter = 1
    queen_row = 0
    queen_column = 0
    queen_found = False

    # Find queen to mutate
    for i, row in list(enumerate(child)):
        for j, element in list(enumerate(row)):
            
            if child[i][j] == 1:                
                if queens_counter == queen_number:
                    queen_row = i
                    queen_column = j                    
                    queen_found = True
                    break
                else:
                    queens_counter += 1

        if queen_found:
            break
            
    # print("Antes----: ")
    # show_board(child)            
    # print("Queen number "+str(queen_number))
    # print("Row ["+str(queen_row)+"] Column ["+str(queen_column)+"]")
    
    # Copy board
    mutate_board = copy.deepcopy(child)  
    mutate_board[queen_row][queen_column] = 0
    
    # print("Tablero antes de mutar----: ")
    # show_board(mutate_board)   


    # Mutate----------------------           

    # Corners

    left_up_corner = False
    left_down_corner = False
    right_up_corner = False
    right_down_corner = False

    corner = False

    if (queen_row == 0) and (queen_column == 0):
        corner = True
        left_up_corner = True
    elif (queen_row == (n-1)) and (queen_column == 0):
        corner = True
        left_down_corner = True
    elif (queen_row == 0) and (queen_column == (n-1)):
        corner = True
        right_up_corner = True
    elif (queen_row == (n-1)) and (queen_column == (n-1)):
        corner = True
        right_down_corner = True


    # Choosing direction
    direction = 0    
    evals = 0
    queen_placed = False
    directions_visited = []

    while (queen_placed == False) and (evals < 4):
        
        aux_direction = direction

        if corner:
            if left_up_corner:        
                
                if direction == 0:
                    direction = random.randint(2, 3)
                else:
                    while direction == aux_direction:
                        direction = random.randint(2, 3)
                
            elif left_down_corner:

                if direction == 0:
                    direction = random.randint(1, 2)
                else:
                    while direction == aux_direction:
                        direction = random.randint(1, 2)
                
            elif right_up_corner:

                if direction == 0:
                    direction = random.randint(3, 4)
                else:
                    while direction == aux_direction:
                        direction = random.randint(3, 4)
                
            elif right_down_corner:

                posible_direction = [1, 4]
                if direction == 0:                    
                    direction = random.choice(posible_direction)
                else:                                    
                    while direction == aux_direction:
                        direction = random.choice(posible_direction)

        else:
    
            if queen_column == 0:

                       
                result = select_different_queen(directions_visited, direction, 1, 3, 3)
                direction = result[0]
                directions_visited = result[1]

            elif queen_row == 0:
                
                result = select_different_queen(directions_visited, direction, 2, 4, 3)
                direction = result[0]
                directions_visited = result[1]

            elif queen_row == (n-1):

                posible_direction = [1, 2, 4]                

                result = select_different_queen_variation(directions_visited, direction, posible_direction, 3)             
                direction = result[0]
                directions_visited = result[1]
                

            elif queen_column == (n-1):

                posible_direction = [1, 3, 4]                

                result = select_different_queen_variation(directions_visited, direction, posible_direction, 3)             
                direction = result[0]
                directions_visited = result[1]

            else:
                
                result = select_different_queen(directions_visited, direction, 1, 4, 4)
                direction = result[0]
                directions_visited = result[1]


        new_queen_row = queen_row
        new_queen_column = queen_column

        if direction == 1:
            new_queen_row -= 1
        elif direction == 2:
            new_queen_column -= 1
        elif direction == 3:
            new_queen_row += 1
        elif direction == 4:
            new_queen_column -= 1        

        if mutate_board[new_queen_row][new_queen_column] == 0:
            mutate_board[new_queen_row][new_queen_column] = 1
            queen_placed = True
        else:
            evals += 1

            
    # print("Tablero después de mutar----: ")
    # show_board(mutate_board)   

    mutation_result = []
    if queen_placed:
        mutation_result.append(queen_placed)
        mutation_result.append(mutate_board)
        return mutation_result
    else:
        mutation_result.append(queen_placed)
        return mutation_result


def select_different_queen(directions_visited, direction, lower_limit, upper_limit, limit_values):
   
    result = []    

    if direction == 0:
        direction = random.randint(lower_limit, upper_limit)    
        directions_visited.append(direction)

    else:

        different_queen = False
        while different_queen == False:     

            if len(directions_visited) == limit_values:
                break

            direction = random.randint(lower_limit, upper_limit)
            
            if direction in directions_visited:
                direction = random.randint(lower_limit, upper_limit)
            else:
                different_queen = True
                directions_visited.append(direction)             

    result.append(direction)
    result.append(directions_visited)
    return result


def select_different_queen_variation(directions_visited, direction, posible_direction, limit_values):
   
    result = []    

    if direction == 0:
        direction = direction = random.choice(posible_direction)
        directions_visited.append(direction)

    else:

        different_queen = False
        while different_queen == False:     

            if len(directions_visited) == limit_values:
                break

            direction = random.choice(posible_direction)
            
            if direction in directions_visited:
                direction = random.choice(posible_direction)
            else:
                different_queen = True
                directions_visited.append(direction)                

    result.append(direction)
    result.append(directions_visited)
    return result


def run():

    population = 100
    generation = []
    n=8

    # Generate boards
    for i in range(population):
        board = []
        board = switch_matrix(board, n)     
        board = fill(board, n)        
        generation.append(board)
        # print('Board N: '+str(i))
        # show_board(board)
        

    is_found = False
    evaluations = 0
    solution_board = []
    solution_board = switch_matrix(solution_board, n)

    while (evaluations < 1000) and (is_found == False):
        
        print("Evaluacion: "+str(evaluations))
        evaluations += 1

        decendents_list = []

        # Generate 10 descendants
        for i in range(10):

            # Fathers selection
            best_fathers = fathers_selection(population, n, generation)

            # Generate child
            child = []
            child = switch_matrix(child, n)     

            child = generate_child(generation, best_fathers, n)

            #Check Mutation
            #mutate_child(child, n)

            mutationProbability = random.randint(1, 10)        
            is_mutated = False
            if mutationProbability <= 8:
                is_mutated = True
            
            if is_mutated:
                
                successful_mutacion = False
                while successful_mutacion == False:

                    mutation_result = mutate_child(child, n)
                    if mutation_result[0]:
                        decendents_list.append(mutation_result[1])
                        successful_mutacion = True

            else:
                decendents_list.append(child)

        
        # print("Numero de descendientes: "+str(len(decendents_list)))

        # Order population based on their attacks to replace the worst individuals
        for i in range(population):
            for j in range(population-1):
                
                number_of_attacks = count_attacks(generation[j], n)
                auxiliary_number_of_attacks = count_attacks(generation[j+1], n)

                if number_of_attacks > auxiliary_number_of_attacks:
                    
                    auxiliary_board = []
                    auxiliary_board = switch_matrix(auxiliary_board, n)                              
                    auxiliary_board = generation[j]

                    generation[j] = generation[j+1]
                    generation[j+1] = auxiliary_board



        # Replace worst individuals of the board population with the created offspring
        i=99
        while i >= 90:
            generation.pop()
            i -= 1
        
        for j in range(len(decendents_list)):
            generation.append(decendents_list[j])
        
        
        for i in range(population):
            number_of_attacks = count_attacks(generation[i], n)
            if number_of_attacks == 0:
                is_found = True
                solution_board = generation[i]

        
    if is_found:
        print('\n')
        print("Evaluations "+str(evaluations))
        show_board(solution_board)
    else:
        print("Maximum number of evaluations reached!!!")
        print("Evaluations "+str(evaluations))

    
    
    
    # n= int(input("Escribe el numero de reinas: "))
    # m=n
    # board = []
    # for i in range(n):
    #     board.append(['_'] * n)

    # fill(board, n)
    # imprimir_board(board)


if __name__ == '__main__':
    run()
