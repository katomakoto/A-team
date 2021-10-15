# 仮想敵との対戦用
import multiprocessing
import os
import math
import random
import itertools
from typing import Tuple, List
import numpy as np
import time

HEXADECIMAL = ("0", "1", "2", "3", "4", "5", "6", "7",
               "8", "9", "a", "b", "c", "d", "e", "f")
ALL_NUMBER_LIST = [''.join(v)
                   for v in itertools.permutations(HEXADECIMAL, 5)]

N = 1


class NumberGuessSimple_Opp():
    def __init__(self) -> None:
        # すべての数が入ったリストを作成
        self.number_list = ALL_NUMBER_LIST
        self.number_list_simple = []
        self.number_list_simple_before = None
        self.guess: str = None
        self.hit: int = None
        self.blow: int = None
        self.number_target = "".join(random.sample(HEXADECIMAL, 5,))
        self.expected_val_list = None
        self.non_used_num = None
        self.len_num_list = None
        self.state = None
        self.hit_blow_key = {(5, 0): 0, (4, 0): 1, (3, 2): 2,
                             (3, 1): 3, (3, 0): 4, (2, 3): 5,
                             (2, 2): 6, (2, 1): 7, (2, 0): 8,
                             (1, 4): 9, (1, 3): 10, (1, 2): 11,
                             (1, 1): 12, (1, 0): 13, (0, 5): 14,
                             (0, 4): 15, (0, 3): 16, (0, 2): 17,
                             (0, 1): 18, (0, 0): 19}
        return None

    def first_guess(self) -> str:
        """
        最初は予想も何もないので，適当な数を入れてみる
        """
        self.guess = "".join(random.sample(HEXADECIMAL, 5,))
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
        self.hit = hit
        self.blow = blow
        estimation_list = []
        for number in self.number_list:
            h, b = self.Check_hitandblow(self.guess, number)
            if (h, b) == (hit, blow):
                estimation_list.append(number)
        self.number_list = list(set(self.number_list) & set(estimation_list))

        # random.shuffle(self.number_list)

        self.len_num_list = len(self.number_list)
        return None

    def return_guess(self) -> str:
        """
            処理によって答えを絞ったリストから，ランダムで数を返す
        """
        if (self.hit, self.blow) == (4, 0) and self.len_num_list >= 4:
            used_num = list(self.guess)
            non_used_num = []
            for num in HEXADECIMAL:
                if num not in used_num:
                    non_used_num.append(num)
            all_num = []
            for num in self.number_list:
                all_num += list(num)
            only_num = [x for x in non_used_num if x in all_num]
            n = len(only_num)//2
            num_list = random.sample(only_num, n) + \
                random.sample(used_num, 5-n)
            binary_list = [''.join(v)
                           for v in itertools.permutations(num_list, 5)]
            self.guess = random.choice((binary_list))
        else:
            self.guess = random.choice(self.number_list)
        # self.guess = random.choice(self.number_list_simple)

        return self.guess

    def Calculation_Expected_Value3(self) -> str:
        # 期待値計算用
        if self.state == None:
            self.guess = random.choice(self.number_list)

        elif self.len_num_list > 15:
            # print('CPU count: ', os.cpu_count())  # 宮下さんの使用できるcpuの数の表示
            with multiprocessing.Pool(os.cpu_count()) as poolmanager:
                A = poolmanager.map(
                    self.return_distribution, self.number_list[0:min(self.len_num_list, 1100)])
                # self.number_listに対して並列処理をかけているので，引数がguessの役割をしています
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
            self.guess = self.guess = random.choice(self.number_list)
        self.state = "最初ではない"
        return self.guess

    def return_distribution(self, guess) -> float:
        distribution_list = np.array([0]*20)
        for target in self.number_list:
            hit, blow = self.Check_hitandblow(guess, target)
            key = self.hit_blow_key[hit, blow]
            distribution_list[key] += 1
        ans = sum(np.power(distribution_list, 2))/len(distribution_list)
        return ans

    def return_len_list(self, guess) -> float:
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


def main():
    win = 0
    lose = 0
    drow = 0
    sum_opp = 0
    sum = 0
    f = open("result.txt", "w")
    for i in range(1000):
        count_opp = 1  # 解答回数を数える
        number_target = "".join(random.sample(HEXADECIMAL, 5,))
        play = NumberGuessSimple_Opp()
        guess = play.first_guess()

        hit, blow = play.Check_hitandblow(guess, number_target)
        while (hit, blow) != (5, 0):
            play.Search_number(hit, blow)
            guess = play.return_guess()
            hit, blow = play.Check_hitandblow(guess, number_target)
            count_opp += 1
        sum_opp += count_opp

        count = 1  # 解答回数を数える
        number_target = "".join(random.sample(HEXADECIMAL, 5,))
        play = NumberGuessSimple_Opp()
        guess = play.first_guess()
        hit, blow = play.Check_hitandblow(guess, number_target)
        while (hit, blow) != (5, 0):
            play.Search_number(hit, blow)
            guess = play.Calculation_Expected_Value3()
            hit, blow = play.Check_hitandblow(guess, number_target)
            count += 1
        f.write(str(count) + "\n")
        sum += count
        print(count, count_opp)
        if count < count_opp:
            win += 1
        elif count == count_opp:
            drow += 1
        else:
            lose += 1
    f.close()
    print(win, drow, lose)
    print(sum/1000, sum_opp/1000)


if __name__ == "__main__":
    start = time.time()
    main()
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
