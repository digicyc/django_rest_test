from snippets.models import Snippet, Content
from snippets.serializers import SnippetSerializer, UserSerializer, TestSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def pre_save(self, obj):
        obj.owner = self.request.user


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET', 'POST'])
def gettest(request, format=None):
    if request.method == 'POST':
        # '{"creators": []}'
        # list of creators.
        creators = request.DATA.get('creators', '')

        if not creators:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        r_data = {}
        # It's okie if query fails we pass empty value back
        # then they can handle it.
        for creator in creators:
            try:
                content = Content.objects.get(creator=creator)
                resp = TestSerializer(content)
                r_data[creator] = resp.data

            except Content.DoesNotExist:
                r_data[creator] = {}

        return Response(r_data)


