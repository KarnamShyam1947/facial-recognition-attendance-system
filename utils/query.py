import face_recognition
import cv2, os
import numpy as np
import mysql.connector
import pickle as pkl
from dotenv import load_dotenv

secrets = load_dotenv(".env")

load_query = "SELECT * FROM face_encodings"
config = {
    "host": secrets['DB_HOST_URL'],
    "port": secrets['DB_PORT'],
    "database": secrets['DB_DATABASE'],
    "user": secrets['DB_USERNAME'],
    "password": secrets['DB_PASSWORD'],
    "charset": "utf8",
    "use_unicode": True,
    "get_warnings": True,
}
    
def load_encoding():
    encoding = []
    names = []

    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    
    results = cur.execute(load_query)
    # print(results)
    for r in cur.fetchall():
        encoding.append(pkl.loads(r[2]))
        names.append(r[1])

    cur.close()
    cnx.close()

    return names, encoding

def get_predictions(query_path, known_face_encodings, known_face_names):
    print("started prediction")
    results = []

    frame = cv2.imread(query_path)
    # rgb_frame = frame[:, :, ::-1]
    
    face_locations = face_recognition.face_locations(frame)
    print("faces detected : ", len(face_locations))

    face_encodings = face_recognition.face_encodings(frame, face_locations)
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            print(name)
            results.append(name)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)
    
    cv2.imwrite('static/result.png',frame)

    return results

def get_result(file_path):
    known_face_names, known_face_encodings = load_encoding()
    return get_predictions(file_path, known_face_encodings, known_face_names)

if __name__ == "__main__":
    known_face_names, known_face_encodings = load_encoding()
    get_predictions("faces/test.jpg", known_face_encodings, known_face_names)


