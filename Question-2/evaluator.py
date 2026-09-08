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
