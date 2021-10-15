from typing import Union, List
import requests
import time
import sys

class RequestsAPI():
    def __init__(self, player_id, player_name):
        self.PLAYER_NAME:str = player_name
        self.PLAYER_ID:str = player_id
        self.ROOM_ID:int = None
        self.URL = "https://damp-earth-70561.herokuapp.com"

    def set_room_id(self, room_id:int):
        """
        クラス変数self.ROOM_IDへの登録．
        Args:
            room_id (int): 保持する部屋の番号
        Returns:
            None
        """
        self.ROOM_ID = room_id
        return None
        
    def __requests_get_wrapper(self, url: str, post_json: dict = None, headers: dict = None) -> Union[dict, List[dict]]:
        """
        getリクエストの処理用．
        Args:
            url (str): 使用するAPIのurl
            post_json (dict): 送信するjson
            headers (dict): 送信のheader
        Returns:
            dict or List[dict]: 取得したjson
        """
        resp = requests.get(url, headers=headers, json=post_json)
        if resp.status_code != 200: #確認用にprintして，もう一度送信する
            print("Response={}".format(resp.status_code))
            time.sleep(1)
            resp = requests.get(url, headers=headers, json=post_json)   
            if resp.status_code != 200: #ダメなら中断
                #sys.exit()
                pass
        return resp.json()

    def __requests_post_wrapper(self, url: str, post_json: dict = None, headers: dict = None) -> Union[dict, List[dict]]:
        """
        postリクエストの処理用．
        Args:
            url (str): 使用するAPIのurl
            post_json (dict): 送信するjson
            headers (dict): 送信のheader
        Returns:
            dict or List[dict]: 取得したjson
        """
        resp = requests.post(url, headers=headers, json=post_json)
        if resp.status_code != 200: #確認用にprintして，もう一度送信する
            print("Response={}".format(resp.status_code))
            time.sleep(1)
            resp = requests.post(url, headers=headers, json=post_json)            
            if resp.status_code != 200: #ダメなら中断
                #sys.exit()
                pass
        return resp.json()

    def get_rooms_info(self) -> List[dict]:
        """
        /rooms へのリクエスト．
        Returns:
            List[dict]: 取得したjson
        """
        url_get_all_room = self.URL + "/rooms"
        return self.__requests_get_wrapper(url_get_all_room)

    def get_room_info(self, room_id: int) -> dict:
        """
        /rooms/{room_id} へのリクエスト．
        Returns:
            dict: 取得したjson
        """
        url_get_room = self.URL + "/rooms/" + str(room_id)
        return self.__requests_get_wrapper(url_get_room)

    def get_table_infomation(self) -> dict:
        """
        /rooms/{room_id}/players/{player_name}/table へのリクエスト
        テーブルの情報を持ってくる．
        以下の関数はこの情報を使う．
        Returns:
            dict: 取得したjson
        """
        url_register_answer = self.URL + "/rooms/" + \
            str(self.ROOM_ID) + "/players/" + self.PLAYER_NAME + "/table"
        return self.__requests_get_wrapper(url_register_answer)

    def post_enter_room(self) -> dict:
        """
        /rooms/{room_id} へのリクエスト
        self.ROOM_IDの部屋にself.PLAYER_IDが入る
        Returns:
            dict: 取得したjson
        """
        url_get_all_room = self.URL + "/rooms"
        post_json = {
            "player_id": self.PLAYER_ID,
            "room_id": self.ROOM_ID,
        }
        return self.__requests_post_wrapper(url_get_all_room, post_json=post_json)

    def post_register_guess(self, number_guess: int) -> dict:
        """
        /rooms/{room_id}/players/{player_name}/table/guesses へのリクエスト
        Args:
            number_guess (int): 予測する数字
        Returns:
            dict: 取得したjson
        """
        headers = {"Content-Type": "application/json"}
        url_post_guessnumber = self.URL + "/rooms/" + \
            str(self.ROOM_ID) + "/players/" + self.PLAYER_NAME + "/table/guesses"
        post_data = {
            "player_id": self.PLAYER_ID,
            "guess": str(number_guess)
        }
        return self.__requests_post_wrapper(url_post_guessnumber, headers=headers, post_json=post_data)

    def post_register_answer(self, my_answer: str) -> int:
        """
        /rooms/{room_id}/players/{player_name}/hidden へのリクエスト
        相手に当ててもらう数を登録する
        Args:
            my_answer (str): 登録する答え
        Returns:
            dict: 取得したjson
        """
        url_register_answer = self.URL + "/rooms/" + \
            str(self.ROOM_ID) + "/players/" + self.PLAYER_NAME + "/hidden"
        post_data = {
            "player_id": self.PLAYER_ID,
            "hidden_number": my_answer
        }
        return self.__requests_post_wrapper(url_register_answer, post_json=post_data)