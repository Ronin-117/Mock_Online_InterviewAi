# Create your views here.
# myapp/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pyttsx3

@api_view(['POST'])  # Important: Only allow POST requests
def speak_text(request):
    if request.method == 'POST':
        try:
            text = request.data.get('text', "Hello from Django!")  # Get text from request
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            return Response({"message": f"Successfully spoke: {text}"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    return Response({"error": "Invalid method"}, status=400)

@api_view(['GET'])
def get_data(request):
    data = {
        "message": "This is data from th"
    }
    return Response(data)
