from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
import datetime

from predict.models import Selling


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    username = serializers.CharField(
            max_length=32,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=6, max_length=100, write_only=True)
    token = serializers.SerializerMethodField(
        label=("Token"),
        read_only=True
    )

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        # return token.key
        if not created:
            # update the created time of the token to keep it valid
            token.created = datetime.datetime.utcnow()
            token.save()
        return getattr(token, 'key')

    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('token', 'id', 'email', 'username', 'password')
        read_only_fields = ('token',)


class ShopSerializer(serializers.ModelSerializer):
    shop_name = serializers.SerializerMethodField()
    turnover = serializers.DecimalField(decimal_places=4, max_digits=20)
    profit = serializers.DecimalField(decimal_places=4, max_digits=20)
    total_vat = serializers.DecimalField(decimal_places=4, max_digits=20)
    total_excise = serializers.DecimalField(decimal_places=4, max_digits=20)

    def get_shop_name(self, instance):
        return instance['shop_name']

    class Meta:
        model = Selling
        fields = ("turnover", "shop_name", "profit", "total_vat", "total_excise")


class CategorySerializer(serializers.ModelSerializer):
    сategory_name = serializers.SerializerMethodField()
    turnover = serializers.DecimalField(decimal_places=4, max_digits=20)
    profit = serializers.DecimalField(decimal_places=4, max_digits=20)
    total_vat = serializers.DecimalField(decimal_places=4, max_digits=20)
    total_excise = serializers.DecimalField(decimal_places=4, max_digits=20)

    def get_сategory_name(self, instance):
        return instance['сategory_name']

    class Meta:
        model = Selling
        fields = ("turnover", "сategory_name", "profit", "total_vat", "total_excise")


class ProductSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    turnover = serializers.DecimalField(decimal_places=4, max_digits=20)
    profit = serializers.DecimalField(decimal_places=4, max_digits=20)
    total_vat = serializers.DecimalField(decimal_places=4, max_digits=20)
    total_excise = serializers.DecimalField(decimal_places=4, max_digits=20)

    def get_product_name(self, instance):
        return instance['product_name']

    class Meta:
        model = Selling
        fields = ("turnover", "product_name", "profit", "total_vat", "total_excise")