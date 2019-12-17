import socket
import threading
from random import randint
import tkinter as tk
from des import DesKey


LARGE_FONT = ("Verdana", 12)
bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindsocket.setblocking(1)
bindsocket.bind(('', 9000))
bindsocket.listen(5)
fromaddr = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
q = 1087
alpha = 59
key_exchange = None
priv_key = randint(1, q)
#  AXA mod q
pub_key = (alpha ** priv_key) % q
dh_key = 0
socket_list = []

class ChatApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        global cached_primes
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        F = StartPage
        frame = F(container,self)
        self.frames[F] = frame
        frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")
        #print(username)

    def create_window(self, cont):
        counter = 1
        t = tk.Toplevel()


class StartPage(tk.Frame):
    # esta pagina controla la conneccion
    # usuario inserta su nombre y presiona conectar para realizar la conexion con el servidor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.messageBox = tk.Text()
        self.messageBox.pack()
        sendMessageText = tk.Entry()
        sendMessageText.pack()

        sendToConn1 = tk.Button(self, text="Send To Connection 1",
                                command=lambda: self.send_to_1(sendMessageText.get()))
        sendToConn1.pack()

        sendToConn2 = tk.Button(self, text="Send To Connection 2",
                                command=lambda: self.send_to_2(sendMessageText.get()))
        sendToConn2.pack()

        self.waiting_thread()

        # connectButton = tk.Button(self, text="Connect", command=lambda: [self.waiting_thread(), self.connect()])
        #
        # connectButton.pack()



    def send_to_1(self, message):
        global s, shared_key
        print(message + " sent")
        to_send = message.encode('utf-8')
        to_send = shared_key.encrypt(to_send, padding=True)
        socket_list[0].sendall(to_send)

    def send_to_2(self, message):
        global s, shared_key
        print(message + " sent")
        to_send = message.encode('utf-8')
        to_send = shared_key.encrypt(to_send, padding=True)
        socket_list[1].sendall(to_send)

    def recieve(self, newsocket):
        print("DH_key:", dh_key)
        while True:
            print("recieving")
            data = None
            while data is None:
                data = newsocket.recv(1024)
            # decrypt
            data = shared_key.decrypt(data, padding=True)
            print("Server says: " + data.decode("utf-8"))
            self.messageBox.insert('1.0', data.decode("utf-8"))

    def waiting_thread(self):
        t = threading.Thread(target=self.waitForConnection)
        t.start()

    def waitForConnection(self):
        global bindsocket, s, key_exchange, pub_key, dh_key, shared_key, socket_list

        print("waiting for connection")

        while True:
            try:
                (newsocket, fromaddr) = bindsocket.accept()
                socket_list.append(newsocket)
                print("Connected")
                while True:
                    key_exchange = None
                    while key_exchange is None:
                        key_exchange = newsocket.recv(1024)
                        strings = str(key_exchange, 'utf8')
                        num = int(strings)
                        dh_key = (num ** priv_key) % q
                        str_temp = "00000" + str(dh_key)
                        print(str_temp)
                        shared_key = DesKey(str_temp.encode('utf-8'))
                        newsocket.sendall(bytes(str(pub_key), 'utf8'))

                    break
                print("DH_ Exchange", num)

                print(newsocket)
                t = threading.Thread(target=self.recieve, args=[newsocket])
                t.start()
                #t.join()
            except KeyboardInterrupt:
                print('Program closing...')
                break
        print("closing")
        bindsocket.close()

app = ChatApp()
app.mainloop()