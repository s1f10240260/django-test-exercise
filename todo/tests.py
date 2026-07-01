from django.test import TestCase, Client
from django.utils import timezone
from datetime import datetime
from todo.models import Task

# Create your tests here.
class SampleTestCase(TestCase):
    def test_sample(self):
        self.assertEqual(1 + 2, 3)

class TaskModelTestCase(TestCase):
    def test_create_task1(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        task = Task(title='task1', due_at=due)
        task.save()

        task = Task.objects.get(pk=task.pk)
        self.assertEqual(task.title, 'task1')
        self.assertFalse(task.completed)
        self.assertEqual(task.due_at, due)

    def test_create_task2(self):
        task = Task(title='task2')
        task.save()

        task = Task.objects.get(pk=task.pk)
        self.assertEqual(task.title, 'task2')
        self.assertFalse(task.completed)
        self.assertEqual(task.due_at, None)

    def test_is_overdue_future(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        current = timezone.make_aware(datetime(2024, 6, 30, 0, 0, 0))
        task = Task(title='task1', due_at=due)
        task.save()

        self.assertFalse(task.is_overdue(current))

    def test_is_overdue_past(self):
        due = timezone.make_aware(datetime(2024, 6, 30, 23, 59, 59))
        current = timezone.make_aware(datetime(2024, 7, 1, 0, 0, 0))
        task = Task(title='task1', due_at=due)
        task.save()

        self.assertTrue(task.is_overdue(current))

    def test_is_overdue_none(self):
        current = timezone.make_aware(datetime(2024, 7, 1, 0, 0, 0))
        task = Task(title='task2')
        task.save()

        self.assertFalse(task.is_overdue(current))

class CreateTaskViewTestCase(TestCase):
    def test_status_code_200(self):
        response = self.client.get('/todo/')
        self.assertEqual(response.status_code, 200)

    def test_task_create_form_in_context(self):
        response = self.client.get('/todo/')
        self.assertIn('tasks', response.context)

    def test_task_create_post(self):
        response = self.client.post('/todo/', {'title': 'task1', 'due_at': '2024-06-30T23:59:59'})
        self.assertEqual(response.status_code, 302)

    def test_task_create_redirect(self):
        response = self.client.post('/todo/', {'title': 'task1', 'due_at': '2024-06-30T23:59:59'})
        self.assertRedirects(response, '/todo/')

class TodoViewTestCase(TestCase):
    def test_index_get_three_content(self):
        task1 = Task(title='task1', due_at=timezone.make_aware(datetime(2023, 7, 1)))
        task1.save()
        task2 = Task(title='task2', due_at=timezone.make_aware(datetime(2023, 8, 1)))
        task2.save()
        task3 = Task(title='task3', due_at=timezone.make_aware(datetime(2023, 9, 1)))
        task3.save()
        client = Client()
        response = client.get('/todo/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'todo/index.html')
        self.assertEqual(len(response.context['tasks']), 3)
        self.assertEqual(response.context['tasks'][0], task1)
        self.assertEqual(response.context['tasks'][1], task2)
        self.assertEqual(response.context['tasks'][2], task3)