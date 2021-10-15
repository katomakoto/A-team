import sys
from typing import Tuple
from numpy.random import RandomState
import random
from requestsapi import RequestsAPI

class HitAndBlow(RequestsAPI):
    def __init__(self, player_id, player_name, random_state=1) -> None:
        super().__init__(player_id, player_name)

        self.RANDOM_STATE = random_state
        self.HEXADECIMAL = ("0", "1", "2", "3", "4", "5", "6", "7", 
                            "8", "9", "a", "b", "c", "d", "e", "f")
        self.nowplayer = None
        self.state_wl = None
        self.guess = None
        self.hit = None
        self.blow = None
        self.winner = None
        self.game_end_count = None
        self.OPPONENT_NAME = None
        self.VACANT_ROOMS = [1000, 2000]
        return None

    def __enter_room(self) -> None:
        """
        self.ROOM_IDの部屋に入る．
        Returns:
            None
        """
        self.post_enter_room()
        print("Player {} enter the room {}".format(
            self.PLAYER_NAME, self.ROOM_ID))
        return None

    def try_enter_room(self) -> None:
        """
        空いていればself.ROOM_IDの部屋に入る．入室済みの場合は何もしない．他のアカウントで埋まっている場合は停止．
        Returns:
            None
        """
        room_info = self.get_room_info(room_id=self.ROOM_ID)
        if room_info["player1"] == None:
            self.__enter_room()
        elif room_info["player1"] == self.PLAYER_NAME:
            print("Player {} is already in the room {}".format(
                self.PLAYER_NAME, self.ROOM_ID))
        else:
            if room_info["player2"] == self.PLAYER_NAME:
                print("Player {} is already in the room {}".format(
                    self.PLAYER_NAME, self.ROOM_ID))
            elif room_info["player2"] != None:
                print("Other player {} interrupt in the room {}. Exit.".format(
                    room_info["player2"], self.ROOM_ID))
                sys.exit()
            else:
                self.__enter_room()
        return None

    def check_ready(self) -> bool:
        """
        対戦相手がそろったかどうか確認する
        埋まっている場合True
        他の対戦相手がいる場合はそのうち対応
        Returns:
            bool: 判定
        """
        room_info = self.get_room_info(room_id=self.ROOM_ID)
        ans_flag = False
        if room_info["player1"] != None:
            if room_info["player2"] != None:
                ans_flag = True

        return ans_flag

    def define_answer(self) -> str:
        """
        当ててもらう数を決めて(何かしらの工夫をして，当てにくい数を出題することも,,,,)登録する．
        Returns:
            str: 相手に当ててもらう答えの数
        """
        r = RandomState(self.RANDOM_STATE)
        """
        これでは同じ文字を含む文字列が出力されてしまうことがある
        ランダムに要素を一つ選択: random.choice()
        ランダムに複数の要素を選択（重複なし）: random.sample()
        ランダムに複数の要素を選択（重複あり）: random.choices()
        変更を加えたが，random_stateの使い方が不明でした．
        """
        #my_answer = "".join(r.choice(self.HEXADECIMAL, 5))
        my_answer = "".join(random.sample(self.HEXADECIMAL, 5,))
        self.post_register_answer(my_answer)
        return my_answer

    def table_infomation(self) -> None:
        """
        テーブルの情報を持ってくる．
        以下の関数はこの情報を使う
        Returns:
            None
        """
        resp = self.get_table_infomation()
        self.nowplayer = resp["now_player"]
        self.state_wl = resp["state"]
        table = resp["table"]
        if table is not None:
            if len(table)!=0:
                #self.guess = table[-1]["guess"]
                self.hit = table[-1]["hit"]
                self.blow = table[-1]["blow"]
        self.winner = resp["winner"]
        self.game_end_count = resp["game_end_count"]
        return None

    def judge_victory_or_defeat(self) -> bool:
        """
        勝ち負け判定
        Returns:
            bool: 勝敗が決しているかの判定
        """
        self.table_infomation()
        return self.state_wl == 3

    def check_turn(self) -> bool:
        """
        自分のターンか確認する．
        Returns:
            bool: 自分の手番か動かの判定
        """
        self.table_infomation()
        return self.nowplayer == self.PLAYER_NAME