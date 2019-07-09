from unittest import TestCase
import k2_util

class K2UtilTests(TestCase):
    def test_to_snake_case(self):
        self.assertIsNone(k2_util.to_snake_case(None))
        self.assertEqual('', k2_util.to_snake_case(''))
        self.assertEqual('hello_world', k2_util.to_snake_case('hello world!'))
        self.assertEqual('1234_hello_world', k2_util.to_snake_case('1234 hello world!'))
        self.assertEqual('hello_1234_world', k2_util.to_snake_case('hello 1234 world!'))
        self.assertEqual('hmm_how_about_this', k2_util.to_snake_case('  {Hmm how aBout @£$%^ this!@£$'))
        
    def test_to_kebab_case(self):
        self.assertIsNone(k2_util.to_kebab_case(None))
        self.assertEqual('', k2_util.to_kebab_case(''))
        self.assertEqual('hello-world', k2_util.to_kebab_case('hello world!'))
        self.assertEqual('hmm-how-about-this', k2_util.to_kebab_case('  {Hmm how aBout @£$%^ this!@£$'))

    def test_to_camel_case(self):
        self.assertIsNone(k2_util.to_camel_case(None))
        self.assertEqual('', k2_util.to_camel_case(''))
        self.assertEqual('helloWorld', k2_util.to_camel_case('hello world!'))
        self.assertEqual('model1', k2_util.to_camel_case('model1'))
        self.assertEqual('helloWorld', k2_util.to_camel_case('1234 hello world!'))
        self.assertEqual('hello1234World', k2_util.to_camel_case('hello 1234 world!'))
        self.assertEqual('hmmHowAboutThis', k2_util.to_camel_case('  {Hmm how aBout @£$%^ this!@£$'))

    def test_to_class_case(self):
        self.assertIsNone(k2_util.to_class_case(None))
        self.assertEqual('', k2_util.to_class_case(''))
        self.assertEqual('HelloWorld', k2_util.to_class_case('hello world!'))
        self.assertEqual('Model1', k2_util.to_class_case('model1'))
        self.assertEqual('HelloWorld', k2_util.to_class_case('1234 hello world!'))
        self.assertEqual('Hello1234World', k2_util.to_class_case('hello 1234 world!'))
        self.assertEqual('HmmHowAboutThis', k2_util.to_class_case('  {Hmm how aBout @£$%^ this!@£$'))

    def test_to_sentence_case(self):
        self.assertIsNone(k2_util.to_sentence_case(None))
        self.assertEqual('', k2_util.to_sentence_case(''))
        self.assertEqual('Hello world', k2_util.to_sentence_case('hello world!'))
        self.assertEqual('Hello World', k2_util.to_sentence_case('hello World!'))
        self.assertEqual('1234 hello world', k2_util.to_sentence_case('1234 hello world!'))
        self.assertEqual('Hello 1234 World', k2_util.to_sentence_case('hello 1234 World!'))
        self.assertEqual('Hmm how aBout this', k2_util.to_sentence_case('  {Hmm how aBout @£$%^ this!@£$'))

    def test_to_title_case(self):
        self.assertIsNone(k2_util.to_title_case(None))
        self.assertEqual('', k2_util.to_title_case(''))
        self.assertEqual('Hello World', k2_util.to_title_case('hello world!'))
        self.assertEqual('Hello World', k2_util.to_title_case('hello World!'))
        self.assertEqual('1234 Hello World', k2_util.to_title_case('1234 hello world!'))
        self.assertEqual('Hello 1234 World', k2_util.to_title_case('hello 1234 World!'))
        self.assertEqual('Hmm How About This', k2_util.to_title_case('  {Hmm how aBout @£$%^ this!@£$'))
        
    def test_to_plural(self):
        self.assertIsNone(k2_util.to_plural(None))
        self.assertEqual('', k2_util.to_plural(''))
        self.assertEqual('foos', k2_util.to_plural('foo'))
        self.assertEqual('cacti', k2_util.to_plural('cactus'))
        self.assertEqual('leaves', k2_util.to_plural('leaf'))
        self.assertEqual('1234', k2_util.to_plural('1234'))
        self.assertEqual('tries', k2_util.to_plural('try'))
        self.assertEqual('days', k2_util.to_plural('day'))
        
    def test_filter_dict(self):
        d1={
            'a': 'A',
            'b': 'B',
            'c': 'C'
        }
        test = k2_util.filter_dict(d1, ['a', 'b'])
        self.assertEqual(2, len(test))
        self.assertTrue('a' in test)
        self.assertTrue('b' in test)
        self.assertTrue('c' not in test)
        
    def test_strip_dict(self):
        d1={
            'a': 'A',
            'b': 'B',
            'c': 'C'
        }
        test = k2_util.strip_dict(d1, ['a', 'b'])
        self.assertEqual(1, len(test))
        self.assertTrue('a' not in test)
        self.assertTrue('b' not in test)
        self.assertTrue('c' in test)
        
if __name__ == '__main__':
    unittest.main()

