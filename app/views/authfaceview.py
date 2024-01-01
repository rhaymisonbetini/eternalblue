from rest_framework.views import APIView
from rest_framework.response import Response
from app.services import (FaceService, Uploads)


class AuthFaceView(APIView):
    def __init__(self, *args, **kwargs):
        super(AuthFaceView, self).__init__(*args, **kwargs)
        self.faceservice = FaceService()
        self.uploads = Uploads()

    def post(self, request) -> object:
        try:
            image_data = request.data.get('face')
            if image_data:
                uploaded_file = self.uploads.save_image(image_data)
                is_auth = self.faceservice.identify_face(uploaded_file)
                if is_auth:
                    return Response({"message": "authorized"}, status=201)
                return Response({"message": "unauthorized"}, status=401)
            return Response({'message': 'images_must_be_provided'}, status=400)
        except Exception as e:
            return Response({"message": str(e)}, status=500)
