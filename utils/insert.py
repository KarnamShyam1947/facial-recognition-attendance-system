import face_recognition
import mysql.connector
import pickle as pkl
import numpy as np
import cv2

insert_query = "INSERT INTO face_encodings(name, encoding) values(%s, %s)"
load_query = "SELECT * FROM face_encodings"

def insert(file_path, name):
    print("insert.....")

    config = {
        "host": "localhost",
        "port": 3306,
        "database": "face_attendance_system",
        "user": "root",
        "password": "",
        "charset": "utf8",
        "use_unicode": True,
        "get_warnings": True,
    }
    
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()

    frame = cv2.imread(file_path)
    # rgb_frame = frame[:, :, ::-1]
    
    face_locations = face_recognition.face_locations(frame)
    print("faces detected : ", len(face_locations))
    if len(face_locations) <= 0:
        return False
    
    image = face_recognition.load_image_file(file_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    
    cur.execute(insert_query, (name, pkl.dumps(face_encoding), ))
    cnx.commit()

    cur.close()
    cnx.close()

    return True

# def load_encoding(config):
#     encoding = []
#     names = []

#     cnx = mysql.connector.connect(**config)
#     cur = cnx.cursor()
    
#     results = cur.execute(load_query)
#     # print(results)
#     for r in cur.fetchall():
#         encoding.append(pkl.loads(r[2]))
#         names.append(r[1])

#     cur.close()
#     cnx.close()

#     return names, encoding

if __name__ == "__main__":
    pass

    # known_face_names, known_face_encodings = load_encoding(config)

    # video_capture = cv2.VideoCapture(0)
    # while True:
    
    #     ret, frame = video_capture.read()
        
    #     rgb_frame = frame[:, :, ::-1]
        
    #     face_locations = face_recognition.face_locations(rgb_frame)
    #     face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        
    #     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            
    #         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    #         name = "Unknown"

    #         face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    #         best_match_index = np.argmin(face_distances)
    #         if matches[best_match_index]:
    #             name = known_face_names[best_match_index]
    #             print(name)
            
    #         cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            
    #         cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    #         font = cv2.FONT_HERSHEY_DUPLEX
    #         cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        
    #     cv2.imshow('Video', frame)

        
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break


    # video_capture.release()
    # cv2.destroyAllWindows()