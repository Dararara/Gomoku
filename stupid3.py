import numpy as np
import random
import time
#最新版本

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
rem_num=8
random.seed(0)
one_side_length = 5
time_limit = 4.8
max_num = 9999999999
min_num = -9999999999
#don't change the class name
class AI(object):
    
    
    def is_empty(self):
        empty = True
        for i in range(self.chessboard_size):
            for j in range(self.chessboard_size):
                if self.chessboard[i][j] != 0:
                    empty = False
                    break
            if not empty:
                break
        return empty

    #chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        #you are white or black
        self.color = color
        #the max time you should use
        self.time_out = time_out
        #you need add your decision into your candidate list
        self.candidate_list = []

    def go(self, chessboard):
        start_time = time.time()
        self.candidate_list.clear()
        self.chessboard = chessboard
        if self.is_empty() and self.color == COLOR_BLACK:
            self.candidate_list.append((self.chessboard_size // 2, self.chessboard_size // 2))
        else:
            
            a = self.max_min(6, start_time)
            self.candidate_list.append([a[0], a[1]])
            print(self.candidate_list)
    
    def is_over(self, x, y):
        over = 0
        a = self.get_score(x, y)
        if self.chessboard[x][y] == self.color and a >= 1000000:
            over = 1
        if self.chessboard[x][y] == -self.color and a >= 1000000:
            over = 2
        return over
    
    def evaluate_fun(self):
        score_table = np.zeros((self.chessboard_size, self.chessboard_size))
        ai_score = 0
        human_score = 0
        for x in range(self.chessboard_size):
            for y in range(self.chessboard_size):
                if(self.chessboard[x][y] == self.color):
                    ai_score = max(ai_score, self.get_score(x, y))
                elif(self.chessboard[x][y] == -self.color):
                    human_score = max(human_score, self.get_score(x, y))
        return ai_score - human_score



    def left_and_right(self, x, y):
        
        if(self.chessboard[x][y] == 0): return []
        left = []
        right = []
        current = self.chessboard[x][y]

        m = x
        length = one_side_length
        while m > 0 and length > 0:
            m -= 1
            if(self.chessboard[m][y] == -current):
                left.insert(0,str(self.chessboard[m][y]))
                break
            else:
                left.insert(0,str(self.chessboard[m][y]))
            if m == 0:
                left.insert(0, str(-current))
        m = x

        length = one_side_length
        while m < self.chessboard_size - 1 and length > 0:
            m += 1
            length -= 1
            if(self.chessboard[m][y] == -current):
                right.append(str(self.chessboard[m][y]))    
                break            
            else:
                right.append(str(self.chessboard[m][y]))
            if m == self.chessboard_size - 1:
                right.append(str(-current))
            
        return left + [str(self.chessboard[x][y])] + right           
    def up_and_down(self, x, y):
        up = []
        down = []
        if(self.chessboard[x][y] == 0): return []
        current = self.chessboard[x][y]

        n = y
        length = one_side_length
        while n > 0 and length > 0:
            n -= 1
            length -= 1
            if(self.chessboard[x][n] == -current): 
                up.insert(0, str(self.chessboard[x][n]))
                break
            else:
                up.insert(0, str(self.chessboard[x][n]))
            if(n == 0):
                up.insert(0, str(-current))
            
        
        n = y
        length = one_side_length
        while n < self.chessboard_size - 1 and length > 0:
            n += 1
            length -= 1
            if(self.chessboard[x][n] == -current): 
                down.append(str(self.chessboard[x][n]))
                break
            else:
                down.append(str(self.chessboard[x][n]))
            if(n == 0):
                down.append(str(-current))
            
        return up + [str(self.chessboard[x][y])] + down
    def upleft_and_downright(self, x, y):
        leftup = []
        rightdown = []
        if(self.chessboard[x][y] == 0): return []
        current = self.chessboard[x][y]

        length = one_side_length
        m, n = x, y
        while m > 0 and n > 0 and length > 0:
            m -= 1
            n -= 1
            length -= 1
            if(self.chessboard[m][n] == -current):
                leftup.insert(0,str(self.chessboard[m][n]))
                break
            else:
                leftup.insert(0,str(self.chessboard[m][n]))
            if(n == 0 or m == 0):
                leftup.insert(0,str(-current))
        
        length = one_side_length
        m, n = x, y
        while m < self.chessboard_size - 1 and n < self.chessboard_size - 1  and length > 0:
            m += 1
            n += 1
            length -= 1
            if(self.chessboard[m][n] == -current):
                rightdown.append(str(self.chessboard[m][n]))
                break
            else:
                rightdown.append(str(self.chessboard[m][n]))
            if(m == self.chessboard_size - 1 or n == self.chessboard_size - 1):
                rightdown.append(str(-current))

        return leftup + [str(self.chessboard[x][y])] + rightdown
    def upright_and_downleft(self, x, y):
        
        rightup=[]
        leftdown=[]
        if(self.chessboard[x][y] == 0): return []
        current = self.chessboard[x][y]
        
        length = one_side_length
        m, n = x, y
        while m < self.chessboard_size - 1 and n > 0 and length > 0:
            m += 1
            n -= 1
            length -= 1
            if(self.chessboard[m][n] == -current):
                rightup.insert(0, str(self.chessboard[m][n]))
                break
            else:
                rightup.insert(0, str(self.chessboard[m][n]))
            if(m == self.chessboard_size - 1 or n == 0):
                rightup.insert(0, str(-current))

        length = one_side_length
        m, n = x, y
        while m > 0 and n < self.chessboard_size - 1 and length > 0:
            m -= 1
            n += 1
            length -= 1
            if(self.chessboard[m][n] == -current):
                leftdown.append(str(self.chessboard[m][n]))
                break
            else:
                leftdown.append(str(self.chessboard[m][n]))
            if(m == 0 or n == self.chessboard_size - 1):
                leftdown.append(str(-current))
            

        return rightup + [str(self.chessboard[x][y])] +leftdown
    
    def get_ones_score(self,s):
        score = 0
        
        fives = s.count('1 1 1 1 1')

        fours = s.count('0 1 1 1 1 0')
        
        threes = s.count('0 0 1 1 1 0 0')
        threes += s.count('0 0 1 1 1 0 2')
        threes += s.count('2 0 1 1 1 0 0')

        jthrees = s.count('0 1 1 0 1 0')
        jthrees += s.count('0 1 0 1 1 0')


        twos = s.count('0 0 1 1 0 0 0')
        twos += s.count('0 0 1 0 1 0 0')
        twos += s.count('0 0 0 1 1 0 0')
        twos += s.count('0 0 1 1 0 0 2')
        twos += s.count('0 0 1 0 1 0 2')
        twos += s.count('0 0 0 1 1 0 2')
        twos += s.count('2 0 0 1 1 0 0')
        twos += s.count('2 0 1 0 1 0 0')
        twos += s.count('2 0 1 1 0 0 0')


        jtwos = s.count('0 1 0 0 1 0')


        bfours = s.count('2 1 1 1 1 0') 
        bfours += s.count('0 1 1 1 1 2')


        cfours = s.count('1 0 1 1 1') 
        cfours += s.count('1 1 1 0 1')
        cfours += s.count('1 1 0 1 1')

        mthrees = s.count('2 1 1 1 0 0')
        mthrees += s.count('2 1 1 0 1 0')
        mthrees += s.count('2 1 0 1 1 0 2')
        mthrees += s.count('2 0 1 1 1 0 2')
        mthrees += s.count('0 0 1 1 1 2')
        mthrees += s.count('2 0 1 1 0 1 2')
        mthrees += s.count('0 1 0 1 1 2')


        m2threes = s.count('1 0 0 1 1 2') 
        m2threes += s.count('2 1 0 1 0 1 2') 
        m2threes += s.count('2 1 1 0 0 1')


        mtwos = s.count('2 1 1 0 0 0')
        mtwos += s.count('2 1 0 1 0 0 2')
        mtwos += s.count('2 1 0 0 1 0 2')
        mtwos += s.count('2 0 0 1 0 1 2')
        mtwos += s.count('0 0 0 1 1 2')
        mtwos += s.count('2 0 1 0 0 1 2')
        mtwos += s.count('2 0 0 1 0 1 2')
        mtwos += s.count('2 1 0 0 0 1 2')
        
        
        
        
        
        if (fives >= 1):  # 成5
            score += 1000000
        elif ( fours >= 1 or bfours >= 2 or (bfours >= 1 and threes + cfours + jthrees >= 1) or cfours >= 2  or(cfours >= 1 and threes + jthrees >= 1)
        ):
            score += 150000
        elif (threes + jthrees >= 2):
            score += 5000
        elif ((threes + jthrees >= 1 and bfours>=1)):
            score += 3000
        elif (threes >= 1 and mthrees + twos >= 1):
            score += 1000
        elif (jthrees >= 1 and mthrees + twos + jtwos >= 1):
            score += 900
        elif (cfours):
            score += 500
        elif (bfours):
            score += 400
        else:
            score = mtwos * 10 + m2threes * 30 + mthrees * 50 + twos * 60
        return score
    def get_score(self, x, y):
        a = self.left_and_right(x, y)
        b = self.up_and_down(x, y)
        c = self.upleft_and_downright(x, y)
        d = self.upright_and_downleft(x, y)
        together = ['3'] + a + ['3'] + b + ['3'] + c + ['3'] + d + ['3']
        str1 = ' '.join(together)
        score = 0
        if self.chessboard[x][y] == 1:
            str1 = str1.replace('3', '2')
            str1 = str1.replace('-1', '2')
            score = self.get_ones_score(str1)
        elif self.chessboard[x][y] == -1:
            str1 = str1.replace('-1','4')#必须先运行这一步，不然-1会变成-2
            str1 = str1.replace('1', '2')
            str1 = str1.replace('4', '1')
            str1 = str1.replace('3', '2')
            score = self.get_ones_score(str1)
        return score

    def is_break(self, start_time):
        timeout = False
        end_time = time.time()
        if (end_time - start_time >= time_limit):
            timeout = True
        return timeout


    def max_min(self, nowdepth, start_time):
        best = min_num
        points = self.mini_generator()
        best_points = []
        alpha = max_num
        beta = min_num
        for i in points:
            self.chessboard[i[0]][i[1]] = self.color
            value = self.min(nowdepth - 1, alpha, beta, i[0], i[1], start_time)
            print(i, value)
            if(self.is_break(start_time)):
                break
            if(value == best):
                best_points.append(i)
            if(value > best):
                best_points = []
                best = value
                best_points.append(i)
            self.chessboard[i[0]][i[1]] = COLOR_NONE
        result = random.choice(best_points)
        return result
    def min(self, nowdepth, alpha, beta, x, y, start_time):
        if(nowdepth == 0):
            return self.evaluate_fun()
        if(self.is_over(x, y) == 1):
            return max_num
        best = max_num
        points = self.generator(-self.color)
        for i in points:
            self.chessboard[i[0]][i[1]] = -self.color
            alpha = min(alpha, best)
            value = self.max(nowdepth-1, alpha, beta, i[0], i[1], start_time)
            if(self.is_break(start_time)): break
            self.chessboard[i[0], i[1]] = COLOR_NONE
            best = min(value, best)
            if(value < beta): break
        return best
    def max(self, nowdepth, alpha, beta, x, y, start_time):
        if(nowdepth == 0):
            return self.evaluate_fun()
        if(self.is_over(x, y) == 2):
            return min_num
        best = min_num
        points = self.generator(self.color)
        for i in points:
            self.chessboard[i[0], i[1]] = self.color
            beta = max(beta, best)
            value = self.min(nowdepth-1, alpha, beta, x, y, start_time)
            if self.is_break(start_time):
                break
            self.chessboard[i[0], i[1]] = COLOR_NONE
            best = max(value, best)
            if(value > alpha): break
        return best
        



    def find_min(self,points):
        min_score = max_num
        min_index = 0
        for i in range(len(points)):
            if(points[i][2] < min_score):
                min_score = points[i][2]
                min_index = i
        return [min_score, min_index]
    def find_max(self, points):
        #list of [x, y, maxscore], find the one with highest score
        max_score = 0
        max_index = 0
        for i in range(len(points)):
            if(points[i][2] > max_score):
                max_score = points[i][2]
                max_index = i
        return [max_score, max_index]



    def mini_generator(self):
        next_go = []
        min_score = max_num
        score = 0
        for x in range(self.chessboard_size):
            for y in range(self.chessboard_size):
                if(self.chessboard[x][y] == 0):
                    if(self.has_neighbor(x, y, 2)):
                        self.chessboard[x][y] = self.color
                        ai_score = self.get_score(x, y)
                        self.chessboard[x][y] = COLOR_NONE

                        self.chessboard[x][y] = -self.color
                        human_score = self.get_score(x, y)
                        self.chessboard[x][y] = COLOR_NONE

                        score = max(ai_score, human_score)
                        if len(next_go) < rem_num:
                            next_go.append([x,y,score])
                            min_score = min(min_score, score)
                        else:
                            if score > min_score:
                                index = self.find_min(next_go)[1]
                                next_go[index] = [x, y, score]
                                min_score = self.find_min(next_go)[0]
        result = []
        
        for i in range(len(next_go)):
            q = next_go[self.find_max(next_go)[1]]
            next_go.remove(q)
            result.append([q[0],q[1]])
        return  result
    
    def generator(self, role):
        best_my = 0
        best_rival = 0
        best_my_points = []
        best_rival_points = []
        for x in range(self.chessboard_size):
            for y in range(self.chessboard_size):
                if(self.chessboard[x][y] == 0):
                    if(self.has_neighbor(x, y, 2)):
                        self.chessboard[x][y] = role
                        my_value = self.get_score(x, y)
                        self.chessboard[x][y] = COLOR_NONE

                        self.chessboard[x][y] = -role
                        rival_value = self.get_score(x, y)
                        self.chessboard[x][y] = COLOR_NONE

                        if(my_value == best_my):
                            best_my_points.append([x, y])
                        if(my_value > best_my):
                            best_my = my_value
                            best_my_points = []
                            best_my_points.append([x, y])
                        if(rival_value == best_rival):
                            best_rival_points.append([x, y])
                        if(rival_value > best_rival):
                            best_rival = rival_value
                            best_rival_points = []
                            best_rival_points.append([x, y])
                        
        if(best_my >= best_rival):
            return best_my_points
        else:
            return best_rival_points
    
    def has_neighbor(self, x, y, distance):
        x_start = x -distance
        x_end = x + distance + 1
        y_start = y - distance
        y_end = y + distance + 1

        for i in range(x_start, x_end):
            for j in range(y_start, y_end):
                if j < 0 or j > self.chessboard_size-1 or i < 0 or i > self.chessboard_size - 1:
                    continue
                if self.chessboard[i][j] != 0:
                    return True
        return False
        
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

a.go(chessboard)
print(a.candidate_list)'''