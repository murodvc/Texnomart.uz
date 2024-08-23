from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token
from texnomart import views, auth
from texnomart.views import Comments, CommentCreateView

router = DefaultRouter()
router.register('categories', views.CategoryModelViewSet, basename='category')
router.register('products', views.ProductModelViewSet, basename='product')

urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetail.as_view(), name='detail_category'),
    path('category/add-category/', views.AddCategory.as_view(), name='add_category'),
    path('category/<slug:slug>/delete/', views.DeleteCategory.as_view(), name='delete_category'),
    path('category/<slug:slug>/edit/', views.UpdateCategory.as_view(), name='edit_category'),
    path('modelviewset/', include(router.urls)),

    # product
    path('', views.ProductList.as_view(), name='product_list'),
    path('product/add-product/', views.AddProduct.as_view(), name='add_product'),
    path('product/<int:pk>', views.ProductDetail.as_view(), name='detail_product'),
    path('product/<int:pk>/delete/', views.DeleteProduct.as_view(), name='delete_product'),
    path('product/<int:pk>/edit/', views.Updateproduct.as_view(), name='edit_product'),
    path('product/<int:pk>/product-attributes/', views.ProductAttributes.as_view(), name='product_attributes'),

    # attributes
    path('attribute-keys/', views.AttributeKey.as_view(), name='attribute_key'),
    path('attribute-values/', views.AttributeValues.as_view(), name='attribute_value'),


    path('comments/', Comments.as_view(), name='comments'),
    path('add-comment/', CommentCreateView.as_view(), name='add_comments'),



#     TokenAuthentication
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),


#     login, register, logout
    path('register/', auth.RegisterView.as_view(), name='register'),
    path('login/', auth.LoginView.as_view(), name='login'),
    path('logout/', auth.LogoutView.as_view(), name='logout'),

#     JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')

]