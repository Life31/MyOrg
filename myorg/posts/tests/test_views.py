import time

from django import forms
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Follow, Group, Post

User = get_user_model()
test_user_name = 'test_user'
test_user2_name = 'test_user_2'
author_user_name = 'author_user'


class PaginatorViewsTest(TestCase):
    def setUp(self):
        test_user_name = 'test_user'
        self.user = User.objects.create(username=test_user_name)
        self.group = Group.objects.create(
            title='Test_group',
            description='Test_description',
            slug='test_slug',
        )
        for i in range(11):
            Post.objects.create(text='test text',
                                author=self.user,
                                group=self.group)
        self.client = Client()
        self.client.force_login(self.user)
        cache.clear()

    def test_first_page_contains_10_records(self):
        urls = {
            reverse('index'): 'main page',
            reverse('group', kwargs={'slug': 'test_slug'}): 'group page',
            reverse('profile', kwargs={'username': test_user_name}): 'profile'
        }
        for url in urls.keys():
            response = self.client.get(url)
            self.assertEqual(len(response.context.get('page').object_list),
                             10)

    def test_second_page_contains_1_record(self):
        response = self.client.get(reverse('index') + '?page=2')
        print(response.context.get('page').object_list)
        self.assertEqual(len(response.context.get('page').object_list), 1)


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username=test_user_name)
        cls.post = Post.objects.create(
            text='а' * 100,
            author=PostsPagesTests.user
        )
        time.sleep(0.2)
        cls.group = Group.objects.create(
            title='Test_group',
            description='Test_description',
            slug='test_slug',
        )
        cls.post2 = Post.objects.create(
            text='с' * 20,
            author=PostsPagesTests.user,
            group=PostsPagesTests.group
        )
        time.sleep(0.2)
        cls.group_b = Group.objects.create(
            title='Test_group_b',
            description='Test_description_b',
            slug='test_slug_b',
        )
        cls.post3 = Post.objects.create(
            text='б' * 20,
            author=PostsPagesTests.user,
            group=PostsPagesTests.group_b
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostsPagesTests.user)
        self.author_user = User.objects.create_user(
            username=author_user_name, )
        self.user2 = User.objects.create_user(
            username=test_user2_name, )

    def test_authorized_pages_uses_correct_template(self):
        """
        Соответствует ли ожиданиям шаблоны для страниц:
            1)index;
            2)post_new;
            3)group/slug.
        """
        templates_page_names = {
            reverse('index'): 'index.html',
            reverse('post_new'): 'new_post.html',
            reverse('group', kwargs={'slug': 'test_slug'}): 'group.html',
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_guest_pages_show_correct_context(self):
        """
        Соответствует ли ожиданиям context для:
            1)home_page;
            2)group_page;
            3)profile_page.
        """
        all_stuff = {
            reverse('index'): [PostsPagesTests.post],
            reverse('group',
                    kwargs={'slug': 'test_slug'}): [
                        PostsPagesTests.post2,
                        {'group': PostsPagesTests.group}],
            reverse('profile',
                    kwargs={'username': test_user_name}): [
                        PostsPagesTests.post,
                        {'author': PostsPagesTests.user,
                         'count': PostsPagesTests.user.posts.count()}]
        }

        for reverse_name, expected in all_stuff.items():
            response = self.guest_client.get(reverse_name)
            print(response.context.get('page').object_list)
            self.assertEqual(response.context.get('page').object_list[-1],
                             expected[0])
            if len(expected) > 1:
                for value, context in expected[1].items():
                    with self.subTest(value=value):
                        self.assertEqual(response.context[value], context)

    def test_authorized_pages_show_correct_context(self):
        """
        Соответствует ли ожиданиям context для:
            1)post_new;
            2)post_edit.
        """
        urls = {
            'new post page': reverse('post_new'),
            'post edit page': reverse('post_edit', kwargs={
                'username': test_user_name,
                'post_id': PostsPagesTests.post.id
            })
        }
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for name, url in urls.items():
            response = self.authorized_client.get(url)
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    if name == 'post edit page':
                        self.assertTrue(response.context.get('edit'))
                    form_field = response.context['form'].fields[value]
                    self.assertIsInstance(form_field, expected)

    def test_post_show_correct_context(self):
        """
        Соответствует ли ожиданиям context для:
            1)post_page.
        """
        response = self.authorized_client.get(reverse('post', kwargs={
            'username': test_user_name,
            'post_id': PostsPagesTests.post.id
        }))
        context_values = {
            'post': PostsPagesTests.post,
            'author': PostsPagesTests.user,
            'count': PostsPagesTests.user.posts.count(),
        }
        for value, expected in context_values.items():
            with self.subTest(value=value):
                self.assertEqual(response.context[value], expected)

    def test_home_page_show_post_new_with_group(self):
        """
        Пост из группы отображается на главной странице.
        """
        response = self.guest_client.get(reverse('index'))
        self.assertIn(PostsPagesTests.post3,
                      response.context.get('page').object_list)

    def test_post_new_with_group_shows_not_in_other_group_page(self):
        """
        Пост из группы А не отображается в группе В.
        """
        response = self.guest_client.get(reverse(
            'group', kwargs={'slug': 'test_slug'}
        ))
        self.assertNotIn(PostsPagesTests.post3,
                         response.context.get('page').object_list)

    def test_subs_list(self):
        author_text = 'Hi there'
        Follow.objects.create(
            author=self.author_user,
            user=self.user
        )
        Post.objects.create(
            author=self.author_user,
            group=self.group,
            text=author_text
        )
        """Пост отображается у подписчиков"""
        response = self.authorized_client.get(reverse('follow_index'),
                                              follow=True)
        if 'paginator' in response.context:
            rc = response.context['page'].object_list[0]
        else:
            rc = response.context['post']
        self.assertEqual(rc.text, author_text)
        self.assertEqual(rc.author, self.author_user)
        self.assertEqual(rc.group, self.group)

        """Пост не отображается у неподписчиков"""
        self.authorized_client.force_login(self.user2)
        response = self.authorized_client.get(reverse('follow_index'),
                                              follow=True)
        posts_num = len(response.context['page'].object_list)
        self.assertEqual(posts_num, 0)

    def test_subscribe(self):
        sub_before = self.user.follower.count()
        self.authorized_client.get(
            reverse("profile_follow", args=[self.author_user])
        )
        sub_after = self.user.follower.count()
        self.assertEqual(sub_before, 0)
        self.assertEqual(sub_after, 1)

    def test_unsubscribe(self):
        Follow.objects.create(
            author=self.author_user,
            user=self.user
        )
        sub_before = self.user.follower.count()
        self.authorized_client.get(
            reverse("profile_unfollow", args=[self.author_user])
        )
        sub_after = self.user.follower.count()
        self.assertEqual(sub_before, 1)
        self.assertEqual(sub_after, 0)
