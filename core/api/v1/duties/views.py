from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from datetime import datetime, timedelta
from django.db.models import Q

from core.api.v1.duties.serializers import (
    CreateSwapDutiesRequestSerializer,
    CreateSwapPeopleRequestSerializer,
    KitchenDutySerializer,
    SwapDutiesRequestSerializer,
    SwapPeopleRequestSerializer,
)
from core.apps.duties.models import KitchenDuty, SwapDutiesRequest, SwapPeopleRequest
from core.apps.users.models import CustomUser


class DutyRecordsViewSet(ListModelMixin, GenericViewSet):
    queryset = KitchenDuty.objects.order_by("-date")
    serializer_class = KitchenDutySerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        today = datetime.today()
        queryset = self.queryset.filter(
            Q(date__gte=today), Q(date__lte=today + timedelta(days=28))
        )
        if self.action == "my_duties":
            queryset = queryset.filter(people=self.request.user)
        if self.action == "nearest_duty":
            queryset = queryset.filter(people=self.request.user)[:1]
        return queryset

    @action(methods=("GET",), detail=True)
    def duties_to_swap(self, request, pk, *args, **kwargs):
        current = self.get_object()
        queryset = self.get_queryset().exclude(pk=current.pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=("GET",), detail=False)
    def my_duties(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=("GET",), detail=False)
    def nearest_duty(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class SwapRequestsViewSet(ListModelMixin, GenericViewSet):
    queryset = SwapDutiesRequest.objects.order_by("-created_at")
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, serializer_class, *args, **kwargs):
        return serializer_class(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        swap_people_queryset = SwapPeopleRequest.objects.filter(
            to_swap=request.user
        ).order_by("-created_at")
        swap_duties_queryset = SwapDutiesRequest.objects.filter(
            second_user=request.user
        ).order_by("-created_at")

        swap_people_serializer = self.get_serializer(
            SwapPeopleRequestSerializer, swap_people_queryset, many=True
        )
        swap_duties_serializer = self.get_serializer(
            SwapDutiesRequestSerializer, swap_duties_queryset, many=True
        )

        data = sorted(
            swap_duties_serializer.data + swap_people_serializer.data,
            key=lambda x: x["created_at"],
        )
        return Response(data)


class SwapDutiesViewSet(ListModelMixin, GenericViewSet):
    queryset = SwapDutiesRequest.objects.order_by("-created_at")
    serializer_class = SwapDutiesRequestSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create_swap_duties_request":
            return CreateSwapDutiesRequestSerializer
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        if self.action == "list":
            return self.queryset.filter(first_user=self.request.user)
        if self.action == "get_incoming_requests":
            return self.queryset.filter(second_user=self.request.user)
        return self.queryset

    @action(methods=("GET",), detail=False)
    def get_incoming_requests(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=("POST",), detail=True)
    def accept_swap_duties_request(self, request, pk, *args, **kwargs):
        swap_request: SwapDutiesRequest = self.get_object()
        swap_request.accept(request.user)

        serializer = self.get_serializer(swap_request)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=("POST",), detail=True)
    def decline_swap_duties_request(self, request, pk, *args, **kwargs):
        swap_request: SwapDutiesRequest = self.get_object()
        swap_request.decline(request.user)

        serializer = self.get_serializer(swap_request)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=("POST",), detail=True)
    def cancel_swap_duties_request(self, request, pk, *args, **kwargs):
        swap_request: SwapDutiesRequest = self.get_object()
        swap_request.cancel(request.user)

        serializer = self.get_serializer(swap_request)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=("POST",), detail=False)
    def create_swap_duties_request(self, request, *args, **kwargs):
        initiator = request.user
        data = self.get_serializer(request.data).data

        initiator_duty = KitchenDuty.objects.get(pk=data.get("initiator_duty_pk"))
        to_swap_duty = KitchenDuty.objects.get(pk=data.get("to_swap_duty_pk"))
        to_swap_user = CustomUser.objects.get(pk=data.get("to_swap_resident_pk"))

        swap_request = SwapDutiesRequest.objects.create(
            first_duty=initiator_duty,
            first_user=initiator,
            second_duty=to_swap_duty,
            second_user=to_swap_user,
        )

        serializer = SwapDutiesRequestSerializer(swap_request)
        return Response(serializer.data, status=HTTP_201_CREATED)


class SwapPeopleViewSet(ListModelMixin, GenericViewSet):
    queryset = SwapPeopleRequest.objects.order_by("-created_at")
    serializer_class = SwapPeopleRequestSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create_swap_people_request":
            return CreateSwapPeopleRequestSerializer
        return super().get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self):
        if self.action == "list":
            return self.queryset.filter(current_user=self.request.user)
        if self.action == "get_incoming_requests":
            return self.queryset.filter(to_swap=self.request.user)
        return self.queryset

    @action(methods=("GET",), detail=False)
    def get_incoming_requests(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=("POST",), detail=True)
    def accept_swap_people_request(self, request, pk, *args, **kwargs):
        swap_request: SwapPeopleRequest = self.get_object()
        swap_request.accept(request.user)

        serializer = self.get_serializer(swap_request)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=("POST",), detail=True)
    def decline_swap_people_request(self, request, pk, *args, **kwargs):
        swap_request: SwapPeopleRequest = self.get_object()
        swap_request.decline(request.user)

        serializer = self.get_serializer(swap_request)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=("POST",), detail=True)
    def cancel_swap_people_request(self, request, pk, *args, **kwargs):
        swap_request: SwapPeopleRequest = self.get_object()
        swap_request.cancel(request.user)

        serializer = self.get_serializer(swap_request)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=("POST",), detail=False)
    def create_swap_people_request(self, request, *args, **kwargs):
        initiator = request.user
        data = self.get_serializer(request.data).data

        to_swap_user = CustomUser.objects.get(pk=data.get("to_swap_user_pk"))
        to_swap_duty = KitchenDuty.objects.get(pk=data.get("to_swap_duty_pk"))

        swap_request = SwapPeopleRequest.objects.create(
            current_user=initiator, to_swap=to_swap_user, duty=to_swap_duty
        )

        serializer = self.serializer_class(swap_request)
        return Response(serializer.data, status=HTTP_201_CREATED)
