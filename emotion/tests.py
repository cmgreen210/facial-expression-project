from django.test import TestCase
from emotion.models import validate_request_type, validate_image_csv
from django.core.exceptions import ValidationError
import pep8


class ValidatorTests(TestCase):
    def test_request_type(self):
        validate_request_type(0)
        validate_request_type(1)
        self.assertRaises(ValidationError, validate_request_type, "0")
        self.assertRaises(ValidationError, validate_request_type, "1")
        self.assertRaises(ValidationError, validate_request_type, -1)

    def test_validate_image_csv(self):
        height = 2
        width = 3
        value = "1,2,3,4,5,6"
        validate_image_csv(value, height, width)

        self.assertRaises(ValidationError, validate_image_csv, value)
        self.assertRaises(ValidationError, validate_image_csv, value,
                          separator='\t')


class CodeStyleTest(TestCase):
    def setUp(self):
        self._file_list = ['emotion/tests.py',
                           'emotion/forms.py',
                           'emotion/models.py',
                           'emotion/views.py',
                           'emotion/urls.py']

    def test_pep(self):
        """Test for PEP8 conformance"""

        pep8style = pep8.StyleGuide(quiet=False)

        result = pep8style.check_files(self._file_list)
        self.assertEqual(result.total_errors, 0,
                         result.print_statistics())
