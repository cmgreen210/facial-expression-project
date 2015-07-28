import os

from django.test import TestCase
from django.core.exceptions import ValidationError
import pep8

from django_expression.models import validate_request_type


class ValidatorTests(TestCase):
    def test_request_type(self):
        validate_request_type(0)
        validate_request_type(1)
        self.assertRaises(ValidationError, validate_request_type, "0")
        self.assertRaises(ValidationError, validate_request_type, "1")
        self.assertRaises(ValidationError, validate_request_type, -1)


class CodeStyleTest(TestCase):

    def test_pep(self):
        """Test for PEP8 conformance"""

        root_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.join(root_dir, '../')

        file_list = []
        for root, _, files in os.walk(root_dir):
            for f in files:
                _, ext = os.path.splitext(f)
                if ext == '.py' and not ('migrations' in root):
                    file_list.append(os.path.abspath(os.path.join(root, f)))

        pep8style = pep8.StyleGuide(quiet=False)

        result = pep8style.check_files(file_list)

        self.assertEqual(result.total_errors, 0,
                         result.print_statistics())
