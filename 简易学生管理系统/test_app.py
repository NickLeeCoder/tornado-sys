
import json

def post():
    # json_s = [1,2,3,4]
    json_s = [{'sda':'dhas','dsa':12},{'das':'dsa','das':222}]

    a = json.dumps(json_s, ensure_ascii=False)
    print(a)


post()