"""
Test module for reports models.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date, time
from .models import UserProfile, SafetyReport, Comment


class UserProfileModelTest(TestCase):
    """Test suite for UserProfile model"""

    def setUp(self):
        """Set up test user and profile"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_profile_creation(self):
        """Test UserProfile creation when User is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)

    def test_user_profile_str(self):
        """Test the string representation of UserProfile"""
        expected = f"{self.user.email} - Regular User"
        self.assertEqual(str(self.user.profile), expected)

    def test_default_role_is_regular(self):
        """Test that default role is 'regular'"""
        self.assertEqual(self.user.profile.role, 'regular')

    def test_is_investigator_method_regular_user(self):
        """Test is_investigator returns False for regular user"""
        self.assertFalse(self.user.profile.is_investigator())

    def test_is_investigator_method_investigator_user(self):
        """Test is_investigator returns True for investigator"""
        self.user.profile.role = 'investigator'
        self.user.profile.save()
        self.assertTrue(self.user.profile.is_investigator())

    def test_is_investigator_method_admin_user(self):
        """Test is_investigator returns True for admin"""
        self.user.profile.role = 'admin'
        self.user.profile.save()
        self.assertTrue(self.user.profile.is_investigator())

    def test_is_admin_method_regular_user(self):
        """Test is_admin returns False for regular user"""
        self.assertFalse(self.user.profile.is_admin())

    def test_is_admin_method_investigator_user(self):
        """Test is_admin returns False for investigator"""
        self.user.profile.role = 'investigator'
        self.user.profile.save()
        self.assertFalse(self.user.profile.is_admin())

    def test_is_admin_method_admin_user(self):
        """Test is_admin returns True for admin"""
        self.user.profile.role = 'admin'
        self.user.profile.save()
        self.assertTrue(self.user.profile.is_admin())


class SafetyReportModelTest(TestCase):
    """Test suite for SafetyReport model"""

    def setUp(self):
        """Set up test user and safety report"""
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

    def test_safety_report_creation(self):
        """Test that SafetyReport is created successfully"""
        self.assertIsInstance(self.report, SafetyReport)
        self.assertEqual(self.report.author, self.user)

    def test_safety_report_str(self):
        """Test the string representation of SafetyReport"""
        expected = "Safety Report - Test Airport on 2025-01-15"
        self.assertEqual(str(self.report), expected)

    def test_default_investigation_status(self):
        """Test that default investigation status is 'waiting'"""
        self.assertEqual(self.report.investigation_status, 'waiting')

    def test_get_status_color_waiting(self):
        """Test get_status_color for waiting status"""
        self.assertEqual(self.report.get_status_color(), 'primary')

    def test_get_status_color_investigating(self):
        """Test get_status_color for investigating status"""
        self.report.investigation_status = 'investigating'
        self.assertEqual(self.report.get_status_color(), 'warning')

    def test_get_status_color_closed(self):
        """Test get_status_color for closed status"""
        self.report.investigation_status = 'closed'
        self.assertEqual(self.report.get_status_color(), 'secondary')

    def test_get_status_color_dismissed(self):
        """Test get_status_color for dismissed status"""
        self.report.investigation_status = 'dismissed'
        self.assertEqual(self.report.get_status_color(), 'dark')

    def test_get_status_icon_waiting(self):
        """Test get_status_icon for waiting status"""
        self.assertEqual(self.report.get_status_icon(), 'fas fa-clock')

    def test_get_status_icon_investigating(self):
        """Test get_status_icon for investigating status"""
        self.report.investigation_status = 'investigating'
        self.assertEqual(self.report.get_status_icon(), 'fas fa-search')

    def test_get_status_icon_closed(self):
        """Test get_status_icon for closed status"""
        self.report.investigation_status = 'closed'
        self.assertEqual(self.report.get_status_icon(), 'fas fa-check-circle')

    def test_get_status_icon_dismissed(self):
        """Test get_status_icon for dismissed status"""
        self.report.investigation_status = 'dismissed'
        self.assertEqual(self.report.get_status_icon(), 'fas fa-times-circle')

    def test_get_absolute_url(self):
        """Test get_absolute_url returns correct URL"""
        expected_url = f'/report/{self.report.pk}/'
        self.assertEqual(self.report.get_absolute_url(), expected_url)

    def test_reports_ordering(self):
        """Test that reports are ordered by created_at descending"""
        report2 = SafetyReport.objects.create(
            author=self.user,
            place='Second Airport',
            date=date(2025, 1, 16),
            time=time(15, 30),
            description='Second test description'
        )
        reports = SafetyReport.objects.all()
        self.assertEqual(reports[0], report2)
        self.assertEqual(reports[1], self.report)


class CommentModelTest(TestCase):
    """Test suite for Comment model"""

    def setUp(self):
        """Set up test user, report, and comment"""
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
        self.comment = Comment.objects.create(
            report=self.report,
            author=self.user,
            content='Test comment content'
        )

    def test_comment_creation(self):
        """Test that Comment is created successfully"""
        self.assertIsInstance(self.comment, Comment)
        self.assertEqual(self.comment.report, self.report)
        self.assertEqual(self.comment.author, self.user)

    def test_comment_str(self):
        """Test the string representation of Comment"""
        expected = f"Comment by {self.user.email} on Test Airport"
        self.assertEqual(str(self.comment), expected)

    def test_comment_related_to_report(self):
        """Test that comment is properly related to report"""
        self.assertIn(self.comment, self.report.comments.all())

    def test_comments_ordering(self):
        """Test that comments are ordered by created_at ascending"""
        comment2 = Comment.objects.create(
            report=self.report,
            author=self.user,
            content='Second test comment'
        )
        comments = self.report.comments.all()
        self.assertEqual(comments[0], self.comment)
        self.assertEqual(comments[1], comment2)
