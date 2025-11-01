from fastmcp import FastMCP
from todo_db import TodoDB
from typing import Annotated, NamedTuple
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, 'tasks.json')

# Todo Class
class Todo(NamedTuple):
    filename: str
    text: str
    line_num: int


todo_db = TodoDB()
# todo_db.sample_data()

# Create the MCP server
mcp = FastMCP("TODO_MCP")

# Tools
@mcp.tool(
    name="tool_add_todos",
    description="Add a list of todos to the database",
)
def add_tools(
    todos: list[Todo]
):
    for todo in todos:
        todo_db.add(todo.filename, todo.text, todo.line_num)

    return len(todos)

@mcp.tool(
    name="tool_add_todo",
    description="Add a todo to the database",
)
def add_todo(
    filename: Annotated[str, "The filename of the file to add the todo to"],
    text: Annotated[str, "The text of the todo to add"],
    line_num: Annotated[int, "The line number of the todo to add"],
):
    return todo_db.add(filename, text, line_num)

def get_todo(
    filename: str,
):
    return todo_db.get(filename)

def delete_todo(
    filename: str,
):
    todo_db.delete_todos(filename)
    return "Todos deleted successfully"

# Resource
@mcp.resource(
    name="resource_todos_for_file",
    description="Get the todos for a file",
    uri="todo://{filename}/todos",
)
def get_todos_for_file(
    filename: Annotated[str, "Source file containing the #TODO"],
):
    todo = todo_db.get(filename)
    return [ text for text in todo.values() ]

# Start the MCP server
def main():
    mcp.run()

if __name__ == "__main__":
    run()
