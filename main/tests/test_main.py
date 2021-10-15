import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from main.hitandblow import HitAndBlow

class test_demo(unittest.TestCase):
    def test_all_fnc(self):
        """
        対戦のための関数のテスト
        空いている部屋を探して，すべて行う
        """
        return None
        player_test_id1 = "6839fe8a-78ce-4d4c-92af-1962aa3b3cc5"
        player_test_name1 = "A"
        player_test_id2 = "7ae6a8d9-e168-46c0-9d5b-68ab13e383b0"
        player_test_name2 = "A2"
        # 空いている部屋に入る
        print(player_test_name1)        
        test_play_1 = HitAndBlow(player_id=player_test_id1, player_name=player_test_name1)
        test_play_1.define_room_id() 
        test_play_1.check_enter_room()
        # Aのいる部屋に入る
        print(player_test_name2)                
        test_play_2 = HitAndBlow(player_id=player_test_id2, player_name=player_test_name2, random_state=2)
        test_play_2.define_room_id(opponent_name="A") 
        test_play_2.check_enter_room()

        assert test_play_1.ROOM_ID == test_play_2.ROOM_ID

        #部屋の確認
        resp = test_play_1.get_room_info(test_play_1.ROOM_ID)
        assert resp['player1'] == player_test_name1
        assert resp['player2'] == player_test_name2
        assert test_play_1.check_ready() == test_play_2.check_ready()

        #数字の定義
        my_answer_1 = test_play_1.define_answer()
        my_answer_2 = test_play_1.define_answer()
        my_answer_3 = test_play_2.define_answer()

        #assert my_answer_1 == my_answer_2
        assert my_answer_1 != my_answer_3
        print(my_answer_1)
        print(my_answer_2)

        #数字の登録
        test_play_1.register_answer(my_answer_2)
        test_play_2.register_answer(my_answer_3)

        def print_room_information(test_play):
            resp = test_play.get_room_info(test_play.ROOM_ID)
            print(resp)

        def print_table_infomation(test_play):
            print("now_player: {}, hit: {}, blow: {}, winner: {}, game_end_count: {}".format(
                test_play.nowplayer, test_play.hit, test_play.blow, test_play.winner, test_play.game_end_count
            ))
        
        def check_5digit(number_guess):
            assert len(number_guess) == 5, "5桁ではありません"
            for i in number_guess:
                # 0~fが使われているか
                assert i in test_play_1.HEXADECIMAL, "16進数以外の文字が使われています"
                # 文字が複数回使われていないか
                assert number_guess.count(
                    i) == 1, i + "が" + str(number_guess.count(i)) + "回使われています"

        print_room_information(test_play_1)

        #数あて
        test_play_1.number_guess()
        check_5digit(test_play_1.guess)

        test_play_1.register_guess()
        test_play_1.table_infomation()
        print_table_infomation(test_play_1)

        test_play_2.number_guess()
        check_5digit(test_play_2.guess)

        test_play_2.register_guess()
        test_play_2.table_infomation()
        print_table_infomation(test_play_2)

        print_room_information(test_play_1)

    def test_in_room_1006(self):
        """
        対戦のための関数のテスト,各部屋で一度しかできない入出と数字の登録は除く
        room_id=1006でテスト
        """
        player_test_id1 = "6839fe8a-78ce-4d4c-92af-1962aa3b3cc5"
        player_test_name1 = "A"
        player_test_id2 = "7ae6a8d9-e168-46c0-9d5b-68ab13e383b0"
        player_test_name2 = "A2"

        print(player_test_name1)        
        test_play_1 = HitAndBlow(player_id=player_test_id1, player_name=player_test_name1)
        test_play_1.ROOM_ID = 1006
        test_play_1.check_enter_room()

        print(player_test_name2)                
        test_play_2 = HitAndBlow(player_id=player_test_id2, player_name=player_test_name2, random_state=2)
        test_play_2.ROOM_ID = 1006
        test_play_2.OPPONENT_NAME = "A"
        test_play_2.check_enter_room()

        assert test_play_1.ROOM_ID == test_play_2.ROOM_ID

        #部屋の確認
        resp = test_play_1.get_room_info(test_play_1.ROOM_ID)
        assert resp['player1'] == player_test_name1
        assert resp['player2'] == player_test_name2
        assert test_play_1.check_ready() == test_play_2.check_ready()

        #数字の定義
        my_answer_1 = test_play_1.define_answer()
        my_answer_2 = test_play_1.define_answer()
        my_answer_3 = test_play_2.define_answer()

        #assert my_answer_1 == my_answer_2
        assert my_answer_1 != my_answer_3
        print(my_answer_1)
        print(my_answer_2)

        def print_room_information(test_play):
            resp = test_play.get_room_info(test_play.ROOM_ID)
            print(resp)

        def print_table_infomation(test_play):
            print("now_player: {}, hit: {}, blow: {}, winner: {}, game_end_count: {}".format(
                test_play.nowplayer, test_play.hit, test_play.blow, test_play.winner, test_play.game_end_count
            ))
        
        def check_5digit(number_guess):
            assert len(number_guess) == 5, "5桁ではありません"
            for i in number_guess:
                # 0~fが使われているか
                assert i in test_play_1.HEXADECIMAL, "16進数以外の文字が使われています"
                # 文字が複数回使われていないか
                assert number_guess.count(
                    i) == 1, i + "が" + str(number_guess.count(i)) + "回使われています"

        print_room_information(test_play_1)

        #数あて
        test_play_1.number_guess()
        check_5digit(test_play_1.guess)

        test_play_1.register_guess()
        test_play_1.table_infomation()
        print_table_infomation(test_play_1)

        test_play_2.number_guess()
        check_5digit(test_play_2.guess)

        test_play_2.register_guess()
        test_play_2.table_infomation()
        print_table_infomation(test_play_2)

        print_room_information(test_play_1)
