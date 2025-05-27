import face_recognition
import cv2
import os
import glob
import numpy as np

class FaceRecognitionSystem:
    def __init__(self, scaling_factor=0.25):
        self.face_encodings = []
        self.person_ids = []
        self.scaling_factor = scaling_factor

    def load_face_database(self, images_directory):
        image_files = glob.glob(os.path.join(images_directory, "*.*"))
        print(f"Loading {len(image_files)} images for recognition...")

        for image_path in image_files:
            image = cv2.imread(image_path)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            filename = os.path.basename(image_path)
            person_id = os.path.splitext(filename)[0]
            
            try:
                face_encoding = face_recognition.face_encodings(rgb_image)[0]
                self.face_encodings.append(face_encoding)
                self.person_ids.append(person_id)
            except IndexError:
                print(f"Warning: No face found in {filename}")

        print("Face database loaded successfully")

    def process_frame(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.scaling_factor, fy=self.scaling_factor)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        detected_faces = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.face_encodings, face_encoding)
            person_id = "Unknown"

            if True in matches:
                face_distances = face_recognition.face_distance(self.face_encodings, face_encoding)
                best_match = np.argmin(face_distances)
                if matches[best_match]:
                    person_id = self.person_ids[best_match]

            detected_faces.append(person_id)

        face_locations = np.array(face_locations) / self.scaling_factor
        return face_locations.astype(int), detected_faces