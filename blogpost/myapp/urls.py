from django.urls import path
from myapp import views

app_name='myapp'
urlpatterns = [
        path('register/',views.register,name="register"),
        # path('login/',views.loginview,name="login"),
        # path('logout/',views.logoutview,name="logout"),
        path('<int:pk>/newpost/',views.newpost,name="newpost"),
        path('draft/',views.DraftPost.as_view(), name="draft"),
        path('<int:pk>',views.PostDetail.as_view(),name="detail"),
        path('<int:pk>/publish/', views.publishview, name = "publish"),
        path('<int:pk>/edit/', views.EditView.as_view(), name = "edit"),
        path('<int:pk>/delete/', views.DeletingView.as_view(), name = "delete"),
        path('<int:pk>/comment/',views.addcomment,name = "comment"),
        path('<int:pk>/approvecom',views.approvecom,name = "approvecom"),
        path('<int:pk>/deletecom',views.deletecom,name = "deletecom"),
]
