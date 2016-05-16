import json
import random
import sys
import time
class Verdict:
    def __init__(self):
        self.seed = int(time.time())
        random.seed(self.seed)
        self.board = [[0 for i in range(4)] for j in range(4)]
        self.score = 0
        self.dx = [0, -1, 0, 1]
        self.dy = [-1, 0, 1, 0]
        self.mp = {
                'LEFT' : 0,
                'UP' : 1,
                'RIGHT' : 2,
                'DOWN' : 3
               }
        self.TOTAL_TIME_LIMIT = 120000
        self.total_time = 0
        self.display = {}
        
    def send_action(self, action):
        print(json.dumps(action))

    def report_winner(self):
        self.display['board'] = self.board
        action = {
                    'action' : 'stop',
                    'score' : self.score,
                    'display' : self.display
                 }
        self.send_action(action)
    
    def query_command(self):
        json_string = raw_input()
        command = json.loads(json_string)
        return command
    
    def query_player(self):
        self.display['board'] = self.board
        message = '\n'.join([ ' '.join( [str(_) for _ in row]) for row in self.board ] ) + '\n'
        action = {
                    'action' : 'next',
                    'nextPlayer' : 0,
                    'writeMsg' : message,
                    'display' : self.display,
                    'score' : self.score
                 }

        if self.seed:
            action['seed'] = str(self.seed)
            self.seed = None

        self.send_action(action)
        return self.query_command()

    def generate_tile(self):
        #generate tile 2 if there is an empty cell
        empty = 0
        for i in range(4):
            for j in range(4):
                if not self.board[i][j]:
                    empty += 1
        if empty == 0:
            return None
        while True:
            x = random.randrange(0, 4)
            y = random.randrange(0, 4)
            if not self.board[x][y]:
                self.board[x][y] = 2
                return [x, y, 2]
    
    def pull_left(self):
        #pull the board to left
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    for k in range(j + 1, 4):
                        if self.board[i][k]:
                            self.board[i][j] = self.board[i][k]
                            self.board[i][k] = 0
                            break
                if self.board[i][j] == 0:
                    break
                for k in range(j + 1, 4):
                    if self.board[i][k]:
                        if self.board[i][j] == self.board[i][k]:
                            self.board[i][k] = 0
                            self.board[i][j] *= 2
                            self.score += self.board[i][j]
                        break


    def rotate(self):
        #rotate board 90 deg anticlockwise
        self.board = [list(_) for _ in zip(*self.board)][::-1]

    def update(self, d):
        for i in range(d):
            self.rotate()
        self.pull_left()
        for i in range((4 - d) & 3):
            self.rotate()
    
    def inside(self, x, y):
        return 0 <= x < 4 and 0 <= y < 4
    
    def valid_move(self, d):
        for i in range(4):
            for j in range(4):
                if not self.board[i][j]:
                    continue
                nx, ny = i + self.dx[d], j + self.dy[d]
                if not self.inside(nx, ny):
                    continue
                if self.board[i][j] == self.board[nx][ny] or self.board[nx][ny] == 0:
                    return True

        return False
    
    def end_game(self):
        #end if total time > total time limit
        if self.total_time > self.TOTAL_TIME_LIMIT:
            return True
        #not end if there is empty cell/adjacent cell with same value
        for i in range(4):
            for j in range(4):
                if not self.board[i][j]:
                    return False
                nx, ny = i + 1, j
                if self.inside(nx, ny) and self.board[i][j] == self.board[nx][ny]:
                    return False
                nx, ny = i, j + 1
                if self.inside(nx, ny) and self.board[i][j] == self.board[nx][ny]:
                    return False
        return True


    def main(self):
        command = self.query_command()
        if command['command'] != 'start':
            return

        self.players = command['players']
        self.display['players'] = self.players
        self.display['newTile'] = self.generate_tile()
        self.display['score'] = self.score
        self.display['totalTime'] = 0

        while not self.end_game():
            command = self.query_player()
            self.display.pop('players', None)
            self.display['newTile'] = None
            self.display['movement'] = None
            self.display['time'] = command['time']
            self.display['message'] = command['command']
            self.total_time += command['time']
            self.display['totalTime'] = self.total_time

            if command['command'] != 'player':
                break
            
            d = command['stdout'].strip().upper()
            if (d not in self.mp) or (not self.valid_move(self.mp[d])):
                if d not in self.mp:
                    self.display['movement'] = None
                else:
                    self.display['movement'] = self.mp[d]
                self.display['message'] = 'invalid'
                break

            self.update(self.mp[d])
            self.display['newTile'] = self.generate_tile()
            self.display['movement'] = self.mp[d]
            self.display['score'] = self.score

        if self.display['message'] == 'player':
            self.display['message'] = 'ok' if self.total_time <= self.TOTAL_TIME_LIMIT else 'ttle'
        self.report_winner()

if __name__ == '__main__':
    verdict = Verdict()
    verdict.main()
