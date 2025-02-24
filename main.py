import tls_client 
import random
import time
import re
import toml
import ctypes
import threading
import string
import requests
import uuid

from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps
from logmagix import Logger, Home


with open('input/config.toml') as f:
    config = toml.load(f)

DEBUG = config['dev'].get('Debug', False)
log = Logger()

def debug(func_or_message, *args, **kwargs) -> callable:
    if callable(func_or_message):
        @wraps(func_or_message)
        def wrapper(*args, **kwargs):
            result = func_or_message(*args, **kwargs)
            if DEBUG:
                log.debug(f"{func_or_message.__name__} returned: {result}")
            return result
        return wrapper
    else:
        if DEBUG:
            log.debug(f"Debug: {func_or_message}")

def debug_response(response) -> None:
    debug(response.headers)
    debug(response.text)
    debug(response.status_code)

class Miscellaneous:
    @debug
    def get_proxies(self) -> dict:
        try:
            if config['dev'].get('Proxyless', False):
                return None
                
            with open('input/proxies.txt') as f:
                proxies = [line.strip() for line in f if line.strip()]
                if not proxies:
                    log.warning("No proxies available. Running in proxyless mode.")
                    return None
                
                proxy_choice = random.choice(proxies)
                proxy_dict = {
                    "http": f"http://{proxy_choice}",
                    "https": f"http://{proxy_choice}"
                }
                log.debug(f"Using proxy: {proxy_choice}")
                return proxy_dict
        except FileNotFoundError:
            log.failure("Proxy file not found. Running in proxyless mode.")
            return None

    @debug 
    def generate_email(self, domain: str = "cybertemp.xyz"):
        username = f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=20))}"
        email = f"{username}@{domain}"
        return email
    
    @debug 
    def randomize_user_agent(self) -> str:
        platforms = [
            "Windows NT 10.0; Win64; x64",
            "Windows NT 10.0; WOW64",
            "Macintosh; Intel Mac OS X 10_15_7",
            "Macintosh; Intel Mac OS X 11_2_3",
            "X11; Linux x86_64",
            "X11; Linux i686",
            "X11; Ubuntu; Linux x86_64",
        ]
        
        browsers = [
            ("Chrome", f"{random.randint(90, 140)}.0.{random.randint(1000, 4999)}.0"),
            ("Firefox", f"{random.randint(80, 115)}.0"),
            ("Safari", f"{random.randint(13, 16)}.{random.randint(0, 3)}"),
            ("Edge", f"{random.randint(90, 140)}.0.{random.randint(1000, 4999)}.0"),
        ]
        
        webkit_version = f"{random.randint(500, 600)}.{random.randint(0, 99)}"
        platform = random.choice(platforms)
        browser_name, browser_version = random.choice(browsers)
        
        if browser_name == "Safari":
            user_agent = (
                f"Mozilla/5.0 ({platform}) AppleWebKit/{webkit_version} (KHTML, like Gecko) "
                f"Version/{browser_version} Safari/{webkit_version}"
            )
        elif browser_name == "Firefox":
            user_agent = f"Mozilla/5.0 ({platform}; rv:{browser_version}) Gecko/20100101 Firefox/{browser_version}"
        else:
            user_agent = (
                f"Mozilla/5.0 ({platform}) AppleWebKit/{webkit_version} (KHTML, like Gecko) "
                f"{browser_name}/{browser_version} Safari/{webkit_version}"
            )
        
        return user_agent

    class Title:
        def __init__(self) -> None:
            self.running = False
            self.total = 0

        def increment_total(self):
            self.total += 1

        def start_title_updates(self, start_time) -> None:
            self.running = True
            def updater():
                while self.running:
                    self.update_title(start_time)
                    time.sleep(0.5)
            threading.Thread(target=updater, daemon=True).start()

        def stop_title_updates(self) -> None:
            self.running = False

        def update_title(self, start_time) -> None:
            try:
                elapsed_time = round(time.time() - start_time, 2)
                title = f'discord.cyberious.xyz | Total: {self.total} | Time Elapsed: {elapsed_time}s'

                sanitized_title = ''.join(c if c.isprintable() else '?' for c in title)
                ctypes.windll.kernel32.SetConsoleTitleW(sanitized_title)
            except Exception as e:
                log.debug(f"Failed to update console title: {e}")

class AccountCreator:
    def __init__(self, proxy_dict: dict = None) -> None:
        self.session = tls_client.Session("chrome_133", random_tls_extension_order=True)
        self.session.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'connection': 'keep-alive',
            'content-type': 'application/json',
            'host': 'api2.amplitude.com',
            'origin': 'https://app.requestly.io',
            'referer': 'https://app.requestly.io/',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': Miscellaneous().randomize_user_agent()
        }
        
        self.session.proxies = proxy_dict
        
        self.device_id = str(uuid.uuid4())
        self.session_id = int(time.time() * 1000 - random.randint(2000, 99999))
    
    @debug
    def send_verification_email(self, email: str) -> bool:
        params = {
            'key': 'AIzaSyC2WOxTtgKH554wCezEJ4plxnMNXaUSFXY',
        }

        json_data = {
            'requestType': 'EMAIL_SIGNIN',
            'email': email,
            'clientType': 'CLIENT_TYPE_WEB',
            'continueUrl': 'https://app.requestly.io/home',
            'canHandleCodeInApp': True,
        }

        response = requests.post(
            'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode',
            params=params,
            json=json_data,
        )

        debug_response(response)

        if response.status_code == 200:
            return True
        else:
            log.failure(f"Failed to send the verification email: {response.text}, {response.status_code}")
        
        return False
    
    @debug
    def get_user_id(self, email: str, oob_code: str) -> str: # Register
        params = {
            'key': 'AIzaSyC2WOxTtgKH554wCezEJ4plxnMNXaUSFXY',
        }

        json_data = {
            'email': email,
            'oobCode': oob_code,
        }

        response = requests.post(
            'https://identitytoolkit.googleapis.com/v1/accounts:signInWithEmailLink',
            params=params,
            json=json_data,
        )

        debug_response(response)

        if response.status_code == 200:
            return response.json().get("localId")
        else:
            log.failure(f"Failed to get the user id: {response.text}, {response.status_code}")
        

class EmailHandler:
    def __init__(self, api_key: str = None) -> None:
        self.session = requests.Session()

        if (api_key):
            self.session.headers = {"X-API-KEY": api_key}

    @debug
    def check_mailbox(self, email: str, max_retries: int = 5) -> list | None:
        debug(f"Checking mailbox for {email}")
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(f'https://www.cybertemp.xyz/api/getMail?email={email}')
                if response.status_code == 200:
                    return response.json()
                else:
                    log.failure(f"Failed to check mailbox: {response.text}, {response.status_code}")
                    debug(response.json(), response.status_code)
                    break
            except Exception as e:
                log.failure(f"Error checking mailbox: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
                break
        return None

    @debug
    def get_mail_id(self, email: str) -> str | None:
        attempt = 0
        debug(f"Getting verification message id for {email}")
        while attempt < 20: 
            messages = self.check_mailbox(email)
            if messages:
                for message in messages:
                    if 'Sign in to Requestly' in message.get("subject", ""):
                        debug(message)
                        return message.get("id")
            attempt += 1
            time.sleep(1.5)
        debug(f"No verification message found after {attempt} attempts")
        return None 

    @debug
    def fetch_message(self, email: str, message_id: str) -> dict | None:
        debug(f"Fetching message {message_id} for {email}")
        messages = self.check_mailbox(email)
        if messages:
            for message in messages:
                if message.get("id") == message_id:
                    return {
                        "text": message.get("content", ""),
                        "html": message.get("html", ""),
                        "subject": message.get("subject", "")
                    }
        return None
    
    @debug
    def get_verification_code(self, email: str) -> str | None:
        debug(f"Getting verification code for {email}")
        
        mail_id = self.get_mail_id(email)
        if mail_id:
            message = self.fetch_message(email, mail_id)
            if message:
                html_content = message.get("html", "")
                
                # Extract oobCode from the verification link
                oob_match = re.search(r'oobCode=([^&]+)', html_content)
                if oob_match:
                    return oob_match.group(1)
        return None

def create_account(api_key: str = None) -> bool:
    try:
        account_start_time = time.time()

        Misc = Miscellaneous()
        proxies = Misc.get_proxies()
        Email_Handler = EmailHandler(api_key)
        Account_Generator = AccountCreator(proxies)
        
        email = Misc.generate_email()

        log.info(f"Starting a new account creation process for {email[:8]}...")

        if Account_Generator.send_verification_email(email):
            log.info("Sent verification email, checking for verification code...")
            oob_code = Email_Handler.get_verification_code(email)
            log.info(f"Got code: {oob_code[:10]}.. registering....")
           
            if oob_code:
                uid = Account_Generator.get_user_id(email, oob_code)

                if uid:
                    with open("output/accounts.txt", "a") as f:
                        f.write(f"{email}:{uid}\n")
                        
                    log.message("Requestly", f"Account created successfully: {email[:8]}... ", account_start_time, time.time())
                    return True
                
        return False
    except Exception as e:
        log.failure(f"Error during account creation process: {e}")
        return False


def main() -> None:
    try:
        start_time = time.time()
        
        # Initialize basic classes
        Misc = Miscellaneous()
        Banner = Home("Requestly Generator", align="center", credits="discord.cyberious.xyz")
        
        # Display Banner
        Banner.display()

        thread_count = config['dev'].get('Threads', 1)
        api_key = config["data"].get("Cybertemp_Api_Key")

        # Start updating the title
        title_updater = Misc.Title()
        title_updater.start_title_updates(start_time)

        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            while True:
                futures = [
                    executor.submit(create_account, api_key)
                    for _ in range(thread_count)
                ]

                for future in as_completed(futures):
                    try:
                        if future.result():
                            title_updater.increment_total()
                    except Exception as e:
                        log.failure(f"Thread error: {e}")

    except KeyboardInterrupt:
        log.info("Process interrupted by user. Exiting...")
    except Exception as e:
        log.failure(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()