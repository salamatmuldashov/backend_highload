from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DataItemSerializer
from .utils import quorum_read, quorum_write
from .models import DataItem

# class DataReadView(APIView):
#     def get(self, request, key):
#         value = quorum_read(key)
#         return Response({'value': value})

# class DataWriteView(APIView):
#     def post(self, request):
#         serializer = DataItemSerializer(data=request.data)
#         if serializer.is_valid():
#             key = serializer.validated_data['key']
#             value = serializer.validated_data['value']
#             success = quorum_write(key, value)
#             if success:
#                 return Response({'message': 'Write successful'}, status=201)
#             else:
#                 return Response({'message': 'Write failed'}, status=500)
#         return Response(serializer.errors, status=400)
    
class DataReadView(APIView):
    def get(self, request, key):
        try:
            data_item = DataItem.objects.get(key=key)
            return Response({'value': data_item.value}, status=status.HTTP_200_OK)
        except DataItem.DoesNotExist:
            return Response({'message': 'Key not found'}, status=status.HTTP_404_NOT_FOUND)

class DataWriteView(APIView):
    def get(self, request):
        data_items = DataItem.objects.all()
        serializer = DataItemSerializer(data_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DataItemSerializer(data=request.data)
        if serializer.is_valid():
            key = serializer.validated_data['key']
            value = serializer.validated_data['value']
            DataItem.objects.update_or_create(key=key, defaults={'value': value})
            return Response({'message': 'Write successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)