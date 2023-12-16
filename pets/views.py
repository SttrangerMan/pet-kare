from rest_framework.views import status, Response, Request, APIView
from .models import Pet
from .serializers import PetSerializer
from groups.models import Group
from traits.models import Trait
from rest_framework.pagination import PageNumberPagination


class PetsViews(APIView, PageNumberPagination):
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        groupData = serializer.validated_data.pop("group")
        traitData = serializer.validated_data.pop("traits")

        try:
            group = Group.objects.get(
                scientific_name__iexact=groupData["scientific_name"]
            )
        except Group.DoesNotExist:
            group = Group.objects.create(**groupData)
        pet_object = Pet.objects.create(group=group, **serializer.validated_data)

        for t in traitData:
            try:
                trait = Trait.objects.get(name__iexact=t["name"])
            except Trait.DoesNotExist:
                trait = Trait.objects.create(**t)
            pet_object.traits.add(trait)

        serializer = PetSerializer(instance=pet_object)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)
