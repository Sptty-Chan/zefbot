import requests, re, shutil, os, time
from base64 import b64decode
from urllib.parse import unquote
from bs4 import BeautifulSoup as parser


class App:
    def __init__(self):
        self.banner = "sdSSSSSSSbs    sSSs    sSSs    sSSs_sSSs     .S S.\n YSSSSSSSS%S   d%%SP   d%%SP   d%%SP~YS%%b   .SS SS.\n        S%S   d%S'    d%S'    d%S'     `S%b  S%S S%S\n       S&S    S%S     S%S     S%S       S%S  S%S S%S\n      S&S     S&S     S&S     S&S       S&S  S%S S%S\n      S&S     S&S_Ss  S&S_Ss  S&S       S&S   SS SS\n     S&S      S&S~SP  S&S~SP  S&S       S&S    S S\n    S*S       S&S     S&S     S&S       S&S    SSS\n   S*S        S*b     S*b     S*b       d*S    S*S\n .s*S         S*S.    S*S     S*S.     .S*S    S*S\n sY*SSSSSSSP   SSSbs  S*S      SSSbs_sdSSS     S*S\nsY*SSSSSSSSP    YSSP  S*S       YSSP~YSSY      S*S\n                      SP                       SP\n                      Y                        Y\n\n[==================================================]\n\n                Author: Sptty Chan\n       Github: https://github.com/sptty-chan\n      Facebook: http://fb.com/100024425583446\n\n[==================================================]\n"
        self.baseurl = "https://zefoy.com"
        self.baseheaders = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; Infinix X688B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.62 Mobile Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Host": "zefoy.com",
        }

    def create_session(self):
        modheaders = self.baseheaders
        modheaders["Sec-Fetch-Dest"] = "image"
        modheaders["Sec-Fetch-Mode"] = "no-cors"
        modheaders["Accept"] = "image/avif,image/webp,*/*"
        print(self.banner)
        print("[∆] Periksa gambar image.png dan masukkan kata yang anda lihat")
        print("[∆] ketik R/r untuk merefresh kode")
        while True:
            self.session = requests.Session()
            try:
                req = self.session.get(self.baseurl, headers=self.baseheaders).text
            except requests.exceptions.ConnectionError:
                exit("[∆] Koneksi internet anda terputus")
            capturl = self.baseurl + re.findall(
                r"(\/\w+\.php\?(.*))cl", req, re.MULTILINE
            )[0][0].split('"')[0].replace("amp;", "")
            captchapayload = {}
            pars = parser(req, "html.parser").find("form", {"method": "POST"})
            for z in pars("input"):
                try:
                    captchapayload[z["name"]] = z["value"]
                except:
                    if z["name"] == "token":
                        captchapayload["token"] = ""
                        continue
                    captchapayload["captcha"] = z["name"]
            saveimage = self.session.get(
                capturl, headers=modheaders, cookies=self.session.cookies, stream=True
            )
            with open("image.png", "wb") as wr:
                saveimage.raw.decode_content = True
                shutil.copyfileobj(saveimage.raw, wr)
                wr.close()
            code = input("[∆] Kode: ")
            if code not in list("Rr"):
                captchapayload[captchapayload["captcha"]] = code
                del captchapayload["captcha"]
                try:
                    postcapt = self.session.post(
                        self.baseurl,
                        headers=self.baseheaders,
                        cookies=self.session.cookies,
                        data=captchapayload,
                    ).text
                    self.nexturl = (
                        self.baseurl
                        + "/"
                        + parser(postcapt, "html.parser")
                        .find("div", {"class": "t-views-menu"})
                        .find("form")["action"]
                    )
                    self.gpayload = {
                        parser(postcapt, "html.parser").find(
                            "input", {"type": "search"}
                        )["name"]: ""
                    }
                    break
                except requests.exceptions.ConnectionError:
                    exit("[∆] Koneksi internet anda terputus")
                except AttributeError:
                    print("[∆] Kode salah")
                    print("[∆] Gambar pada file image.png telah diganti")
                    print("[∆] Periksa kembali file image.png & coba lagi")
            else:
                print("[∆] Gambar pada file image.png telah diganti")
                print("[∆] Periksa kembali file image.png & coba lagi")

    def postone(self):
        modheaders = self.baseheaders
        del modheaders["Upgrade-Insecure-Requests"]
        modheaders["X-Requested-With"] = "XMLHttpRequest"
        modheaders["Sec-Fetch-Dest"] = "empty"
        modheaders["Sec-Fetch-Site"] = "same-origin"
        modheaders["Origin"] = "https://zefoy.com"
        print("\n[==================================================]\n")
        print("[∆] Masukkan url video tiktok anda")
        while True:
            try:
                nest = self.session
                vturl = input("[∆] Url video tiktok: ")
                self.gpayload[list(self.gpayload.keys())[0]] = vturl
                test = nest.post(
                    self.nexturl,
                    headers=modheaders,
                    cookies=nest.cookies,
                    data=self.gpayload,
                ).text
                texter = (
                    b64decode(unquote(test[::-1])).decode("utf-8").replace("\n", "  ")
                )
                if "Please enter valid video URL" in texter:
                    print("[∆] Video tidak ditemukan")
                else:
                    break
            except requests.exceptions.ConnectionError:
                print("[∆] Koneksi internet anda terputus")
        self.submit(modheaders, vturl)

    def submit(self, modheaders, vturl):
        print("\n[==================================================]\n")
        print(
            "[∆] Jika gagal 3 kali berturut turut, aktifkan & matikan mode pesawat 5 detik"
        )
        print("[∆] Tekan ctrl + z jika ingin berhenti")
        print("\n[==================================================]\n")
        while True:
            try:
                sender = self.session.post(
                    self.nexturl,
                    headers=modheaders,
                    cookies=self.session.cookies,
                    data=self.gpayload,
                ).text
                pars = (
                    parser(
                        b64decode(unquote(sender[::-1]))
                        .decode("utf-8")
                        .replace("\n", "  "),
                        "html.parser",
                    )
                    .find("form")
                    .find("input")
                )
                payload = {pars["name"]: pars["value"]}
                submitr = self.session.post(
                    self.nexturl,
                    headers=modheaders,
                    cookies=self.session.cookies,
                    data=payload,
                ).text
                texter = (
                    b64decode(unquote(submitr[::-1]))
                    .decode("utf-8")
                    .replace("\n", "  ")
                )
                if "Successfully" in texter:
                    print("\r[✓] Sukses mengirim 1000 views")
                else:
                    print("\r[×] Gagal mengirim views")
            except AttributeError:
                print("\r[×] Gagal mengirim views")
            except requests.exceptions.ConnectionError:
                print("\r[×] Gagal mengirim views, koneksi terputus")
            for i in range(1, 301):
                print(f"\r[∆] Delay {300-i} detik", end="")
                time.sleep(1)


if __name__ == "__main__":
    os.system("clear")
    app = App()
    app.create_session()
    app.postone()
