/* 自動でプレイヤー情報入力 */
function auto_input_form(id, name){
    document.getElementById("player-id").value = id;
    document.getElementById("player-name").value = name;
}

// djangoとの通信のサンプル
function post_django(init, room_id, mode_number, guess_number){
    var form = $(this);
    return $.ajax({
        url: form.prop("action"),
        type: 'POST',
        dataType: 'json',
        
        data: {"init":init, "room_id":room_id, "mode":mode_number, "guess": guess_number}
    }).done(function(data, textStatus, jqXHR) {
        return data;
    });
}


function post_guess(){
    return $.ajax({
        url: 'https://damp-earth-70561.herokuapp.com/rooms/1005/players/A/table/guesses',
        type: 'POST',
        headers: {     'Accept': 'application/json',     'Content-Type': 'application/json',   },
        
        data: JSON.stringify({"player_id": "6839fe8a-78ce-4d4c-92af-1962aa3b3cc5","guess": "01234"})
    }).done(function(data, textStatus, jqXHR) {
        return data;
    }).fail(function (data, textStatus, errorThrown) {
        // 通信失敗時の処理
        err = "(status_code : " + data.status + " [detail: " + data.responseJSON.detail + "])";
        error_occurreed(err=err);
    });
}
