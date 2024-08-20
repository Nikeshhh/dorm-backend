from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from datetime import datetime, timedelta
from django.db.models import Q
from drf_spectacular.utils import extend_schema

from core.api.v1.duties.serializers import (
    CreateSwapDutiesRequestSerializer,
    CreateSwapPeopleRequestSerializer,
    KitchenDutySerializer,
    SwapDutiesRequestSerializer,
    SwapPeopleRequestSerializer,
)
from core.apps.duties.models import KitchenDuty, SwapDutiesRequest, SwapPeopleRequest
from core.apps.duties.services import SwapDutiesService, SwapPeopleService
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

    @extend_schema(tags=["DutyRecords"])
    def list(self, request, *args, **kwargs):
        """Получить список всех дежурств."""
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["DutyRecords"])
    @action(methods=("GET",), detail=True, url_path="to-swap")
    def duties_to_swap(self, request, pk, *args, **kwargs):
        """Получить список дежурств, доступных для обмена."""
        current = self.get_object()
        queryset = self.get_queryset().exclude(pk=current.pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(tags=["DutyRecords"])
    @action(methods=("GET",), detail=False, url_path="my")
    def my_duties(self, request, *args, **kwargs):
        """Получить список всех дежурств текущего пользователя."""
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["DutyRecords"])
    @action(methods=("GET",), detail=False, url_path="nearest")
    def nearest_duty(self, request, *args, **kwargs):
        """Получить ближайшее дежурство текущего пользователя."""
        return super().list(request, *args, **kwargs)


class SwapRequestsViewSet(ListModelMixin, GenericViewSet):
    queryset = SwapDutiesRequest.objects.order_by("-created_at")
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, serializer_class, *args, **kwargs):
        return serializer_class(*args, **kwargs)

    @extend_schema(tags=["SwapRequests"])
    def list(self, request, *args, **kwargs):
        """Получить список всех запросов на обмен и на замену."""
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


class SwapDutiesViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = SwapDutiesRequest.objects.order_by("-created_at")
    serializer_class = SwapDutiesRequestSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateSwapDutiesRequestSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action == "list":
            return self.queryset.filter(first_user=self.request.user)
        if self.action == "get_incoming_requests":
            return self.queryset.filter(second_user=self.request.user)
        return self.queryset

    @extend_schema(tags=["SwapDuties"])
    def create(self, request, *args, **kwargs):
        """
        Создать запрос на обмен дежурствами.

        :raises RoleViolationException: Если текущий пользователь не является проживающим.
        :raises DutySwapException: Если дежурства идентичны.
        :raises DutySwapException: Если пользователи идентичны.
        """
        initiator = request.user
        data = self.get_serializer(request.data).data

        # TODO: Replace this logic with service logic
        initiator_duty = KitchenDuty.objects.get(pk=data.get("initiator_duty_pk"))
        to_swap_duty = KitchenDuty.objects.get(pk=data.get("to_swap_duty_pk"))
        to_swap_user = CustomUser.objects.get(pk=data.get("to_swap_resident_pk"))

        swap_request = SwapDutiesService.create(
            initiator_duty=initiator_duty,
            initiator=initiator,
            target_duty=to_swap_duty,
            target=to_swap_user,
        )

        serializer = SwapDutiesRequestSerializer(swap_request)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @extend_schema(tags=["SwapDuties"])
    def list(self, request, *args, **kwargs):
        """Получить список всех запросов на обмен дежурствами."""
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["SwapDuties"])
    @action(methods=("GET",), detail=False, url_path="incoming")
    def get_incoming_requests(self, request, *args, **kwargs):
        """Получить входящие запросы на обмен дежурствами для текущего пользователя."""
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["SwapDuties"])
    @action(methods=("POST",), detail=True, url_path="accept")
    def accept_swap_duties_request(self, request, pk, *args, **kwargs):
        """
        Принять запрос на обмен дежурствами.

        :raises SwapRequestStatusException: Если дежурство недоступно для изменения.
        :raises DutySwapException: Если запрос не направлен текущему пользователю.
        """
        # TODO: Replace this logic with service logic
        swap_request: SwapDutiesRequest = self.get_object()

        swap_duties_service = SwapDutiesService(request.user, swap_request)
        swap_duties_service.accept()

        serializer = self.get_serializer(swap_request)
        return Response(serializer.data, status=HTTP_200_OK)

    @extend_schema(tags=["SwapDuties"])
    @action(methods=("POST",), detail=True, url_path="decline")
    def decline_swap_duties_request(self, request, pk, *args, **kwargs):
        """
        Отклонить запрос на обмен дежурствами.

        :raises SwapRequestStatusException: Если дежурство недоступно для изменения.
        :raises DutySwapException: Если запрос не направлен текущему пользователю.
        """
        # TODO: Replace this logic with service logic
        swap_request: SwapDutiesRequest = self.get_object()

        swap_duties_service = SwapDutiesService(request.user, swap_request)
        swap_duties_service.decline()

        serializer = self.get_serializer(swap_request)
        return Response(serializer.data, status=HTTP_200_OK)

    @extend_schema(tags=["SwapDuties"])
    @action(methods=("POST",), detail=True, url_path="cancel")
    def cancel_swap_duties_request(self, request, pk, *args, **kwargs):
        """
        Отменить исходящий запрос на обмен дежурствами.

        :raises SwapRequestStatusException: Если дежурство недоступно для изменения.
        :raises DutySwapException: Если пользователь не имеет доступа к этому действию.
        """
        # TODO: Replace this logic with service logic
        swap_request: SwapDutiesRequest = self.get_object()

        swap_duties_service = SwapDutiesService(request.user, swap_request)
        swap_duties_service.cancel()

        serializer = self.get_serializer(swap_request)
        return Response(serializer.data, status=HTTP_200_OK)


class SwapPeopleViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = SwapPeopleRequest.objects.order_by("-created_at")
    serializer_class = SwapPeopleRequestSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
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

    @extend_schema(tags=["SwapPeople"])
    def create(self, request, *args, **kwargs):
        """
        Создать запрос на замену.

        :raises RoleViolationException: Если текущий пользователь не является проижвающим.
        :raises DutySwapException: Если текущий пользователь не принадлежит к текущему дежурству.
        :raises DutySwapException: Если заменяемый пользователь не принадлежит к текущему дежурству.
        :raises DutySwapException: Если пользователи идентичны.
        """
        initiator = request.user
        data = self.get_serializer(request.data).data

        # TODO: replace with service logic
        to_swap_user = CustomUser.objects.get(pk=data.get("to_swap_user_pk"))
        to_swap_duty = KitchenDuty.objects.get(pk=data.get("to_swap_duty_pk"))

        swap_people_service = SwapPeopleService(initiator)

        swap_request = swap_people_service.create(
            initiator=initiator, target=to_swap_user, initiator_duty=to_swap_duty
        )

        serializer = self.serializer_class(swap_request)
        return Response(serializer.data, status=HTTP_201_CREATED)

    @extend_schema(tags=["SwapPeople"])
    def list(self, request, *args, **kwargs):
        """Получить список всех запросов на замену."""
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["SwapPeople"])
    @action(methods=("GET",), detail=False, url_path="incoming")
    def get_incoming_requests(self, request, *args, **kwargs):
        """Получить список входящих запросов на замену для текущего пользователя."""
        return super().list(request, *args, **kwargs)

    @extend_schema(tags=["SwapPeople"])
    @action(methods=("POST",), detail=True, url_path="accept")
    def accept_swap_people_request(self, request, pk, *args, **kwargs):
        """
        Принять запрос на замену.

        :raises SwapRequestStatusException: Если дежурство недоступно для изменения.
        :raises DutySwapException: Если заявка не направлена текущему пользователю.
        """
        # TODO: replace with service logic
        swap_request: SwapPeopleRequest = self.get_object()

        swap_people_service = SwapPeopleService(request.user, swap_request)
        swap_people_service.accept()

        serializer = self.get_serializer(swap_request)
        return Response(serializer.data, status=HTTP_200_OK)

    @extend_schema(tags=["SwapPeople"])
    @action(methods=("POST",), detail=True, url_path="decline")
    def decline_swap_people_request(self, request, pk, *args, **kwargs):
        """
        Отклонить запрос на замену.

        :raises SwapRequestStatusException: Если дежурство недоступно для изменения.
        :raises DutySwapException: Если заявка не направлена текущему пользователю.
        """
        # TODO: replace with service logic
        swap_request: SwapPeopleRequest = self.get_object()

        swap_people_service = SwapPeopleService(request.user, swap_request)
        swap_people_service.decline()

        serializer = self.get_serializer(swap_request)
        return Response(serializer.data, status=HTTP_200_OK)

    @extend_schema(tags=["SwapPeople"])
    @action(methods=("POST",), detail=True, url_path="cancel")
    def cancel_swap_people_request(self, request, pk, *args, **kwargs):
        """
        Отменить запрос на замену.

        :raises SwapRequestStatusException: Если дежурство недоступно для изменения.
        :raises DutySwapException: Если заявка не направлена текущему пользователю.
        """
        # TODO: replace with service logic
        swap_request: SwapPeopleRequest = self.get_object()

        swap_people_service = SwapPeopleService(request.user, swap_request)
        swap_people_service.cancel()

        serializer = self.get_serializer(swap_request)
        return Response(serializer.data, status=HTTP_200_OK)
