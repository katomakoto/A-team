from hitandblow import HitAndBlow
import itertools
import random
from numpy.random import RandomState
from typing import Tuple, Union, List
import time


class NumberGuess(HitAndBlow):
    def __init__(self, player_id="6839fe8a-78ce-4d4c-92af-1962aa3b3cc5", player_name="A", random_state=1, hit=4, blow=0, guess="01234") -> None:
        super().__init__(player_id, player_name, random_state=random_state)
        # すべての数が入ったリストを作成
        self.number_list: List[str] = [
            ''.join(v) for v in itertools.permutations(self.HEXADECIMAL, 5)]
        self.guess: str = guess
        self.hit: int = hit
        self.blow: int = blow
        return None

    def number_guess(self) -> str:

        if self.guess == None:
            my_first_guess = self.first_guess()
            return my_first_guess
        else:
            self.judge_func_from_hitandblow()
            return self.return_guess()

    def first_guess(self) -> str:
        """
        最初は予想も何もないので，適当な数を入れてみる
        乱数を使用？
        """
        # r = RandomState(self.RANDOM_STATE)
        # my_first_guess = "".join(r.choice(self.HEXADECIMAL, 5))
        my_first_guess = "".join(random.sample(self.HEXADECIMAL, 5,))
        return my_first_guess

    def judge_func_from_hitandblow(self) -> None:
        """
        1回目なら適当に数を返す関数を返す
        それ以外なら，hitとblowの結果に応じて関数を返す
        """
        if self.hit == 4 and self.blow == 0:
            self.number_list = NumberGuess.hit4_blow0(self)
            pass
        elif self.hit == 3 and self.blow == 2:
            NumberGuess.hit3_blow2(self)
        elif self.hit == 3 and self.blow == 1:
            NumberGuess.hit3_blow1(self)
        elif self.hit == 3 and self.blow == 0:
            NumberGuess.hit3_blow0(self)
        elif self.hit == 2 and self.blow == 3:
            NumberGuess.hit2_blow3(self)
        elif self.hit == 2 and self.blow == 2:
            NumberGuess.hit2_blow2(self)
        elif self.hit == 2 and self.blow == 1:
            NumberGuess.hit2_blow1(self)
        elif self.hit == 2 and self.blow == 0:
            NumberGuess.hit2_blow0(self)
        elif self.hit == 1 and self.blow == 4:
            NumberGuess.hit1_blow4(self)
        elif self.hit == 1 and self.blow == 3:
            NumberGuess.hit1_blow3(self)
        elif self.hit == 1 and self.blow == 2:
            NumberGuess.hit1_blow2(self)
        elif self.hit == 1 and self.blow == 1:
            NumberGuess.hit1_blow1(self)
        elif self.hit == 1 and self.blow == 0:
            NumberGuess.hit1_blow0(self)
        elif self.hit == 0 and self.blow == 5:
            NumberGuess.hit0_blow5(self)
        elif self.hit == 0 and self.blow == 4:
            NumberGuess.hit0_blow4(self)
        elif self.hit == 0 and self.blow == 3:
            NumberGuess.hit0_blow3(self)
        elif self.hit == 0 and self.blow == 2:
            NumberGuess.hit0_blow2(self)
        elif self.hit == 0 and self.blow == 1:
            NumberGuess.hit0_blow1(self)
        elif self.hit == 0 and self.blow == 0:
            NumberGuess().hit0_blow0(self)
        else:
            # 万が一，どれにも当てはまらなかったらどうするか検討中
            NumberGuess().first_guess(self)

    def return_guess(self) -> str:
        """
        処理によって答えを絞ったリストから，ランダムで数を返す
        """
        self.guess = random.choice(self.number_list)
        return self.guess

    def hit4_blow0(self) -> List:
        """
        4hit0blowの情報から，可能性の無い数をall_numbers_listから消す
        55通り以内まで絞れるはず
        """
        used_num = list(self.guess)
        not_used_num = [num for num in self.HEXADECIMAL if num not in used_num]
        # 直近の推測値と4ヒット0ブローの情報だけから可能性のあると考えられる数が入るリスト
        estimation_list = [self.guess.replace(used_num[j], not_used_num[i]) for j in range(
            len(used_num)) for i in range(len(not_used_num))]

        # これまでで絞ってきたnumber_listと今回のestimation_listに共通する数を取り出す

        number_list = list(set(self.number_list) & set(estimation_list))
        return number_list

    def hit3_blow2(self) -> List:
        """
        3hit2blowの情報から，可能性の無い数をnumber_listから消す
        10通り以内まで絞れるはず
        """
        used_num = list(self.guess)
        estimation_list = []
        for i in range(4):
            for j in range(i+1, 5):
                estimation_list.append(self.guess.replace(used_num[j], "X").replace(
                    used_num[i], used_num[j]).replace("X", used_num[i]))
        number_list = list(set(self.number_list) & set(estimation_list))
        return number_list

    def hit3_blow1(self) -> List:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        110通り以内まで絞れるはず
        """
        used_num = list(self.guess)
        not_used_num = [num for num in self.HEXADECIMAL if num not in used_num]
        estimation_list = []
        for i in range(4):
            for j in range(i+1, 5):
                for k in range(11):
                    estimation_list.append(self.guess.replace(used_num[j], "X").replace(
                        used_num[i], used_num[j]).replace("X", not_used_num[k]))
        number_list = list(set(self.number_list) & set(estimation_list))
        return number_list

    def hit3_blow0(self) -> List:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        1100通り以内まで絞れるはず
        """
        used_num = list(self.guess)
        not_used_num = [num for num in self.HEXADECIMAL if num not in used_num]
        estimation_list = []
        for i in range(4):
            for j in range(i+1, 5):
                for k in range(len(not_used_num)-1):
                    for l in range(k+1, len(not_used_num)):
                        estimation_list.append(self.guess.replace(used_num[i], not_used_num[k]).replace(
                            used_num[j], not_used_num[l]))
                        estimation_list.append(self.guess.replace(used_num[i], not_used_num[l]).replace(
                            used_num[j], not_used_num[k]))
        number_list = list(set(self.number_list) & set(estimation_list))
        return number_list

    def hit2_blow3(self) -> List:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        20通り以内まで絞れるはず
        """
        used_num = list(self.guess)
        estimation_list = []
        for i in range(len(used_num)-2):
            for j in range(i+1, len(used_num)-1):
                for k in range(j+1, len(used_num)):
                    estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                        used_num[j], "Y").replace(used_num[k], used_num[i]).replace("X", used_num[j]).replace("Y", used_num[k]))
                    estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                        used_num[j], "Y").replace(used_num[k], used_num[j]).replace("X", used_num[k]).replace("Y", used_num[i]))
        number_list = list(set(self.number_list) & set(estimation_list))
        return number_list

    def hit2_blow2(self) -> List:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        330通り以内まで絞れるはず
        """
        used_num = list(self.guess)
        not_used_num = [num for num in self.HEXADECIMAL if num not in used_num]
        estimation_list = []
        for i in range(len(used_num)-2):
            for j in range(i+1, len(used_num)-1):
                for k in range(j+1, len(used_num)):
                    for l in range(len(not_used_num)):
                        estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                            used_num[j], "Y").replace(used_num[k], not_used_num[l]).replace("X", used_num[j]).replace("Y", used_num[i]))
                        estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                            used_num[j], "Y").replace(used_num[k], used_num[i]).replace("X", used_num[k]).replace("Y", not_used_num[l]))
                        estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                            used_num[j], "Y").replace(used_num[k], used_num[j]).replace("X", not_used_num[l]).replace("Y", used_num[k]))
        number_list = list(set(self.number_list) & set(estimation_list))
        return number_list

    def hit2_blow1(self) -> None:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        2200通り以内まで絞れるはず
        """
        used_num = list(self.guess)
        not_used_num = [num for num in self.HEXADECIMAL if num not in used_num]
        estimation_list = []
        seed = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for i in range(len(used_num)-2):
            for j in range(i+1, len(used_num)-1):
                for k in range(j+1, len(used_num)):
                    for m, l in list(itertools.permutations(seed, 2)):
                        estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                            used_num[j], "Y").replace(used_num[k], not_used_num[m]).replace("X", not_used_num[l]).replace("Y", used_num[i]))
                        estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                            used_num[j], "Y").replace(used_num[k], used_num[i]).replace("X", not_used_num[m]).replace("Y", not_used_num[l]))
                        estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                            used_num[j], "Y").replace(used_num[k], not_used_num[m]).replace("X", used_num[j]).replace("Y", not_used_num[l]))
                        estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                            used_num[j], "Y").replace(used_num[k], used_num[j]).replace("X", not_used_num[m]).replace("Y", not_used_num[l]))
                        estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                            used_num[j], "Y").replace(used_num[k], not_used_num[m]).replace("X", used_num[k]).replace("Y", not_used_num[l]))
                        estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                            used_num[j], "Y").replace(used_num[k], not_used_num[m]).replace("X", not_used_num[l]).replace("Y", used_num[k]))
        number_list = list(set(self.number_list) & set(estimation_list))
        return number_list

    def hit2_blow0(self) -> List:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        9900通り以内まで絞れるはず
        """
        used_num = list(self.guess)
        not_used_num = [num for num in self.HEXADECIMAL if num not in used_num]
        estimation_list = []
        seed = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for i in range(len(used_num)-2):
            for j in range(i+1, len(used_num)-1):
                for k in range(j+1, len(used_num)):
                    for l, m, n in list(itertools.permutations(seed, 3)):
                        estimation_list.append(self.guess.replace(used_num[i], not_used_num[l]).replace(
                            used_num[j], not_used_num[m]).replace(used_num[k], not_used_num[n]))
        number_list = list(set(self.number_list) & set(estimation_list))
        return number_list

    def hit1_blow4(self) -> List:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        45通り以内まで絞れるはず
        """
        used_num = tuple(self.guess)

        start1 = time.perf_counter()
        index_num = [0, 1, 2, 3, 4]
        estimation_list = []
        for f_index, fixed_num in enumerate(used_num):
            shuffle_index = [v for v in index_num if v != f_index]  # 固定された数字と，
            # 入れ替える数字のうち先頭に使用されている数字のインデックス除いた.
            head_index, shuffle_index = shuffle_index[0], shuffle_index[1:]
            switched_index = [v for v in shuffle_index if v !=
                              head_index]  # 入れ替えを考えるインデックスのリスト
            for val in shuffle_index:
                switched_index_for_used = [
                    v for v in switched_index if v != val]
                for sw_index in switched_index:
                    rest_index = [v for v in switched_index if v != sw_index]
                    ans = [fixed_num]*5
                    ans[head_index], ans[sw_index] = used_num[val], used_num[head_index]
                    # もし入替が不要なら
                    if rest_index[0] == switched_index_for_used[1] or rest_index[1] == switched_index_for_used[0]:
                        ans[rest_index[0]], ans[rest_index[1]] = used_num[switched_index_for_used[0]
                                                                          ], used_num[switched_index_for_used[1]]
                    else:
                        ans[rest_index[0]], ans[rest_index[1]] = used_num[switched_index_for_used[1]
                                                                          ], used_num[switched_index_for_used[0]]
                    estimation_list.append(''.join(ans))
        t1 = (time.perf_counter() - start1)*1000
        estimation_list_copm = estimation_list

        start2 = time.perf_counter()
        estimation_list = []
        seed = [0, 1, 2, 3, 4]
        for i, j, k, l in list(itertools.combinations(seed, 4)):

            estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[k]).replace("X", used_num[j]).replace("Y", used_num[i]).replace("Z", used_num[l]))
            estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[i]).replace("X", used_num[j]).replace("Y", used_num[k]).replace("Z", used_num[l]))
            estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[k]).replace("X", used_num[j]).replace("Y", used_num[l]).replace("Z", used_num[i]))
            estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[j]).replace("X", used_num[k]).replace("Y", used_num[i]).replace("Z", used_num[l]))
            estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[j]).replace("X", used_num[k]).replace("Y", used_num[l]).replace("Z", used_num[i]))
            estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[i]).replace("X", used_num[k]).replace("Y", used_num[l]).replace("Z", used_num[j]))
            estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[k]).replace("X", used_num[l]).replace("Y", used_num[i]).replace("Z", used_num[j]))
            estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[j]).replace("X", used_num[l]).replace("Y", used_num[k]).replace("Z", used_num[i]))
            estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[i]).replace("X", used_num[l]).replace("Y", used_num[k]).replace("Z", used_num[j]))
        number_list = list(set(self.number_list) & set(estimation_list))
        return number_list

    def hit1_blow3(self) -> List:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        605通り以内まで絞れるはず
        """
        used_num = list(self.guess)
        not_used_num = [num for num in self.HEXADECIMAL if num not in used_num]
        estimation_list = []
        seed = [0, 1, 2, 3, 4]

        for m in range(len(not_used_num)):
            for i, j, k, l in list(itertools.combinations(seed, 4)):
                estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                    used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[k]).replace("X", used_num[j]).replace("Y", used_num[i]).replace("Z", not_used_num[m]))
                estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                    used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[i]).replace("X", used_num[j]).replace("Y", used_num[k]).replace("Z", not_used_num[m]))
                estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                    used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[k]).replace("X", used_num[j]).replace("Y", not_used_num[m]).replace("Z", used_num[i]))
                estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                    used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[j]).replace("X", used_num[k]).replace("Y", used_num[i]).replace("Z", not_used_num[m]))
                estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                    used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[j]).replace("X", used_num[k]).replace("Y", not_used_num[m]).replace("Z", used_num[i]))
                estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                    used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[i]).replace("X", used_num[k]).replace("Y", not_used_num[m]).replace("Z", used_num[j]))
                estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                    used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[k]).replace("X", not_used_num[m]).replace("Y", used_num[i]).replace("Z", used_num[j]))
                estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                    used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[j]).replace("X", not_used_num[m]).replace("Y", used_num[k]).replace("Z", used_num[i]))
                estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                    used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], used_num[i]).replace("X", not_used_num[m]).replace("Y", used_num[k]).replace("Z", used_num[j]))
                estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                    used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], not_used_num[m]).replace("X", used_num[j]).replace("Y", used_num[k]).replace("Z", used_num[i]))
                estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                    used_num[j], "Y").replace(used_num[k], "Z").replace(used_num[l], not_used_num[m]).replace("X", used_num[k]).replace("Y", used_num[i]).replace("Z", used_num[j]))

        number_list = list(set(self.number_list) & set(estimation_list))
        return number_list

    def hit1_blow2(self) -> None:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        10450通り以内まで絞れるはず
        """
        # 編集中
        used_num = list(self.guess)
        not_used_num = [num for num in self.HEXADECIMAL if num not in used_num]
        estimation_list = []
        seed = [0, 1, 2, 3, 4]
        xyzw_list = list(itertools.permutations(["X", "Y", "Z", "W"], 4))

        # for n, o in list(itertools.permutations(not_used_num, 2)):
        for i, j, k, l, m in list(itertools.permutations(seed, 5)):

            estimation_list.append(self.guess.replace(used_num[i], "X").replace(
                used_num[j], "Y").replace(used_num[k], "Z").replace("W", used_num[l])).replace("X", ).replace(
                "Y", ).replace("Z", ).replace("W", used_num[l])
        print(len(estimation_list))
        number_list = list(set(self.number_list) & set(estimation_list))
        return number_list

    def hit1_blow1(self) -> None:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        14850通り以内まで絞れるはず
        """

    def hit1_blow0(self) -> None:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        39600通り以内まで絞れるはず
        """

    def hit0_blow5(self) -> None:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        44通り以内まで絞れるはず
        """

    def hit0_blow4(self) -> None:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        5610通り以内まで絞れるはず
        """

    def hit0_blow3(self) -> None:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        58850通り以内まで絞れるはず
        """

    def hit0_blow2(self) -> None:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        173250通り以内まで絞れるはず
        """

    def hit0_blow1(self) -> None:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        158400通り以内まで絞れるはず
        """

    def hit0_blow0(self) -> None:
        """
        hitandblowの情報から，可能性の無い数をall_numbers_listから消す
        55440通り以内まで絞れるはず
        """


if __name__ == "__main__":
    player_test_id1 = "6839fe8a-78ce-4d4c-92af-1962aa3b3cc5"
    player_test_name1 = "A"
    player_test_id2 = "7ae6a8d9-e168-46c0-9d5b-68ab13e383b0"
    player_test_name2 = "A2"

    print(player_test_name1)
    test_play_1 = NumberGuess(
        player_id=player_test_id1, player_name=player_test_name1)
    test_play_1.ROOM_ID = 1006
    test_play_1.check_enter_room()

    ans = test_play_1.hit1_blow4()
    ans.sort()
    print(ans)
    print(len(ans))
