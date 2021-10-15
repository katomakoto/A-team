//var timer_wait_opponent;
//var timer_get_info;
//var flag_ready = false;

class GameApi extends Table {
    constructor() {
		super(headings, rows);
		this.player_id = null;
		this.player_name = null;
		this.room_id = null;
		//this.guess = null;
		//this.row_num = null;
		this.URL = "https://damp-earth-70561.herokuapp.com";
		this.array_cong_img = new Array("https://res.cloudinary.com/hx3z2s9d0/image/upload/v1633852701/congratulations/makeover.jpg", 
										"https://res.cloudinary.com/hx3z2s9d0/image/upload/v1634103726/congratulations/maid_tmp_img.png", 
										"https://res.cloudinary.com/hx3z2s9d0/image/upload/v1634120885/congratulations/openYourMouth.png",
										"https://res.cloudinary.com/hx3z2s9d0/image/upload/v1577196192/ritsu_1.png")
		this.array_cong_message = new Array("君のためにイメチェンしたんだけど...どう？", "こういうの好きって聞いたから...似合ってる..かな///", "お菓子作ったの！はい、あーん", "おめでとう！すごい！")
		this.hidden_number = null;
		this.your_turn = false;
		this.table_info = null;

		this.play_num = 0;

		this.flag_reset_table = true;
		
		//個人戦・CPU対戦のときの答えのhidden
		this.true_opponent_hidden = null;
		this.flag_give_up = false;

		this.timer_wait_opponent;
		this.timer_get_info;

		this.add_row = function(info_json) {
			this.turn += 1;
			info_json["n"] = this.turn_num;
			this.rows = [info_json];
			this.createRows();
		};
    
    }

    //get rooms
    get_all_rooms(){
		return $.ajax({
			url: this.URL + '/rooms/',
			type: 'GET',
			headers:{'X-CSRFToken': '{{csrf_token}}'},
			
			dataType: 'json'
		}).done(function(data, textStatus, jqXHR) {
			return data;
		}).fail(function (data, textStatus, errorThrown) {
			// 通信失敗時の処理
			var err = "(status_code : " + data.status + " [detail: " + data.responseJSON.detail + "])";
			error_occurreed(err=err);
		});
	}

    //1. enter room (これからスタートする！)
    enter_room(player_id, player_name, room_id, hidden_number){
		var self = this;
		if (room_id == ""){
			room_id = "1005";







		}
		this.player_id = player_id;
		this.player_name = player_name;
		this.room_id = parseInt(room_id);
		this.hidden_number = hidden_number;
		console.log(this.player_name);
		return $.ajax({
			url: this.URL + '/rooms',
			type: 'POST',
			headers: {     'Accept': 'application/json',     'Content-Type': 'application/json',   },
			
			data: JSON.stringify({"player_id": this.player_id,"room_id": this.room_id})
		}).done(function(data, textStatus, jqXHR) {
			self.game_ready();

		}).fail(function (data, textStatus, errorThrown) {
			// 通信失敗時の処理
			
			//入室出来ず、部屋のplayerでない場合に退出
			var response = self.get_room();
			response.then(function(data){
				if (data.player2 == self.player_name || data.player1 == self.player_name){
					status_logger("入室済みです");
					self.game_ready();
				}else {
					status_logger("部屋にすでに別の人が入っています...");
				}
			});	
		});
	}

	game_ready(){
		//初期化
		this.your_turn = false;
		this.table_info = null;
		this.flag_reset_table = true;
		//text 初期化
		document.getElementById("turn-text").innerText = "開始準備中";
		document.getElementById("opponent-guess").innerText = "xxxxx";
		document.getElementById("opponent-hit-number").innerText = 0;
		document.getElementById("opponent-blow-number").innerText = 0;

		//ゲーム用意
		this.play_num = this.play_num + 1;
		status_logger("", null, "line" + this.play_num.toString());
		var line = document.getElementById("line" + this.play_num.toString());
		line.innerHTML = '<a href="https://social-plugins.line.me/lineit/share?url=' 
							+ location.href.slice(0, location.href.length - location.hash.length) 
							+ '&text=ともだちがHIT AND BLOWで遊んでいるよ！%0a 部屋番号 ' 
							+ this.room_id.toString() 
							+ ' にアクセスして対戦しよう！" target="_blank" rel="nofollow noopener noreferrer">' 
							+ '<img src="https://res.cloudinary.com/hx3z2s9d0/image/upload/v1633444901/line_300_f0pk2i.jpg" width="40" height="40" alt="LINEで送る" /></a>';
		status_logger("部屋番号 " + this.room_id.toString() + " に入室出来たよ！上のアイコンから友達にシェアしよう！")
		document.getElementById("girl").src = "https://res.cloudinary.com/hx3z2s9d0/image/upload/v1577196192/ritsu_1.png";

		//待つ段階に移行
		this.start_timer_wait_opponent();
	}

	//2. そろうまで待つ
	start_timer_wait_opponent(){
		var self = this;
		status_logger("対戦相手を待ちます", null, "wait_opponent" + this.play_num.toString());
		self.timer_wait_opponent = setInterval(function(){self.wait_opponent()},1000);
	}
	wait_opponent(){
		var self = this;
		//log更新
		var text_tmp = document.getElementById("wait_opponent" + this.play_num.toString()).innerText;
        if (document.getElementById("wait_opponent" + this.play_num.toString()).innerText.length < 15){
            document.getElementById("wait_opponent" + this.play_num.toString()).innerText += ".";
        }else{
            document.getElementById("wait_opponent" + this.play_num.toString()).innerText = document.getElementById("wait_opponent" + this.play_num.toString()).innerText.slice(0, 9);
        }
		//相手が入室したかどうか情報をget
		var response = this.get_room();
        response.then(function(data){
            if (data.player2 != null){
				status_logger("相手が入室しました！");
				self.post_hidden();
			}
        });
	}

	get_room(){
		return $.ajax({
			url: this.URL + '/rooms/' + this.room_id.toString(),
			type: 'GET',
			headers:{'X-CSRFToken': '{{csrf_token}}'},
			
			dataType: 'json'
		}).done(function(data, textStatus, jqXHR) {
			return data;
		}).fail(function (data, textStatus, errorThrown) {
			// 通信失敗時の処理
			var err = "(status_code : " + data.status + " [detail: " + data.responseJSON.detail + "])";
			error_occurreed(err=err);
		});
	}

	//3. 繰り返す部分（入室したらpost hidden, table_info取る, guess登録する）
	post_hidden(){
		var self = this;
		return $.ajax({
			url: this.URL + "/rooms/" + this.room_id.toString() + "/players/" + this.player_name + "/hidden",
			type: 'POST',
			headers: {     'Accept': 'application/json',     'Content-Type': 'application/json',   },
			
			data: JSON.stringify({"player_id": this.player_id,"hidden_number": this.hidden_number})
		}).done(function(data, textStatus, jqXHR) {
			self.game_content();
			//return data;
		}).fail(function (data, textStatus, errorThrown) {
			// 通信失敗時の処理
			if (data.text == 400 || data.status == 400) {
				//self.game_content();
			}else{
				var err = "(status_code : " + data.status + " [detail: " + data.responseJSON.detail + "])";
				error_occurreed(err=err);
			}
		});
	}

	game_content(){
		var self = this;
		status_logger("準備完了！");
		clearInterval(self.timer_wait_opponent);
		
		console.log("done 'post_hidden' and start game")
		self.timer_get_info = setInterval(function(){self.get_table_info(false)},1000);
	}

	get_table_info(add_row_flag, guess=null){
		var self = this;
		var response = this.get_table();
		//console.log(response);
        response.then(function(data){
			self.table_info = data.table;
			if (self.table_info != null) {//すでに始まっているときのtableの処理
				if (self.table_info.length != 0 && self.flag_reset_table) { 
					self.flag_reset_table = false;
					add_row_flag = false;
					var array_rows = []
					for (var i=0; i< self.table_info.length; i++){
						var table_row = self.table_info[i]
						array_rows.push({n: i+1,guess: table_row.guess, hit: table_row.hit, blow: table_row.blow})
					}
					self.turn_num = i;
					self.rows = array_rows;
					self.createRows();

					const el = document.getElementById('left-hand');
                	el.scrollTo(0, el.scrollHeight);
				}
			}

			//相手のstatus
			if (data.opponent_table.length != 0) {
				var latest_opponent_status = data.opponent_table[data.opponent_table.length - 1]
				document.getElementById("opponent-guess").innerText = latest_opponent_status.guess;
				document.getElementById("opponent-hit-number").innerText = latest_opponent_status.hit;
				document.getElementById("opponent-blow-number").innerText = latest_opponent_status.blow;
			}			

			//post_guessに呼ばれた時の処理
			if (add_row_flag){
				
				if (guess == self.table_info[self.table_info.length - 1].guess){
					var table_tmp = self.table_info[self.table_info.length - 1]
					self.add_row({n: "",guess: table_tmp.guess, hit: table_tmp.hit, blow: table_tmp.blow});
					var hit_and_blow_status = table_tmp.hit + table_tmp.blow
					if (hit_and_blow_status > 4){
						status_logger("すごい！！！！");
					}else if (hit_and_blow_status > 3){
						status_logger("もう少し！");
						document.getElementById("girl").src = "https://res.cloudinary.com/hx3z2s9d0/image/upload/v1577196192/ritsu_1.png";
					}else if (hit_and_blow_status > 2){
						status_logger("いい感じ！！");
					}else if (hit_and_blow_status > 1){
						status_logger("その調子！");
						document.getElementById("girl").src = "https://res.cloudinary.com/hx3z2s9d0/image/upload/v1577199279/ritsu_2.png";
					}else {
						status_logger("がんばれ！");
					}
					const el = document.getElementById('left-hand');
                	el.scrollTo(0, el.scrollHeight);
				}
			}
			//通常の処理
			//console.log(data.winner);
			var flag_draw = false; //引き分け
			if (data.table.length != 0 && data.opponent_table.length != 0){
				if (data.table[data.table.length - 1].hit == 5 && data.opponent_table[data.opponent_table.length - 1].hit == 5){
					flag_draw = true;
				}
			}
			if (data.state == 3 || self.flag_give_up){ //終了
				console.log("勝者");
				console.log(data.winner);
				clearInterval(self.timer_get_info);
				if (flag_draw){
					status_logger("引き分け！頑張ったね！");
					
					//text
					document.getElementById("turn-text").innerText = "引き分け";
				}else if (data.winner == self.player_name){
					status_logger("やったね！おめでとう！");
					document.getElementById("girl").src = "https://res.cloudinary.com/hx3z2s9d0/image/upload/v1577196192/ritsu_1.png";
					//var index_int = Math.floor(Math.random() * 3)
					var index_int = 3;
					if (self.turn_num < 6){index_int = 0;}
					else if (self.turn_num < 9){index_int = 1;}
					else if (self.turn_num < 12){index_int = 2;}
					else{index_int = 3;}
					display_modal(self.array_cong_img[index_int], self.array_cong_message[index_int], "420px");
					
					//text
					document.getElementById("turn-text").innerText = "勝利！";
				}else{
					status_logger("残念...");
					document.getElementById("girl").src = "https://res.cloudinary.com/hx3z2s9d0/image/upload/v1577173674/ritsu_3.gif";
					
					//text
					document.getElementById("turn-text").innerText = "敗北...";
				}

				if (self.true_opponent_hidden != null) {
					document.getElementById("turn-text").innerText = "正解：" + self.true_opponent_hidden;
					document.getElementById("turn-status").style.zIndex = 1;
					
					//個人戦とCPU対戦の初期化
					self.flag_give_up = false;
					self.true_opponent_hidden = null;
				}
				

				//初期化
				document.getElementById("turn-text").style.color = "#229e6f";
				self.your_turn = false;
				self.turn_num = 0;
				self.flag_reset_table = true;
				document.getElementById("register-player-info-button").disabled = false;
				document.getElementById("post-button").disabled = true;
			}else if (data.now_player == self.player_name){
				if (self.your_turn == false) {
					self.your_turn = true;
					self.turn_num += 1;
					status_logger(self.turn_num.toString() +  "手目だよ！");
					document.getElementById("post-button").disabled = false;
					//text
					document.getElementById("turn-text").innerText = "あなたのターン";
					document.getElementById("turn-text").style.color = "#ff2121";
				}
			}else if (data.now_player != self.player_name){
				console.log(self.player_name);
				console.log(data.now_player);
				document.getElementById("post-button").disabled = true;
				console.log("opponent turn");
				self.your_turn = false;

				//text
				document.getElementById("turn-text").innerText = "相手のターン";
				document.getElementById("turn-text").style.color = "#212cff";
			}
        });
	}
	

	get_table(){
		return $.ajax({
			url: this.URL + '/rooms/' + this.room_id.toString() + "/players/" + this.player_name + "/table",
			type: 'GET',
			headers:{'X-CSRFToken': '{{csrf_token}}'},
			
			dataType: 'json'
		}).done(function(data, textStatus, jqXHR) {
			return data;
		}).fail(function (data, textStatus, errorThrown) {
			// 通信失敗時の処理
			var err = "(status_code : " + data.status + " [detail: " + data.responseJSON.detail + "])";
			error_occurreed(err=err);
		});
	}

    //post guess
    post_guess(guess){
		var self = this;
		
		return $.ajax({
			url: this.URL + "/rooms/" + this.room_id.toString() + "/players/" + this.player_name + "/table/guesses",
			type: 'POST',
			headers: {     'Accept': 'application/json',     'Content-Type': 'application/json',   },
			
			data: JSON.stringify({"player_id": this.player_id,"guess": guess})
		}).done(function(data, textStatus, jqXHR) {
			console.log(guess);
			self.get_table_info(true, guess);
			
		}).fail(function (data, textStatus, errorThrown) {
			// 通信失敗時の処理
			var err = "(status_code : " + data.status + " [detail: " + data.responseJSON.detail + "])";
			error_occurreed(err=err);
		});
	}
}

