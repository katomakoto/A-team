from hitandblow import HitAndBlow
import os
import multiprocessing
import time
import random
import itertools
from typing import Tuple
import numpy as np


class NumberGuessSimple(HitAndBlow):
    def __init__(self, player_id="6839fe8a-78ce-4d4c-92af-1962aa3b3cc5", player_name="A") -> None:
        super().__init__(player_id, player_name)

        # すべての数が入ったリストを作成
        self.number_list = [
            ''.join(v) for v in itertools.permutations(self.HEXADECIMAL, 5)]
        self.number_target = "".join(
            random.sample(self.HEXADECIMAL, 5,))
        self.state = None
        self.hit_blow_key = {(5, 0): 0, (4, 0): 1, (3, 2): 2,
                             (3, 1): 3, (3, 0): 4, (2, 3): 5,
                             (2, 2): 6, (2, 1): 7, (2, 0): 8,
                             (1, 4): 9, (1, 3): 10, (1, 2): 11,
                             (1, 1): 12, (1, 0): 13, (0, 5): 14,
                             (0, 4): 15, (0, 3): 16, (0, 2): 17,
                             (0, 1): 18, (0, 0): 19, }
        return None

    def Calculation_Expected_Value3(self) -> str:
        """
        期待値計算部分
        序盤：ランダムで返す
        中盤：一部に期待値計算
        終盤：全部を期待値計算
        """
        if self.state == None:
            self.guess = random.choice(self.number_list)
        elif self.len_num_list > 16:
            with multiprocessing.Pool(os.cpu_count()) as poolmanager:
                A = poolmanager.map(
                    self.return_distribution, self.number_list[0:min(self.len_num_list, 1400)])
            i = A.index(min(A))
            self.guess = self.number_list[i]
        elif self.len_num_list > 2:
            used_num = []
            for number_in_list in self.number_list:
                for num in list(number_in_list):
                    if num not in used_num:
                        used_num.append(num)
            guess_list = [''.join(v)
                          for v in itertools.permutations(used_num, 5)]
            with multiprocessing.Pool(os.cpu_count()) as poolmanager:
                B = poolmanager.map(
                    self.return_len_list, guess_list)
            index = B.index(min(B))
            self.guess = guess_list[index]
        else:
            self.guess = random.choice(self.number_list)

        self.state = "最初の期待値計算ではない"
        return self.guess

    def return_distribution(self, guess) -> float:
        """
        なにかを予想すると5hit0blow,4hit0blow,3hit2blow,,,の20パターンのうち，いずれかが返ってくる．
        ここでは，ある予想手に対して答えの候補が20パターンのうち，どのように分布するかを調べる．
        分布が均等な方が，より候補を減らせると期待できる．
        並列処理のため，関数化している．
        """
        distribution_list = np.array([0]*20)
        for target in self.number_list:
            hit, blow = self.Check_hitandblow(guess, target)
            key = self.hit_blow_key[hit, blow]
            distribution_list[key] += 1
        sq_val = np.power(distribution_list, 2)  # エラー回避
        return sum(sq_val)/len(distribution_list)

    def return_len_list(self, guess) -> float:
        """
        ここではある予想手に対して，現在の答えの候補をどこまで減らすことができるかを計算
        答えの候補以外も予想手に設定する．
        これにより，ある程度数が判明してきたときに，わざわざ判明している数を入力することがなくなったりする．
        （すでに分かっている数を入力するのは無駄であり，その枠を有効活用すべき）
        並列処理のため，関数化している．
        """
        A = []
        for target in self.number_list:
            hit, blow = self.Check_hitandblow(guess, target)
            estimation_list = []
            for number in self.number_list:
                h, b = self.Check_hitandblow(guess, number)
                if (h, b) == (hit, blow):
                    estimation_list.append(number)
            len_list = len(list(set(self.number_list)
                                & set(estimation_list)))
            A.append(len_list**2)
        ans = sum(A)/len(A)
        return ans

    def first_guess(self) -> str:
        """
        最初は何も予想できないので，適当な数を入れる
        """
        self.guess = "".join(random.sample(self.HEXADECIMAL, 5,))
        return self.guess

    def Check_hitandblow(self, guess: str, number_target: str) -> Tuple[int, int]:
        """
        何ヒット何ブローなのか調べる
        n:桁数（n=5で固定）
        number_guess:推測値
        number_target:答え
        """
        hit, blow = 0, 0
        for n, m in zip(guess, number_target):
            if n == m:
                hit += 1
            elif n in number_target:
                blow += 1
        return (hit, blow)

    def Search_number(self, hit, blow) -> None:
        """
        答えとなる可能性があるリストに絞っていく
        """
        estimation_list = []
        for number in self.number_list:
            h, b = self.Check_hitandblow(self.guess, number)
            if (h, b) == (hit, blow):
                estimation_list.append(number)
        self.number_list = list(set(self.number_list) & set(estimation_list))

        random.shuffle(self.number_list)
        print("残りの解答候補数={}".format(len(self.number_list)))
        self.len_num_list = len(self.number_list)
        return None

    def return_guess(self) -> str:
        """
        処理によって答えを絞ったリストから，ランダムで数を返す
        """
        self.guess = random.choice(self.number_list)
        return self.guess

    def print_table_infomation(self) -> None:
        """
        printして確認する用
        """
        self.table_infomation()
        print("guess: {}, hit: {}, blow: {}, nowplayer: {}, winner: {}, game_end_count: {}, state: {}".format(
            self.guess, self.hit, self.blow, self.nowplayer, self.winner, self.game_end_count, self.state_wl
            ))
        return None

    def number_guess_algorithm(self):
        """
        提出する対戦用のアルゴリズム．hitblowの情報をapiでとってきて，予測した結果をpostする．self.Calculation_Expected_Value3()の期待値計算を行う．
        """
        if self.state == None:
            self.state_2 = True
            self.first_guess()

        self.table_infomation()
        if self.state != None:
            self.Search_number(int(self.hit), int(self.blow))
            if self.state_2:
                self.state_2 = False
                self.state = None
            self.Calculation_Expected_Value3()
        self.post_register_guess(self.guess) 
        self.print_table_infomation()    
        if self.state == None:    
            if self.state_2:
                self.state = "2nd"
        return None

    def number_guess_algorithm_for_web(self):
        """
        webのCPU対戦用．hitblowの情報をapiでとってきて，予測した結果をpostする．期待値計算を行わないことで負荷低減．
        """
        if self.state == None:
            self.first_guess()
        self.table_infomation()
        if self.state != None:
            self.Search_number(int(self.hit), int(self.blow))
            self.guess = random.choice(self.number_list)
        else:
            self.state = "aaa"
        self.post_register_guess(self.guess) 
        self.print_table_infomation()        
        return None


def main1():
    """
    自分で問題を作って，自分で解く
    テスト用
    """
    HEXADECIMAL = ("0", "1", "2", "3", "4", "5", "6", "7",
                   "8", "9", "a", "b", "c", "d", "e", "f")
    sum = 0
    for i in range(10):
        count = 1  # 解答回数を数える
        number_target = "".join(random.sample(HEXADECIMAL, 5,))
        play = NumberGuessSimple()
        guess = play.first_guess()
        hit, blow = play.Check_hitandblow(guess, number_target)
        print("ANS   GUESS H B")
        print("---------------")
        print(number_target, guess, hit, blow)
        while (hit, blow) != (5, 0):
            play.Search_number(hit, blow)
            guess = play.Calculation_Expected_Value3()
            hit, blow = play.Check_hitandblow(guess, number_target)
            print(number_target, guess, hit, blow)
            count += 1

        else:
            print("正解  ", count, "回")
        sum += count
    print(sum/100)


def main2():
    """
    デモ用
    相手の数を当てる
    """
    sum = 0
    count = 1
    play = NumberGuessSimple()
    guess = play.first_guess()
    print("予想：", guess)
    print("結果を入力してください")
    hit = int(input("hit="))
    blow = int(input("blow="))
    print("---------------")
    while (hit, blow) != (5, 0):
        play.Search_number(hit, blow)
        guess = play.Calculation_Expected_Value3()
        print("予想：", guess)
        print("結果を入力してください")
        hit = int(input("hit="))
        blow = int(input("blow="))
        print("---------------")
        print(guess, hit, blow)
        count += 1
    else:
        print("解答回数：", count, "回")
    sum += count
    print(sum)


if __name__ == "__main__":
    start = time.time()
    main1()
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
