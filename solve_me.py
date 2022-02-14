from http.server import BaseHTTPRequestHandler, HTTPServer
from jinja2 import Environment, FileSystemLoader


class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def recursion(self, key, value):
        key = int(key)
        if key in self.current_items.keys():
            self.recursion(key + 1, self.current_items[key])
        self.current_items[key] = value

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            for line in file.readlines():
                self.completed_items.append(line[:-1])

            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def runserver(self):
        address = "127.0.0.1"
        port = 8000
        server_address = (address, port)
        httpd = HTTPServer(server_address, TasksServer)
        print(f"Started HTTP Server on http://{address}:{port}")
        httpd.serve_forever()

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "runserver":
            self.runserver()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics
$ python tasks.py runserver # Starts the tasks management server"""
        )

    def add(self, args):
        if len(args) <= 1:
            print("Error: Missing tasks string. Nothing added!")
        else:
            self.recursion(args[0], args[1])
            print(f'Added task: "{args[1]}" with priority {args[0]}')
            self.write_current()

    def done(self, args):
        key = int(args[0])
        if key in self.current_items.keys():
            self.completed_items.append(self.current_items[key])
            self.current_items.pop(key)
            self.write_completed()
            self.write_current()
            print("Marked item as done.")
        else:
            print(f"Error: no incomplete item with priority {args[0]} exists.")

    def delete(self, args):
        key = int(args[0])
        if key in self.current_items.keys():
            self.current_items.pop(key)
            self.write_current()
            print(f"Deleted item with priority {args[0]}")
        else:
            print(
                f"Error: item with priority {args[0]} does not exist. Nothing deleted."
            )

    def pending_tasks(self):
        pending = ""
        index = 1
        for key in sorted(self.current_items.keys()):
            pending += f"{index}. {self.current_items[key]} [{key}]\n"
            index = index + 1
        return pending

    def completed_tasks(self):
        completed = ""
        index = 1
        for value in self.completed_items:
            completed += f"{index}. {value}\n"
            index = index + 1
        return completed

    def ls(self):
        print(self.pending_tasks())

    def report(self):
        print(f"Pending : {len(self.current_items)}")
        print(self.pending_tasks())
        print(f"\nCompleted : {len(self.completed_items)}")
        print(self.completed_tasks())

    def jinjaloader(self, file):
        file_loader = FileSystemLoader("templates")
        env = Environment(loader=file_loader)
        template = env.get_template(file)
        return template

    def render_pending_tasks(self):
        pending = self.pending_tasks()
        template = self.jinjaloader("pending.html")
        output = template.render(pending=pending, len=len(self.current_items))
        return output

    def render_completed_tasks(self):
        completed = self.completed_tasks()
        template = self.jinjaloader("completed.html")
        output = template.render(completed=completed, len=len(self.completed_items))
        return output


class TasksServer(TasksCommand, BaseHTTPRequestHandler):
    def do_GET(self):
        task_command_object = TasksCommand()
        if self.path == "/tasks":
            content = task_command_object.render_pending_tasks()
        elif self.path == "/completed":
            content = task_command_object.render_completed_tasks()
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())
