# Rule-Engine-Application

## Overview
This Flask Rule Engine is a lightweight web application that evaluates user eligibility based on predefined rules. It uses Abstract Syntax Trees (ASTs) to represent and manipulate logical rules. This project allows users to:

- Create, modify, and combine rules.
- Evaluate data against these rules.
- Potentially extend the engine with user-defined functions for advanced conditions.

## Features
**Create rules**: Define rules like age >= 18 AND income >= 30000.
**Modify rules**: Change operators or operands in existing rules.
**Combine rules**: Merge multiple rules logically using AND/OR.
**Evaluate data**: Check if the input data matches the rules.
**Future extension**: Supports user-defined functions for advanced conditions.

## Requirements
Make sure your system has the following installed:

- Python 3.x: Download from python.org.
- pip: Comes bundled with Python, but can be installed via:
  python -m ensurepip
- Git: Install from git-scm.com.
- Virtualenv (Optional but recommended): To manage project dependencies.

## Setup
1. **Clone the Repository:**
   - git clone https://github.com/spriyanshi407/flask-rule-engine.git
   - cd flask-rule-engine
2. **Create Virtual Environment**
    - python -m venv venv
    - source venv/bin/activate   # On macOS/Linux
    - venv\Scripts\activate      # On Windows
3. pip install Flask Flask-CORS
4. set FLASK_APP=app.py
5. set FLASK_ENV=development
6. flask run

## Usage
1. **Add a New Rule:**
Navigate to the UI at http://localhost:5000.
Enter rules like:
age >= 18 AND income >= 30000
Click Create Rule to add the rule.
2. **Modify a Rule:**
Provide the rule index, modification type (operator/operand), and the new value.
Example:
Change operator from AND to OR.
Update operand from age >= 18 to age >= 21.
3. **Combine Rules:**
Combine multiple rules logically with the AND/OR operator.
4. **Evaluate Data Against Rules:**
**Input sample data:**
{
  "age": 40,
  "department": "sales",
  "income": 30000,
  "spend": 1500
}
Get a result indicating whether the data satisfies the rules.

## How It Works
**Abstract Syntax Tree (AST)**:
Each rule is represented as a tree with nodes for operands (like age >= 18) and operators (like AND).

**Adding Rules:**
When a rule is created, it is converted into an AST node and stored in memory.

**Modifying Rules:**
Users can change operators or operand values within the AST to reflect new rules.

**Combining Rules:**
Multiple rules are merged into a single AST with logical operators like AND/OR.

**Evaluating Rules:**
The rules are evaluated against input data using Python's eval function, but variable values are substituted with the actual data before execution.

## Future Enhancements
**User-Defined Functions:**
In the future, users can define custom functions to extend rule logic.

**Database Integration:**
Store rules in a database for better persistence and scalability.

**Authentication:**
Add user authentication for secure rule management.

## Contributing
Feel free to fork the repository and submit pull requests. Contributions are always welcome!
