from django.test import TestCase
from . import to_snake_case
from . import to_kebab_case
from . import to_camel_case
from . import to_class_case
from . import to_sentence_case
from . import to_title_case

class K2UtilTests(TestCase):
    def test_to_snake_case(self):
        self.assertIsNone(to_snake_case(None))
        self.assertEquals('', to_snake_case(''))
        self.assertEquals('hello_world', to_snake_case('hello world!'))
        self.assertEquals('1234_hello_world', to_snake_case('1234 hello world!'))
        self.assertEquals('hello_1234_world', to_snake_case('hello 1234 world!'))
        self.assertEquals('hmm_how_about_this', to_snake_case('  {Hmm how aBout @£$%^ this!@£$'))
        
    def test_to_kebab_case(self):
        self.assertIsNone(to_kebab_case(None))
        self.assertEquals('', to_kebab_case(''))
        self.assertEquals('hello-world', to_kebab_case('hello world!'))
        self.assertEquals('hmm-how-about-this', to_kebab_case('  {Hmm how aBout @£$%^ this!@£$'))

    def test_to_camel_case(self):
        self.assertIsNone(to_camel_case(None))
        self.assertEquals('', to_camel_case(''))
        self.assertEquals('helloWorld', to_camel_case('hello world!'))
        self.assertEquals('model1', to_camel_case('model1'))
        self.assertEquals('helloWorld', to_camel_case('1234 hello world!'))
        self.assertEquals('hello1234World', to_camel_case('hello 1234 world!'))
        self.assertEquals('hmmHowAboutThis', to_camel_case('  {Hmm how aBout @£$%^ this!@£$'))

    def test_to_class_case(self):
        self.assertIsNone(to_class_case(None))
        self.assertEquals('', to_class_case(''))
        self.assertEquals('HelloWorld', to_class_case('hello world!'))
        self.assertEquals('Model1', to_class_case('model1'))
        self.assertEquals('HelloWorld', to_class_case('1234 hello world!'))
        self.assertEquals('Hello1234World', to_class_case('hello 1234 world!'))
        self.assertEquals('HmmHowAboutThis', to_class_case('  {Hmm how aBout @£$%^ this!@£$'))

    def test_to_sentence_case(self):
        self.assertIsNone(to_sentence_case(None))
        self.assertEquals('', to_sentence_case(''))
        self.assertEquals('Hello world', to_sentence_case('hello world!'))
        self.assertEquals('Hello World', to_sentence_case('hello World!'))
        self.assertEquals('1234 hello world', to_sentence_case('1234 hello world!'))
        self.assertEquals('Hello 1234 World', to_sentence_case('hello 1234 World!'))
        self.assertEquals('Hmm how aBout this', to_sentence_case('  {Hmm how aBout @£$%^ this!@£$'))

    def test_to_title_case(self):
        self.assertIsNone(to_title_case(None))
        self.assertEquals('', to_title_case(''))
        self.assertEquals('Hello World', to_title_case('hello world!'))
        self.assertEquals('Hello World', to_title_case('hello World!'))
        self.assertEquals('1234 Hello World', to_title_case('1234 hello world!'))
        self.assertEquals('Hello 1234 World', to_title_case('hello 1234 World!'))
        self.assertEquals('Hmm How About This', to_title_case('  {Hmm how aBout @£$%^ this!@£$'))

