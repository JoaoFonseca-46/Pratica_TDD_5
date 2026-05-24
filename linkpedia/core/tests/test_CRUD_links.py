from django.test import TestCase
from django.contrib.auth.models import User

from core.models import LinkModel


class LinkCRUDTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username='joao',
            email='joao@cps.sp.gov.br',
            password='123456'
        )

        self.client.login(
            username='joao',
            password='123456'
        )

        self.link = LinkModel.objects.create(
            titulo='Google',
            link='https://google.com',
            observacao='Site de pesquisa'
        )


    # TESTE 1
    def test_listar_links(self):

        response = self.client.get('/links/')

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            'Google'
        )


    # TESTE 2
    def test_cadastrar_link(self):

        response = self.client.post('/cadastrar/', {

            'titulo': 'YouTube',

            'link': 'https://youtube.com',

            'observacao': 'Vídeos'

        })

        self.assertEqual(response.status_code, 302)

        self.assertTrue(

            LinkModel.objects.filter(
                titulo='YouTube'
            ).exists()

        )


    # TESTE 3
    def test_editar_link(self):

        response = self.client.post(

            f'/editar/{self.link.id}/',

            {
                'titulo': 'Google Editado',
                'link': 'https://google.com',
                'observacao': 'Atualizado'
            }

        )

        self.assertEqual(response.status_code, 302)

        self.link.refresh_from_db()

        self.assertEqual(
            self.link.titulo,
            'Google Editado'
        )


    # TESTE 4
    def test_excluir_link(self):

        response = self.client.post(
            f'/excluir/{self.link.id}/'
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(

            LinkModel.objects.filter(
                id=self.link.id
            ).exists()

        )


    # TESTE 5
    def test_usuario_deslogado_redirecionado(self):

        self.client.logout()

        response = self.client.get('/links/')

        self.assertEqual(response.status_code, 302)