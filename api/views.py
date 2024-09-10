from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SectionSerializer
from .check_time_table import check_and_update_timetable

@api_view(['POST'])
def get_timetable_updates(request):
    serializer = SectionSerializer(data=request.data)
    
    if serializer.is_valid():
        section = serializer.validated_data['section']
        response_text = check_and_update_timetable(section)
        return Response({'message': response_text})
    return Response(serializer.errors, status=400)
