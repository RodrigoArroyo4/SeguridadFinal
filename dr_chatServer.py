import socket
import threading

import tkinter as tk

LARGE_FONT = ("Verdana", 12)
print("works")
bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindsocket.setblocking(1)
bindsocket.bind(('', 8082))
bindsocket.listen(5)
fromaddr = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class ChatApp(tk.Tk):

    def __init__(self, *args, **kwargs):
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
#esta pagina controla la conneccion
#usuario inserta su nombre y presiona conectar para realizar la conexion con el servidor
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # self.bind("<<ShowFrame>>", self.on_show_frame)
        # self.waitForConnection()
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.messageBox = tk.Text()
        self.messageBox.pack()

        sendMessageText = tk.Entry()
        sendMessageText.pack()

        sendButton = tk.Button(self, text="Send",
                            command=lambda: self.send_to_chat(sendMessageText.get()))
        sendButton.pack()

        connectButton = tk.Button(self, text="Connect", command=lambda: [self.waiting_thread(), self.connect()])

        connectButton.pack()


        # self.MessageArea = tk.Text(self, height = 25, width = 25, padx = 5, pady = 5)
        # self.MessageArea.pack()

    # def on_show_frame(self, event):
    #     print("waiting for connection")
    #     t = threading.Thread(target=self.waitForConnection())
    #     t.start()

    def send_to_chat(self, message):
        global s
        print(message + " sent")
        s.sendall(message.encode('ASCII'))

    def connect(self):
        global s
        s.connect(('', 8081))

    def recieve(self, newsocket):

        while True:
            print("recieving")
            data = None
            while data is None:
                data = newsocket.recv(1024)
            print("Server says: " + data.decode("ASCII"))
            self.messageBox.insert('1.0', data.decode("ASCII"))

    def waiting_thread(self):
        t = threading.Thread(target=self.waitForConnection)
        t.start()

    def waitForConnection(self):
        global bindsocket

        print("waiting for connection")
        # if __name__ == '__main__':

        while True:
            try:
                (newsocket, fromaddr) = bindsocket.accept()
                print(newsocket)
                t = threading.Thread(target=self.recieve, args=[newsocket])
                t.start()
                #t.join()
            except KeyboardInterrupt:
                print('Program closing...')
                break
        print("closing")
        bindsocket.close()


    def deal_with_client(conn, addr):
        data = None
        text = ''
        print('Chatting with: ' + str(addr))
        while text != 'disconnect':
            while data is None:
                data = conn.recv(1024)

            print("Client says: " + data.decode('ASCII'))

            if data.decode('ASCII') != 'disconnect':
                data = None
            else:
                break

            text = input('Server: ')
            conn.sendall(text.encode('ASCII'))
        conn.close()




app = ChatApp()
app.mainloop()



# read bloqueante
# def recieveMessage():






