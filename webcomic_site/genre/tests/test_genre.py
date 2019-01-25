from webcomic_site.tests import BaseTest
from webcomic_site.genre.models import Genre


class CreateGenreTest(BaseTest):
    def setUp(self):
        super().setUp()
        self.genre1 = Genre(name='New Genre')
        self.genre1.save()
        self.genre2 = Genre(name='New Genre')
        self.genre2.save()

    def test_create_genre_slug_successful(self):
        self.assertEqual('new-genre', self.genre1.slug)
        self.assertEqual('new-genre-2', self.genre2.slug)
