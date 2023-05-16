'''
启动flask
'''
from contextlib import nullcontext
import logging
from flask import Flask
from flask import request
from faceService import add, find

def set_logging(rank=-1):
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO if rank in [-1, 0] else logging.WARN)
def create_app():
    app = Flask(__name__)
    return app

app = create_app()


@app.route("/face/add", methods=['POST'])
def face_add():
    json = request.json
    name = json['name']
    image = json['base64Img']
    add(image, name)
    result = {"success": True}
    return result

@app.route("/face/find", methods=['POST'])
def face_find():
    json = request.json
    image = json['base64Img']
    result = find(image)
    return result

set_logging()
# app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)