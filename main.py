# Coded by: Haxinja/Anikin Luke Abales
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import datetime
import firebase_admin
from firebase_admin import db
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import threading, base64

cred_data = {
    "type": "service_account",
    "project_id": "pycli-chat",
    "private_key_id": "6a73bc17d582174525a5e40e2685442dd77e5d59",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCPYnVtBQNKuVfr\nunVS/eMBVcggoxb9VQ95ID+N2Wnvf8x/hwt0zK5viVe9NV3ZYJZ7Ls5OMi/CjKMo\n+UIr5TQiAUjkAzhGej4yOwucBjZUxbn+DxxHY91tOkKeX1IGN2DRmdtT82dDte4d\nU+QJ/u/8bP47Dz8B2zqGEUOe+VU6nKaVpkYN1HyhBVPdWcy8uNEvt68pqnW+XBzD\ns7+loR1F91X+l79gKFjjmwCSshFKiGXM2NrbNi6J1u9Pk6SYLhZAulFiibzNupO1\nLFU/te4SisMhFDPvKrm2wX3RLtztm0I6fX31r68ED/vGR83jUxxwZqm72fX7SzD1\n2lWR/JmLAgMBAAECggEAFJLgczPXRL89fLHffc4M5uHOen229xi1GgCPk09RTQU9\nwZq4q8S8JChFMlKtqbBF8gea9fYWNkiEbNpUgq87q27FwmSCjFJOtFnBO7JZ1Ltz\ntEmqGXBHPbywrGrUU9dZtBmV3VY9SKZFNBNtKCYFfLyNlMnblOzxA9BcWeZAMs2V\nIo+0wMqik7Urlj9i1hOzV8piWXiKT5Iu7C928ux9j0DtBN5feMyuiyF3z74YhK7S\ndkw9jO7WvqjBKOiGdEXCb9BgxNkF7HRIwKj5VJPviF9Pik4quvMzUKqEUk0jegGD\nRjtsPKWpBRqxh30JHwbypV0nuPOqN6A6Vqq5S/nHKQKBgQDDIQNuFqh5EwX3Dt2b\n67s9PuyCCxQxTO+Yr53EzxUxxb+041blDrih7+48YmSw1Nrituu/cyNRraxkf5R7\nEV0gD9TRhXKd/23jEFhMf7vlb1Wxw5RjwGQN/SxYiuxAXORkhz6dAUAjivATDVnv\nq54L2dh8MputaeILJ2wvvy8XRwKBgQC8HST0NbrYXCPhF4thCy36kZCBhm3frVRG\nDa/XzM6IFCwm2gY/6UZ/hV/TUbU6IETFQOI/wRDGela9Zx0LLZJyS8oIhzTBNTLN\n0d9QYw5P6xAxCVm+rMSYN+wItoRfC6WCC70zZ1JFQuKe+BvCW3V2LWyHAexawSFe\nmzr6T3mVnQKBgFMDM3tdRlUj47DEcUEJG4Ilx+ZXIkMLEQ9q/vqggsrG7xTcdrZB\n+ghik366+U1FcM1stoSfThJMiX/Dyv5EV9LxCUANvsI6zZwA8x+wY9Zq9BEJPJLn\nYWmWIIyWpYWIP14JL3kJ9ChqzlG8p1tQLo+qIPBNc29mEVVfcyYo9ra3AoGAAJvH\nhtK1rAWASDYfSU0T9P+LjB+3M0YIQ8G/k98hu+b0zZte8c37YGY6DSDyiSGZl1nC\nYZpqR3oV1b8DpQmcs6nzGVv2m7lkVK4dHtFzNmb4QnBZTfiZGjT0GoMcooITIvyO\nvB/VcEvrF8CNtm89TgiPlVA4R4LgbMHryut+5TECgYAhoRuz9kk2yO5vMAAuJRbN\n7z+TuopOFRe7RSX6IYp8l7F2+wUcP5nhGSQYxmgZI3t6fDRUujfS9deev1fpPeEN\n/gRq58RvH94270AX+CeeHnp0HwPKnNNSMP+SqxYrrO+I/G4R34O5H8RG2rbc7gPx\nyAknaf4Lvd5Ga1e64GMcpg==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-qib69@pycli-chat.iam.gserviceaccount.com",
    "client_id": "112278219217537039383",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-qib69%40pycli-chat.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

cred = firebase_admin.credentials.Certificate(cred_data)
firebase_admin.initialize_app(cred, {"databaseURL": "https://pycli-chat-default-rtdb.firebaseio.com"})


class AESCipher:
    def __init__(self, key=None):
        self.key = key if key else get_random_bytes(32)
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def encrypt(self, plaintext):
        return self.cipher.encrypt(pad(plaintext, AES.block_size))

    def decrypt(self, encrypted):
        try:
            return unpad(self.cipher.decrypt(encrypted), AES.block_size)
        except Exception as err:
            # return "{Mismatch-Tkn}".encode('utf-8')
            return ''.encode('utf-8')

    def __str__(self):
        return "Key -> {}".format(self.key.hex())


class PyCliChat:
    def __init__(self):
        self.username = None
        self.token = None
        self.channel = "main"
        self.thread = None
        self.stop_event = None

    def enc_data(self, data):
        self.cipher = AESCipher(bytes(self.token, 'utf-8'))
        data = self.cipher.encrypt(data.encode('utf-8'))
        return base64.b64encode(data).decode('utf-8')

    def dec_data(self, data):
        self.cipher = AESCipher(bytes(self.token, 'utf-8'))
        data = base64.b64decode(data)
        return self.cipher.decrypt(data).decode('utf-8')

    def system_sf_db(self, message):
        ref = db.reference(f"/{self.channel}")
        timestamp = str(datetime.now())
        user = self.enc_data(f"({datetime.now():%Y-%m-%d})[SYSTEM]")
        message = self.enc_data(message)
        data = {
            "msg": message,
            "timestamp": timestamp,
            "username": user
        }
        ref.push(data)

    def sf_db(self, message): # store to database
        ref = db.reference(f"/{self.channel}")
        timestamp = str(datetime.now())
        user = self.enc_data(self.username)
        message = self.enc_data(message)
        data = {
            "msg": message,
            "timestamp": timestamp,
            "username": user
        }
        ref.push(data)

    def rf_db(self):  # retrieve from database
        ref = db.reference(f"/{self.channel}")
        messages = []
        chats = ref.get()
        try:
            for key, val in chats.items():
                username = self.dec_data(val["username"])
                message = self.dec_data(val["msg"])
                if(username != '' or message != ''):
                    messages.append(f'{username}: {message}')
            return messages
        except AttributeError:
            pass

    def send_message(self):
        message = entry.get()
        if(message.strip() != ""):
            self.sf_db(message)
            entry.delete(0, tk.END)

    def receive_messages(self):
        chat_history.config(state=tk.NORMAL)
        chat_history.delete(1.0, tk.END)
        messages = self.rf_db()
        try:
            for message in messages:
                chat_history.insert(tk.END, message + "\n")
            chat_history.config(state=tk.DISABLED)
            chat_history.see(tk.END)
        except:
            pass

    def refresh_thread(self):
        while not self.stop_event.wait(1):
            main_window.after(1000, self.receive_messages)

    def open_chatbox(self):
        self.token = token_entry.get()
        self.username = username_entry.get()
        if(ch_entry.get() != ""):
            self.channel = ch_entry.get()

        if(self.token.strip() == "" or self.username.strip() == ""):
            messagebox.showerror("Error", "Token and username cannot be empty.")
        elif(len(self.token) != 32):
            messagebox.showerror("Error", "Token Length must be equal to 32 characters!")
        else:
            self.system_sf_db(f"{self.username} has joined the chat!")
            main_window.deiconify()
            main_window.title(f"Channel: [{self.channel}] | PyChat - Welcome, {self.username}")
            main_window.geometry("400x400")
            main_window.configure(bg="black")
            main_window.resizable(0, 0)

            ch_label.destroy()
            ch_entry.destroy()
            token_label.destroy()
            token_entry.destroy()
            username_label.destroy()
            username_entry.destroy()
            login_button.destroy()

            global chat_history, entry

            chat_history = tk.Text(main_window, height=20, width=50, bg="black", fg="green")
            chat_history.config(state=tk.DISABLED)
            chat_history.pack()

            input_frame = tk.Frame(main_window, bg="black")
            input_frame.pack()

            entry = tk.Entry(input_frame, width=50, bg="black", fg="green")
            entry.bind("<Return>", lambda event: self.send_message())  # Bind the <Return> key event
            entry.pack(side=tk.LEFT)

            send_button = tk.Button(input_frame, text="Send", command=self.send_message, bg="black", fg="green")
            send_button.pack(side=tk.LEFT)

            send_button = tk.Button(input_frame, text="Refresh", command=self.receive_messages, bg="black", fg="green")
            send_button.pack()

            self.receive_messages()

            self.stop_event = threading.Event()
            self.thread = threading.Thread(target=self.refresh_thread)
            self.thread.start()

    def main(self):
        global main_window, ch_label, ch_entry, token_label, token_entry, username_label, username_entry, login_button

        main_window = tk.Tk()
        main_window.title("(Haxinja's) PyChat - Login")
        main_window.geometry("300x150")
        main_window.configure(bg="black")
        main_window.resizable(0, 0)

        icon_url = "https://avatars.githubusercontent.com/u/108006281?v=4"
        # try:
        #     icon_data = urllib.request.urlopen(icon_url).read()
        #     icon_image = Image.open(io.BytesIO(icon_data))
        #     main_window.iconphoto(True, ImageTk.PhotoImage(icon_image))
        # except:
        #     print("Error loading app icon.")

        ch_label = tk.Label(main_window, text="Channel name (Default=main):", bg="black", fg="green")
        ch_label.pack()
        ch_entry = tk.Entry(main_window, bg="black", fg="green")
        ch_entry.pack()

        token_label = tk.Label(main_window, text="Token:", bg="black", fg="green")
        token_label.pack()
        token_entry = tk.Entry(main_window, bg="black", fg="green")
        token_entry.pack()

        username_label = tk.Label(main_window, text="Username:", bg="black", fg="green")
        username_label.pack()
        username_entry = tk.Entry(main_window, bg="black", fg="green")
        username_entry.pack()

        login_button = tk.Button(main_window, text="Login", command=self.open_chatbox, bg="black", fg="green")
        login_button.pack()

        main_window.mainloop()


if __name__ == "__main__":
    chat = PyCliChat()
    chat.main()

# My chat room token:
# 02601a81bbdb0e6e9afa27197dc3dc68
