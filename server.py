import os

from fastmcp import FastMCP

from tools import (
    marks_to_grade_points,
    calculate_semester_gpa,
    calculate_new_cgpa,
    required_gpa_for_target,
    get_semester_courses,
    get_remaining_credit_hours,
    save_report,
)

mcp = FastMCP("cgpa")

# Each plain Python function becomes an MCP tool: the docstring is the
# description the model reads, the type hints become the input schema.
for fn in (
    marks_to_grade_points,
    calculate_semester_gpa,
    calculate_new_cgpa,
    required_gpa_for_target,
    get_semester_courses,
    get_remaining_credit_hours,
    save_report,
):
    mcp.tool(fn)

if __name__ == "__main__":
    # Local: http://127.0.0.1:8000/mcp   Hosted (e.g. Render) sets PORT.
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "127.0.0.1")
    mcp.run(transport="http", host=host, port=port)
