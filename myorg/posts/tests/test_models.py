from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class GroupPostModelTest(TestCase):
    def setUp(self):
        # USERNAME = 'test_user'
        self.user = User.objects.create(username='tst_user')
        self.post = Post.objects.create(
            text='о' * 100,
            author=self.user
        )
        self.group = Group.objects.create(title='Ж' * 100)

    def test_post_title_length(self):
        content = {
            self.post.text[:15]: str(self.post),
            self.group.title: str(self.group)
        }
        for expected, value in content.items():
            with self.subTest(expected=expected):
                self.assertEqual(expected, value)
