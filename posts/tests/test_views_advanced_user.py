from django.test import TestCase,RequestFactory
from posts.models import Post
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser,User
from django.contrib.auth import get_user_model
from posts.views import post_update,post_create
from django.http.response import Http404
# Create your tests here.
class PostViewAdvanceTestCase(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username='test1', email='test@neeps.in', password='top_secret',
            is_staff=True,is_superuser=True)

    def create_post(self,title='This title'):
        return Post.objects.create(title=title)

    def test_user_auth(self):
        obj = self.create_post(title='Superman will come')
        edit_url = reverse("posts:update",kwargs={"slug":obj.slug})
        request = self.factory.get(edit_url)
        request.user = self.user
        response = post_update(request,slug=obj.slug)
        self.assertEqual(response.status_code,200)
        # print(request.user.is_authenticated())

    def test_user_post(self):
        obj = self.create_post(title='Superman will come')
        request = self.factory.get("posts/create")
        request.user = self.user
        response = post_create(request)
        self.assertEqual(response.status_code,200)
        # print(request.user.is_authenticated())

    def test_unauth_user(self):
        obj = self.create_post(title='Superman will come')
        edit_url = reverse("posts:update",kwargs={"slug":obj.slug})
        request = self.factory.get(edit_url)
        request.user = AnonymousUser()
        response = post_update(request,slug=obj.slug)
        self.assertEqual(response.status_code,404)

    def test_empty_page(self):
        page = 'asdasda/asdad/adasdas'
        request = self.factory.get("page")
        request.user = self.user
        response = post_create(request)
        self.assertEqual(response.status_code,200)






    # def test_update_view(self):
    #     obj = self.create_post(title='Another new title')
    #     edit_url = reverse("posts:update",kwargs={"slug":obj.slug})
    #     response = self.client.get(obj.get_absolute_url()+"edit/")
    #     self.assertEqual(response.status_code,404)   


    # def test_delete_view(self):
    #     obj = self.create_post(title='Whoose there')
    #     delete_url = obj.get_absolute_url()+"delete/"
    #     print(delete_url)
    #     response = self.client.get(delete_url)
    #     self.assertEqual(response.status_code,404)