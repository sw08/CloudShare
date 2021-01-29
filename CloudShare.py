import tkinter as tk
import tkinter.font
from tkinter import filedialog
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from os.path import isfile, isdir, abspath
from tkinter import messagebox
from tkinter.ttk import Combobox, Progressbar, Notebook
from random import randint
import binascii
from threading import Thread

firebase_data = {
    "type": "service_account",
    "project_id": "cloudshare-cefe6",
    "private_key_id": "9356698ac27921295f97614bd4aa7084192ad2f5",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDRkEiiLcnQjIHI\nbNjZW1phc+jzc8U6OGKIiAbNlyDymSv0JvJI6xjWma7m8Yecx/4L8ZqE80k131oI\nGpes45Dz1GG5GOyxqbNh0ihvXcNb5MedyvZHcJwaQI0JR3qDejUnsu5tjRK0qcfv\nf5KPM74Qg3NJCG37kdvs9KkiQaUuQvU3HMSYbgXOjyhcPEa7g+RGnC57jJXLoi9B\neAC4QPV1BAo8KMT6CNtR8AGPYEBsjIVmRLCRn98Mbpe4G5Tw2kW7L4ojtBepmqiS\n2/vR0zl1395lp6RfXioNgtqAkJPxiKyfYJSOOQZRGK+Hhvfthqywencr4/S/dj4Z\nYKWzNnl5AgMBAAECggEAAWyJD6Fqp99BolKCp/n8nbuKqxdeP6sSgWty1pE+6mK5\n+CQl+H5rAjKoUdD1JhRwifsOP8eoVL0+va9yZB+UpIWvyNmyXsPzkcUXqyeCoXUs\n1A/5Z28j3MSH+Yg2Tn5+CydsPN+xTIc95piqumm9L2H+u5eJew2hiSmEnOBLlopf\nbD90WuTCE5weLlr+WQZDVruDlMVELtsk5PJutYljviaanPQwNIjWjsgpjnY5h2d/\n5FJ0bVbl8RgSkkVTvfZi+I/KgyCpGEo4nH2ObHDRYXCo4w7Wf4LO7O0qwCYJuLbm\nR82PMLxEp4u41rHaYoAQu3NFzPxAqHyce8fg3chBDwKBgQDpeww6YDVMlFefOY7F\nuiWarxnrTnIFmxp3/rG4vLL7hPa3KHsYPq2r4lqPrARHuPhfctLi2VGij6A0KVj/\nV0r9Y8sJFcPEb9Cejgj+8ppxea/YCL1fP9Fp0KqWKXBCQDSDO0tgRDs1LmgtczQz\nfO+czSVqYViWjr4d4m9xa4G9QwKBgQDlxrEayD1kU701Zxdl+eIxtg/C69Ak7p++\nG11oiGSpA7ztG9c8N3ofesWQyAWdnW4JXLve7XNqPxPuc+DB9ayI4x5Gduj1hjjW\nNg/lHv+AXrp8Kh5ySP/drrG6MK3j4MpaROWSgLTRyotJUdQlT7HDrsFExWRnQCoL\nqOXo4TtEkwKBgQCAmS6eBJm2yUoNwEUcMTA/J8zN51I0Nj748sbuqrimgpDlRx2t\nt/AuaSlaUvO0kXP0FqmDGxG0yQkDUfbcBTefo1SUd3Fxg+jTPAZGbleUwuKQyheM\nG/l7H9ylgsN7KiQCWClnJ424+AuXZQnOhjTwF6pRErcZjhu3GB4ryXwXQwKBgQDJ\nampE99IY5+6rqTqxgWHuAZG/Y8aJGUOd+Y7f2u+h2Ez767O4bUj33z7fsvZ5O08B\nlfB5cdwB/lkSZTFX1Grxc2VOj12WG5om7Czyw0Fk3aTKwoD93U+smz3f4FwNrTaz\n+kDjMz9NxyZhlwFH05wX1FBGYGGqwGwa3GrswMKbUQKBgFVOUPWeef36P29RXqnv\nWWnbWtYjOnkUHmsJLMEMmKU9dsUrBcQfcqz1A76b8xKKmWMzus96dOLvhgnnbUJ0\nE+Ae6Xvqxi5cn1HAgDpwjj1qagjzzVaAIfDxvArIUqBJvXapfPoySP7PwKkPtYzl\nv6f0qAq/gzndB76+Oy5nKzPr\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-wrx41@cloudshare-cefe6.iam.gserviceaccount.com",
    "client_id": "109497707511971902408",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-wrx41%40cloudshare-cefe6.iam.gserviceaccount.com"
}

cred = credentials.Certificate(firebase_data)
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://cloudshare-cefe6-default-rtdb.firebaseio.com/'
})

root = tk.Tk()
root.title('CloudShare')
root.resizable(False, False)
root.geometry('275x325+100+100')
#root.iconbitmap(abspath('logo.ico'))

tabs = Notebook(root)
tabs.pack(fill='both', expand=True)

uploadframe = tk.Frame(root, bd=0)
downloadframe = tk.Frame(root, bd=0)
infoframe = tk.Frame(root, bd=0)

tabs.add(uploadframe, text='업로드')
tabs.add(downloadframe, text='다운로드')
tabs.add(infoframe, text='정보')

titleFont = tkinter.font.Font(family="맑은 고딕", size=20, weight="bold")
contentFont = tkinter.font.Font(family='맑은 고딕', size=12)


def convertBase(number, base):
    T="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    i,j=divmod(number,base)
    if i==0: return T[j]
    else: return convertBase(i,base)+T[j]

def addzero(code):
    for i in range(6-len(code)):
        code = '0' + code
    return code

def create_code():
    a = randint(0, 2176782335)
    a_36 = convertBase(a, 36)
    dir = db.reference(addzero(str(a_36)))
    while dir.get() is not None:
        a = randint(0, 2176782335)
        a_36 = convertBase(a, 36)
        dir = db.reference(addzero(str(a_36)))
    a_36 = (a_36).upper()
    return a_36

def makeCode():
    run_thread = Thread(target=create_code)
    run_thread.setDaemon(True)
    a = run_thread.start()
    return a

def collectUploadFile():
    route = filedialog.askopenfilename(initialdir="C:/", title='파일 선택')
    if route != '':
        UploadrouteEntry.delete(0, len(UploadrouteEntry.get()))
        UploadrouteEntry.insert(0, route)

def collectDownloadFile():
    route = filedialog.askdirectory(initialdir="C:/", title='폴더 선택')
    if route != '':
        DownloadrouteEntry.delete(0, len(DownloadrouteEntry.get()))
        DownloadrouteEntry.insert(0, route)

def uploadFile(route):
    if isfile(route):
        if CanusedCombo.get() not in ['1', '2', '3', '4', '5']:
            messagebox.showwarning("경고", '최대 파일 다운로드 횟수를 올바르게 입력해 주십시오')
            return
        code = makeCode()
        with open(route, 'rb') as f:
            binary = f.read()
        binary = binascii.hexlify(binary)
        route = route.replace('\\\\', '/').replace('\\', '/')
        filename = route.split('/') 
        filename = filename[len(filename)-1]
        code = addzero(code)
        dir = db.reference()
        binary = str(binary)
        canused = str(CanusedCombo.get())
        try:
            dir.update({code:
                {"filename": filename,
                "fileHex": binary,
                "used": "0",
                "canused": canused}
            })
            UploadcodeLabel.configure(text=f'파일 다운로드 코드: {code}')
        except:
            messagebox.showerror('오류', '파일을 업로드할 수 없습니다')
    else:
        messagebox.showwarning("경고", "파일이 존재하지 않습니다.")

def downloadFile():
    code = (DownloadCodeEntry.get()).upper()
    dir = db.reference(code)
    if dir.get() is None:
        messagebox.showwarning("경고", "서버에서 파일을 찾을 수 없습니다")
        return
    if not isdir(DownloadrouteEntry.get()):
        messagebox.showwarning("경고", "다운로드 파일을 저장할 폴더를 찾을 수 없습니다")
        return
    data = dir.get()
    binary = data['fileHex']
    filename = data['filename']
    binary = eval(f"b'{binary[2:]}")
    binary = binascii.unhexlify(binary)
    with open(f'{DownloadrouteEntry.get()}/{filename}', 'wb') as f:
        f.write(binary)
    if int(data['used']) == int(data['canused']):
        dir.delete()
        return
    data['used'] = str(int(data['used']) + 1)
    dir.update(data)

UploadrouteEntry = tk.Entry(uploadframe, font=contentFont, bg="#ffffff", width=20)
UploadrouteBtn = tk.Button(uploadframe, text='찾아보기', command=collectUploadFile, font=contentFont)
UploadBtn = tk.Button(uploadframe, text='업로드', command=lambda: uploadFile(UploadrouteEntry.get()), font=contentFont)
CanusedCombo = Combobox(uploadframe, values=['1', '2', '3', '4', '5'], font=contentFont, state='readonly')
UploadcodeLabel = tk.Label(uploadframe, font=contentFont, text='')

UploadrouteEntry.pack(pady=10, padx=20, fill='x')
UploadrouteBtn.pack()
CanusedCombo.pack(pady=10)
UploadBtn.pack()
UploadcodeLabel.pack(pady=20)

Label1 = tk.Label(downloadframe, text='다운로드할 폴더')
DownloadCodeEntry = tk.Entry(downloadframe, font=contentFont, bg='#ffffff')
DownloadBtn = tk.Button(downloadframe, text='다운로드', command=downloadFile, font=contentFont)
Label2 = tk.Label(downloadframe, text='다운로드 코드')
DownloadrouteEntry = tk.Entry(downloadframe, font=contentFont, bg="#ffffff", width=20)
DownloadrouteBtn = tk.Button(downloadframe, text='찾아보기', command=collectDownloadFile, font=contentFont)

Label1.pack(pady=10)
DownloadrouteEntry.pack()
DownloadrouteBtn.pack(pady=10)
Label2.pack()
DownloadCodeEntry.pack(pady=10)
DownloadBtn.pack()

makerLabel = tk.Label(infoframe, text='제작: Studio Orora', font=titleFont)
versionLabel = tk.Label(infoframe, text='버전: 1.0', font=titleFont)
makerLabel.pack()
versionLabel.pack()

CanusedCombo.set("다운로드 가능 횟수")

root.mainloop()