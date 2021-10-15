from number_guess import NumberGuess
import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class test_demo(unittest.TestCase):

    def test_all_func(self):
        test_play = NumberGuess()
        my_first_guess = test_play.first_guess()
        assert len(my_first_guess) == 5, "5桁ではありません"
        for i in my_first_guess:
            # 0~fが使われているか
            assert i in NumberGuess().HEXADECIMAL, "16進数以外の文字が使われています"
            # 文字が複数回使われていないか
            assert my_first_guess.count(
                i) == 1, i + "が" + str(my_first_guess.count(i)) + "回使われています"

        if test_play.hit == 4 and test_play.blow == 0:
            num_list = test_play.hit4_blow0()
            assert len(num_list) <= 55

        test_play.judge_func_from_hitandblow()

        my_guess = test_play.return_guess()
        assert len(my_guess) == 5, "5桁ではありません"
        for i in my_guess:
            # 0~fが使われているか
            assert i in NumberGuess().HEXADECIMAL, "16進数以外の文字が使われています"
            # 文字が複数回使われていないか
            assert my_guess.count(
                i) == 1, i + "が" + str(my_guess.count(i)) + "回使われています"

    def test_first_guess(self):
        my_first_guess = NumberGuess().first_guess()
        assert len(my_first_guess) == 5, "5桁ではありません"
        for i in my_first_guess:
            # 0~fが使われているか
            assert i in NumberGuess().HEXADECIMAL, "16進数以外の文字が使われています"
            # 文字が複数回使われていないか
            assert my_first_guess.count(
                i) == 1, i + "が" + str(my_first_guess.count(i)) + "回使われています"

    # def test_judge_func_from_hitandblow(self):
        # func = NumberGuess(hit=4, blow=0).judge_func_from_hitandblow()
        # assert func == NumberGuess().hit4_blow0()

    def test_return_guess(self):
        my_guess = NumberGuess().return_guess()
        assert len(my_guess) == 5, "5桁ではありません"
        for i in my_guess:
            # 0~fが使われているか
            assert i in NumberGuess().HEXADECIMAL, "16進数以外の文字が使われています"
            # 文字が複数回使われていないか
            assert my_guess.count(
                i) == 1, i + "が" + str(my_guess.count(i)) + "回使われています"

    def test_hit4_blow0(self):
        test_play = NumberGuess(guess="01234")
        num_list = test_play.hit4_blow0()
        assert len(num_list) == 55

    def test_hit3_blow2(self):
        test_play = NumberGuess(guess="01234")
        num_list = test_play.hit3_blow2()
        assert len(num_list) == 10

    def test_hit3_blow1(self):
        test_play = NumberGuess(guess="01234")
        num_list = test_play.hit3_blow1()

        assert len(num_list) == 110

    def test_hit3_blow0(self):
        test_play = NumberGuess(guess="01234")
        num_list = test_play.hit3_blow0()
        assert len(num_list) == 1100

    def test_hit2_blow3(self):
        test_play = NumberGuess(guess="01234")
        num_list = test_play.hit2_blow3()
        # num_list.sort()
        # print(num_list)
        assert len(num_list) == 20

    def test_hit2_blow2(self):
        test_play = NumberGuess(guess="01234")
        num_list = test_play.hit2_blow2()
        assert len(num_list) == 330

    def test_hit2_blow1(self):
        test_play = NumberGuess(guess="01234")
        num_list = test_play.hit2_blow1()
        assert len(num_list) == 6600

    def test_hit2_blow0(self):
        test_play = NumberGuess(guess="01234")
        num_list = test_play.hit2_blow0()
        assert len(num_list) == 9900

    def test_hit1_blow4(self):
        test_play = NumberGuess(guess="01234")
        num_list = test_play.hit1_blow4()
        assert len(num_list) == 45

    def test_hit1_blow3(self):
        test_play = NumberGuess(guess="01234")
        num_list = test_play.hit1_blow3()
        assert len(num_list) == 605

    def test_hit1_blow2(self):
        test_play = NumberGuess(guess="01234")
        num_list = test_play.hit1_blow2()
        assert len(num_list) == 10450

    def test_hit1_blow1(self):
        pass

    def test_hit1_blow0(self):
        pass

    def test_hit0_blow5(self):
        pass

    def test_hit0_blow4(self):
        pass

    def test_hit0_blow3(self):
        pass

    def test_hit0_blow2(self):
        pass

    def test_hit0_blow1(self):
        pass

    def test_hit0_blow0(self):
        pass

    def test_in_room_1006(self):
        pass
