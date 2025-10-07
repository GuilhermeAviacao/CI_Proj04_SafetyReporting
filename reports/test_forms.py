"""
Test module for reports forms.
"""
from django.test import TestCase
from datetime import date, time
from .forms import SafetyReportForm, CommentForm


class SafetyReportFormTest(TestCase):
    """Test suite for SafetyReportForm"""

    def test_form_is_valid_with_all_required_fields(self):
        """Test that form is valid when all required fields are provided"""
        form = SafetyReportForm(data={
            'place': 'Test Airport',
            'date': date(2025, 1, 15),
            'time': time(14, 30),
            'description': 'Test safety incident description',
        })
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_without_place(self):
        """Test that form is invalid when place is missing"""
        form = SafetyReportForm(data={
            'date': date(2025, 1, 15),
            'time': time(14, 30),
            'description': 'Test safety incident description',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('place', form.errors)

    def test_form_is_invalid_without_date(self):
        """Test that form is invalid when date is missing"""
        form = SafetyReportForm(data={
            'place': 'Test Airport',
            'time': time(14, 30),
            'description': 'Test safety incident description',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_form_is_invalid_without_time(self):
        """Test that form is invalid when time is missing"""
        form = SafetyReportForm(data={
            'place': 'Test Airport',
            'date': date(2025, 1, 15),
            'description': 'Test safety incident description',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('time', form.errors)

    def test_form_is_invalid_without_description(self):
        """Test that form is invalid when description is missing"""
        form = SafetyReportForm(data={
            'place': 'Test Airport',
            'date': date(2025, 1, 15),
            'time': time(14, 30),
        })
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_form_is_valid_without_image(self):
        """Test that form is valid without image (optional field)"""
        form = SafetyReportForm(data={
            'place': 'Test Airport',
            'date': date(2025, 1, 15),
            'time': time(14, 30),
            'description': 'Test safety incident description',
        })
        self.assertTrue(form.is_valid())

    def test_form_fields(self):
        """Test that form has correct fields"""
        form = SafetyReportForm()
        expected_fields = ['place', 'date', 'time', 'description', 'image']
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_place_widget_has_correct_class(self):
        """Test that place widget has form-control class"""
        form = SafetyReportForm()
        self.assertIn('form-control', form.fields['place'].widget.attrs['class'])

    def test_date_widget_has_form_control_class(self):
        """Test that date widget has form-control class"""
        form = SafetyReportForm()
        self.assertIn('form-control', form.fields['date'].widget.attrs['class'])

    def test_time_widget_has_form_control_class(self):
        """Test that time widget has form-control class"""
        form = SafetyReportForm()
        self.assertIn('form-control', form.fields['time'].widget.attrs['class'])

    def test_description_widget_has_correct_rows(self):
        """Test that description widget has correct number of rows"""
        form = SafetyReportForm()
        self.assertEqual(form.fields['description'].widget.attrs['rows'], 8)


class CommentFormTest(TestCase):
    """Test suite for CommentForm"""

    def test_form_is_valid_with_content(self):
        """Test that form is valid when content is provided"""
        form = CommentForm(data={
            'content': 'This is a test comment',
        })
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_without_content(self):
        """Test that form is invalid when content is missing"""
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_form_is_invalid_with_empty_content(self):
        """Test that form is invalid when content is empty"""
        form = CommentForm(data={
            'content': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_form_fields(self):
        """Test that form has correct fields"""
        form = CommentForm()
        expected_fields = ['content']
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_content_label(self):
        """Test that content field has correct label"""
        form = CommentForm()
        self.assertEqual(form.fields['content'].label, "Add Comment")

    def test_content_widget_has_correct_class(self):
        """Test that content widget has form-control class"""
        form = CommentForm()
        self.assertIn('form-control', form.fields['content'].widget.attrs['class'])

    def test_content_widget_has_correct_rows(self):
        """Test that content widget has correct number of rows"""
        form = CommentForm()
        self.assertEqual(form.fields['content'].widget.attrs['rows'], 1)

    def test_content_is_required(self):
        """Test that content field is required"""
        form = CommentForm()
        self.assertTrue(form.fields['content'].required)
