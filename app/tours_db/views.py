from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from tours_db.models import Customers
from tours_db.serializers import TutorialSerializer
from rest_framework.decorators import api_view

# Create your views here.
# def index(request):
#     return render(request, "tutorials/index.html")


def index(request):
    print("------------------------- I AM HERE")
    queryset = Customers.objects.all()
    return render(request, "tutorials/index.html", {'tutorials': queryset})


class index(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tutorials/index.html'

    def get(self, request):
        queryset = Customers.objects.all()
        return Response({'customers': queryset})


class list_all_tutorials(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'tutorials/tutorial_list.html'

    def get(self, request):
        queryset = Customers.objects.all()
        return Response({'customers': queryset})


# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    if request.method == 'GET':
        customers = Customers.objects.all()

        f_name = request.GET.get('f_name', None)
        if f_name is not None:
            customers = customers.filter(f_name__icontains=f_name)

        tutorials_serializer = TutorialSerializer(customers, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data,
                                status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Customers.objects.all().delete()
        return JsonResponse(
            {
                'message':
                '{} Tutorials were deleted successfully!'.format(count[0])
            },
            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    try:
        customers = Customers.objects.get(pk=pk)
    except Customers.DoesNotExist:
        return JsonResponse({'message': 'The tutorial does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        tutorial_serializer = TutorialSerializer(customers)
        return JsonResponse(tutorial_serializer.data)

    elif request.method == 'PUT':
        tutorial_data = JSONParser().parse(request)
        tutorial_serializer = TutorialSerializer(customers, data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data)
        return JsonResponse(tutorial_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        customers.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'},
                            status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def tutorial_list_published(request):
    customers = Customers.objects.filter(published=True)

    if request.method == 'GET':
        tutorials_serializer = TutorialSerializer(customers, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)