import re

COLORS_COMPILED_PATTERN = re.compile(r"\x1B\[([0-9]{1,3}(;[0-9]{1,2})?)?[mGK]")


class GrepService:
    def grep(self, params):
        file_addresses = self.get_file_addresses(params)

        output = []
        for file_address in file_addresses:
            with open(file_address, "r", encoding="utf-8") as file:
                output += self.grep_in_file(params, file, len(output))

        if params.get("hide_colors", False):
            output = [COLORS_COMPILED_PATTERN.sub("", line) for line in output]

        return output

    def grep_in_file(self, params, file, current_output_size):
        after = params.get("after", 0)
        before = params.get("before", 0)
        output = []
        before_counter = 0
        part = []
        found = False
        for line in file:
            part.append(line)
            found_patterns = all(self._lookup(params, pattern, line) for pattern in params["patterns"])
            if found_patterns:
                before_counter = len(part)
                found = True

            if not found and len(part) > before:
                part.pop(0)

            if found and len(part) >= before_counter + after:
                found = False
                before_counter = 0
                output += part
                part = []

            if current_output_size + len(output) >= params.get("max_line_numbers", 1000):
                break
        if found:
            output += part
        return output

    def get_file_addresses(self, params):
        return [params.get("address", ".")]

    def _lookup(self, params, pattern, text):
        if params.get("is_regex", False):
            return re.search(pattern, text)
        if not params.get("is_case_sensitive", False):
            return pattern.lower() in text.lower()
        return pattern in text


grep_service = GrepService()
