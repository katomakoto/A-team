from number_guess_simple import NumberGuessSimple
from battle100A import battle100

def check_vacant_rooms(player_test_name, player_test_id):   
    """
    デバック用に空きの部屋を見つけるためのコード．引数はなんでもよい．
    """     
    myclass = NumberGuessSimple(player_id=player_test_id, player_name=player_test_name)
    j_list = myclass.get_rooms_info()
    rooms_info = []
    for j in j_list:
        rooms_info.append(j["id"])
    rooms_info.sort()
    print(rooms_info)
    return None

if __name__ == "__main__":   
    player_test_name, player_test_id = "A2", "7ae6a8d9-e168-46c0-9d5b-68ab13e383b0"
    check_vacant_rooms(player_test_name, player_test_id) 
    while True:
        try:          
            room_id = int(input("Room ID: "))
            if room_id>0:
                break
        except:
            print("自然数を入力してください．")
    battle100(room_id=room_id, room_round=100, player_test_name=player_test_name, player_test_id=player_test_id)