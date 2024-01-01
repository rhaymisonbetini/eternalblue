from rest_framework.views import APIView
from rest_framework.response import Response
from app.services import TransformService


class SQLGeneratorView(APIView):
    def __init__(self, *args, **kwargs):
        super(SQLGeneratorView, self).__init__(*args, **kwargs)
        self.transformer = TransformService()

    def post(self, request):
        try:
            question = request.data.get('question')
            if question:
                llama_response = self.transformer.ask(question)
                return Response({'response': llama_response}, 200)
            return Response({'response': 'No_question_identified'})
        except Exception as e:
            return Response({'response': str(e)}, status=500)
