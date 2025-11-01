from fastmcp import FastMCP
from todo_db import TodoDB
from typing import Annotated


todo_db = TodoDB()
todo_db.sample_data()

# Create the MCP server
mcp = FastMCP("TODO_MCP")

# Tools
@mcp.tool(
    name="tool_add_tood",
    description="Add a todo to the database",
)
def add_tool(
    filename: Annotated[str, "The filename of the file to add the todo to"],
    text: Annotated[str, "The text of the todo to add"],
    line_num: Annotated[int, "The line number of the todo to add"],
):
    return todo_db.add(filename, text, line_num)

def get_tool(
    filename: str,
):
    return todo_db.get(filename)

def delete_tool(
    filename: str,
):
    todo_db.delete_todos(filename)
    return "Todos deleted successfully"

# Resource
@mcp.resource(
    name="resource_todos_for_file",
    description="Get the todos for a file",
)
def get_todos_for_file(
    filename: Annotated[str, "Source file containing the #TODO"],
):
    todo = todo_db.get(filename)
    return [ text for text in todo.values() ]

# Start the MCP server
def run():
    mcp.run()

if __name__ == "__main__":
    run()
