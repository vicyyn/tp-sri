import re
from boolean_parser import parse

class QueryEvaluator:
    def __init__(self):
        self.operator_mapping = {
            '=': 'equal',
            '>': 'greater_than',
            '<': 'less_than',
            '>=': 'greater_than_or_equal',
            '<=': 'less_than_or_equal',
            '!=': 'not_equal'
        }

    def _is_function_call(self, text):
        pattern = r'(\w+)\((.*)\)'
        return re.match(pattern, text)

    def _parse_arguments(self, args_string):
        arguments, current_arg, paren_count = [], '', 0

        for char in args_string:
            if char == ',' and paren_count == 0:
                arguments.append(current_arg.strip())
                current_arg = ''
            else:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                current_arg += char

        arguments.append(current_arg.strip())
        return list(map(self._process_argument, arguments))

    def _get_function_details(self, func_string):
        match = self._is_function_call(func_string)

        if match:
            name, args_string = match.group(1), match.group(2)
            args = self._parse_arguments(args_string) if args_string else []
            return name, args
        else:
            return func_string

    def _transform_expression(self, expr):
        operand1, operator, operand2 = "", "", ""
        for char in expr:
            if char.isalnum() or char == ' ':
                if operator:
                    operand2 += char
                else:
                    operand1 += char
            else:
                operator += char

        if operator in self.operator_mapping:
            transformed = f"{self.operator_mapping[operator]}({operand1.strip()}, {operand2.strip()})"
            return transformed
        else:
            return expr

    def _process_argument(self, arg):
        if self._is_function_call(arg):
            return self._get_function_details(arg)
        else:
            return self._get_function_details(self._transform_expression(arg))

    # Implement the comparison functions (equal, not_equal, greater_than, etc.)
    # ...

    def evaluate_query(self, query, index):
        query_function = getattr(self, query[0], lambda *args: [])
        return query_function(*query[1], index)

    def filter_index(self, query_str, index):
        parsed_query = str(parse(query_str))
        transformed_query = self._process_argument(parsed_query)
        return self.evaluate_query(transformed_query, index)


# Example Usage
# evaluator = QueryEvaluator()
# result = evaluator.filter_index("query", index)
