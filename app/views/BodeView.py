from rest_framework.views import APIView
from rest_framework.response import Response
from app.services import BodeService


class BodeView(APIView):
    def __init__(self, *args, **kwargs):
        super(BodeView, self).__init__(*args, **kwargs)
        self.bodeService = BodeService()

    def post(self, request):
        question = request.data.get('question')
        input = request.data.get('input')
        bode = self.bodeService.ask(question, input)
        return Response({"response": bode})
