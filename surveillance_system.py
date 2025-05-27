import cv2
from face_recognition_system import FaceRecognitionSystem

def start_surveillance(db_manager):
    face_system = FaceRecognitionSystem()
    face_system.load_face_database("images/")
    
    camera = cv2.VideoCapture(0)
    
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        face_locations, person_ids = face_system.process_frame(frame)
        
        for (y1, x2, y2, x1), person_id in zip(face_locations, person_ids):
            if person_id != "Unknown":
                db_manager.update_location(person_id, "Current Location")
                details = db_manager.get_person_details(person_id)
                name = details[0] if details else "Unknown"
                
                color = (0, 255, 0) if person_id != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, name, (x1, y1 - 10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

        cv2.imshow("Security Surveillance", frame)
        
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break
    
    camera.release()
    cv2.destroyAllWindows()