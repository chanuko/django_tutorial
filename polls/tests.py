from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
import datetime

from .models import Question


# Create your tests here.


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_wuestions(self):
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "No polls are available")
        self.assertQuerysetEqual(
            res.context['latest_question_list'], []
        )

    def test_past_question(self):
        create_question(question_text='過去の質問', days=-30)
        res = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            res.context['latest_question_list'], ['<Question: 過去の質問>']
        )

    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        res = self.client.get(reverse('polls:index'))
        self.assertContains(res, "No polls are available.")
        self.assertQuerysetEqual(res.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        create_question(question_text="過去の質問", days=-30)
        create_question(question_text="未来の質問", days=30)
        res = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            res.context['latest_question_list'],
            ['<Question: 過去の質問>']
        )

    def test_two_past_questions(self):
        create_question(question_text="過去の質問１", days=-30)
        create_question(question_text="過去の質問２", days=-5)
        res = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            res.context['latest_question_list'],
            ['<Question: 過去の質問２>', '<Question: 過去の質問１>']
        )