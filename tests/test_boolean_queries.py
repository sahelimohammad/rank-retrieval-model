"""Check the preserved Boolean search implementation against its saved index."""
import ast
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from CosineSimilarity import CosineSimilarity
from PreprocessQuery import PreprocessQuery


def read_saved_index():
    """Read the original OrderedDict weights without evaluating arbitrary code."""
    tree = ast.parse((ROOT / 'tfidf_weights' / 'weights.txt').read_text(encoding='utf-8'), mode='eval').body
    if not (isinstance(tree, ast.Call) and isinstance(tree.func, ast.Name) and tree.func.id == 'OrderedDict'
            and len(tree.args) == 1 and not tree.keywords):
        raise ValueError('Unexpected format in the saved TF-IDF weights')
    terms = dict(ast.literal_eval(tree.args[0]))
    files = ast.literal_eval((ROOT / 'Indexes' / 'file_index.txt').read_text(encoding='utf-8'))
    return terms, files


class BooleanSearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.terms, cls.files = read_saved_index()

    def run_query(self, text):
        # These patches avoid downloading resources during this small logic test.
        # They do not change any project source files.
        with patch('PreprocessQuery.all_stop_words', return_value=[]), patch(
            'PreprocessQuery.lemmatize_text', side_effect=lambda s: [[s.lower()]]
        ):
            preprocessor = PreprocessQuery(text)
        self.assertTrue(preprocessor.boolean2)
        obj = CosineSimilarity.__new__(CosineSimilarity)
        obj.file_index = self.files
        obj.tfidf = self.terms
        return obj.check_boolean(preprocessor.boolean2)

    def test_or_plus(self):
        self.assertEqual(len(self.run_query('sport + line')), 20)
        self.assertEqual(self.run_query('sport + line'), self.run_query('sport OR line'))

    def test_and(self):
        self.assertEqual(self.run_query('sport AND line'), ['nike.txt', 'yahoo.txt'])

    def test_not(self):
        self.assertEqual(len(self.run_query('NOT sport')), 36)
        self.assertEqual(self.run_query('sport NOT line'),
                         ['puma.txt', 'reddit.txt', 'reliance.txt'])
        self.assertEqual(self.run_query('sport NOT line'),
                         self.run_query('sport AND NOT line'))

    def test_parentheses(self):
        self.assertEqual(len(self.run_query('(sport + line) AND NOT technology')), 7)

    def test_invalid_query(self):
        obj = CosineSimilarity.__new__(CosineSimilarity)
        obj.file_index = self.files
        obj.tfidf = self.terms
        with self.assertRaises(ValueError):
            obj.check_boolean(['sport', 'AND'])


if __name__ == '__main__':
    unittest.main()
