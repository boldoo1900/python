# -*- coding: utf-8 -*-

import base64
import collections
import hashlib
import http.server
import mimetypes
import os
import random
import re
import threading
import time
import tkinter
import urllib

import PIL.Image  # Pillow
import PIL.ImageTk

random.seed()

DELTA = -240
INTERVAL = int(1 / 60 * 1000)
SIZE_BASE = 30
IMAGE_SIZE_BASE = 256
DIFFUSE_DELTA = 120
DIFFUSE_TRANSPARENT_DELTA = -10
DIFFUSE_TRANSPARENT_PLUS_TIME = 0.1
DIFFUSE_SCALE_DELTA = (IMAGE_SIZE_BASE + DIFFUSE_DELTA * 2) / IMAGE_SIZE_BASE
RATE = collections.defaultdict(lambda: 1, {
    "0": 0.75,
    "2": 2
})
HTML_BASE = open("index.html", "r", -1, "utf8").read()
FIXB_BASE = """<button name="fid" value="{}"><img src="{}" style="height:50pt;"></button>"""
ANCHOR = "<!---->"
_TRANSPARENT_NT = "#F0F0F0"
_TRANSPARENT_POSIX = "systemTransparent"
IMAGE_FILE_EXT = {
    "jpg", "jpeg", "jpe", "jfif", "pjpeg", "pjp",  # JPEG
    "png",  # PNG
    "gif",  # GIF
    "bmp", "dib",  # BMP
}
IMAGE_MIME_SUBTYPE = {"jpeg", "png", "gif", "bmp"}
IMAGE_URI_REGEX = re.compile(
    "^https?://([A-Za-z0-9][A-Za-z0-9\-]{1,61}[A-Za-z0-9]\.|[A-Za-z0-9]{1,2}\.)+[A-Za-z]+/[\w/:%#\$&\?\(\)~\.=\+\-]+\.(" + "|".join(
        IMAGE_FILE_EXT) + ")$|" +
    "^data:image/(" + "|".join(IMAGE_MIME_SUBTYPE) + ");base64,([0-9a-zA-Z/\+]+={0,3}$)"
)
IMAGE_GET_SEMAPHORE = threading.Semaphore()
queue = []
image_list = []


class server_handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('content-length'))
        data = urllib.parse.parse_qs(
            self.rfile.read(content_len).decode('utf-8'))
        queue.append(data)
        self.send_response_only(204)
        self.end_headers()
        self.close_connection = True

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_DATA)
        self.close_connection = True


class Motions(tkinter.Toplevel):
    def __init__(self, parent, screen_width, screen_height, q, *a, **k):
        super().__init__(parent, *a, **k)

        self.geometry("+{}+{}".format(screen_width, screen_height))
        self.overrideredirect(True)
        transparent(self)
        self.attributes("-topmost", True)
        self.configure(bg=TRANSPARENT)
        self._deploy(**q)
        self._x = screen_width
        self._y = screen_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.after(INTERVAL, self.setup)

    def select_motion(self, name):
        if name == "diffusion":
            self.tick = self._diffusion
            self.setup = self._diffusion_setup
        else:
            self.tick = self._to_left
            self.setup = self._to_left_setup

    def _to_left(self):
        t = time.time()
        self._x += int(self._d * (t - self._t))
        if self._x + self._W > 0:
            self.destroy()
            print("destroy", id(self))
        else:
            self.geometry("+{}+{}".format(self._x, self._y))
            self._t = t
            self.after(INTERVAL, self.tick)

    def _to_left_setup(self):
        size, x, y = self.geometry().split("+")
        w, h = size.split("x")
        self._W = int(w)
        self._H = int(h)
        self._y = random.randint(0, self.screen_height - self._H)
        self._t = time.time()
        self.tick()
        print("activate", id(self), size)

    def _diffusion(self):
        t = time.time()
        dx = int(self.dif_dx * (t - self._t))
        dy = int(self.dif_dy * (t - self._t))
        self._x -= dx
        self._y -= dy
        self._W += dx * 2
        self._H += dy * 2
        self._a += self.dif_a * (t - self._t)
        self._s = self._W / self._ws
        if self._a == 0:
            self.destroy()
            print("destroy", id(self))
        else:
            self.wm_attributes('-alpha', min(self._a, 1))
            self._content_resize(self._s)
            self._content.configure(
                width=int(self._W),
                height=int(self._H)
            )
            self.geometry("+{}+{}".format(
                self._x, self._y))
            self._t = t
            self.after(INTERVAL, self.tick)

    def _diffusion_setup(self):
        size, x, y = self.geometry().split("+")
        w, h = size.split("x")
        self._W = int(w)
        self._H = int(h)
        self._x = random.randint(0, self.screen_width - self._W)
        self._y = random.randint(0, self.screen_height - self._H)
        self._ws = self._W
        self._a = 1 - DIFFUSE_TRANSPARENT_PLUS_TIME * self.dif_a
        self._s = 1
        self._t = time.time()
        self.tick()
        print("activate", id(self), size, x, y)


class StringWindow(Motions):
    def _deploy(self,
                text=[""],
                color_R=["0"],
                color_G=["0"],
                color_B=["0"],
                speed=["1"],
                size=["1"],
                motion=["to_left"]):
        color = "#{:02x}{:02x}{:02x}".format(
            int(color_R[0]),
            int(color_G[0]),
            int(color_B[0]))
        self._d = DELTA * RATE[speed[0]]
        self._dif_d = DIFFUSE_DELTA * RATE[speed[0]]
        self.dif_dx = self._dif_d
        self.dif_dy = self._dif_d
        self.dif_ds = 1
        self.dif_a = DIFFUSE_TRANSPARENT_DELTA * RATE[speed[0]]
        self.select_motion(motion[0])
        self.rate = RATE[size[0]]
        self._content = tkinter.Label(self,
                                      text=text[0],
                                      bg=TRANSPARENT,
                                      fg=color,
                                      font=("", int(SIZE_BASE * self.rate))
                                      )
        self._content.pack()

    def _content_resize(self, scale=1):
        self._content.configure(
            font=("", int(SIZE_BASE * self.rate * scale))
        )


class ImageWindow(Motions):
    def _deploy(self,
                motion=["to_left"],
                speed=["1"],
                size=["1"],
                **k):
        self.select_motion(motion[0])
        image_file_name = get_image_filename(**k)
        image = PIL.Image.open(image_file_name)
        w, h = image.size
        self._d = DELTA * RATE[speed[0]]
        self.rate = RATE[size[0]]
        rate = IMAGE_SIZE_BASE / max(w, h) * self.rate
        self._dif_d = DIFFUSE_DELTA * RATE[speed[0]]
        self.dif_dx = self._dif_d * w / max(w, h)
        self.dif_dy = self._dif_d * h / max(w, h)
        self.dif_ds = DIFFUSE_SCALE_DELTA * self.rate
        self.dif_a = DIFFUSE_TRANSPARENT_DELTA * RATE[speed[0]]
        self.__image_w = int(w * rate)
        self.__image_h = int(h * rate)
        self.image = image.resize((self.__image_w, self.__image_h))
        self._img = PIL.ImageTk.PhotoImage(self.image)
        self._content = tkinter.Canvas(self,
                                       width=int(w * rate),
                                       height=int(h * rate),
                                       fill=TRANSPARENT,
                                       )
        self._content.create_image(self.__image_w / 2, self.__image_h / 2, image=self._img)
        self._content.place(x=0, y=0)
        self._content.pack()

    def _content_resize(self, scale=1):
        image = self.image.resize((
            int(self.__image_w * scale),
            int(self.__image_h * scale)
        ))
        del self._img
        self._img = PIL.ImageTk.PhotoImage(image)
        self._content.create_image(
            int(self.__image_w * scale / 2),
            int(self.__image_h * scale / 2),
            image=self._img)


OBJECTS = {
    -1: StringWindow,
    -2: ImageWindow
}


class MainWindow(tkinter.Tk):
    def __init__(self, server):
        super().__init__()
        self.title("2525")
        btn = tkinter.Button(self, text="shutdown", command=self.kill)
        btn.grid()
        self._server = server
        self.tick()
        self._screen_width = self.winfo_screenwidth()
        self._screen_height = self.winfo_screenheight()
        print("object control ready")

    def kill(self):
        self.destroy()
        self._server.shutdown()
        print("shutdown")

    def tick(self):
        self.after(INTERVAL, self.tick)
        while queue:
            q = queue.pop(0)
            ID = int(q["fid"][0])
            print(ID, q)
            if ID < 0:
                OBJECTS[ID](self, self._screen_width, self._screen_height, q)
            else:
                ImageWindow(self, self._screen_width, self._screen_height, q)


def main_server(host="", port=2525):
    try:
        server = http.server.ThreadingHTTPServer((host, port), server_handler)
    except Exception:
        server = http.server.HTTPServer((host, port), server_handler)
    threading.Thread(target=server.serve_forever, daemon=False)
    print("server ready")
    return server


def get_image_filename(uri=[""], fid=[""]):
    IMAGE_GET_SEMAPHORE.acquire()
    try:
        ID = int(fid[0])
        if ID <= 0:
            uri = uri[0]
            match = IMAGE_URI_REGEX.match(uri)
            assert match
            is_data_uri = uri[0] == "d"
            hashed = hashlib.sha256(uri.encode())
            digest = base64.b32encode(hashed.digest()).decode().replace("=", "")
            if is_data_uri:
                subtype = match.group(2)
                file_name = digest + "." + subtype
            else:
                file_name = digest + os.path.splitext(uri)[1]
            cache_dir = os.path.join(mypath, "cache")
            if not os.path.isdir(cache_dir):
                os.mkdir(cache_dir)
            file_name = os.path.join(cache_dir, file_name)
            if not os.path.isfile(file_name):
                if is_data_uri:
                    data = base64.b64decode(match.group(3))
                    with open(file_name, "wb") as wf:
                        wf.write(data)
                else:
                    urllib.request.urlretrieve(uri, file_name)
            return file_name
        else:
            return image_list[ID]
    finally:
        IMAGE_GET_SEMAPHORE.release()


def _transparent_nt(self):
    self.wm_attributes("-transparentcolor", _TRANSPARENT_NT)


def _transparent_posix(self):
    self.wm_attributes("-transparent", True)


if __name__ == "__main__":
    data = ""
    mypath = os.path.abspath(os.path.dirname(__file__))
    image_d = os.path.join(mypath, "image")
    for n, i in enumerate(
            filter(
                lambda x: os.path.splitext(x)[1][1:] in IMAGE_FILE_EXT,
                os.listdir(image_d)
            )
    ) if os.path.isdir(image_d) else []:
        p = os.path.join(mypath, "image", i)
        uri = "data:{};base64,{}".format(
            mimetypes.guess_type(i)[0],
            base64.b64encode(open(p, "rb").read()).decode()
        )
        data += FIXB_BASE.format(n, uri)
        image_list.append(p)
        print(n, i)
    if os.name == "nt":
        transparent = _transparent_nt
        TRANSPARENT = _TRANSPARENT_NT
    else:
        transparent = _transparent_posix
        TRANSPARENT = _TRANSPARENT_POSIX
    HTML_DATA = HTML_BASE.replace(ANCHOR, data).encode("utf8")
    MainWindow(main_server(port=2525)).mainloop()
