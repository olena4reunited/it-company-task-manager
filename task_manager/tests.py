import datetime
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from task_manager.models import Task, TaskType, Position
from task_manager.forms import TaskForm, WorkerCreationForm

User = get_user_model()


class TaskManagerModelTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Bug Fix")
        self.task = Task.objects.create(
            name="Test Task",
            description="This is a test task",
            deadline=timezone.now().date() + datetime.timedelta(days=7),
            task_type=self.task_type,
            created_by=self.user
        )
        self.task.assignees.add(self.user)

    def test_task_creation(self):
        self.assertEqual(self.task.name, "Test Task")
        self.assertFalse(self.task.is_completed)
        self.assertEqual(self.task.priority, "medium")

    def test_task_str_representation(self):
        self.assertEqual(str(self.task), "Task object (1)")

    def test_task_type_str_representation(self):
        self.assertEqual(str(self.task_type), "Bug Fix")

    def test_worker_str_representation(self):
        self.assertEqual(str(self.user), " ")


class TaskManagerViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.position = Position.objects.create(name="Manager")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Feature")
        self.task = Task.objects.create(
            name="View Test Task",
            description="This is a test task for view testing",
            deadline=timezone.now().date() + datetime.timedelta(days=14),
            task_type=self.task_type,
            created_by=self.user
        )
        self.task.assignees.add(self.user)

    def test_index_view(self):
        response = self.client.get(reverse('task-manager:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/index.html')

    def test_task_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task-manager:user-tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test Task")
        self.assertTemplateUsed(response, 'task_manager/user_task_list.html')

    def test_task_detail_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task-manager:task-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Test Task")
        self.assertTemplateUsed(response, 'task_manager/task_detail.html')

    def test_task_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task-manager:task-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/task_form.html')

        task_data = {
            'name': 'New Task',
            'description': 'This is a new task',
            'deadline': timezone.now().date() + datetime.timedelta(days=7),
            'task_type': self.task_type.id,
            'assignees': [self.user.id],
            'priority': 'high'
        }
        response = self.client.post(reverse('task-manager:task-create'), data=task_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task-manager:task-update', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/task_form.html')

        updated_data = {
            'name': 'Updated Task',
            'description': 'This task has been updated',
            'deadline': timezone.now().date() + datetime.timedelta(days=10),
            'task_type': self.task_type.id,
            'assignees': [self.user.id],
            'priority': 'low'
        }
        response = self.client.post(reverse('task-manager:task-update', args=[self.task.id]), data=updated_data)
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')
        self.assertEqual(self.task.priority, 'low')

    def test_task_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task-manager:task-delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/task_confirm_delete.html')

        # Test POST request
        response = self.client.post(reverse('task-manager:task-delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


class TaskManagerFormTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Tester")
        self.user = User.objects.create_user(
            username="formtestuser",
            password="formtestpass123",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Testing")

    def test_task_form_valid_data(self):
        form_data = {
            'name': 'Form Test Task',
            'description': 'This is a task created in a form test',
            'deadline': timezone.now().date() + datetime.timedelta(days=5),
            'task_type': self.task_type.id,
            'assignees': [self.user.id],
            'priority': 'high'
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid_data(self):
        form_data = {
            'name': '',
            'description': 'This is an invalid task',
            'deadline': timezone.now().date() - datetime.timedelta(days=1),
            'task_type': self.task_type.id,
            'assignees': [self.user.id],
            'priority': 'invalid_priority'
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('deadline', form.errors)
        self.assertIn('priority', form.errors)

    def test_worker_creation_form_valid_data(self):
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'position': self.position.id,
            'password1': 'testpass123',
            'password2': 'testpass123'
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_creation_form_invalid_data(self):
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'invalid_email',
            'position': self.position.id,
            'password1': 'testpass123',
            'password2': 'differentpass123'
        }
        form = WorkerCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('password2', form.errors)


class TaskManagerIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.position = Position.objects.create(name="Integration Tester")
        self.user = User.objects.create_user(
            username="integrationuser",
            password="integrationpass123",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Integration")

    def test_task_lifecycle(self):
        self.client.login(username='integrationuser', password='integrationpass123')

        task_data = {
            'name': 'Integration Test Task',
            'description': 'This task tests the entire lifecycle',
            'deadline': timezone.now().date() + datetime.timedelta(days=3),
            'task_type': self.task_type.id,
            'assignees': [self.user.id],
            'priority': 'high'
        }
        response = self.client.post(reverse('task-manager:task-create'), data=task_data)
        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(name='Integration Test Task')
        self.assertIsNotNone(task)

        update_data = {
            'name': 'Updated Integration Task',
            'description': 'This task has been updated',
            'deadline': timezone.now().date() + datetime.timedelta(days=5),
            'task_type': self.task_type.id,
            'assignees': [self.user.id],
            'priority': 'medium'
        }
        response = self.client.post(reverse('task-manager:task-update', args=[task.id]), data=update_data)
        self.assertEqual(response.status_code, 302)

        task.refresh_from_db()
        self.assertEqual(task.name, 'Updated Integration Task')
        self.assertEqual(task.priority, 'medium')

        response = self.client.post(reverse('task-manager:task-detail', args=[task.id]))
        self.assertEqual(response.status_code, 302)

        task.refresh_from_db()
        self.assertTrue(task.is_completed)

        response = self.client.post(reverse('task-manager:task-delete', args=[task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=task.id).exists())
