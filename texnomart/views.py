from django.db.models import Prefetch
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters, viewsets

from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from texnomart.models import Category, Product, Comment, Image, ProductAttribute, Attribute, AttributeValue
from texnomart.mypaginations import MyLimitOffsetPagination
from texnomart.serializer import CategoryModelSerializer, ProductSerializer, CommentSerializer, \
    AttributeKeySerializer, AttributeValueSerializer, ProductAttributesSerializer


# Create your views here.

# category
@method_decorator(cache_page(10), name='dispatch')
class CategoryList(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = MyLimitOffsetPagination

    filter_backends = (filters.SearchFilter,)
    search_fields = ('category_name',)


class BaseCategoryView:
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategoryModelSerializer
    lookup_field = 'slug'

class AddCategory(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategoryModelSerializer


class CategoryDetail(BaseCategoryView,RetrieveAPIView):
    permission_classes = [IsAuthenticated]

class DeleteCategory(BaseCategoryView, DestroyAPIView):
    permission_classes = [IsAuthenticated]

class UpdateCategory(BaseCategoryView, UpdateAPIView):
    permission_classes = [IsAuthenticated]

class CategoryModelViewSet(BaseCategoryView, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]





# products

@method_decorator(cache_page(10), name='dispatch')
class ProductList(ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Product.objects.select_related(
        'category'
    ).prefetch_related(
        Prefetch('comments', queryset=Comment.objects.all()),
        # Prefetch('image', queryset=Image.objects.all()),
        Prefetch('productattribute_set', queryset=ProductAttribute.objects.all())
    ).all()
    serializer_class = ProductSerializer
    pagination_class = MyLimitOffsetPagination

    filter_backends = (filters.SearchFilter,)
    search_fields = ('product_name', 'price',)

class BaseProductView:
    queryset = Product.objects.select_related(
        'category'
    ).prefetch_related(
        Prefetch('comments', queryset=Comment.objects.all()),
        # Prefetch('image', queryset=Image.objects.all()),
        Prefetch('productattribute_set', queryset=ProductAttribute.objects.all())
    ).all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'


class AddProduct(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
class ProductDetail(BaseProductView, RetrieveAPIView):
    permission_classes = [IsAuthenticated]

class DeleteProduct(BaseProductView, DestroyAPIView):
    permission_classes = [IsAuthenticated]

class Updateproduct(BaseProductView, UpdateAPIView):
    permission_classes = [IsAuthenticated]

class ProductModelViewSet(BaseProductView, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]





@method_decorator(cache_page(10), name='dispatch')
class Comments(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.select_related('product').all()
    serializer_class = CommentSerializer
    pagination_class = MyLimitOffsetPagination



class CommentCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Comment.objects.prefetch_related('product').all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class AttributeKey(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Attribute.objects.prefetch_related('productattribute_set').all()
    serializer_class = AttributeKeySerializer
    pagination_class = MyLimitOffsetPagination

class AttributeValues(ListAPIView):
    permission_classes = [AllowAny]
    queryset = AttributeValue.objects.prefetch_related('productattribute_set__attribute').all()
    serializer_class = AttributeValueSerializer
    pagination_class = MyLimitOffsetPagination


class ProductAttributes(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductAttributesSerializer
    lookup_field = 'pk'

