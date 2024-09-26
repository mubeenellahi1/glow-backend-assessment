from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Business
from .serializers import BusinessSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    @swagger_auto_schema(
        request_body=BusinessSerializer, responses={201: BusinessSerializer()}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @swagger_auto_schema(
        method="post",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "industry": openapi.Schema(type=openapi.TYPE_STRING),
                "contact": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "phone": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
                "status": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: BusinessSerializer()},
    )
    @action(detail=True, methods=["post"])
    def update_workflow(self, request, pk=None):
        business = self.get_object()

        serializer = self.get_serializer(business, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
