from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'socialsite'

urlpatterns = [
    path('socialhome/', views.HomePage.as_view(), name="socialhome"),
    path('login/', views.SocialLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name="signup"),
    path('groups/', views.ListGroups.as_view(), name="groups"),
    path("newgroup/", views.CreateGroup.as_view(), name="creategroup"),
    path("posts/in/<slug>/", views.SingleGroup.as_view(), name="single"),
    path("join/<slug>/", views.JoinGroup.as_view(), name="join"),
    path("leave/<slug>/", views.LeaveGroup.as_view(), name="leave"),
    path('posts/', views.PostList.as_view(), name="posts"),
    path("newpost/", views.CreatePost.as_view(), name="createpost"),
    path("by/<username>/", views.UserPosts.as_view(), name="for_user"),
    path("by/<username>/<int:pk>/", views.PostDetail.as_view(), name="single"),
    path("delete/<int:pk>/", views.DeletePost.as_view(), name="delete"),
    path('test/', views.TestPage.as_view(), name="test"),

]
