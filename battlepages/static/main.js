//ユーザー情報登録
//当ててもらう数登録

//フォーム ✓
//数の登録
//ボタンで入力　✓
//post + hit blow win 情報
//テーブルの行追加　✓
//statusを絵で表示 ✓
//log流す　✓
//postボタンをunavailableにする
//トグル(部屋作成・特定の部屋指定（他の人がいるところ））（対人orCPU）で、CPU選択のときのみ部屋番号を送る？

//記録とか取る？database




/* 入力したら次の項目に移動*/
function nextfeild(str) {
    var flag_prob = textCheck(str);
    if (!flag_prob) {
        if (str.value.length >= str.maxLength) {
            for (var i = 0, elm = str.form.elements; i < elm.length; i++) {
                if (elm[i] == str) {
                    (elm[i + 1] || elm[0]).focus();
                    break;
                }
            }
        }
        document.girl.src = "https://res.cloudinary.com/hx3z2s9d0/image/upload/v1577199279/ritsu_2.png";
    }
    
    return (str);
}

/* 入力すると元の文字を消す*/ 
function clearfield(str) {
    str.value = "";
}

/* 0-9a-fにマッチする文字のみ使用可能*/ 
function textCheck(str) {
    // 文頭から文末まで全て0-9かチェック
    if(!str.value.match(/^[0-9a-f]+$/) && (str.value != "")){
        // そうでなければ入力文字を空白に変換
        str.value="";
        console.log(str.value);
        document.girl.src = "https://res.cloudinary.com/hx3z2s9d0/image/upload/v1577173674/ritsu_3.gif";
        status_logger("適切な文字を使用してね！");
        return true;
    }
    return false;
}

/*numボタンを押すときに呼び出す */
var activeEl = document.getElementById("number0");
//console.log(activeEl);
window.onclick = function(){
    activeEl = document.activeElement;
    //console.log(activeEl)
}
function num_button(button) { // "button" is button element
    const num_form_array = ["number0", "number1", "number2", "number3", "number4"]
    //var activeEl = document.activeElement;
    //console.log(num_form_array.includes(activeEl.id));
    //console.log((activeEl.id));
    if (num_form_array.includes(activeEl.id)) {
        activeEl.value = button.id.substr(7, 1); //ex) "0" of "button_0"
    }else{
        activeEl = document.getElementById("number0");
        activeEl.value = button.id.substr(7, 1);
    }
    nextfeild(activeEl);
}

/* post button */
function get_num_form(){
    num0 = document.getElementById("number0").value;
    num1 = document.getElementById("number1").value;
    num2 = document.getElementById("number2").value;
    num3 = document.getElementById("number3").value;
    num4 = document.getElementById("number4").value;
    return check_valid_num(num0 + num1 + num2 + num3 + num4);
}

function check_valid_num(num){
    if (num.match(/^[0-9a-f]+$/) && (num.length == 5)){
        if (existsSameValue(num)){
            return "input with duplicate";
        }
        //console.log(existsSameValue(num));
        return num;
    }else{
        return "input not properly"; //不適切な文字（たぶんない）か、文字数足りない
    }
}
// 重複チェッカ―
function existsSameValue(a){
    var s = new Set(a);
    return s.size != a.length;
}

/* clear button */
function all_clear() {
    document.getElementById("number0").value = "";
    document.getElementById("number1").value = "";
    document.getElementById("number2").value = "";
    document.getElementById("number3").value = "";
    document.getElementById("number4").value = "";
}

/* status log の表示*/
function status_logger(str, link=null, id="") {
    var dom = document.createElement("li");
    // リストタグにClass属性を付与
    dom.classList.add('box');

    //id付与
    dom.setAttribute('id', id);
    
    // 投稿内容を作成
    var a = document.createElement('a');
    var text = document.createTextNode(str);
    a.appendChild(text);
    if (link != null){
        a.href = link;
    }
    dom.appendChild(a);
    
    // 投稿内容をチャットエリアに追記
    var log_cont = document.getElementById("log");
    //console.log(log_cont);
    log_cont.appendChild(dom);
    // scrollの位置を一番下に
    const el = document.getElementById('log-container');
    el.scrollTo(0, el.scrollHeight);


}

/*logの非表示・再表示 */
document.getElementById('girl').addEventListener('click',function(){
    document.getElementById("place-of-log").animate([{opacity: '1'}, {opacity: '0'}], {
        duration: 500,      // アニメが終了するまでの時間(ミリ秒)
        fill: 'forwards'    // アニメ完了後に最初の状態に戻さない
    });
    document.getElementById("place-of-log").style.pointerEvents = "none";
    document.getElementById("visible-adviser").animate([{opacity: '0'}, {opacity: '1'}], {
        duration: 500,      // アニメが終了するまでの時間(ミリ秒)
        fill: 'forwards'    // アニメ完了後に最初の状態に戻さない
    });
    document.getElementById("visible-adviser").style.pointerEvents = "auto";
});
document.getElementById('visible-adviser').addEventListener('click',function(){
    document.getElementById("place-of-log").animate([{opacity: '0'}, {opacity: '1'}], {
        duration: 500,      // アニメが終了するまでの時間(ミリ秒)
        fill: 'forwards'    // アニメ完了後に最初の状態に戻さない
    });
    
    document.getElementById("place-of-log").style.pointerEvents = "auto";
    document.getElementById("visible-adviser").animate([{opacity: '1'}, {opacity: '0'}], {
        duration: 500,      // アニメが終了するまでの時間(ミリ秒)
        fill: 'forwards'    // アニメ完了後に最初の状態に戻さない
    });
    document.getElementById("visible-adviser").style.pointerEvents = "none";
});

/* エラー時のlog */
function error_occurreed(err=null) {
    message = "エラーが発生しました...";
    if (err != null){
        message = message + err;
    }
    status_logger(message);
    document.girl.src = "https://res.cloudinary.com/hx3z2s9d0/image/upload/v1577173674/ritsu_3.gif";
}
