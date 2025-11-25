"""
Test module for reports views.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, time
from .models import (SafetyReport,
                     Comment, UserProfile)


class AboutViewTest(TestCase):
    """Test suite for about view"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()

    def test_about_view_status_code(self):
        """Test that about view returns 200 status code"""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_about_view_uses_correct_template(self):
        """Test that about view uses correct template"""
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'reports/about.html')


class BoardViewTest(TestCase):
    """Test suite for board view"""

    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Create multiple reports for pagination testing
        for i in range(10):
            SafetyReport.objects.create(
                author=self.user,
                place=f'Airport {i}',
                date=date(2025, 1, 15),
                time=time(14, 30),
                description=f'Test description {i}'
            )

    def test_board_view_status_code(self):
        """Test that board view returns 200 status code"""
        response = self.client.get(reverse('board'))
        self.assertEqual(response.status_code, 200)

    def test_board_view_uses_correct_template(self):
        """Test that board view uses correct template"""
        response = self.client.get(reverse('board'))
        self.assertTemplateUsed(response, 'reports/board.html')

    def test_board_view_pagination(self):
        """Test that board view paginates results (6 per page)"""
        response = self.client.get(reverse('board'))
        self.assertTrue('page_obj' in response.context)
        self.assertEqual(len(response.context['page_obj']), 6)

    def test_board_view_search_functionality(self):
        """Test that board view search works correctly"""
        response = self.client.get(reverse('board'), {'search': 'Airport 5'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('search_query', response.context)


class ReportDetailViewTest(TestCase):
    """Test suite for report_detail view"""

    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.report = SafetyReport.objects.create(
            author=self.user,
            place='Test Airport',
            date=date(2025, 1, 15),
            time=time(14, 30),
            description='Test safety incident description'
        )

    def test_report_detail_view_status_code(self):
        """Test that report_detail view returns 200 status code"""
        response = self.client.get(
            reverse('report_detail', args=[self.report.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_report_detail_view_uses_correct_template(self):
        """Test that report_detail view uses correct template"""
        response = self.client.get(
            reverse('report_detail', args=[self.report.pk])
        )
        self.assertTemplateUsed(response, 'reports/report_detail.html')

    def test_report_detail_view_contains_report_data(self):
        """Test that report_detail view contains correct report data"""
        rresponse = self.client.get(
            reverse('report_detail', args=[self.report.pk])
        )
        self.assertEqual(response.context['report'], self.report)

    def test_report_detail_view_404_for_invalid_pk(self):
        """Test that report_detail view returns 404 for non-existent report"""
        response = self.client.get(reverse('report_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_sees_comment_form(self):
        """Test that authenticated users see the comment form"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('report_detail', args=[self.report.pk])
        )
        self.assertIsNotNone(response.context['comment_form'])

    def test_unauthenticated_user_no_comment_form(self):
        """Test that unauthenticated users don't see comment form"""
        response = self.client.get(
            reverse('report_detail', args=[self.report.pk])
        )
        self.assertIsNone(response.context['comment_form'])

    def test_post_comment_authenticated_user(self):
        """Test that authenticated users can post comments"""
        self.client.login(username='testuser', password='testpass123')
        self.client.post(
            reverse('report_detail', args=[self.report.pk]),
            {'content': 'Test comment'}
        )
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().content, 'Test comment')


class CreateReportViewTest(TestCase):
    """Test suite for create_report view"""

    def setUp(self):
        """Set up test client and test user"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_report_requires_login(self):
        """Test that create_report view requires authentication"""
        response = self.client.get(reverse('create_report'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_create_report_authenticated_status_code(self):
        """Test that authenticated users can access create_report view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('create_report'))
        self.assertEqual(response.status_code, 200)

    def test_create_report_uses_correct_template(self):
        """Test that create_report view uses correct template"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('create_report'))
        self.assertTemplateUsed(response, 'reports/create_report.html')

    def test_create_report_post_valid_data(self):
        """Test creating report with valid data"""
        self.client.login(username='testuser', password='testpass123')
        self.client.post(reverse('create_report'), {
            'place': 'Test Airport',
            'date': '2025-01-15',
            'time': '14:30',
            'description': 'Test safety incident description'
        })
        self.assertEqual(SafetyReport.objects.count(), 1)
        self.assertEqual(SafetyReport.objects.first().place, 'Test Airport')


class InvestigationsViewTest(TestCase):
    """Test suite for investigations view"""

    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Create reports with different statuses
        SafetyReport.objects.create(
            author=self.user,
            place='Airport 1',
            date=date(2025, 1, 15),
            time=time(14, 30),
            description='Test 1',
            investigation_status='waiting'
        )
        SafetyReport.objects.create(
            author=self.user,
            place='Airport 2',
            date=date(2025, 1, 15),
            time=time(14, 30),
            description='Test 2',
            investigation_status='investigating'
        )

    def test_investigations_view_status_code(self):
        """Test that investigations view returns 200 status code"""
        response = self.client.get(reverse('investigations'))
        self.assertEqual(response.status_code, 200)

    def test_investigations_view_uses_correct_template(self):
        """Test that investigations view uses correct template"""
        response = self.client.get(reverse('investigations'))
        self.assertTemplateUsed(response, 'reports/investigations.html')

    def test_investigations_view_contains_status_data(self):
        """Test that investigations view contains status statistics"""
        response = self.client.get(reverse('investigations'))
        self.assertIn('status_data', response.context)
        self.assertIn('status_percentages', response.context)
        self.assertIn('total_reports', response.context)
        self.assertEqual(response.context['total_reports'], 2)


class UpdateInvestigationStatusViewTest(TestCase):
    """Test suite for update_investigation_status view"""

    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        self.regular_user = User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='testpass123'
        )
        self.investigator_user = User.objects.create_user(
            username='investigator',
            email='investigator@example.com',
            password='testpass123'
        )
        # Set investigator role
        self.investigator_user.profile.role = 'investigator'
        self.investigator_user.profile.save()

        self.report = SafetyReport.objects.create(
            author=self.regular_user,
            place='Test Airport',
            date=date(2025, 1, 15),
            time=time(14, 30),
            description='Test description'
        )

    def test_update_status_requires_login(self):
        """Test that update status requires authentication"""
        response = self.client.post(
            reverse('update_investigation_status', args=[self.report.pk]),
            {'status': 'investigating'}
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_update_status_requires_investigator_role(self):
        """Test that only investigators can update status"""
        self.client.login(username='regularuser', password='testpass123')
        response = self.client.post(
            reverse('update_investigation_status', args=[self.report.pk]),
            {'status': 'investigating'}
        )
        self.assertEqual(response.status_code, 403)

    def test_update_status_investigator_can_update(self):
        """Test that investigators can update status"""
        self.client.login(username='investigator', password='testpass123')
        response = self.client.post(
            reverse('update_investigation_status', args=[self.report.pk]),
            {'status': 'investigating'}
        )
        self.assertEqual(response.status_code, 200)
        self.report.refresh_from_db()
        self.assertEqual(self.report.investigation_status, 'investigating')


class EditCommentViewTest(TestCase):
    """Test suite for edit_comment view"""

    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.report = SafetyReport.objects.create(
            author=self.user,
            place='Test Airport',
            date=date(2025, 1, 15),
            time=time(14, 30),
            description='Test description'
        )
        self.comment = Comment.objects.create(
            report=self.report,
            author=self.user,
            content='Original comment'
        )

    def test_edit_comment_requires_login(self):
        """Test that edit comment requires authentication"""
        response = self.client.get(
            reverse('edit_comment', args=[self.comment.pk])
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_edit_comment_only_author_can_edit(self):
        """Test that only comment author can edit"""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(
            reverse('edit_comment', args=[self.comment.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_edit_comment_author_can_edit(self):
        """Test that comment author can edit"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('edit_comment', args=[self.comment.pk])
        )
        self.assertEqual(response.status_code, 200)


class DeleteCommentViewTest(TestCase):
    """Test suite for delete_comment view"""

    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.report = SafetyReport.objects.create(
            author=self.user,
            place='Test Airport',
            date=date(2025, 1, 15),
            time=time(14, 30),
            description='Test description'
        )
        self.comment = Comment.objects.create(
            report=self.report,
            author=self.user,
            content='Test comment'
        )

    def test_delete_comment_requires_login(self):
        """Test that delete comment requires authentication"""
        response = self.client.get(
            reverse('delete_comment', args=[self.comment.pk])
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_delete_comment_only_author_can_delete(self):
        """Test that only comment author can delete"""
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(
            reverse('delete_comment', args=[self.comment.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_comment_author_can_delete(self):
        """Test that comment author can delete"""
        self.client.login(username='testuser', password='testpass123')
        self.client.post(
            reverse('delete_comment', args=[self.comment.pk])
        )
        self.assertEqual(Comment.objects.count(), 0)
