from rest_framework import serializers
from .models import User, Cart, Products


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'
