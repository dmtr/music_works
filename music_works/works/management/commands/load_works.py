import logging
from collections import namedtuple
from csv import DictReader
from typing import Generator, List, Optional, TextIO

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction

from works.models import MusicWork

logger = logging.getLogger(__name__)

Work = namedtuple("Work", ["iswc", "title", "contributors"])


def work_generator(csv_file: TextIO) -> Generator[Work, None, None]:
    reader = DictReader(csv_file)
    for row in reader:
        contributors = row["contributors"].split("|")
        yield Work(
            iswc=row["iswc"] if row["iswc"] else None,
            title=row["title"],
            contributors=contributors,
        )


def create_work(work: Work) -> Optional[MusicWork]:
    try:
        with transaction.atomic():
            return MusicWork.objects.create(
                iswc=work.iswc, title=work.title, contributors=work.contributors
            )
    except IntegrityError:
        logger.debug("Already exists %s", work)


def merge_contributors(contributors1: List[str], contributors2: List[str]) -> List[str]:
    """Merge two lists of contributors.
       Assumes that strings are case-sensitive (John and john are different names)
    """
    contributors = set(contributors1)
    contributors.update(contributors2)
    return sorted(list(contributors))


def update_work(music_work: MusicWork, work: Work) -> None:
    contributors = merge_contributors(music_work.contributors, work.contributors)
    update_fields = []

    if sorted(music_work.contributors) != contributors:
        music_work.contributors = contributors
        update_fields.append("contributors")

    if music_work.iswc is None and work.iswc is not None:
        music_work.iswc = work.iswc
        update_fields.append("iswc")

    if update_fields:
        music_work.save(update_fields=update_fields)


def find_music_work(work: Work) -> List[MusicWork]:
    music_works = []
    if work.iswc:
        music_works = MusicWork.objects.filter(iswc=work.iswc)

    if music_works:
        return music_works

    return MusicWork.objects.filter(
        title=work.title, contributors__overlap=work.contributors
    )


def process_music_work(work: Work) -> Optional[MusicWork]:
    logger.debug("Got %s", work)
    with transaction.atomic():
        music_works = find_music_work(work)
        if len(music_works) == 0:
            return create_work(work)
        elif len(music_works) == 1:
            music_work = music_works[0]
            update_work(music_work, work)
            return music_work
        else:
            logger.warning(
                "Found multiple work objects for %s, can not reconsile", work
            )


class Command(BaseCommand):
    help = "Load and reconcile works data from csv file"

    def add_arguments(self, parser):
        parser.add_argument("path", type=str)

    def handle(self, *args, **options):
        logger.info("Start")
        try:
            csv_file = open(options["path"])
            works = work_generator(csv_file)
            counter = 0

            for work in works:
                music_work = process_music_work(work)
                logger.debug("Got %s", music_work)
                counter += 1

            logger.info("Finished, processed %d works", counter)
        except Exception as exc:
            raise CommandError(exc)
