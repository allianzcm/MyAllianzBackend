from rest_framework.viewsets import ModelViewSet
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter


class CoreBaseModelViewSet(ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]

    def get_queryset(self):
        assert self.model is not None, (
            "'%s' model property."
            % self.__class__.__name__
        )
        return self.model.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)