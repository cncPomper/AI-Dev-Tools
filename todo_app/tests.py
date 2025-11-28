from django.test import TestCase, Client
from django.urls import reverse
from .models import Todo
from datetime import date, timedelta
from django.utils import timezone

class TodoModelTests(TestCase):
    def test_create_todo_item(self):
        """
        Tests that a Todo item can be created and saved.
        """
        todo = Todo.objects.create(
            title="Buy groceries",
            description="Milk, eggs, bread",
            due_date=date.today() + timedelta(days=7),
            resolved=False
        )
        self.assertEqual(todo.title, "Buy groceries")
        self.assertEqual(todo.description, "Milk, eggs, bread")
        self.assertEqual(todo.due_date, date.today() + timedelta(days=7))
        self.assertFalse(todo.resolved)
        self.assertIsNotNone(todo.created_at)

    def test_todo_default_values(self):
        """
        Tests that 'resolved' defaults to False and 'created_at' is set automatically.
        """
        todo = Todo.objects.create(title="Default Check")
        self.assertFalse(todo.resolved)
        self.assertIsNotNone(todo.created_at)
        self.assertIsNone(todo.due_date)
        self.assertIsNone(todo.description)

    def test_todo_string_representation(self):
        """
        Tests the string representation of a Todo object.
        """
        todo = Todo.objects.create(title="Test String Repr")
        self.assertEqual(str(todo), "Test String Repr")


class TodoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo1 = Todo.objects.create(
            title="Task 1",
            description="Description for Task 1",
            due_date=date.today() + timedelta(days=1),
            resolved=False
        )
        self.todo2 = Todo.objects.create(
            title="Task 2",
            description="Description for Task 2",
            due_date=date.today() + timedelta(days=5),
            resolved=True
        )
        self.todo_list_url = reverse('todo_app:todo_list')
        self.todo_create_url = reverse('todo_app:todo_create')
        self.todo_detail_url = reverse('todo_app:todo_detail', args=[self.todo1.pk])
        self.todo_edit_url = reverse('todo_app:todo_edit', args=[self.todo1.pk])
        self.todo_delete_url = reverse('todo_app:todo_delete', args=[self.todo1.pk])
        self.todo_toggle_resolved_url = reverse('todo_app:todo_toggle_resolved', args=[self.todo1.pk])

    # --- Todo List View Tests ---
    def test_todo_list_display_all_todos(self):
        """
        The todo_list view should display all existing TODOs.
        """
        response = self.client.get(self.todo_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/todo_list.html')
        self.assertContains(response, self.todo1.title)
        self.assertContains(response, self.todo2.title)
        self.assertQuerySetEqual(response.context['todos'], [self.todo2, self.todo1], ordered=False) # Ordered by created_at desc

    def test_todo_list_no_todos_exist(self):
        """
        The todo_list view should display a message when no TODOs exist.
        """
        Todo.objects.all().delete() # Delete existing todos
        response = self.client.get(self.todo_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No TODOs yet. Start by creating one!")
        self.assertQuerySetEqual(response.context['todos'], [])

    # --- Todo Create View Tests ---
    def test_todo_create_get_request(self):
        """
        GET request to todo_create should render the form.
        """
        response = self.client.get(self.todo_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/todo_form.html')
        self.assertContains(response, "Create New Todo")

    def test_todo_create_post_valid_data(self):
        """
        POST request with valid data should create a new TODO and redirect.
        """
        new_todo_data = {
            'title': 'New Valid Task',
            'description': 'This is a new task.',
            'due_date': date.today().isoformat(),
            # 'resolved': 'off' # Checkbox typically sends 'on' or nothing for unchecked
        }
        response = self.client.post(self.todo_create_url, new_todo_data, follow=True)
        self.assertRedirects(response, self.todo_list_url)
        self.assertEqual(Todo.objects.count(), 3)
        new_todo = Todo.objects.get(title='New Valid Task')
        self.assertEqual(new_todo.description, 'This is a new task.')
        self.assertEqual(new_todo.due_date, date.today())
        self.assertFalse(new_todo.resolved)

    def test_todo_create_post_invalid_data(self):
        """
        POST request with invalid data should not create a TODO and show form errors.
        """
        invalid_todo_data = {
            'title': '', # Title is required
            'description': 'This task has no title.',
            'due_date': '2023-02-30', # Invalid date
        }
        response = self.client.post(self.todo_create_url, invalid_todo_data)
        self.assertEqual(response.status_code, 200) # Form re-rendered with errors
        self.assertTemplateUsed(response, 'todo_app/todo_form.html')
        self.assertContains(response, "This field is required.")
        self.assertContains(response, "Enter a valid date.")
        self.assertEqual(Todo.objects.count(), 2) # No new todo created

    # --- Todo Detail View Tests ---
    def test_todo_detail_display_existing_todo(self):
        """
        The todo_detail view should display details for an existing TODO.
        """
        response = self.client.get(self.todo_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/todo_detail.html')
        self.assertContains(response, self.todo1.title)
        self.assertContains(response, self.todo1.description)
        self.assertContains(response, "Pending") # self.todo1.resolved is False

    def test_todo_detail_non_existent_todo_returns_404(self):
        """
        Requesting details for a non-existent TODO should return a 404.
        """
        response = self.client.get(reverse('todo_app:todo_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    # --- Todo Edit View Tests ---
    def test_todo_edit_get_request(self):
        """
        GET request to todo_edit should render the form pre-filled with existing data.
        """
        response = self.client.get(self.todo_edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/todo_form.html')
        self.assertContains(response, self.todo1.title)
        self.assertContains(response, self.todo1.description)
        self.assertContains(response, "Edit Todo")

    def test_todo_edit_post_valid_data(self):
        """
        POST request with valid data should update the TODO and redirect.
        """
        updated_data = {
            'title': 'Updated Task 1',
            'description': 'Updated description.',
            'due_date': (date.today() + timedelta(days=10)).isoformat(),
            'resolved': 'on'
        }
        response = self.client.post(self.todo_edit_url, updated_data, follow=True)
        self.assertRedirects(response, self.todo_list_url)
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, 'Updated Task 1')
        self.assertEqual(self.todo1.description, 'Updated description.')
        self.assertTrue(self.todo1.resolved)

    def test_todo_edit_post_invalid_data(self):
        """
        POST request with invalid data should not update the TODO and show errors.
        """
        original_title = self.todo1.title
        invalid_data = {
            'title': '', # Title is required
            'description': 'Still the same description',
            'due_date': date.today().isoformat(),
        }
        response = self.client.post(self.todo_edit_url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/todo_form.html')
        self.assertContains(response, "This field is required.")
        self.todo1.refresh_from_db()
        self.assertEqual(self.todo1.title, original_title) # Title should not have changed

    def test_todo_edit_non_existent_todo_returns_404(self):
        """
        Attempting to edit a non-existent TODO should return a 404.
        """
        response = self.client.get(reverse('todo_app:todo_edit', args=[999]))
        self.assertEqual(response.status_code, 404)

    # --- Todo Delete View Tests ---
    def test_todo_delete_get_request(self):
        """
        GET request to todo_delete should render the confirmation page.
        """
        response = self.client.get(self.todo_delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_app/todo_confirm_delete.html')
        self.assertContains(response, f"Are you sure you want to delete \"{self.todo1.title}\"")

    def test_todo_delete_post_request(self):
        """
        POST request should delete the TODO and redirect.
        """
        response = self.client.post(self.todo_delete_url, follow=True)
        self.assertRedirects(response, self.todo_list_url)
        self.assertEqual(Todo.objects.count(), 1) # Only todo2 should remain
        self.assertFalse(Todo.objects.filter(pk=self.todo1.pk).exists())

    def test_todo_delete_non_existent_todo_returns_404(self):
        """
        Attempting to delete a non-existent TODO should return a 404.
        """
        response = self.client.post(reverse('todo_app:todo_delete', args=[999]))
        self.assertEqual(response.status_code, 404)

    # --- Todo Toggle Resolved View Tests ---
    def test_todo_toggle_resolved_to_true(self):
        """
        Toggling an unresolved TODO should mark it as resolved.
        """
        self.assertFalse(self.todo1.resolved)
        response = self.client.post(self.todo_toggle_resolved_url, follow=True)
        self.assertRedirects(response, self.todo_list_url)
        self.todo1.refresh_from_db()
        self.assertTrue(self.todo1.resolved)

    def test_todo_toggle_resolved_to_false(self):
        """
        Toggling a resolved TODO should mark it as unresolved.
        """
        self.assertTrue(self.todo2.resolved)
        toggle_url = reverse('todo_app:todo_toggle_resolved', args=[self.todo2.pk])
        response = self.client.post(toggle_url, follow=True)
        self.assertRedirects(response, self.todo_list_url)
        self.todo2.refresh_from_db()
        self.assertFalse(self.todo2.resolved)

    def test_todo_toggle_resolved_non_existent_todo_returns_404(self):
        """
        Attempting to toggle a non-existent TODO should return a 404.
        """
        response = self.client.post(reverse('todo_app:todo_toggle_resolved', args=[999]))
        self.assertEqual(response.status_code, 404)
