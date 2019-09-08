import numpy as np
import random
import time
import copy
COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
ONE = 10
TWO = 100
THREE = 1000
FOUR =  100000
FIVE =  10000000
BLOCKED_ONE = 1
BLOCKED_TWO = 10
BLOCKED_THREE = 100
BLOCKED_FOUR = 10000
MAX = FIVE * 10
MIN = -MAX

random.seed(1)
class AI(object):
    #chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        #you are white or black
        self.color = color
        #the max time you should use
        self.time_out = time_out
        #you need add your decision into your candidate list
        self.candidate_list = []

        

    def has_neighbor(self, x, y, distance, count):
        
        x_start = x - distance
        x_end = x + distance
        y_start = y - distance
        y_end = y + distance
        for i in range(x_start, x_end + 1):
            if(i < 0 or i >= self.chessboard_size): continue
            for j in range(y_start, y_end + 1):
                if(j < 0 or j >= self.chessboard_size): continue
                if(i == x and j == y): continue
                if(self.chessboard[i][j] != COLOR_NONE):
                    count -= 1
                    if(count < 1): return True
        return False
   
    #the input is current chessboard
    def go(self, chessboard):
        #clear candidate_list
        self.candidate_list.clear()
        self.chessboard = chessboard
        #algorithm here

        #random decision
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        pos_idx = random.randint(0, len(idx) - 1)
        new_pos = idx[pos_idx]

        #find new pos
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        #print(self.has_neighbor(new_pos[0], new_pos[1], 2, 2))
        #self.evaluate_point(new_pos[0], new_pos[1], -1)
        self.candidate_list.append(new_pos)
        w_num = 0
        b_num = 0
        none_num = 0
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if(self.chessboard[i][j] == COLOR_BLACK): b_num += 1
                elif(self.chessboard[i][j] == COLOR_WHITE): w_num += 1
                elif(self.chessboard[i][j] == COLOR_NONE): none_num += 1
        if(b_num == 0 and w_num == 0):
            self.candidate_list.append([7, 7])
            return None


        self.init_score()
        candidate = self.gen(self.color)
        
        v_max = -100000000
        print(candidate)
        print(self.chessboard)
        #self.alphabeta(self.color, 2, 100000000, -100000000)
        #print(self.candidate_list)
        
        for i in range(len(candidate)):
            #print('hello world')
            temp = candidate[i]
            
            #下棋
            #print(temp, self.color)
            self.chessboard[temp[0]][temp[1]] = self.color
            self.init_score()
            #print(self.my_score)
            #print(self.rival_score)
            my_value = self.negamax(-self.color, 2)
            #print(temp, my_value)
            #归位
            
            self.chessboard[temp[0]][temp[1]] = COLOR_NONE
            if(my_value > v_max):
                #
                print(temp)
                self.candidate_list.append(temp)
                v_max = my_value
        
    
    def evaluate_point(self, x, y, role):
        #print(x, y, role)
        
        result = 0
        empty = 0
        count = 0
        block = 0
        secondCount = 0
        len = self.chessboard_size
        
        
        
        #direction 1
        count = 1
        block = 0
        empty = -1
        secondCount = 0
        i = y
        while True:
            i += 1
            if(i >= len):
                block += 1
                break
            current_pos = self.chessboard[x][i]
            
            if(current_pos == COLOR_NONE):
                if(empty == -1 and i < len-1 and self.chessboard[x][i+1] == role):
                    empty = count
                    continue
                else:
                    break
            
            if(current_pos == role):
                count += 1
                continue
            else:
                block += 1
                break
        i = y
        
        while True:
            i -= 1
            if(i < 0):
                block += 1
                break
            current_pos = self.chessboard[x][i]

            if(current_pos == COLOR_NONE):
                if(empty == -1 and i > 0 and self.chessboard[x][i-1] == role):
                    empty = 0
                    continue
                else:
                    break
            if(current_pos == role):
                secondCount += 1
                if(empty != -1):
                    empty += 1
                continue
            else:
                block += 1
                break
        count += secondCount
        result += self.count_to_score(count, block, empty)
        #print(result, end=', ')
        #direction 2
        count = 1
        block = 0
        empty = -1
        secondCount = 0
        i = x
        while True:
            i += 1
            if(i >= len):
                block += 1
                break
            current_pos = self.chessboard[i][y]
            
            if(current_pos == COLOR_NONE):
                if(empty == -1 and i < len-1 and self.chessboard[i+1][y] == role):
                    empty = count
                    continue
                else:
                    break
            
            if(current_pos == role):
                count += 1
                continue
            else:
                block += 1
                break
        i = x
        while True:
            i -= 1
            if(i < 0):
                block += 1
                break
            current_pos = self.chessboard[i][y]

            if(current_pos == COLOR_NONE):
                if(empty == -1 and i > 0 and self.chessboard[i-1][y] == role):
                    empty = 0
                    continue
                else:
                    break
            if(current_pos == role):
                secondCount += 1
                if(empty != -1):
                    empty += 1
                continue
            else:
                block += 1
                break
        count += secondCount
        result += self.count_to_score(count, block, empty)
        #print(result, end=', ')
        #direction 3
        count = 1
        block = 0
        empty = -1
        secondCount = 0
        i = 0
        while True:
            i += 1
            temp_x = x + i
            temp_y = y - i
            if(temp_x < 0 or temp_y < 0 or temp_x >= len or temp_y >= len):
                block += 1
                break
            current_pos = self.chessboard[temp_x][temp_y]
            
            if(current_pos == COLOR_NONE):
                if(empty == -1 and temp_x < len-1 and temp_y > 0 and self.chessboard[temp_x+1][temp_y-1] == role):
                    empty = count
                    continue
                else:
                    break
            
            if(current_pos == role):
                count += 1
                continue
            else:
                block += 1
                break
        i = 0
        while True:
            i += 1
            temp_x = x - i
            temp_y = y + i
            if(temp_x < 0 or temp_y < 0 or temp_x >= len or temp_y >= len):
                block += 1
                break
            current_pos = self.chessboard[temp_x][temp_y]

            if(current_pos == COLOR_NONE):
                if(empty == -1 and temp_x > 0 and temp_y < len-1 and self.chessboard[temp_x-1][temp_y+1] == role):
                    empty = 0
                    continue
                else:
                    break
            if(current_pos == role):
                secondCount += 1
                if(empty != -1):
                    empty += 1
                continue
            else:
                block += 1
                break
        count += secondCount
        result += self.count_to_score(count, block, empty)
        #if(self.chessboard[5][5] == 1): print("attention", temp_x, temp_y, count, secondCount, block, empty)
        #direction 4
        count = 1
        block = 0
        empty = -1
        secondCount = 0
        i = 0
        while True:
            i += 1
            temp_x = x + i
            temp_y = y + i
            if(temp_x >= len or temp_y >= len):
                block += 1
                break
            current_pos = self.chessboard[temp_x][temp_y]
            
            if(current_pos == COLOR_NONE):
                if(empty == -1 and temp_x < len-1 and temp_y < len-1 and self.chessboard[temp_x+1][temp_y+1] == role):
                    empty = count
                    continue
                else:
                    break
            
            if(current_pos == role):
                count += 1
                continue
            else:
                block += 1
                break
        i = 0
        while True:
            i += 1
            temp_x = x-i
            temp_y = y-i
            if(temp_x < 0 or temp_y < 0):
                block += 1
                break
            current_pos = self.chessboard[temp_x][temp_y]

            if(current_pos == COLOR_NONE):
                if(empty == -1 and temp_x > 0 and temp_y > 0 and self.chessboard[temp_x-1][temp_y-1] == role):
                    empty = 0
                    continue
                else:
                    break
            if(current_pos == role):
                secondCount += 1
                if(empty != -1):
                    empty += 1
                continue
            else:
                block += 1
                break
        count += secondCount
        
        result += self.count_to_score(count, block, empty)
        #print(result)
        #print(x, y, role, block, empty ,count)
        return result

    def count_to_score(self, count, block, empty):
        
        if(empty <= 0):
            # 1 1 1 1 1
            if(count >= 5): return FIVE
            if(block == 0):
                if(count == 1): return ONE
                elif(count == 2): return TWO
                elif(count == 3): return THREE
                elif(count == 4): return FOUR
            
            if(block == 1):
                if(count == 1): return BLOCKED_ONE
                elif(count == 2): return BLOCKED_TWO
                elif(count == 3): return BLOCKED_THREE
                elif(count == 4): return BLOCKED_FOUR
        
        elif(empty == 1 or empty == count - 1):
            # 1 1 1 0 1
            if(count >= 6):
                return FIVE
            if(block == 0):
                if(count == 2): return TWO/2
                if(count == 3): return THREE
                if(count == 4): return BLOCKED_FOUR
                if(count == 5): return FOUR
            if(block == 1):
                if(count == 2): return BLOCKED_TWO
                if(count == 3): return BLOCKED_THREE
                if(count == 4): return BLOCKED_FOUR
                if(count == 5): return BLOCKED_FOUR
        
        elif(empty == 2 or empty == count - 2):
            # 1 1 0 1 1
            if(count >= 7):
                return FIVE
            if(block == 0):
                if(count == 3): return THREE
                if(count == 4): return BLOCKED_FOUR
                if(count == 5): return BLOCKED_FOUR
                if(count == 6): return FOUR
            if(block == 1):
                if(count == 3): return BLOCKED_THREE
                if(count == 4): return BLOCKED_FOUR
                if(count == 5): return BLOCKED_FOUR
                if(count == 6): return FOUR
            if(block == 2):
                if(count >= 4): return BLOCKED_FOUR
            
        elif(empty == 3 or empty == count - 3):
            # 1 1 1 0 1 1 1
            if(count >= 8): return FIVE
            if(block == 0):
                if(count == 4): return THREE # 0 1 0 1 1 1 0
                if(count == 5): return THREE # 0 1 1 0 1 1 1 0
                if(count == 6): return BLOCKED_FOUR  #0 1 1 1 0 1 1 1 0
                if(count == 7): return FOUR
            if(block == 1):
                if(count == 4): return BLOCKED_FOUR
                if(count == 5): return BLOCKED_FOUR
                if(count == 6): return BLOCKED_FOUR
                if(count == 7): return FOUR
            if(block == 2):
                if(count >= 4): return BLOCKED_FOUR
        
        elif(empty == 4 or empty == count - 4):
            if(count >= 9): return FIVE
            if(block == 0):
                if(count >= 5): return FOUR
            if(block == 1):
                if(count >= 5 and count < 8): return BLOCKED_FOUR
                if(count == 8): return FOUR
            if(block == 2):
                if(count >= 5): return BLOCKED_FOUR
        elif(empty == 5 or empty == count - 4): return FIVE
        
        return 0

    def init_score(self):
        self.my_score = np.zeros((self.chessboard_size, self.chessboard_size),dtype=int)
        self.rival_score = np.zeros((self.chessboard_size, self.chessboard_size), dtype=int)
        
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if(self.chessboard[i][j] == COLOR_NONE):
                    if(self.has_neighbor(i, j, 2, 2)):
                        self.my_score[i][j] = self.evaluate_point(i, j, self.color)
                        self.rival_score[i][j] = self.evaluate_point(i, j, -self.color)
                
                elif(self.chessboard[i][j] == self.color):
                    self.my_score[i][j] = self.evaluate_point(i, j, self.color)
                    self.rival_score[i][j] = 0
                elif(self.chessboard[i][j] == -self.color):
                    self.rival_score[i][j] = self.evaluate_point(i, j, -self.color)
                    self.my_score[i][j] = 0
                #print(i, j, self.my_score[i][j], self.rival_score[i][j])
             
    def evaluate_all(self, role):
        #print(self.chessboard)
        self.my_max_score = 0
        self.rival_max_score = 0
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if(self.chessboard[i][j] == self.color):
                    self.my_max_score += self.my_score[i][j]
                elif (self.chessboard[i][j] == -self.color):
                    self.rival_max_score += self.rival_score[i][j]
        if(role == self.color): return self.my_max_score - self.rival_max_score
        else: return self.rival_max_score -self.my_max_score

    def gen(self, role):
        #局面不明朗的时候需要特殊处理,比如开局
        fives = []
        my_fours = []
        rival_fours = []
        my_blocked_fours = []
        rival_blocked_fours = []
        my_two_threes = []
        rival_two_threes = []
        my_threes = []
        rival_threes = []
        my_twos = []
        rival_twos = []
        neighbors = []
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if(self.chessboard[i][j] == COLOR_NONE):
                    if(self.has_neighbor(i, j, 2, 2) == False): continue
                    my_score = self.my_score[i][j]
                    rival_score = self.rival_score[i][j]
                    pos = [i, j]
                    #if(i == 4, j == 11): print(4, 11, my_score, rival_score)
                    #if(i == 7, j == 8): print(7, 8, my_score, rival_score)
                    if(my_score >= FIVE or rival_score >= 5):
                        fives.append(pos)
                    elif(my_score >= FOUR):
                        my_fours.append(pos)
                    elif(rival_score >= FOUR):
                        rival_fours.append(pos)
                    elif(my_score >= BLOCKED_FOUR):
                        my_blocked_fours.append(pos)
                    elif(rival_score >= BLOCKED_FOUR):
                        rival_blocked_fours.append(pos)
                    elif(my_score >= 2 * THREE):
                        print('hi')
                        my_two_threes.append(pos)
                    elif(rival_score >= 2 * THREE):
                        rival_two_threes.append(pos)
                    elif(my_score >= THREE):
                        my_threes.append(pos)
                    elif(rival_score >= THREE):
                        rival_threes.append(pos)
                    elif(my_score >= TWO):
                        my_twos.append(pos)
                    elif(rival_score >= TWO):
                        rival_twos.append(pos)
                    else: neighbors.append(pos)
        
        #如果有五个,直接返回,搞定
        if(fives): return fives
        
        #如果自己有活四,直接活四,注意名称变化
        if(role == self.color and my_fours): return my_fours
        if(role == -self.color and rival_fours): return rival_fours
        
        #对面有活四,自己没冲四
        if(role == self.color and rival_fours and not my_blocked_fours): return rival_fours
        if(role == -self.color and my_fours and not rival_blocked_fours): return my_fours
        
        #对面有活四,自己有冲四,都考虑
        if(role == self.color and (my_fours or rival_fours)): return my_fours
        if(role == -self.color and (my_fours or rival_fours)): return rival_fours + my_fours + rival_blocked_fours + my_blocked_fours
        
        #大于等于活三的棋
        #print('from here')
        if(role == self.color): result = my_two_threes + rival_two_threes + my_blocked_fours + rival_blocked_fours + my_threes + rival_threes
        if(role == -self.color): result = rival_two_threes + my_two_threes + rival_blocked_fours + my_blocked_fours + rival_threes + my_threes
        if(result): return result
        #print('till here')
        #剩下的拼一起
        if(role == self.color): result = my_twos + rival_twos + neighbors
        if(role == -self.color): result = rival_twos + my_twos + neighbors
        return result
    def negamax(self, role, deep):
        
        deep -= 1
        if(deep > 0):
            candidate = self.gen(role)
            v_min = 1000000000
            v_max = -1000000000
            for i in range(len(candidate)):
                #print(i)
                temp = candidate[i]
                #下棋
                self.chessboard[temp[0]][temp[1]] = role
                
                value = -self.negamax(-role, deep)
                #归位
                self.chessboard[temp[0]][temp[1]] = COLOR_NONE
                if(deep%2 == 1):
                    #max level
                    v_min = min(v_min, value)
                else:
                    v_max = max(v_max, value)

            if(deep%2 == 1):
                return v_min
            else:
                return v_max 
        self.init_score()
        return self.evaluate_all(role)

    '''
    def negamax(self, candidates, role, deep, alpha, beta):
        for i in range(len(candidates)):
            p = candidates[i]
            self.chessboard[p[0]][p[1]] = role
            steps = [p]
            v = r(deep-1, -beta, -alpha, -role, 1, copy.deepcopy(steps))
            v.score *= -1
            alpha = max(alpha, v.score)
            self.chessboard[p[0]][p[1]] = COLOR_NONE
            ###p.v = v
        return alpha
    
    def r(self, deep, alpha, beta, role, step, steps):
        _e = self.evaluate_all(role)
        _leaf = leaf(_e, step, steps)
        if(deep <= 0 or _e >= FIVE or _e <= FIVE):
            return _leaf
        best = leaf(MIN, step, steps)
        points = self.gen(role)
        if(not points): return _leaf
        for i in range(len(points)):
            p = points[i]
            self.chessboard[p[o]][p[1]] = role
            _deep = deep - 1
            _steps = copy.deepcopy(steps)
            _steps.append(p)
            v = r(_deep, -beta, -alpha, -role, step+1, _steps)
            v.score *= -1
            self.chessboard[p[0]][p[1]] = COLOR_NONE
            if(v.score > best.score):
                best = v
            alpha = max(best.score, alpha)
            if(v.score >= beta):
                v.score = MAX - 1
                return v
        return best
    
    def deeping(self, candidates, role, deep):
        bestscore = 0
        for i in range(2,deep+1, 2):
            bestscore = self.negamax(candidates, role, i, MIN, MAX)
            if(bestscore >= FIVE): break

        


class leaf:
    def __init__(score, step, steps):
        self.score = score
        self.step = step
        self.steps = steps





a = AI(15, -1, 5)
chessboard = np.zeros((15, 15), dtype=np.int)
chessboard[6, 7] = -1
chessboard[7, 7] = 1
chessboard[7, 6] = -1
chessboard[8, 5] = 1
chessboard[8, 7] = -1
chessboard[6, 5] = 1
chessboard[7, 5] = -1
chessboard[8, 6] = 1
chessboard[6, 8] = -1
chessboard[6, 6] = 1
chessboard[8, 8] = -1
chessboard[9, 8] = 1
chessboard[7, 8] = -1
chessboard[9, 6] = 1
chessboard[5, 8] = -1
chessboard[4, 8] = 1
chessboard[8, 9] = -1
chessboard[5, 6] = 1
chessboard[8, 10] = -1
chessboard[8, 11] = 1
chessboard[9, 10] = -1
chessboard[10, 11] = 1
chessboard[4, 9] = -1
chessboard[3, 10] = 1
chessboard[9, 11] = -1
chessboard[7, 9] = 1
chessboard[6, 10] = -1
chessboard[7, 10] = 1
chessboard = np.zeros((15, 15), dtype=np.int)
a.go(chessboard)
print(a.candidate_list)



a = AI(15, -1, 5)
chessboard = np.zeros((15, 15), dtype=np.int)
chessboard[7, 7] = -1
chessboard[8, 7] = 1
chessboard[8, 6] = -1
chessboard[6, 8] = 1
chessboard[8, 8] = -1
chessboard[6, 6] = 1
chessboard[6, 7] = -1
chessboard[7, 8] = 1
chessboard[9, 6] = -1
chessboard[7, 6] = 1
chessboard[9, 8] = -1
chessboard[9,7 ] = 1
chessboard[10, 7] = -1
chessboard[11, 8] = 1
chessboard[11,6] = -1
chessboard[12,5] = 1
chessboard[12, 7] = -1
chessboard[10, 6] = 1
chessboard[10, 5] = -1
chessboard[9, 4] = 1
chessboard[8,5] = -1
chessboard[7,4] = 1
chessboard[9,5] = -1
chessboard[7,5] = 1
chessboard[10,4] = -1
chessboard[11,3] = 1
chessboard[13,8] = -1
chessboard[14,9] = 1
chessboard[7,10] = -1
chessboard[8,9] = 1
chessboard[7,3] = -1
chessboard[4,8] = 1
chessboard[5, 7] = -1
chessboard[4, 7] = 1
a.go(chessboard)
print(a.candidate_list)


双三有问题
四三
'''
a = AI(15, -1, 5)
chessboard = np.zeros((15, 15), dtype=np.int)
chessboard = np.array(
    [[ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
     [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
     [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
     [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
     [ 1,  0,  0,  0,  0,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0],
     [ 0,  0,  0,  0,  -1, 0,  0,  0,  0,  0,  1,  1,  0,  0,  0],
     [ 0,  0,  0,  0,  0,  0,  0, -1,  0,  1,  0,  1,  0,  0,  0],
     [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
     [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
     [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
     [ 0,  0,  0,  0,  0, -1,  0,  0,  0,  0,  0,  0,  0,  0,  0],
     [ 0,  0,  0,  0,  0,  0,  0, -1,  0,  0,  0,  0,  0,  0,  0],
     [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
     [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
     [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]

)

a.chessboard = chessboard
a.init_score()
print(a.evaluate_point(7, 8, -1))
print(a.evaluate_point(4, 11, -1))

a.go(chessboard)