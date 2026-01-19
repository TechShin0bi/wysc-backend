from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserDetailSerializer

class MeView(APIView):
    """
    View to get the currently authenticated user's details.
    Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return the authenticated user's details.
        """
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)