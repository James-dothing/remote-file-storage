auth_key = "SECRET_KEY_CHANGE_THIS_TO_WHATEVER_YOU_WANT_kldSFkwU23FflWcvSNJjl"

AUTO_DELETE = False # IF SET TO TRUE THE DELETED FILE IS LOST FOREVER
# IF AUTO DELETE IS SET TO FALSE THE DELETED FILE IS MOVED TO TRASH BIN FOLDER

FAST_ASSET_LOADING = True # IF SET TO TRUE THE ASSET IS STORED IN RAM
# FAST ASSET LOADING SHOULD TURN ON IF YOU WILLING TO SACRIFICE 500 KB OF RAM FOR FASTER ASSET LOADING
# FAST ASSET LOADING SHOULD TURN ON IF YOU'RE USING HDD TO STORE FILES

import os
import time
import shutil
import base64
import flask

app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024 * 1024

if not os.path.exists("access"):
    os.mkdir("access")
elif os.path.isfile("access"):
    raise "access is a file go remove or do whatever"

if not AUTO_DELETE:
    if not os.path.exists("trash-bin"):
        os.mkdir("trash-bin")
    elif os.path.isfile("trash-bin"):
        raise "trash-bin is a file go remove or do whatever"

if not os.path.exists("asset"):
    raise "missing asset folder"

assets = {}
index = ""
ce = ""

if FAST_ASSET_LOADING:
    index = open("asset/index.html", "r",  encoding="utf-8").read()
    ce = open("asset/login.html", "r",  encoding="utf-8").read()
    for file in os.listdir("asset"):
        if file.split(".")[1] == "png" or file.split(".")[1] == "ttf":
            assets[file] = open("asset/" + file, "rb").read()

def encode_base64(s):
    return base64.urlsafe_b64encode(s.encode("utf-8")).decode("utf-8")

def decode_base64(s):
    s += "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s).decode("utf-8")

def log(s):
    open("error_log.txt", "a").write(time.ctime() + ": "+ str(s) +"\n")

@app.route("/")
def home():
    auth = flask.request.cookies.get("token")
    if not auth == auth_key:
        return ce, 200
    if FAST_ASSET_LOADING:
        return index, 200
    return open("asset/index.html", "r",  encoding="utf-8").read(), 200

@app.route("/view")
def view():
    auth = flask.request.cookies.get("token")
    if not auth == auth_key:
        print(flask.request.headers.get("User-Agent"))
        flask.abort(401)

    raw_path = flask.request.args.get("p")
    path_to_des = "access"
    if raw_path:
        try:
            parts = decode_base64(raw_path)
            path_to_des = os.path.join(path_to_des, parts)
        except Exception as e:
            log(e)
            flask.abort(404, 'ERROR BASE64 IS INVAILD OR IDK IF OPERATOR READING THIS CHECK THE ERROR LOG FOLDER')

    if not os.path.exists(path_to_des):
        flask.abort(404, 'file or folder not found')

    if os.path.isfile(path_to_des):
        return flask.send_file(path_to_des)
    
    flask.abort(400, "no")

@app.route("/asset")
def get_asset():
    asset_name = flask.request.args.get("a")

    if not asset_name:
        flask.abort(400, "missing asset name guh")

    if FAST_ASSET_LOADING:
        if asset_name + ".png" in assets:
            return assets[asset_name + ".png"], 200
        if asset_name + ".ttf" in assets:
            return assets[asset_name + ".ttf"], 200
        
    if os.path.exists(os.path.join("asset",asset_name+".png")):
        return open(os.path.join("asset",asset_name+".png"), "rb"), 200
    if os.path.exists(os.path.join("asset",asset_name+".ttf")):
        return open(os.path.join("asset",asset_name)+".ttf", "rb"), 200
    
    flask.abort(404, "asset not found")

@app.route("/file", methods=["GET", "POST", "PATCH", "DELETE"])
def download():
    auth = flask.request.cookies.get("token")
    if not auth == auth_key:
        print(flask.request.headers.get("User-Agent"))
        flask.abort(401)
    
    raw_path = flask.request.args.get("p")
    path_to_des = "access"
    if raw_path:
        try:
            parts = decode_base64(raw_path)
            path_to_des = os.path.join(path_to_des, parts)
        except Exception as e:
            log(e)
            flask.abort(404, 'ERROR BASE64 IS INVAILD OR IDK IF THE OPERATOR READING THIS CHECK THE ERROR LOG FOLDER')

    if not os.path.exists(path_to_des):
        flask.abort(404, 'file or folder not found')

    if flask.request.method == "GET":
        if os.path.isfile(path_to_des):
            return flask.send_file(path_to_des, as_attachment=True)
        files = []
        folders = []
        for (dirpath, dirnames, filenames) in os.walk(path_to_des):
            files.extend(filenames)
            folders.extend(dirnames)
            break
        return {"children": {"files": files, "folders": folders}}, 200
    
    if flask.request.method == "POST":
        if os.path.isfile(path_to_des):
            flask.abort(400, "the path to place the file is a file not a folder this is not roblox buddy >:(")

        NN = flask.request.args.get("f")

        if NN:
            try:
                NN = decode_base64(NN)
            except:
                flask.abort("failed to decode base64", 400)
            os.mkdir(os.path.join(path_to_des, NN))
            return {}, 200
        files = flask.request.files.getlist("file")

        if not files or files[0].filename == "":
            flask.abort(400, "no file were uploaded")

        saved_files = []

        for file in files:
            filename = file.filename
            filepath = os.path.join(path_to_des, filename)

            # stream :D
            with open(filepath, "wb") as f:
                while True:
                    chunk = file.stream.read(1024 * 1024)  # 1MB
                    if not chunk:
                        break
                    f.write(chunk)

            saved_files.append(filename)

        return {}, 200

    if flask.request.method == "PATCH":

        NN = flask.request.args.get("n")

        if not NN:
            flask.abort(400, "Missing new name parameter")
         
        name = ""
        try:
            NN = decode_base64(NN)
            name = os.path.basename(path_to_des)
        except Exception as e:
            log(e)
            flask.abort(400,"the naming is invaild >:(")
        
        if os.path.isfile(path_to_des):
            if not '.' in NN:
                NN = NN + "." + name.split(".")[len(name.split("."))-1]
            elif len(NN.split(".")[len(NN.split("."))-1]) > 4:
                NN = NN + "." + name.split(".")[len(name.split("."))-1]

        try:
            parent = os.path.dirname(path_to_des)
            new_name = os.path.join(parent, NN)
            os.rename(path_to_des, new_name)
        except Exception as e:
            log(e)
            flask.abort(400,"the naming is invaild >:(")
        return {}, 200

    if flask.request.method == "DELETE":
        name = os.path.basename(path_to_des)
        if os.path.isfile(path_to_des):
            if AUTO_DELETE == False:
                parent = os.path.dirname(path_to_des)
                new_name = os.path.join(parent, str(int(time.time())) + "__SS__" + name)
                os.rename(path_to_des, new_name)
                shutil.move(new_name, "trash-bin")
            else:
                os.remove(path_to_des)
        else:
            if AUTO_DELETE == False:
                dst = os.path.join("trash-bin", f"{int(time.time())}__SS__{name}")
                shutil.move(path_to_des, dst)
            else:
                shutil.rmtree(path_to_des)
        return {}, 200
