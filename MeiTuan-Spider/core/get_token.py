import json
import zlib
import base64
from time import time
from urllib.parse import urlencode

# 解密美团token


class Encrypt(object):
    def _compress(self, data):
        # 进行数据压缩
        if isinstance(data, dict):
            data = json.dumps(data).replace(' ', '')
        data = bytes(data.encode())
        return zlib.compress(data)

    def _encode(self, data):
        # 进行数据的base64编码
        if not isinstance(data, bytes):
             data = bytes(data.encode())
        return base64.b64encode(data)

    def encrypt(self, data):
        # 进行token或sign加密
        _token = self._encode(self._compress(data))
        return _token.decode()


class Decrypt(object):
    def _decode(self, data):
        # 进行数据的base64解码
        return base64.b64decode(data)

    def _decompress(self, data):
        # 进行数据解码
        return zlib.decompress(data)


class Token(object):
    # 构造token
    def __init__(self, cur_href, ref_url, city, page, uuid):
        """
        :param cur_href: current-url
        :param ref_url: referer-url
        :param city: city name
        :param page: current-page
        :param uuid: cookies
        """
        self.encrypt = Encrypt()
        self.city = city
        self.page = page
        self.cookie = uuid
        self.cur_href = cur_href
        self.ref_url = ref_url
        self.sign = None
        self.token = None

    def __str__(self):
        sign = self.get_sign
        self.sign = self.encrypt.encrypt(sign)
        self.token = self.get_token(self.get_time, self.sign)
        return urlencode({'_token': self.encrypt.encrypt(self.token)})

    @property
    def get_time(self):
        # 获取1970-1-1至今的毫秒数
        return int(time() * 1000)

    def get_token(self, times, sign):
        # token值
        return {
            "rId": 100900,
            "ver": "1.0.6",
            "ts": times,
            "cts": times + 112,
            "brVD": [1366, 635],
            "brR": [[1366, 768], [1366, 738], 24, 24],
            "bI": [self.cur_href, self.ref_url],
            "mT": [],
            "kT": [],
            "aT": [],
            "tT": [],
            "aM": "",
            "sign": sign
        }

    @property
    def get_sign(self):
        _sign = f"areaId=0&cateId=0&cityName={self.city}&dinnerCountAttrId=&optimusCode=1&originUrl={self.cur_href}&page={self.page}&partner=126&platform=1&riskLevel=1&sort=&userId=&uuid={self.cookie}"
        return f'"{_sign}"'
