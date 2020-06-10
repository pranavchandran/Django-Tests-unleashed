from django.test import TestCase
from posts.models import Post
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

# Create your tests here.

User = get_user_model()


class PostModelTestCase(TestCase):

    def create_post(self,title='This title'):
        return Post.objects.create(title=title)

    def test_list_view(self):
        list_url = reverse("posts:list")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code,200)

    def test_update_view(self):
        obj = self.create_post(title='Another new title')
        edit_url = reverse("posts:update",kwargs={"slug":obj.slug})
        response = self.client.get(obj.get_absolute_url()+"edit/")
        self.assertEqual(response.status_code,404)   

    def test_detail_view(self):
        obj = self.create_post(title='Whoose there')
        response = self.client.get(obj.get_absolute_url())
        self.assertEqual(response.status_code,200)

    def test_delete_view(self):
        obj = self.create_post(title='Whoose there')
        delete_url = obj.get_absolute_url()+"delete/"
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code,404)