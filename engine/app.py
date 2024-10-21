from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Home route to render the HTML UI
@app.route('/')
def home():
    return render_template('index.html')

# Node class for the Abstract Syntax Tree (AST)
class Node:
    def __init__(self, type: str, left: 'Node' = None, right: 'Node' = None, value: str = None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

    def to_dict(self):
        return {
            "type": self.type,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
            "value": self.value
        }

    def update_value(self, new_value: str):
        """Update the value of the node."""
        self.value = new_value

    def replace_child(self, child: 'Node', new_child: 'Node'):
        """Replace a child node with a new child node."""
        if self.left == child:
            self.left = new_child
        elif self.right == child:
            self.right = new_child

    def change_operator(self, new_operator: str):
        if self.type == "operator":
            self.update_value(new_operator)
        else:
            raise ValueError("Node is not an operator")

    def update_operand(self, new_value: str):
        if self.type == "operand":
            self.update_value(new_value)
        else:
            raise ValueError("Node is not an operand")

# Global variable to store rules (ASTs)
rules = []

def ast_to_expression(node):
    """Convert an AST node into a valid Python logical expression."""
    if node.type == "operand":
        return node.value  # Example: 'age >= 18'
    
    elif node.type == "operator":
        # Recursively convert left and right nodes to expressions
        left_expr = ast_to_expression(node.left)
        right_expr = ast_to_expression(node.right)
        
        # Combine them using the operator
        return f"({left_expr} and {right_expr})"

    raise ValueError("Invalid node type")

def create_rule(rule_string: str) -> Node:
    rule_string = rule_string.replace("AND", "and").replace("OR", "or")
    return Node("operand", value=rule_string)

@app.route('/rules', methods=['POST'])
def add_rule():
    """Add a new rule to the rules list."""
    data = request.json
    rule_string = data.get('rule')

    if not rule_string:
        return jsonify({"error": "No rule provided"}), 400

    # Create an AST for the rule
    ast = create_rule(rule_string)
    rules.append(ast)  # Store the rule AST

    return jsonify({"message": "Rule created", "AST": ast.to_dict()}), 201

@app.route('/combine', methods=['POST'])
def combine_rules():
    """Combine two or more rules using an AND operator."""
    if len(rules) < 2:
        return jsonify({"error": "At least two rules are required to combine"}), 400

    try:
        # Combine all rules into a single AST
        combined_ast = combine_all_rules(rules)
        rules.append(combined_ast)  # Store the combined AST

        return jsonify({
            "message": "Rules combined successfully!",
            "combined_rule": combined_ast.to_dict()
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def combine_all_rules(rules):
    """Combine multiple rules into a balanced AST."""
    # Base case: If only one rule, return it directly
    if len(rules) == 1:
        return rules[0]  # Rule is already an AST node

    # Split the rules into two halves to form a balanced tree
    mid = len(rules) // 2

    # Recursive calls for left and right subtrees
    left_ast = combine_all_rules(rules[:mid])
    right_ast = combine_all_rules(rules[mid:])

    # Create an AND node that combines the two halves
    combined_node = Node("operator", left=left_ast, right=right_ast, value="AND")

    print(f"Created Combined Node: {combined_node.to_dict()}")  # Debug log

    return combined_node

@app.route('/evaluate', methods=['POST'])
def evaluate():
    """Evaluate the combined rule with the provided data."""
    data = request.json.get('data')
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if not rules:
        return jsonify({"error": "No rules available to evaluate"}), 400

    try:
        # Use the last rule (assuming it's the combined one) for evaluation
        ast = rules[-1]  
        rule_expression = ast_to_expression(ast)  # Get the rule expression from the AST
        print(f"Evaluating Rule: {rule_expression}")
        print(f"With Data: {data}")

        # Evaluate the rule expression against the data safely
        result = eval_rule(rule_expression, data)
        return jsonify({"result": result}), 200
    except Exception as e:
        print(f"Evaluation Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

def eval_rule(rule: str, data: dict) -> any:
    """Evaluate the rule expression safely against the provided data."""
    try:
        # Replace variables in the rule with actual values from the data
        expression = rule
        for key, value in data.items():
            # If value is a string, wrap it in quotes
            if isinstance(value, str):
                expression = expression.replace(key, f'"{value}"')
            else:
                expression = expression.replace(key, str(value))

        print(f"Evaluating Expression: {expression}")

        # Evaluate the final expression
        return eval(expression)
    except SyntaxError as e:
        raise ValueError(f"Error evaluating rule: {str(e)}")

@app.route('/modify_rule', methods=['PUT'])
def modify_rule():
    """Modify an existing rule."""
    data = request.json
    rule_index = data.get('index')  # Index of the rule to modify
    modification_type = data.get('type')  # Type of modification (operator, operand)
    new_value = data.get('new_value')  # New value to set

    if rule_index is None or rule_index < 0 or rule_index >= len(rules):
        return jsonify({"error": "Invalid rule index"}), 400

    rule_ast = rules[rule_index]  # Get the AST for the rule to modify

    try:
        if modification_type == "operator":
            rule_ast.change_operator(new_value)  # Call the instance method
        elif modification_type == "operand":
            rule_ast.update_operand(new_value)  # Call the instance method
        else:
            return jsonify({"error": "Invalid modification type"}), 400

        return jsonify({"message": "Rule modified successfully", "AST": rule_ast.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)