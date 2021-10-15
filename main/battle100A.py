from number_guess_simple import NumberGuessSimple
import time

## 関数
def battle100(room_id:int, room_round:int=100, player_test_name:str="A", player_test_id:str = "6839fe8a-78ce-4d4c-92af-1962aa3b3cc5"):    
    """
    100回対戦用のコード．入力した部屋番号から昇順で連続して対戦する．
    Args:
        room_id (int): 対戦を行う最初の部屋
        room_round (int): 対戦回数
        player_test_name (str): プレイヤー名
        player_test_id (str): プレイヤーID
    Returns:
        None
    """
    battle_round = 0
    while battle_round < room_round:         
        myclass = NumberGuessSimple(player_id=player_test_id, player_name=player_test_name)
        # 対戦前準備
        myclass.set_room_id(room_id+battle_round)
        while not myclass.check_ready():
            myclass.try_enter_room()
            time.sleep(1)   
        myclass.define_answer()
        # 対戦
        while not myclass.judge_victory_or_defeat():
            if myclass.check_turn():
                myclass.number_guess_algorithm()     
            else:
                time.sleep(1)
        # 対戦後
        battle_round += 1
    return None

if __name__ == "__main__":  
    while True:
        try:          
            room_id = int(input("Room ID: "))
            if room_id>0:
                break
        except:
            print("自然数を入力してください．")
    battle100(room_id=room_id, room_round=100)