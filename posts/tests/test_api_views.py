from rest_framework.test import APIRequestFactory,force_authenticate
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser,User
from posts.models import Post

from posts.api.views import (
    PostCreateAPIView,
    PostDeleteAPIView,
    PostDetailAPIView,
    PostListAPIView,
    PostUpdateAPIView,
    )


# User = get_user_model

class PostApiTest(TestCase):
    def setUp(self):
        self.data = {"title":"coming days","content":"time is","publish":timezone.now().date()}
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            username='test1', email='test@neeps.in', password='top_secret',
            is_staff=True,is_superuser=True)

    def create_post(self,title='crucial'):
        return Post.objects.create(title=title)

    def test_get_data(self):
        list_url = reverse("posts-api:list")
        obj =self.create_post()  
        detail_url = reverse('posts-api:detail',kwargs={'slug':obj.slug})

        request = self.factory.get(list_url)
        response = PostListAPIView.as_view()(request)
        self.assertEqual(response.status_code,200)

        request = self.factory.get(detail_url)
        response = PostDetailAPIView.as_view()(request,slug=obj.slug)
        self.assertEqual(response.status_code,200)

    def test_post_data(self):
        create_url = reverse("posts-api:create")
        request = self.factory.post(create_url,data=self.data)
        response1 = PostCreateAPIView.as_view()(request)
        self.assertEqual(response1.status_code,401)
        force_authenticate(request,user=self.user)
        response = PostCreateAPIView.as_view()(request)
        self.assertEqual(response.status_code,201)

    def test_update_data(self):
        obj = self.create_post()
        update_url = reverse("posts-api:update",kwargs={"slug":obj.slug})
        request = self.factory.put(update_url,data=self.data)
        # print(request)
        response1 = PostUpdateAPIView.as_view()(request,slug=obj.slug)
        self.assertEqual(response1.status_code,401)

        force_authenticate(request,user=self.user)
        response = PostUpdateAPIView.as_view()(request,slug=obj.slug)
        self.assertEqual(response.status_code,200)

    def test_delete_data(self):
        obj = self.create_post()
        delete_url = reverse("posts-api:delete",kwargs={"slug":obj.slug})
        request = self.factory.delete(delete_url)
        print(request)
        response1 = PostDeleteAPIView.as_view()(request,slug=obj.slug)
        self.assertEqual(response1.status_code,401)
        force_authenticate(request,user=self.user)
        response = PostDeleteAPIView.as_view()(request,slug=obj.slug)
        self.assertEqual(response.status_code,204)