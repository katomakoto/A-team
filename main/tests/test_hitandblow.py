from main.hitandblow import HitAndBlow
import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class test_demo(unittest.TestCase):
    def setUp(self) -> None:
        self.test_play = HitAndBlow(
            player_id="6839fe8a-78ce-4d4c-92af-1962aa3b3cc5", player_name="A")

        # 対象の部屋番号を1つ探し、それをself.ROOM_IDに設定する
        rooms_info = self.test_play.get_rooms_info()
        for room_info in rooms_info:
            if room_info["id"] > 0:  # 0はresponseの挙動がおかしい
                self.test_play.ROOM_ID = room_info["id"]
                ans = self.test_play.check_ready()
                if ans and (room_info["player1"] == self.test_play.PLAYER_NAME
                            or room_info["player2"] == self.test_play.PLAYER_NAME):
                    # and 1000 <= room_info["id"] <= 1999
                    self.test_play.ROOM_ID = room_info["id"]
                    break

        if self.test_play.ROOM_ID == None:
            raise NotImplementedError()

    def test_initialization(self):
        """
        PLAYER_IDとPLAYER_NAMEへ反映されているかの確認
        player_id="A"
        """
        player_test_id = "6839fe8a-78ce-4d4c-92af-1962aa3b3cc5"
        player_test_name = "A"

        test_play = HitAndBlow(player_id=player_test_id,
                               player_name=player_test_name)

        assert test_play.PLAYER_ID == player_test_id
        assert test_play.PLAYER_NAME == player_test_name

    def test_define_room_id(self):
        """
        define_room_idの検証
        """
        player_test_id = 0  # "6839fe8a-78ce-4d4c-92af-1962aa3b3cc5"
        player_test_name = "A"
        test_play = HitAndBlow(player_id=player_test_id,
                               player_name=player_test_name)

        #
        ans = test_play.define_room_id()
        print('ID of a vacant room = {}'.format(ans))
        assert ans == test_play.ROOM_ID

        # 対戦相手がいる場合の操作
        # room_id=2 team=F 2021/09/23
        ans = test_play.define_room_id(opponent_name="F")
        assert ans == 2

        # keyのミス
        ans = test_play.define_room_id(wrong_key_name="A2")
        assert ans == -1

        # 対戦相手がいる場合の操作
        # room_id=5 team=A 2021/09/23
        player_test_id = 0  # "7ae6a8d9-e168-46c0-9d5b-68ab13e383b0"
        player_test_name = "A2"
        test_play2 = HitAndBlow(player_id=player_test_id,
                                player_name=player_test_name)
        ans = test_play2.define_room_id(opponent_name="A")
        assert ans == 5

        # 対戦相手がいる場合の操作，該当なし
        # room_id=5 team=A 2021/09/23
        player_test_id = 0  # "7ae6a8d9-e168-46c0-9d5b-68ab13e383b0"
        player_test_name = "A"
        test_play2 = HitAndBlow(player_id=player_test_id,
                                player_name=player_test_name)
        ans = test_play2.define_room_id(opponent_name="A2")
        assert ans == -1

    def test_check_enter_room(self):
        """
        check_enter_room
        enter_room
        """
        player_test_id = "6839fe8a-78ce-4d4c-92af-1962aa3b3cc5"
        player_test_name = "A2"

        # 空いている部屋に入る
        test_play = HitAndBlow(player_id=player_test_id,
                               player_name=player_test_name)
        test_play.define_room_id()
        # test_play.check_enter_room() ##実際に入力するのでコメントアウト

        # Aのいる部屋に入る
        test_play = HitAndBlow(player_id=player_test_id,
                               player_name=player_test_name)
        test_play.define_room_id(opponent_name="A")
        # test_play.check_enter_room() ##実際に入力するのでコメントアウト

        # 部屋の確認
        resp = test_play.get_rooms_info()
        print("check enter room:")
        for room_info in resp:
            print(room_info)

    def test_check_ready(self):
        """
        check_ready
        """
        print("")
        test_play = HitAndBlow(player_id="A", player_name="A")
        rooms_info = test_play.get_rooms_info()
        for room_info in rooms_info:
            if room_info["id"] > 0:  # 0はresponseの挙動がおかしい
                test_play.ROOM_ID = room_info["id"]
                ans = test_play.check_ready()
                print("{} <- {}".format(ans, room_info))

    def test_define_answer(self):
        """
        test define_answer
        """
        test_play_1 = HitAndBlow(player_id="A", player_name="A")
        test_play_2 = HitAndBlow(
            player_id="A", player_name="A", random_state=10)
        my_answer_1 = test_play_1.define_answer()
        my_answer_2 = test_play_1.define_answer()
        my_answer_3 = test_play_2.define_answer()

        assert my_answer_1 == my_answer_2
        assert my_answer_1 != my_answer_3

    def test_register_answer(self):
        """
        test register_answer
        """
        my_answer = self.test_play.define_answer()
        assert self.test_play.register_answer(my_answer) == 200

    def test_table_infomation(self):
        """
        test table_infomation
        実際に動かしてみる必要あり
        """
        self.test_play.table_infomation()
        print("now_player: {}, hit: {}, blow: {}, winner: {}, game_end_count: {}".format(
            self.test_play.nowplayer, self.test_play.hit, self.test_play.blow, self.test_play.winner, self.test_play.game_end_count
        ))

    def test_hit_and_blow_check(self):
        """

        """
        pass

    def test_number_guess(self):
        """
        16進数5桁の文字列が出力されているかチェック
        """
        player_test_id = 0  # "6839fe8a-78ce-4d4c-92af-1962aa3b3cc5"
        player_test_name = "A"
        test_play = HitAndBlow(player_id=player_test_id,
                               player_name=player_test_name)
        number_guess = test_play.number_guess()
        # 5桁か
        assert len(number_guess) == 5, "5桁ではありません"
        for i in number_guess:
            # 0~fが使われているか
            assert i in test_play.HEXADECIMAL, "16進数以外の文字が使われています"
            # 文字が複数回使われていないか
            assert number_guess.count(
                i) == 1, i + "が" + str(number_guess.count(i)) + "回使われています"

    def test_register_guess(self):
        """
        test_register_guess
        """
        test_play = HitAndBlow(
            player_id="6839fe8a-78ce-4d4c-92af-1962aa3b3cc5", player_name="A")
        number_guess = test_play.number_guess()
        assert test_play.register_guess(number_guess) == 200
