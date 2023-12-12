import re
from boolean_parser import parse

class QueryEvaluator:
    def __init__(self):
        self.operator_mapping = {
            '=': 'check_equal',
            '>': 'check_greater',
            '<': 'check_less',
            '>=': 'check_greater_equal',
            '<=': 'check_less_equal',
            '!=': 'check_not_equal'
        }

    def check_equal(self, field, value, index):
        return index.get(field, {}).get(value, [])

    def check_not_equal(self, field, value, index):
        result = []
        for key, paths in index.get(field, {}).items():
            if key != value:
                result.extend(paths)
        return result

    def check_less(self, field, value, index):
        result = []
        for key, paths in index.get(field, {}).items():
            if int(key) < int(value):
                result.extend(paths)
        return result

    def check_greater(self, field, value, index):
        result = []
        for key, paths in index.get(field, {}).items():
            if int(key) > int(value):
                result.extend(paths)
        return result

    def check_less_equal(self, field, value, index):
        result = []
        for key, paths in index.get(field, {}).items():
            if int(key) <= int(value):
                result.extend(paths)
        return result

    def check_greater_equal(self, field, value, index):
        result = []
        for key, paths in index.get(field, {}).items():
            if int(key) >= int(value):
                result.extend(paths)
        return result

    def is_function_call(self, text):
        pattern = r'(\w+)\((.*)\)'
        return re.match(pattern, text)

    def parse_function_args(self, args_string):
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
        return list(map(self.process_function_argument, arguments))

    def get_function_details(self, func_string):
        match = self.is_function_call(func_string)

        if match:
            name, args_string = match.group(1), match.group(2)
            args = self.parse_function_args(args_string) if args_string else []
            return name, args
        else:
            return func_string

    def transform_query_expression(self, expr):
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

    def process_function_argument(self, arg):
        if self.is_function_call(arg):
            return self.get_function_details(arg)
        else:
            return self.get_function_details(self.transform_query_expression(arg))

    def execute_query(self, query, index):
        query_function = getattr(self, query[0], lambda *args: [])
        return query_function(*query[1], index)

    def apply_index_filter(self, query_str, index):
        parsed_query = str(parse(query_str))
        transformed_query = self.process_function_argument(parsed_query)
        return self.execute_query(transformed_query, index)

# Example Usage
# evaluator = QueryEvaluator()
# result = evaluator.apply_index_filter("query", index)
