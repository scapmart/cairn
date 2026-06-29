import base64
import hashlib
import hmac
import time


class BitgetAuth:
    def __init__(self, api_key, api_secret, passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase

    def timestamp(self):
        return str(int(time.time() * 1000))

    def sign(self, timestamp, method, request_path, body=""):
        message = timestamp + method.upper() + request_path + body

        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256,
        ).digest()

        return base64.b64encode(signature).decode()

    def headers(self, method, request_path, body=""):
        ts = self.timestamp()
        sign = self.sign(ts, method, request_path, body)

        return {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": sign,
            "ACCESS-TIMESTAMP": ts,
            "ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json",
            "locale": "en-US",
        }