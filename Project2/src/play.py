import math
import copy
import random
import sys
import time
import lib
import numpy




class StoneMovement:
    def __init__(self, pitsnumber=6, stonesinpits=4):

        self.init_num_pits = pitsnumber
        self.init_stone = stonesinpits
        self.pits_num = self.init_num_pits
        self.pits_player1 = {k: self.init_stone for k in range(1, self.pits_num + 1)}
        self.pits_player2 = {k: self.init_stone for k in range(1, self.pits_num + 1)}
        self.store_score = [0, 0]



    def board(self):
        board_set = "\t    "
        for i in range(self.pits_num, 0, -1):
             board_set += " [= " + str(i) + " ] "
        board_set += "\n"
        board_set += "\t---------------------------------------------------------------\n"
        board_set += "   " + str(self.store_score[1]).zfill(2) + "      |  "
        for i in range(len(self.pits_player2) - 1, -1, -1):
            board_set += str(self.pits_player2[i + 1]).zfill(2) + "  |  "
        board_set += "(PLAYER 2)\n"
        board_set += "--------------------------------------------------------------------\n"
        board_set += "(PLAYER 1) |  "
        for i in range(0, len(self.pits_player1)):
            board_set += str(self.pits_player1[i + 1]).zfill(2) + "  |  "
        board_set += "   " + str(self.store_score[0]).zfill(2)
        board_set += "\n"
        board_set += "\t---------------------------------------------------------------\n"
        board_set += "\t    "

        for i in range(self.pits_num):
            board_set += " [= " + str(i + 1) + " ] "
        return board_set

    def reset(self, pitsnumber=6, stonesinpits=4):
        self.init_num_pits = pitsnumber
        self.init_stone = stonesinpits
        self.pits_num = self.init_num_pits
        self.store_score = [0, 0]
        self.pits_player1 = {k: self.init_stone for k in range(1, self.pits_num + 1)}
        self.pits_player2 = {k: self.init_stone for k in range(1, self.pits_num + 1)}

    def intend_movements(self, player):
        if player.player_num == 1:
            pits = self.pits_player1
        else:
            pits = self.pits_player2
        actions = {}
        for (npits, stones) in pits.items():
            if stones != 0:
                actions[npits] = stones
        return actions

    def evaluate(self, player, npits):

            if player.player_num == 1:
                pits = self.pits_player1
                opp_pits = self.pits_player2
            else:
                pits = self.pits_player2
                opp_pits = self.pits_player1
            stones = pits[npits]
            score = self.store_score
            pits[npits] = 0

            npits += 1
            temp = pits
            turn = 1

            while stones > 0:
                turn = 1
                while npits <= len(pits) and stones > 0:
                    pits[npits] += 1
                    npits += 1
                    stones -= 1
                if stones == 0:

                    if pits[npits - 1] == 1:
                        if opp_pits[7 - (npits - 1)] != 0:
                            score[player.player_num - 1] += 1 + opp_pits[7 - (npits - 1)]
                            pits[npits - 1] = 0
                            opp_pits[7 - (npits - 1)] = 0
                    break

                if pits == temp:

                    score[player.player_num - 1] += 1
                    stones -= 1
                    turn = 0

                other_temp = pits
                pits = opp_pits
                opp_pits = other_temp
                npits = 1
            return self.pits_player1, self.pits_player2, self.store_score, turn

    def terminal(self):

        over1 = False
        over2 = False
        if all(value == 0 for value in self.pits_player1.values()):
            self.store_score[1] += sum(self.pits_player2.values())
            self.pits_player2 = self.pits_player1
            over1 = True
        if all(value == 0 for value in self.pits_player2.values()):
            self.store_score[0] += sum(self.pits_player1.values())
            self.pits_player1 = self.pits_player2
            over2 = True
        if over1 or over2:
            return True
        else:
            return False

    def result(self, player_num):

        opp_num = 3 - player_num
        if self.terminal():
            return self.store_score[player_num - 1] > self.store_score[opp_num - 1]
        else:
            return False

    def test_score(self, player):
        if player.player_num == 1:
            return self.store_score[0] - self.store_score[1]
        elif player.player_num == 2:
            return self.store_score[1] - self.store_score[0]





class MancalaAction:
    def __init__(self):
        self.time_player1 = 0
        self.time_player2 = 0
        self.win_player1 = -1
        self.win_player2 = -1

    def gamestart(self, gamestate, player1, player2):

        now_player = player1
        wait_player = player2
        print('GAME START')
        print('PLAYER 1: {}\tPLAYER 2: {}'.format(now_player.player_dict[now_player.type],
                                                  wait_player.player_dict[wait_player.type]))
        time.sleep(1)
        sys.stderr.write(gamestate.board() + '\n')
        sys.stderr.flush()
        time.sleep(1)


        while not gamestate.terminal():
            turn = 0


            while turn == 0 and not gamestate.terminal():
                print('PLAYER {} {}\'S TURN'.format(now_player.player_num,
                                                    now_player.player_dict[now_player.type]))
                move = now_player.choose_playertype(gamestate)
                while move not in gamestate.intend_movements(now_player):
                    print('{} is not valid'.format(move))
                    move = now_player.choose_playertype(gamestate)

                print("PLAYER {} {} made a move:".format(now_player.player_num, now_player.player_dict[now_player.type]) )
                sys.stdout.write('[= '+str(move) +']'+ '\n')
                sys.stderr.flush()

                time.sleep(1)
                # TODO
                turn = gamestate.evaluate(now_player, move)[-1]
                time.sleep(1)
                sys.stderr.write(gamestate.board() + '\n')

                sys.stderr.flush()
                time.sleep(1)
            temp = now_player
            now_player = wait_player
            wait_player = temp

        if gamestate.result(player1.player_num):
            self.win_player1 = 1
            self.win_player2 = 0
            print('GAME OVER')
            time.sleep(1)
            sys.stderr.write(gamestate.board() + '\n')
            sys.stderr.flush()
            time.sleep(1)
            print('PLAYER 1 WINS !')


        elif gamestate.result(player2.player_num):
            self.win_player1 = 0
            self.win_player2 = 1
            print('GAME OVER')
            time.sleep(1)
            sys.stderr.write(gamestate.board() + '\n')
            sys.stderr.flush()
            time.sleep(1)
            print('PLAYER 2 WINS !')

        else:
            self.win_player1 = 2
            self.win_player2 = 2
            print('GAME OVER')
            time.sleep(1)
            sys.stderr.write(gamestate.board() + '\n')
            sys.stderr.flush()
            time.sleep(1)
            print('DRAW')

        return self.time_player1, self.time_player2, self.win_player1, self.win_player2

    def actionstester(self, gamestate, player1, player2):

        now_player = player1
        wait_player = player2

        while not gamestate.terminal():
            turn = 0
            while turn == 0 and not gamestate.terminal():
                move = now_player.choose_playertype(gamestate)
                while move not in gamestate.intend_movements(now_player):
                    move = now_player.choose_playertype(gamestate)
            temp = now_player
            now_player = wait_player
            wait_player = temp

        if gamestate.result(player1.player_num):
            self.win_player1 = 1
            self.win_player2 = 0
        elif gamestate.result(player2.player_num):
            self.win_player1 = 0
            self.win_player2 = 1
        else:
            self.win_player1 = 2
            self.win_player2 = 2
        return self.time_player1, self.time_player2, self.win_player1, self.win_player2




class Players:
    player_dict = {0: 'human', 1: 'random', 2: 'minimax', 3: 'alphabeta'}

    def __init__(self, player_num, player_type):
        self.player_num = player_num
        self.opp_num = 3 - player_num
        self.type = player_type

    def __repr__(self):
        return 'PLAYER {} {} is playing'.format(self.player_num, self.player_dict[self.type])

    def choose_playertype(self, gamestate):
        if self.player_dict[self.type] == 'human':
            move = self.humanchoice(gamestate)
            return move
        elif self.player_dict[self.type] == 'random':
            move = self.randomchoice(gamestate)
            return move
        elif self.player_dict[self.type] == 'minimax':
            move = self.minimaxchoice(gamestate)
            return move
        elif self.player_dict[self.type] == 'alphabeta':
            move = self.alphabetachoice(gamestate)
            return move
        else:
            print('invalid player')
            return -1

    def humanchoice(self, gamestate):
        move = int(input('Please enter the human player move:\n'))
        while move not in gamestate.intend_movements(self):
            sys.stderr.write('illegal move\n')
            move = int(input('Please enter the correct human player move:\n'))
        return move

    def randomchoice(self, gamestate):
        d = gamestate.intend_movements(self)
        move = random.choice(list(d.keys()))
        return move

    def minimaxchoice(self, gamestate, depth=5):
        move = -1
        score = -math.inf
        for npits in gamestate.intend_movements(self):
            state_temp = copy.deepcopy(gamestate)
            state_temp.evaluate
            opp = Players(self.opp_num, self.type)
            s = opp.minvalue(state_temp, depth - 1)
            if s > score:
                move = npits
                score = s
            if s == score:
                move = random.choice([move, npits])
                score = s
        return move

    def maxvalue(self, gamestate, depth):
        if gamestate.terminal() or depth == 0:
            return gamestate.test_score(self)
        score = -math.inf
        for npits in gamestate.intend_movements(self):
            state_temp = copy.deepcopy(gamestate)
            state_temp.evaluate
            opp = Players(self.opp_num, self.type)
            s = opp.minvalue(state_temp, depth - 1)
            if s > score:
                score = s
        return score

    def minvalue(self, gamestate, depth):
        if gamestate.terminal() or depth == 0:
            return gamestate.test_score(self)
        score = math.inf
        for npits in gamestate.intend_movements(self):
            state_temp = copy.deepcopy(gamestate)
            state_temp.evaluate
            opp = Players(self.opp_num, self.type)
            s = opp.maxvalue(state_temp, depth - 1)
            if s < score:
                score = s
        return score

    def alphabetachoice(self, gamestate, depth=5):
        move = -1
        alpha = -math.inf
        beta = math.inf
        score = -math.inf
        for npits in gamestate.intend_movements(self):
            state_temp = copy.deepcopy(gamestate)
            state_temp.evaluate
            opp = Players(self.opp_num, self.type)
            s = opp.minalphabeta(state_temp, alpha, beta, depth - 1)
            if s > score:
                move = npits
                score = s
            if s == score:
                move = random.choice([move, npits])
                score = s
            alpha = max(score, alpha)
        return move

    def maxalphabeta(self, gamestate, alpha, beta, depth):
        if gamestate.terminal() or depth == 0:
            return gamestate.test_score(self)
        score = - math.inf
        for npits in gamestate.intend_movements(self):
            state_temp = copy.deepcopy(gamestate)
            state_temp.evaluate
            opp = Players(self.opp_num, self.type)
            s = max(score, opp.minalphabeta(state_temp, alpha, beta, depth - 1))
            if s >= beta:
                alpha = s
                return alpha
            alpha = max(alpha, s)
        return alpha

    def minalphabeta(self, gamestate, alpha, beta, depth):
        if gamestate.terminal() or depth == 0:
            return gamestate.test_score(self)
        score = math.inf
        for npits in gamestate.intend_movements(self):
            state_temp = copy.deepcopy(gamestate)
            state_temp.evaluate
            opp = Players(self.opp_num, self.type)
            s = min(score, opp.maxalphabeta(state_temp, alpha, beta, depth - 1))
            if s <= alpha:
                beta = s
                return beta
            beta = min(beta, s)
        return beta



class Mancala:

    def start(player1_type, player2_type):
        state = StoneMovement()
        player1 = Players(1, player1_type)
        player2 = Players(2, player2_type)
        begin = MancalaAction()
        begin.gamestart(state, player1, player2)

    if __name__ == "__main__":
        print("Welcome to the mancala game")
        print("player_type: numbers (human player = 0, random player = 1, minimax player = 2,alpha_beta player = 3)")
        player1_type = int(input("please input player1 type in number:"))
        player2_type = int(input("please input player2 type in number:"))
        start(player1_type, player2_type)
