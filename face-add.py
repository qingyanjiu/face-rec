import sys
import dlib
import cv2
import face_recognition
import os
import psycopg2

if len(sys.argv) < 2:
    print("Usage: face-add <image>")
    exit(1)

# Take the image file name from the command line
file_name = sys.argv[1]

# Create a HOG face detector using the built-in dlib class
face_detector = dlib.get_frontal_face_detector()

# Load the image
image = cv2.imread(file_name)

# Run the HOG face detector on the image data
detected_faces = face_detector(image, 1)

print("Found {} faces in the image file {}".format(len(detected_faces), file_name))

if not os.path.exists("./.faces"):
    os.mkdir("./.faces")
connection_db = psycopg2.connect("user='postgres' password='19831226lc' host='43.143.43.63' port='5434' dbname='face'")
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
        query = "INSERT INTO vectors (file, vec_low, vec_high) VALUES ('{}', CUBE(array[{}]), CUBE(array[{}]));".format(
            file_name,
            ','.join(str(s) for s in encodings[0][0:63]),
            ','.join(str(s) for s in encodings[0][64:127]),
        )
        db.execute(query)
        print(query)
        connection_db.commit()
    cv2.imwrite("./.faces/aligned_face_{}_{}_crop.jpg".format(file_name.replace('/', '_'), i), crop)

if connection_db is not None:
    connection_db.close()