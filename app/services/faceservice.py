from django.conf import settings
import os
import face_recognition


class FaceService:
    @staticmethod
    def identify_face(face_identify: str) -> bool:
        auth_face_path = os.path.join(settings.MEDIA_ROOT, 'authorized_face.jpeg')
        auth_face = face_recognition.load_image_file(auth_face_path)
        requested_face = face_recognition.load_image_file(face_identify)

        auth_face_encoding = face_recognition.face_encodings(auth_face)[0]
        requested_face_encoding = face_recognition.face_encodings(requested_face)[0]

        result = face_recognition.compare_faces([auth_face_encoding], requested_face_encoding)
        if result[0]:
            return True
        return False
