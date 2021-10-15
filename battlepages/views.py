from django.views.generic import FormView
from django.http.response import JsonResponse
from .forms import NumberGuessForm
from main.number_guess_simple import NumberGuessSimple

class BattlePAgeView(FormView):
    template_name = "sample.html"
    form_class = NumberGuessForm
    success_url = "/post_success"
    PLAYERS = {} #ここで対戦情報を保持 keyは部屋のID, Tuple

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            data = self._post_django(request)
            return JsonResponse(data)
        return super().post(request, *args, **kwargs)

    def _post_django(self, request):
        print(request.POST)
        init = request.POST.get('init')
        guess = request.POST.get('guess')
        mode = request.POST.get('mode')
        room_id = request.POST.get('room_id')
        play_mode = int(mode)
        ##初期化##
        if init=="true": 
            ##対戦部屋の初期化##
            player_CPU = NumberGuessSimple(player_id="7ae6a8d9-e168-46c0-9d5b-68ab13e383b0", player_name="A2") 
            player_CPU.set_room_id(room_id)
            while not player_CPU.check_ready():
                player_CPU.try_enter_room()
            h_num = list(guess)
            h_num.reverse()
            dummy_ans = "".join(h_num)
            ## 解答の登録 ##
            if play_mode==2: #easy
                player_CPU.HEXADECIMAL = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
            h_ans = player_CPU.define_answer()
            ## 先手をとった時の予測 ## player1が先手番なので，いらないはず？
            if player_CPU.check_turn(): 
                if play_mode==3: #CPU
                    player_CPU.number_guess_algorithm_for_web()   
                else:
                    player_CPU.post_register_guess(dummy_ans)   
            ## クラスの保存 ##  
            self.PLAYERS[room_id] = (player_CPU, h_ans, dummy_ans)
            ## 対戦終了，GIVE UPした部屋の削除 ##               
            drop_id = []
            for account, _, _  in self.PLAYERS.values():
                if account.judge_victory_or_defeat():
                    drop_id.append(account.ROOM_ID)            
            if drop_id != []:
                for id in drop_id:
                    self.PLAYERS.pop(id)
            print("Using room ID: {}".format(list(self.PLAYERS.keys())))     
        ## 対戦中 ##
        elif init=="false":
            player_CPU, h_ans, dummy_ans = self.PLAYERS[room_id]
            if play_mode==1 or play_mode==2:
                res = player_CPU.post_register_guess(dummy_ans)
                print("Room {}: {}".format(room_id, res))
            elif play_mode==3:
                player_CPU.number_guess_algorithm_for_web()
        ## response to js ##
        data = {
            "h_number": h_ans,
        }
        return data