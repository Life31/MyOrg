from django.test import Client, TestCase


class AboutURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.about_urls = ['/about/author/', '/about/tech/']

    def test_author_url_exists_at_desired_location(self):
        for url in self.about_urls:
            response = self.guest_client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_about_urls_uses_correct_templates(self):
        about_context = {
            'about/author.html': '/about/author/',
            'about/tech.html': '/about/tech/'
        }
        for template, url in about_context.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
