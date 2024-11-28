from http import HTTPStatus
import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.USERNAME = 'tsty_user'
        cls.user = User.objects.create(username=cls.USERNAME)
        cls.group = Group.objects.create(
            title="Тест тайтл",
            description="Тестовое описание",
            slug="Test_slug")
        cls.group2 = Group.objects.create(
            title="Тест тайтл2",
            description="Тестовое описание2",
            slug="Test_slug2")
        cls.post = Post.objects.create(
            text="Тестовый текст",
            author=cls.user,
            group=cls.group)
        cls.post2 = Post.objects.create(
            text="Тестовый текст2",
            author=cls.user,
            group=cls.group2)
        cls.form = PostForm()
        cls.count = Post.objects.count()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostFormTests.user)
        cache.clear()

    def test_post_form_create_new_post(self):
        posts_count = Post.objects.count()
        form_data = {'text': 'Тестовый текст для нового поста'}
        response = self.authorized_client.post(
            reverse('post_new'),
            data=form_data,
            follow=True
        )
        self.assertTrue(
            Post.objects.filter(
                author=self.post.author,
                text=form_data['text']
            ).exists()
        )
        self.assertEqual(response.context.get('page').object_list[0].text,
                         form_data['text'])
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_form_edit_post(self):
        posts_count = Post.objects.count()
        form_data = {'text': 'Тестовый текст для измененного поста'}
        self.authorized_client.post(
            reverse('post_edit', kwargs={
                'username': self.USERNAME,
                'post_id': PostFormTests.post2.id,
            }),
            data=form_data,
            follow=True
        )
        edit_post = PostFormTests.post2.id
        self.assertEqual(Post.objects.get(id=edit_post).text,
                         form_data['text'])
        self.assertEqual(Post.objects.count(), posts_count)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_create_new_post(self):
        """Новый пост создаётся успешно"""
        posts_count = Post.objects.count()
        small_gif = (
            b"\x47\x49\x46\x38\x39\x61\x02\x00"
            b"\x01\x00\x80\x00\x00\x00\x00\x00"
            b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
            b"\x00\x00\x00\x2C\x00\x00\x00\x00"
            b"\x02\x00\x01\x00\x00\x02\x02\x0C"
            b"\x0A\x00\x3B"
        )
        uploaded = SimpleUploadedFile(
            name="small.gif", content=small_gif, content_type="image/gif"
        )
        form_data = {
            "text": "Test.",
            "group": self.group.id,
            "image": uploaded,
        }
        response = self.authorized_client.post(
            reverse("post_new"), data=form_data, follow=True
        )
        post = Post.objects.first()
        self.assertRedirects(response, reverse("index"))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertEqual(post.text, form_data["text"])
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group.id, form_data["group"])
        self.assertIsNotNone(response.context["post"].image)
        self.assertEqual(response.status_code, HTTPStatus.OK)
