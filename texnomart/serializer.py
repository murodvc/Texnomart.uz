from django.db.models import Avg
from django.db.models.functions import Round
from rest_framework import serializers
from texnomart.models import Image, Category, Product, Comment, ProductAttribute, Attribute, AttributeValue
from django.contrib.auth.models import User




class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_superuser(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'is_primary', 'product', 'category']

class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'



class ProductAttributesSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()

    def get_attributes(self, instance):
        attributes = ProductAttribute.objects.filter(product=instance)
        attributes_dict = {}
        for product_attribute in attributes:
            attributes_dict[product_attribute.attribute.attribute_name] = product_attribute.value.attribute_value
        return attributes_dict

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'attributes']





class ProductSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='group.category.category_name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    def get_attributes(self, instance):
        attributes = ProductAttribute.objects.filter(product=instance)
        attributes_dict = {}
        for product_attribute in attributes:
            attributes_dict[product_attribute.attribute.attribute_name] = product_attribute.value.attribute_value
        return attributes_dict


    def get_is_liked(self, instance):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        all_likes = instance.users_like.all()
        if user in all_likes:
            return True
        return False


    def get_rating(self, instance):
        rating = Comment.objects.filter(product=instance).aggregate(rating=Round(Avg('rating')))
        if rating.get('rating'):
            return rating.get('rating')
        return 0

    def get_all_images(self, instance):
        images = Image.objects.all().filter(product=instance)
        all_images = []
        request = self.context.get('request')
        for image in images:
            all_images.append(request.build_absolute_uri(image.image.url))
        return all_images

    def get_primary_image(self, instance):
        image = Image.objects.filter(product=instance, is_primary=True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)

    class Meta:
        model = Product
        exclude = ('users_like',)

class CategoryModelSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True, source='category_images')
    category_image = serializers.SerializerMethodField(method_name='foo')
    products = ProductSerializer(many=True, read_only=True)

    def foo(self, instance):
        image = Image.objects.filter(category=instance, is_primary=True).first()
        request = self.context.get('request')
        if image:
            image_url = image.image.url
            return request.build_absolute_uri(image_url)
        return None

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'slug', 'products']


