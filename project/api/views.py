from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token
from .models import Cart, Products
from .serializer import CartSerializer, ProductsSerializer, UserSerializer


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": {'message': "Validation error", 'code': 422}})
    
    user = authenticate(email=email, password=password)

    if not user:
        return Response({'error': {'message': "Authentication failed", 'code': 401}})
    
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'data': {'user_token': token.key}})


@api_view(['POST'])
def signup(request): 
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'data': {'user_token': token.key, 'code': 201}})
    return Response({'error': serializer.errors})


@api_view(['GET'])
def logout(request):
    request.user.auth_token.delete()

    return Response({'data': {'message': 'logout', 'code': 200}})


@api_view(['GET'])
def get_prod(request):
    products = Products.objects.all()
    serializer = ProductsSerializer(products, many=True)

    return Response({'data': serializer.data, 'code': 200})


@api_view(['GET'])
def get_cart(request): 
    if not request.user.is_active:
        return Response({'“error”: {“code”: 403,“message”: “Forbidden for you”}'})
    cart, _ = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    data = []
    cnt = 0
    for i in serializer.data['products']:
        cnt += 1
        data.append({
            'id': cnt,
            'product_id': i['id'],
            'name': i['name'],
            'imgUrl': i['imgUrl'],
            'price': i['price'],
            'category': i['category'],
            "doughType": i["doughType"],
            "size": i["size"]
        })

    return Response({'data': data, 'code': 200})


@api_view(['POST', 'DELETE'])
def add_cart(request, pk):
    if not request.user.is_active:
        return Response({'“error”: {“code”: 403,“message”: “Forbidden for you”}'})
    try:
        product = Products.objects.get(pk=pk)
    except:
        return Response({'error': {'message': 'not Found', 'code': 404}})

    if request.method == 'POST':
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.products.add(product)

        return Response({'message': 'product added to cart', "code": 201})
    elif request.method == 'DELETE':
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.products.remove(product)

        return Response({'message': 'product removed from cart', "code": 200})
