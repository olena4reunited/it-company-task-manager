from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.forms import TaskForm, WorkerCreationForm
from task_manager.models import TaskType, Position, Worker, Task
from django.utils import timezone


class TaskManagerModelsTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="testuser",
            password="testpass",
            first_name="First",
            last_name="Last",
            email="test@example.com",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Development")
        self.task = Task.objects.create(
            name="Test Task",
            description="This is a test task.",
            deadline=timezone.now().date(),
            task_type=self.task_type,
            created_by=self.worker
        )

    def test_task_creation(self):
        self.assertEqual(self.task.name, "Test Task")
        self.assertEqual(self.task.created_by, self.worker)
        self.assertEqual(self.task.task_type, self.task_type)

    def test_position_str(self):
        self.assertEqual(str(self.position), "Developer")

    def test_worker_str(self):
        self.assertEqual(str(self.worker), "First Last")

    def test_task_type_str(self):
        self.assertEqual(str(self.task_type), "Development")



class TaskManagerFormsTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="testuser",
            password="testpass",
            first_name="First",
            last_name="Last",
            email="test@example.com",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Development")

    def test_task_form_valid(self):
        form_data = {
            'name': 'New Task',
            'description': 'A new task description.',
            'deadline': timezone.now().date(),
            'task_type': self.task_type.id,
            'assignees': [self.worker.id]
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_worker_creation_form_valid(self):
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


class TaskManagerViewsTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create_user(
            username="testuser",
            password="testpass",
            first_name="First",
            last_name="Last",
            email="test@example.com",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Development")
        self.task = Task.objects.create(
            name="Test Task",
            description="This is a test task.",
            deadline=timezone.now().date(),
            task_type=self.task_type,
            created_by=self.worker
        )

    def test_task_detail_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('task-manager:task-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/task_detail.html')
        self.assertContains(response, self.task.name)

    def test_task_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task-manager:task-update', args=[self.task.id]), {
            'name': 'Updated Task',
            'description': 'Updated description.',
            'deadline': timezone.now().date(),
            'task_type': self.task_type.id,
            'assignees': [self.worker.id]
        })
        self.task.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task-manager:task-delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after delete
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_worker_detail_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('task-manager:worker-detail', args=[self.worker.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/worker_detail.html')
        self.assertContains(response, self.worker.username)

    def test_worker_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task-manager:worker-update', args=[self.worker.id]), {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com',
            'position': self.position.id
        })
        self.worker.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.worker.username, 'updateduser')

    def test_worker_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('task-manager:worker-delete', args=[self.worker.id]))
        self.assertEqual(response.status_code, 403)

    def test_unauthorized_access(self):
        response = self.client.get(reverse('task-manager:task-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('task-manager:worker-detail', args=[self.worker.id]))
        self.assertEqual(response.status_code, 302)


class TaskManagerAdminTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.client.login(username='admin', password='adminpass')
        self.position = Position.objects.create(name="Developer")
        self.task_type = TaskType.objects.create(name="Development")

    def test_admin_task_type_list(self):
        response = self.client.get(reverse('admin:task_manager_tasktype_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task types")

    def test_admin_position_list(self):
        response = self.client.get(reverse('admin:task_manager_position_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Positions")
