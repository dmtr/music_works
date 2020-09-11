from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from works import models, serializers


class RetrieveMusicWork(APIView):
    def get(self, request, format=None):
        iswc = self.request.query_params.get("iswc", None)
        if iswc is not None:
            try:
                work = models.MusicWork.objects.get(iswc=iswc)
                serializer = serializers.MusicWorkSerializer(work)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)
