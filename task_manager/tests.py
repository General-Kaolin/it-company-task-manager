from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position, Task, TaskType, Worker


class ModelsTests(TestCase):
    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Bug")
        self.assertEqual(str(task_type), "Bug")

    def test_position_str(self):
        position = Position.objects.create(name="Developer")
        self.assertEqual(str(position), "Developer")

    def test_worker_str(self):
        worker = Worker.objects.create_user(
            username="test_worker",
            password="test12345",
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(str(worker), "test_worker (John Doe)")

    def test_task_str(self):
        task_type = TaskType.objects.create(name="Feature")
        task = Task.objects.create(
            name="Implement login",
            deadline="2026-12-31",
            task_type=task_type,
        )
        self.assertEqual(str(task), "Implement login")


class PrivateViewsTests(TestCase):
    """Views require login - test that unauthenticated users are redirected."""

    def test_task_list_login_required(self):
        response = self.client.get(reverse("task_manager:task-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_worker_list_login_required(self):
        response = self.client.get(reverse("task_manager:worker-list"))
        self.assertNotEqual(response.status_code, 200)


class LoggedInViewsTests(TestCase):
    def setUp(self):
        self.user = Worker.objects.create_user(
            username="test_user",
            password="test12345",
        )
        self.client.force_login(self.user)

    def test_task_list_view(self):
        response = self.client.get(reverse("task_manager:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "task_manager/tasks/task_list.html")

    def test_worker_list_view(self):
        response = self.client.get(reverse("task_manager:worker-list"))
        self.assertEqual(response.status_code, 200)

    def test_toggle_assign_task(self):
        task_type = TaskType.objects.create(name="Bug")
        task = Task.objects.create(
            name="Fix bug",
            deadline="2026-12-31",
            task_type=task_type,
        )
        self.assertNotIn(self.user, task.assignees.all())

        self.client.post(
            reverse("task_manager:toggle-task-assign", args=[task.id])
        )
        task.refresh_from_db()
        self.assertIn(self.user, task.assignees.all())
