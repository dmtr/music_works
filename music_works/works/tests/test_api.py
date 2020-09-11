import json

from django.test import TestCase
from django.urls import reverse

from works.models import MusicWork


class APITest(TestCase):
    def setUp(self):
        self.work = MusicWork.objects.create(
            iswc="T0000001234", title="test", contributors=["test contributor"]
        )

    def test_get_ok(self):
        res = self.client.get(reverse("music-works"), {"iswc": self.work.iswc})
        self.assertEqual(200, res.status_code)
        res = json.loads(res.content)
        self.assertEqual(self.work.title, res["title"])
        self.assertEqual(self.work.contributors, res["contributors"])

    def test_get_404(self):
        res = self.client.get(reverse("music-works"), {"iswc": "foo"})
        self.assertEqual(404, res.status_code)

    def test_get_400(self):
        res = self.client.get(reverse("music-works"))
        self.assertEqual(400, res.status_code)
