from main.number_guess_simple import NumberGuessSimple
import time

class BattleInPython(NumberGuessSimple):
    """
    コマンドでの対戦用に継承している．
    """
    def input_room_id(self) -> None:
        """
        部屋番号の入力
        """
        print("部屋番号を入力してください．チームAが使用する範囲={}".format(self.VACANT_ROOMS))
        while True:
            try:
                room_key = int(input("Enter the room number: "))
                if room_key == int(room_key):
                    if self.VACANT_ROOMS[0]<=room_key and self.VACANT_ROOMS[1]>room_key:
                        break
                    else:
                        print("番号が範囲外です．")
            except:
                print("整数ではありません．")
        self.set_room_id(room_key)
        return None

    def wait_the_opponent(self):
        """
        部屋が埋まるまで確認し続ける
        """
        flag = False
        while not flag:
            for i in range(10):
                flag = self.check_ready()
                if flag:
                    print("Standby state for the battle. Please input the hidden number.")
                    break
                time.sleep(1)
            if not flag:
                print("The opponent is not in the room.")
                input("Enter for retry: ")        
        return None

    def input_5digit(self) -> str:
        """
        5桁の数字の入力
        """
        while True:
            my_number = input("Number: ")
            flag = self.check_5digit(my_number)
            if flag:
                break
        return my_number
        

    def check_5digit(self, number_5:str) -> bool:
        """
        16進数5桁であるかの判定
        """
        flag = False
        if len(number_5) == 5:
            for i in number_5:
                if i in self.HEXADECIMAL:
                    if number_5.count(i) == 1:
                        flag=True
                    else:
                        print("{}が{}回使われています．".format(i, number_5.count(i)))
                        break
                else:
                    print("16進数以外の文字が使われています．")
                    break
        else:
            print("5桁の数字ではありません．")
        return flag

    def input_yn(self, disp_str: str):
        """
        yes/noの入力
        Args:
            disp_str (str): 文字列
        Returns:
            bool: 判定
        """        
        while True:
            try:
                ans = input(disp_str+" [y/n]:")
                if ans == "y":
                    return True
                elif ans == "n":
                    return False
            except:
                pass

    def loop_guess(self, suggest_mode = False) -> None:
        """
        対戦中の処理．決着がつくまでのループ処理
        """
        counter = 0
        while True:
            if self.check_turn():
                if suggest_mode:
                    self.suggest_number()
                counter = 0
                self.guess = self.input_5digit()
                self.post_register_guess(self.guess)             
                self.print_table_infomation()
                if self.judge_victory_or_defeat():
                    break
            else:
                counter = counter+1
                time.sleep(5)
                if self.judge_victory_or_defeat():
                    break
                if counter>12:
                    e_inp = self.input_yn(disp_str="A logn wait. Exit the room")
                    if e_inp:
                        break
                    counter = 0  

    def suggest_number(self):
        """
        number_guessから，Search_number，Calculation_Expected_Valueを実行
        結果を表示する
        """
        if self.guess !=None:
            self.Search_number(self.hit, self.blow)
            guess = self.Calculation_Expected_Value()
            print("Suggestion: {}".format(guess))

def player_select():
    while True:
        try:
            player_test_name = input("A/A2: ")
            if player_test_name=="A":
                player_test_id = "6839fe8a-78ce-4d4c-92af-1962aa3b3cc5"
                op_flag = False
                break
            elif player_test_name=="A2":
                player_test_id = "7ae6a8d9-e168-46c0-9d5b-68ab13e383b0"
                op_flag = True
                print("Battle against A")
                break
        except:
            pass
    print("Set player-{}, {}".format(player_test_name, "battle with A" if op_flag else "any opponents are not defined."))
    return player_test_name, player_test_id, op_flag

def main_fnc():  
    player_test_name, player_test_id, op_flag = player_select()
    test_play = BattleInPython(player_id=player_test_id, player_name=player_test_name)
    test_play.input_room_id()
    test_play.try_enter_room()
    test_play.wait_the_opponent()
    my_answer = test_play.input_5digit()
    test_play.post_register_answer(my_answer)    
    test_play.loop_guess(suggest_mode=test_play.input_yn("Do you need a support?"))

if __name__ == "__main__":
    main_fnc()
    pass