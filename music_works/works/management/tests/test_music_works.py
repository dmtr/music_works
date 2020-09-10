from django.test import TestCase

from works.management.commands.load_works import (Work, merge_contributors,
                                                  process_music_work)
from works.models import MusicWork


def _get_work(iswc="T0101234567", title="test", contributors=None):
    return Work(
        iswc=iswc, title=title, contributors=contributors or ["test_contributor"]
    )


class MergeContributorsTest(TestCase):
    def test_merge_equal(self):
        work1 = _get_work()
        work2 = _get_work()
        contributors = merge_contributors(work1.contributors, work2.contributors)
        self.assertEqual(work1.contributors, contributors)
        self.assertEqual(work2.contributors, contributors)

    def test_merge_overlapped(self):
        work1 = _get_work(contributors=["Test1", "Test2"])
        work2 = _get_work(contributors=["Test1", "Test3"])
        contributors = merge_contributors(work1.contributors, work2.contributors)
        self.assertEqual(["Test1", "Test2", "Test3"], contributors)


class ProcessMusicWorkTest(TestCase):
    def setUp(self):
        work = _get_work()
        self.work1 = MusicWork.objects.create(
            iswc=work.iswc, title=work.title, contributors=work.contributors
        )

        work = _get_work(iswc=None, title="work2", contributors=["work2 contributor"])
        self.work2 = MusicWork.objects.create(
            iswc=work.iswc, title=work.title, contributors=work.contributors
        )

    def test_create(self):
        work = _get_work(iswc="T0101234568", title="New Song")
        process_music_work(work)
        from_db = MusicWork.objects.get(iswc=work.iswc)
        self.assertIsNotNone(from_db)
        self.assertEqual(work.iswc, from_db.iswc)
        self.assertEqual(work.title, from_db.title)
        self.assertEqual(work.contributors, from_db.contributors)

    def test_find_and_update_by_iswc(self):
        work = _get_work(contributors=["New Artist"])
        process_music_work(work)
        from_db = MusicWork.objects.get(iswc=work.iswc)
        self.assertIsNotNone(from_db)
        self.assertEqual(work.title, from_db.title)
        self.assertEqual(["New Artist", "test_contributor"], from_db.contributors)

    def test_find_update_by_title_and_contributors(self):
        work = _get_work(
            iswc=None, contributors=["New Artist"] + self.work1.contributors
        )
        process_music_work(work)
        from_db = MusicWork.objects.get(id=self.work1.id)
        self.assertIsNotNone(from_db)
        self.assertEqual(self.work1.iswc, from_db.iswc)
        self.assertEqual(work.title, from_db.title)
        self.assertEqual(["New Artist", "test_contributor"], from_db.contributors)

    def test_iswc_is_updated(self):
        iswc = "T0101234568"
        work = _get_work(
            iswc=iswc,
            title=self.work2.title,
            contributors=["New Artist"] + self.work2.contributors,
        )
        process_music_work(work)
        from_db = MusicWork.objects.get(id=self.work2.id)
        self.assertIsNotNone(from_db)
        self.assertEqual(work.iswc, from_db.iswc)
        self.assertEqual(work.title, from_db.title)
        self.assertEqual(["New Artist", "work2 contributor"], from_db.contributors)
