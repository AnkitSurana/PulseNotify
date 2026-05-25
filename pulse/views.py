from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from .models import PriceAlert
from .serializers import PriceAlertSerializer

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        if not username or not password:
            return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        token = AccessToken.for_user(user)
        return Response({
            'username': user.username,
            'access': str(token),
            'role': user.profile.role
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        token = AccessToken.for_user(user)
        return Response({
            'username': user.username,
            'access': str(token),
            'role': user.profile.role
        }, status=status.HTTP_200_OK)

class AlertListCreateView(generics.ListCreateAPIView):
    serializer_class = PriceAlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PriceAlert.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'route' in data and '-' in data['route']:
            origin, destination = data['route'].split('-')
            data['origin'] = origin.strip()
            data['destination'] = destination.strip()
        if 'threshold' in data:
            data['threshold_price'] = data['threshold']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AlertDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        alert = get_object_or_404(PriceAlert, id=id)
        if alert.user != request.user:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        alert.status = PriceAlert.Status.INACTIVE
        alert.save()
        return Response({'status': 'inactive'}, status=status.HTTP_200_OK)

import random
from django.http import JsonResponse

MOCK_PRICES = {
    'DEL-BOM': (3000, 7000),
    'BLR-HYD': (1500, 4000),
    'DEL-BLR': (4000, 9000),
    'BOM-GOA': (2000, 5000),
}

def get_flight_price(request):
    route = request.GET.get('route', '')
    price_range = MOCK_PRICES.get(route)
    if not price_range:
        return JsonResponse({'error': 'Route not found'}, status=404)
    price = random.randint(*price_range)
    return JsonResponse({'route': route, 'price': price})

from django.db import models as db_models
from django.db.models import Count
from .permissions import IsAdminUser
from .models import NotificationLog

class AdminSummaryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        stats = PriceAlert.objects.aggregate(
            total_alerts=Count('id'),
            active_alerts=Count('id', filter=db_models.Q(status=PriceAlert.Status.ACTIVE)),
            triggered_alerts=Count('id', filter=db_models.Q(status=PriceAlert.Status.TRIGGERED))
        )
        total_notifications = NotificationLog.objects.aggregate(total=Count('id'))['total'] or 0

        top_routes_qs = PriceAlert.objects.values('origin', 'destination').annotate(
            alert_count=Count('id')
        ).order_by('-alert_count')

        top_routes = [
            {
                'route': f"{item['origin']}-{item['destination']}",
                'alert_count': item['alert_count']
            }
            for item in top_routes_qs
        ]

        return Response({
            'total_alerts': stats['total_alerts'] or 0,
            'active_alerts': stats['active_alerts'] or 0,
            'triggered_alerts': stats['triggered_alerts'] or 0,
            'total_notifications': total_notifications,
            'top_routes': top_routes
        }, status=status.HTTP_200_OK)


