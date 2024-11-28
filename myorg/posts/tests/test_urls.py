from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
    username = 'tst_user'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=cls.username)
        cls.user2 = User.objects.create_user(username='test_user2')
        cls.group = Group.objects.create(
            title='Test_group',
            description='Test description',
            slug='test_slug',
        )
        cls.post = Post.objects.create(
            text='test_post',
            author=PostsURLTests.user
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostsURLTests.user)
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(PostsURLTests.user2)
        self.new_url = '/new/'
        self.post_edit = f'/{ self.username }/{ self.post.id }/edit/'
        cache.clear()

    def test_urls_exists_at_desired_location(self):
        urls = [
            '/',
            f'/group/{self.group.slug}/',
            f'/{ self.username }/',
            f'/{ self.username }/{ self.post.id }/',
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_new_post_url_exists_at_desired_location(self):
        response = self.authorized_client.get(self.new_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_new_post_url_redirect_anonymous_on_login(self):
        response = self.guest_client.get(self.new_url, follow=True)
        self.assertRedirects(response, '/auth/login/?next=/new/')

    def test_post_edit_url_not_shows_for_anonymous(self):
        response = self.guest_client.get(self.post_edit)
        self.assertNotEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_url_shows_for_author(self):
        response = self.authorized_client.get(self.post_edit)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_url_not_shows_not_for_author(self):
        response = self.authorized_client2.get(self.post_edit)
        self.assertNotEqual(response.status_code, HTTPStatus.OK)

    def test_post_edit_url_redirect_anonymous_on_login(self):
        response = self.guest_client.get(self.post_edit, follow=True)
        self.assertRedirects(
            response,
            f'/auth/login/?next=/{ self.username }/{ self.post.id }/edit/')

    def test_post_edit_url_redirect_not_author_on_post_url(self):
        response = self.authorized_client2.get(self.post_edit, follow=True)
        self.assertRedirects(response,
                             f'/{ self.username }/{ self.post.id }/')

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            '/': 'index.html',
            f'/group/{self.group.slug}/': 'group.html',
            '/new/': 'new_post.html',
            f'/{ self.username }/{ self.post.id }/edit/': 'new_post.html'
        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
