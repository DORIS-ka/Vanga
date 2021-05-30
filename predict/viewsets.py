from django.contrib.auth import get_user_model
from django.db.models import Sum, F
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from predict.models import Selling
from predict.serializers import ShopSerializer, UserSerializer, CategorySerializer, ProductSerializer


class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer

    queryset = (
        Selling.objects.values('shop_id')
            .annotate(
                turnover=Sum('total_price'),
                profit=Sum('margin_price_total'),
                total_vat=Sum('total_vat'),
                total_excise=Sum('total_excise'),
                shop_name=F('shop__name')
        )
    )
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = (
        Selling.objects.values('category_id')
            .annotate(
                turnover=Sum('total_price'),
                profit=Sum('margin_price_total'),
                total_vat=Sum('total_vat'),
                total_excise=Sum('total_excise'),
                сategory_name=F('category__name')
        )
    )
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication]


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = (
        Selling.objects.values('product_id')
            .annotate(
                turnover=Sum('total_price'),
                profit=Sum('margin_price_total'),
                total_vat=Sum('total_vat'),
                total_excise=Sum('total_excise'),
                product_name=F('product__name')
        )
    )
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication]