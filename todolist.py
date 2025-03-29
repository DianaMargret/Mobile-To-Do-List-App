from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.properties import ObjectProperty

# Set window size for mobile-like appearance (you can adjust these values)
Window.size = (360, 640)

class TaskWidget(BoxLayout):
    def __init__(self, task_text, **kwargs):
        super(TaskWidget, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 40

        # Checkbox for task completion
        self.checkbox = CheckBox(size_hint_x=0.1)
        self.checkbox.bind(active=self.on_checkbox_active)
        
        # Task label
        self.task_label = Label(text=task_text, size_hint_x=0.7)
        
        # Delete button
        self.delete_btn = Button(text='X', size_hint_x=0.2)
        self.delete_btn.bind(on_press=self.delete_task)
        
        self.add_widget(self.checkbox)
        self.add_widget(self.task_label)
        self.add_widget(self.delete_btn)

    def on_checkbox_active(self, checkbox, value):
        if value:
            self.task_label.color = (0.5, 0.5, 0.5, 1)  # Gray out completed task
            self.task_label.text = f"[s]{self.task_label.text}[/s]"  # Strikethrough effect
        else:
            self.task_label.color = (1, 1, 1, 1)  # Return to normal color
            self.task_label.text = self.task_label.text.replace("[s]", "").replace("[/s]", "")

    def delete_task(self, instance):
        self.parent.remove_widget(self)

class TodoApp(App):
    def build(self):
        # Main layout
        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Input area
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        self.task_input = TextInput(hint_text='Enter a task...', multiline=False)
        add_button = Button(text='Add', size_hint_x=0.3)
        add_button.bind(on_press=self.add_task)
        
        input_layout.add_widget(self.task_input)
        input_layout.add_widget(add_button)
        
        # Scrollable task list
        self.task_list = BoxLayout(orientation='vertical', size_hint_y=None)
        self.task_list.bind(minimum_height=self.task_list.setter('height'))
        
        scroll_view = ScrollView()
        scroll_view.add_widget(self.task_list)
        
        # Add all components to root
        self.root.add_widget(input_layout)
        self.root.add_widget(scroll_view)
        
        return self.root

    def add_task(self, instance):
        if self.task_input.text.strip():
            task = TaskWidget(self.task_input.text)
            self.task_list.add_widget(task)
            self.task_input.text = ''  # Clear input field

if __name__ == '__main__':
    TodoApp().run()
