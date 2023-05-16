import base64
import dlib
import cv2
import face_recognition
import os
import numpy as np
from DataBase import Psycopg2Db
from dbConfig import DBConfig

dBConfig = DBConfig()
username = dBConfig.get_conf('username')
password = dBConfig.get_conf('password')
host = dBConfig.get_conf('host')
port = dBConfig.get_conf('port')
db = dBConfig.get_conf('db')

# Create a HOG face detector using the built-in dlib class
face_detector = dlib.get_frontal_face_detector()

psycopg2Db = Psycopg2Db(username, password, host, port, db)

def base64_to_cv2(image_base64):
    # 去掉base64前缀
    image_base64 = image_base64\
        .replace('data:image/jpeg;base64,', '')\
        .replace('data:image/jpg;base64,', '')\
        .replace('data:image/png;base64,', '')
    """base64 image to cv2"""
    image_bytes = base64.b64decode(image_base64)
    np_array = np.frombuffer(image_bytes, np.uint8)
    image_cv2 = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return image_cv2

def add(base64Image, name):

    image = base64_to_cv2(base64Image)

    # Run the HOG face detector on the image data
    detected_faces = face_detector(image, 1)

    if not os.path.exists("./.faces"):
        os.mkdir("./.faces")
    connection_db = psycopg2Db.connect()
    db=connection_db.cursor()
    # Loop through each face we found in the image
    for i, face_rect in enumerate(detected_faces):
        # Detected faces are returned as an object with the coordinates
        # of the top, left, right and bottom edges
        print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(),
                                                                                face_rect.right(), face_rect.bottom()))
        crop = image[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]
        encodings = face_recognition.face_encodings(crop)

        if len(encodings) > 0:
            query = "INSERT INTO vectors (name, vec_low, vec_high) VALUES ('{}', CUBE(array[{}]), CUBE(array[{}]));".format(
                name,
                ','.join(str(s) for s in encodings[0][0:63]),
                ','.join(str(s) for s in encodings[0][64:127]),
            )
            db.execute(query)
            print(query)
            connection_db.commit()
        cv2.imwrite("./.faces/aligned_face_{}_{}_crop.jpg".format(name.replace('/', '_'), i), crop)

    if connection_db is not None:
        connection_db.close()


def find(base64Image):

    result = {}

    image = base64_to_cv2(base64Image)

    # Run the HOG face detector on the image data
    detected_faces = face_detector(image, 1)

    connection_db = psycopg2Db.connect()
    db=connection_db.cursor()

    # Loop through each face we found in the image
    for i, face_rect in enumerate(detected_faces):
        # Detected faces are returned as an object with the coordinates
        # of the top, left, right and bottom edges
        print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(),
                                                                                face_rect.right(), face_rect.bottom()))
        crop = image[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]

    encodings = face_recognition.face_encodings(crop)
    if len(encodings) > 0:
        query = '''
                SELECT name FROM vectors 
                where (CUBE(array[{}]) <-> vec_low) < 0.3 and (CUBE(array[{}]) <-> vec_high) < 0.3
                ORDER BY
                (CUBE(array[{}]) <-> vec_low) + (CUBE(array[{}]) <-> vec_high) ASC LIMIT 1 ;
                '''.format(
            ','.join(str(s) for s in encodings[0][0:63]),
            ','.join(str(s) for s in encodings[0][64:127]),
            ','.join(str(s) for s in encodings[0][0:63]),
            ','.join(str(s) for s in encodings[0][64:127]),
        )
        print(query)
        db.execute(query)
        print("The number of parts: ", db.rowcount)
        row = db.fetchone()

        print(row)

        if row is None:
            result['name'] = 'Unknown'
        else:
            result['name'] = row[0]

        # while row is not None:
        #     print(row)
        #     row = db.fetchone()

        db.close()
    else:
        print("No encodings")

    if connection_db is not None:
        connection_db.close()
        
    return result