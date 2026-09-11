#Part 1 of this Question. Done by Shreeya Niraula: S408727
import os

def tokenize(expression: str) -> list[tuple[str, str]]:
    # Convert the expression into a list of tokens for later processing.
    tokens = []
    position = 0

    while position < len(expression):
        character = expression[position]

        if character.isspace():
            # Ignore whitespace between the different tokens.
            position += 1

        elif "0" <= character <= "9":
            # Read the complete number before adding it as one token.
            number_start = position

            while (
                position < len(expression)
                and "0" <= expression[position] <= "9"
            ):
                position += 1

            # Read the decimal part only when it has digits after the point.
            if position < len(expression) and expression[position] == ".":
                decimal_position = position
                position += 1

                if (
                    position < len(expression)
                    and "0" <= expression[position] <= "9"
                ):
                    while (
                        position < len(expression)
                        and "0" <= expression[position] <= "9"
                    ):
                        position += 1
                else:
                    position = decimal_position

            tokens.append(("NUM", expression[number_start:position]))

        elif character in "+-*/%^":
            # Recognise each supported operator as an OP token.
            tokens.append(("OP", character))
            position += 1

        elif character == "(":
            # Recognise an opening parenthesis.
            tokens.append(("LPAREN", character))
            position += 1

        elif character == ")":
            # Recognise a closing parenthesis.
            tokens.append(("RPAREN", character))
            position += 1

        else:
            # Reject characters that are not part of the expression language.
            raise ValueError(f"Unsupported character: {character}")

    # Mark the end of the token sequence for the parser.
    tokens.append(("END", ""))
    return tokens


def format_tokens(tokens: list[tuple[str, str]]) -> str:
    formatted_tokens = []

    # Format each token using the output format required by the assignment.
    for token_type, token_value in tokens:
        if token_type == "END":
            formatted_tokens.append("[END]")
        else:
            formatted_tokens.append(f"[{token_type}:{token_value}]")

    return " ".join(formatted_tokens)


def parse_primary(
    tokens: list[tuple[str, str]],
    position: int
) -> tuple[tuple, int]:
    token_type, token_value = tokens[position]

    if token_type == "NUM":
        # Convert a number token into a number tree node.
        number_tree = ("num", float(token_value))
        return number_tree, position + 1

    elif token_type == "LPAREN":
        # Parse the expression inside the parenthesised expression.
        position += 1
        inner_tree, position = parse_expression(tokens, position)

        # Check that the parenthesised expression has a closing parenthesis.
        if tokens[position][0] != "RPAREN":
            raise ValueError("Expected closing parenthesis")

        position += 1
        return inner_tree, position

    else:
        # Reject tokens that cannot start a primary expression.
        raise ValueError("Expected a number or opening parenthesis")


def parse_power(
    tokens: list[tuple[str, str]],
    position: int
) -> tuple[tuple, int]:
    # Parse the base expression on the left side of the exponentiation.
    left_tree, position = parse_primary(tokens, position)

    # Check whether the next token is an exponentiation operator.
    if tokens[position][0] == "OP" and tokens[position][1] == "^":
        position += 1

        # Parse the right operand through unary parsing.
        right_tree, position = parse_unary(tokens, position)

        # Build the exponentiation tree from both operands.
        left_tree = ("^", left_tree, right_tree)

    return left_tree, position


def parse_unary(
    tokens: list[tuple[str, str]],
    position: int
) -> tuple[tuple, int]:
    token_type, token_value = tokens[position]

    if token_type == "OP" and token_value == "-":
        # Recognise a unary minus before an operand.
        position += 1

        # Recursively parse the operand to support repeated negation.
        operand_tree, position = parse_unary(tokens, position)
        return ("neg", operand_tree), position

    else:
        # Pass non-negated expressions to the power parser.
        return parse_power(tokens, position)


#Part 2 of this Question. Done by Mohd Ratib: S408795

def parse_multiplicative(
    tokens: list[tuple[str, str]],
    position: int
) -> tuple[tuple, int]:
    # Parse multiplication, division, modulo, and implicit multiplication.
    left_tree, position = parse_unary(tokens, position)

    while True:
        token_type, token_value = tokens[position]

        if token_type == "OP" and token_value in "*/%":
            # Handle normal multiplicative operators from left to right.
            operator = token_value
            position += 1

            right_tree, position = parse_unary(tokens, position)
            left_tree = (operator, left_tree, right_tree)

        elif token_type == "LPAREN":
            # An opening parenthesis directly after an operand means multiplication.
            right_tree, position = parse_unary(tokens, position)
            left_tree = ("*", left_tree, right_tree)

        elif (
            token_type == "NUM"
            and position > 0
            and tokens[position - 1][0] == "RPAREN"
        ):
            # A number directly after a closing parenthesis is also implicit multiplication.
            right_tree, position = parse_unary(tokens, position)
            left_tree = ("*", left_tree, right_tree)

        else:
            break

    return left_tree, position


def parse_additive(
    tokens: list[tuple[str, str]],
    position: int
) -> tuple[tuple, int]:
    # Parse addition and subtraction after higher-precedence operations.
    left_tree, position = parse_multiplicative(tokens, position)

    while (
        tokens[position][0] == "OP"
        and tokens[position][1] in "+-"
    ):
        operator = tokens[position][1]
        position += 1

        # Parse the expression on the right side of the operator.
        right_tree, position = parse_multiplicative(tokens, position)

        # Update the tree so addition and subtraction are left associative.
        left_tree = (operator, left_tree, right_tree)

    return left_tree, position


def parse_expression(
    tokens: list[tuple[str, str]],
    position: int
) -> tuple[tuple, int]:
    # Start parsing an expression from the lowest precedence level.
    return parse_additive(tokens, position)


def format_tree(tree: tuple) -> str:
    # Convert the internal expression tree into the required output format.
    node_type = tree[0]

    if node_type == "num":
        number_value = tree[1]

        # Display whole numbers without a decimal point.
        if number_value.is_integer():
            return str(int(number_value))
        else:
            return str(number_value)

    elif node_type == "neg":
        # Format unary negation using the word "neg".
        operand_text = format_tree(tree[1])
        return f"(neg {operand_text})"

    elif node_type in "+-*/%^":
        # Recursively format both sides of a binary operation.
        left_text = format_tree(tree[1])
        right_text = format_tree(tree[2])

        return f"({node_type} {left_text} {right_text})"

    else:
        raise ValueError("Invalid tree node")


def evaluate_tree(tree: tuple) -> float:
    # Recursively calculate the numeric result of the expression tree.
    node_type = tree[0]

    if node_type == "num":
        return tree[1]

    elif node_type == "neg":
        return -evaluate_tree(tree[1])

    # Evaluate both operands before applying the binary operator.
    left_value = evaluate_tree(tree[1])
    right_value = evaluate_tree(tree[2])

    if node_type == "+":
        return left_value + right_value

    elif node_type == "-":
        return left_value - right_value

    elif node_type == "*":
        return left_value * right_value

    elif node_type == "/":
        return left_value / right_value

    elif node_type == "%":
        return left_value % right_value

    elif node_type == "^":
        result = left_value ** right_value

        # Complex numbers are outside the required result format.
        if isinstance(result, complex):
            raise ValueError("Complex result")

        return float(result)

    else:
        raise ValueError("Invalid operator")


def format_result(value: float) -> str:
    # Format successful results according to the assignment requirements.
    rounded_value = round(value, 4)

    # Whole numbers should be displayed without a decimal point.
    if rounded_value.is_integer():
        return str(int(rounded_value))
    else:
        return str(rounded_value)


def evaluate_file(input_path: str) -> list[dict]:
    # Read expressions from a file, evaluate them, and write the results to output.txt.
    results = []

    with open(input_path, "r") as f:
        lines = f.readlines()

    output_blocks = []

    for line in lines:
        # Remove only the line ending and keep the original expression unchanged.
        expression = line.rstrip("\r\n")

        tree_text = "ERROR"
        tokens_text = "ERROR"
        result_value = "ERROR"
        result_text = "ERROR"

        try:
            # Convert the expression into tokens first.
            tokens = tokenize(expression)
            tokens_text = format_tokens(tokens)

        except ValueError:
            tokens = None

        if tokens is not None:
            try:
                # Parse the tokens and create the expression tree.
                tree, position = parse_expression(tokens, 0)

                # A valid expression must finish at the END token.
                if tokens[position][0] != "END":
                    raise ValueError("Unexpected token")

                tree_text = format_tree(tree)

                try:
                    # Evaluate the tree after successful parsing.
                    result_value = evaluate_tree(tree)
                    result_text = format_result(result_value)

                except (ArithmeticError, ValueError):
                    # Mathematical errors keep the valid tree and tokens.
                    result_value = "ERROR"
                    result_text = "ERROR"

            except (ValueError, IndexError):
                # Parsing errors make the tree and result invalid.
                tree_text = "ERROR"
                result_value = "ERROR"
                result_text = "ERROR"

        results.append({
            "input": expression,
            "tree": tree_text,
            "tokens": tokens_text,
            "result": result_value
        })

        # Build the four-line output block required for each expression.
        output_blocks.append(
            f"Input: {expression}\n"
            f"Tree: {tree_text}\n"
            f"Tokens: {tokens_text}\n"
            f"Result: {result_text}"
        )

    # Create output.txt in the same directory as the input file.
    directory = os.path.dirname(os.path.abspath(input_path))
    output_path = os.path.join(directory, "output.txt")

    with open(output_path, "w") as f:
        # Separate each expression block with one blank line.
        f.write("\n\n".join(output_blocks))

        if output_blocks:
            f.write("\n")

    return results