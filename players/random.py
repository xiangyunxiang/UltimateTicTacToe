import random

from engine import MainBoardCoords, SubBoardCoords, SubBoard
from players.stdout import StdOutPlayer



class Random(StdOutPlayer):
    def __init__(self):
        super().__init__()
        self.win_sub_cond = [
            ((0, 0), (0, 1), (0, 2)),
            ((1, 0), (1, 1), (1, 2)),
            ((2, 0), (2, 1), (2, 2)),
            ((0, 0), (1, 0), (2, 0)),
            ((0, 1), (1, 1), (2, 1)),
            ((0, 2), (1, 2), (2, 2)),
            ((0, 0), (1, 1), (2, 2)),
            ((2, 0), (1, 1), (0, 2))
        ]

    def get_my_move(self):  # -> Tuple[MainBoardCoords, SubBoardCoords]
        main_board_coords = self.pick_next_main_board_coords()
        #sub_board = self.main_board.get_sub_board(main_board_coords)
        sub_board_coords = self.evaluate_cell_value(main_board_coords.row, main_board_coords.col)
        return main_board_coords, sub_board_coords
    
    def evaluate_cell_value(self, board_row, board_col): #board row, board col refer to current subboard
        chance_dict = {}
        self.main_board.main_cell_value = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        oppo_coord = self.main_board.get_oppo_coords()
        self_coord = self.main_board.get_self_coords()
        tie_coord = self.main_board.get_tie_coords()
        for win in self.win_sub_cond:
            chance_dict[win] = 0
            for sel in self_coord:
                if sel in win:
                    chance_dict[win] += 1
            for oppo in oppo_coord:
                if oppo in win:
                    chance_dict[win] -= 100
            for tie in tie_coord:
                if tie in win:
                    chance_dict[win] -= 10
            
            for win in chance_dict:
                if chance_dict[win] == 2:
                    for row in range(0, self.main_board._board_size):
                        for col in range(0, self.main_board._board_size):
                            if (row, col) in win and not self.main_board._board[row][col].is_finished:
                                if self.pick_random_sub_board_coords(self.main_board._board[row][col])[1] == 13000:
                                    self.main_board.main_cell_value[row][col] -= 10000
                                elif self.pick_random_sub_board_coords(self.main_board._board[row][col])[1] == 40000:
                                    if board_row == row and board_col == col:
                                        self.main_board.main_cell_value[row][col] += 10000000
                                    else:
                                        self.main_board.main_cell_value[row][col] -= 10000
                                else:
                                    self.main_board.main_cell_value[row][col] -= 1000
            
            for win in chance_dict:
                if chance_dict[win] < -150:
                    for row in range(0, self.main_board._board_size):
                        for col in range(0, self.main_board._board_size):
                            if (row, col) in win and not self.main_board._board[row][col].is_finished:
                                if self.pick_random_sub_board_coords(self.main_board._board[row][col])[1] == 13000:
                                    self.main_board.main_cell_value[row][col] -= 100000
                                elif self.pick_random_sub_board_coords(self.main_board._board[row][col])[1] == 40000:
                                    if board_row == row and board_col == col:
                                        self.main_board.main_cell_value[row][col] += 1100000
                                    else:
                                        self.main_board.main_cell_value[row][col] -= 1000
                                elif self.pick_random_sub_board_coords(self.main_board._board[row][col])[1] == 0:
                                    self.main_board.main_cell_value[row][col] -= 100
                                else:
                                    self.main_board.main_cell_value[row][col] -= 10
            
            for win in chance_dict:
                if chance_dict[win] < 0 and chance_dict[win] > -150:
                    for row in range(0, self.main_board._board_size):
                        for col in range(0, self.main_board._board_size):
                            if (row, col) in win and not self.main_board._board[row][col].is_finished:
                                self.main_board.main_cell_value[row][col] -= 10


        for row in range(0, self.main_board._board_size):
            for col in range(0, self.main_board._board_size):
                if self.main_board._board[row][col].is_finished:
                    self.main_board.main_cell_value[row][col] -= 1000000
        
        playable_coord = self.pick_all_random_sub_board_coords_value(self.main_board._board[board_row][board_col])
        current_best = (None, -10000000)
        same_list = []
        for coord in playable_coord:
            cell_value = self.main_board.main_cell_value[coord[0]][coord[1]] + playable_coord[coord][1]
            if cell_value > current_best[1]:
                current_best = (playable_coord[coord][0], cell_value)
                same_list = [current_best]
            elif cell_value == current_best[1]:
                current_best = (playable_coord[coord][0], cell_value)
                same_list.append(current_best)
        
        return random.choice(same_list)[0]
            
                

    def pick_next_main_board_coords(self) -> MainBoardCoords:
        if self.main_board.sub_board_next_player_must_play is None:
            playable_coord = self.main_board.get_playable_coords()
            if len(playable_coord) > 0:
                oppo_coord = self.main_board.get_oppo_coords()
                self_coord = self.main_board.get_self_coords()
                tie_coord = self.main_board.get_tie_coords()
                chance_dict = {}
                for win in self.win_sub_cond:
                    chance_dict[win] = 0
                    for sel in self_coord:
                        if sel in win:
                            chance_dict[win] += 1
                    for oppo in oppo_coord:
                        if oppo in win:
                            chance_dict[win] -= 100
                    for tie in tie_coord:
                        if tie in win:
                            chance_dict[win] -= 10
                
                for win in chance_dict:
                    if chance_dict[win] == 2:
                        for playable in playable_coord:
                            if (playable.row, playable.col) in win:
                                return playable

                for win in chance_dict:            
                    if chance_dict[win] < -150:
                        for playable in playable_coord:
                            if (playable.row, playable.col) in win:
                                return playable
                
                for win in chance_dict:            
                    if chance_dict[win] > 0:
                        for playable in playable_coord:
                            if (playable.row, playable.col) in win:
                                return playable
                
                return random.choice(playable_coord)
        else:
            return self.main_board.sub_board_next_player_must_play

    def pick_random_sub_board_coords(self, sub_board: SubBoard) -> SubBoardCoords:
        playable_coord = sub_board.get_playable_coords()
        if len(playable_coord) > 0:
            oppo_coord = sub_board.get_opponent_coords()
            self_coord = sub_board.get_self_coords()
            chance_dict = {}
            for win in self.win_sub_cond:
                chance_dict[win] = 0
                for sel in self_coord:
                    if sel in win:
                        chance_dict[win] += 1
                for oppo in oppo_coord:
                    if oppo in win:
                        chance_dict[win] -= 10
            
            return_list = []
            for win in chance_dict:
                if chance_dict[win] == 2:
                    for playable in playable_coord:
                        if (playable.row, playable.col) in win and playable not in return_list:
                            return_list.append(playable)
            if len(return_list) > 0:
                return (return_list, 40000)

            for win in chance_dict:
                if chance_dict[win] < -10:
                    for playable in playable_coord:
                        if (playable.row, playable.col) in win and playable not in return_list:
                            return_list.append(playable)
            if len(return_list) > 0:
                return (return_list, 13000)
            
            for win in chance_dict:            
                if chance_dict[win] > 0:
                    for playable in playable_coord:
                        if (playable.row, playable.col) in win and playable not in return_list:
                            return_list.append(playable)
            if len(return_list) > 0:
                return (return_list, 100)

            return (playable_coord, 0)
    
    def pick_all_random_sub_board_coords_value(self, sub_board: SubBoard) -> SubBoardCoords:
        playable_coord = sub_board.get_playable_coords()
        if len(playable_coord) > 0:
            oppo_coord = sub_board.get_opponent_coords()
            self_coord = sub_board.get_self_coords()
            chance_dict = {}
            for win in self.win_sub_cond:
                chance_dict[win] = 0
                for sel in self_coord:
                    if sel in win:
                        chance_dict[win] += 1
                for oppo in oppo_coord:
                    if oppo in win:
                        chance_dict[win] -= 10
            
            return_dict = {}
            for win in chance_dict:
                if chance_dict[win] == 2:
                    for playable in playable_coord:
                        if (playable.row, playable.col) in win:
                            if (playable.row, playable.col) not in return_dict:
                                return_dict[(playable.row, playable.col)] = [playable, 40000]
                            else:
                                return_dict[(playable.row, playable.col)][1] += 40000
            

            for win in chance_dict:
                if chance_dict[win] < -10:
                    for playable in playable_coord:
                        if (playable.row, playable.col) in win:
                            if (playable.row, playable.col) not in return_dict:
                                return_dict[(playable.row, playable.col)] = [playable, 13000]
                            else:
                                return_dict[(playable.row, playable.col)][1] += 13000
            
            for win in chance_dict:            
                if chance_dict[win] == 1:
                    for playable in playable_coord:
                        if (playable.row, playable.col) in win:
                            if (playable.row, playable.col) not in return_dict:
                                return_dict[(playable.row, playable.col)] = [playable, 100]
                            else:
                                return_dict[(playable.row, playable.col)][1] += 100
            
            for win in chance_dict:            
                if chance_dict[win] >= -10 and chance_dict[win] <= 0:
                    for playable in playable_coord:
                        if (playable.row, playable.col) in win:
                            if (playable.row, playable.col) not in return_dict:
                                return_dict[(playable.row, playable.col)] = [playable, 0]
            
            return return_dict
            
    def timeout(self):
        return

    def game_over(self, winLoseTie: str, main_board_coords: MainBoardCoords, sub_board_coords: SubBoardCoords):
        return

    def match_over(self, winLoseTie: str, main_board_coords: MainBoardCoords, sub_board_coords: SubBoardCoords):
        return

