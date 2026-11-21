import unittest
from extractor import processarExtracao
from unittest.mock import patch, MagicMock

class TestExtractor(unittest.TestCase):

    # Garante que o bloqueio de textos vazios ocorra corretamete
    def test_textoVazio(self):        
        # Simulando o usuário mandando apenas espaços em branco
        resultado = processarExtracao("   ")
        self.assertEqual(resultado, "Erro: O texto do comprovante não pode estar vazio.")

    # Garente que a IA responda corretamente sem gastar tokens ou acessar a internet
    @patch('extractor.cliente.chat.completions.create')
    def test_extracaoSucesso_mock(self, mock_create):
        # Configutando o mock
        mock_resposta = MagicMock()
        mock_resposta.choices[0].message.content = '{"chave_pix": "123", "valor": "50.00"}'
        mock_create.return_value = mock_resposta

        # Processa a extração falsa
        resultado = processarExtracao("Comprovante de teste de R$ 50,00")

        # Verifica se a função tratou o JSON corretamente
        self.assertTrue(mock_create.called)
        self.assertEqual(resultado, '{"chave_pix": "123", "valor": "50.00"}')

    # Simula uma falha grave na chamada da API para garantir que o código não quebre
    @patch('extractor.cliente.chat.completions.create')
    def test_extracaoErroInesperado_mock(self, mock_create):
        # Coloca um erro na chamada da API
        mock_create.side_effect = Exception("Houve uma falha grave no servidor")
        resultado = processarExtracao("Comprovante de R$ 50,00")
        self.assertEqual(resultado, "[ERRO INESPERADO] Falha durante a extração: Houve uma falha grave no servidor")

if __name__ == '__main__':
    unittest.main()