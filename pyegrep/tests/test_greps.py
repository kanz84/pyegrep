import os
import tempfile
from unittest import TestCase

from pyegrep.greps import grep_service


class GrepServiceTest(TestCase):

    def write(self, temp_dir, filename, lines):
        f_name = os.path.join(temp_dir, filename)
        with open(f_name, "a", encoding="utf-8") as fh:
            for line in lines:
                fh.write(line + "\n")
        return f_name

    def test_grep(self):
        lines = [
            "00QQQ",
            "01QQQ",
            "02XXX",
            "03QQQ",
            "04QQQ",
            "05QQQ",
            "06QQQ",
            "07QQQ",
            "08XXX",
            "09QQQ",
            "10QQQ",
            "11QQQ",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 0, "after": 0, "patterns": "XXX", "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(2, len(output))
            outputs = "".join(output)
            self.assertIn("02XXX", outputs)
            self.assertIn("08XXX", outputs)

    def test_grep_regex(self):
        lines = [
            "00QQQ",
            "01XXX",
            "02CCC",
            "03DDD",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 0, "after": 0, "patterns": [r"[C]+"], "is_regex": True, "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(1, len(output))
            outputs = "".join(output)
            self.assertIn("02CCC", outputs)

    def test_grep_multi_regex(self):
        lines = [
            "00QQQ",
            "01XXX---FFF",
            "02WWWCCC---FFF-------",
            "03DDD",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 0, "after": 0, "patterns": [r"[C]+", r"[F]+"], "is_regex": True, "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(1, len(output))
            outputs = "".join(output)
            self.assertIn("02WWWCCC---FFF-------", outputs)

    def test_grep_without_match(self):
        lines = [
            "00QQQ",
            "01XXX---FFF",
            "02WWWCCC---FFF-------",
            "03DDD",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 0, "after": 0, "patterns": ["ZZZ"], "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(0, len(output))

    def test_grep_after(self):
        lines = [
            "00QQQ",
            "01QQQ",
            "02WWWQQQWWW",
            "03WWWRRRWWW",
            "04QQQ",
            "05WWWXXXWWW",
            "06WWWCCCWWW",
            "07WWWDDDWWW",
            "08WWWEEEWWW",
            "09WWWFFFWWW",
            "10WWWGGGWWW",
            "11WWWHHHWWW",
            "12WWWIIIWWW",
            "13WWWJJJWWW",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 0, "after": 3, "patterns": ["XXX"], "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(4, len(output))
            outputs = "".join(output)
            self.assertIn("05WWWXXXWWW", outputs)
            self.assertIn("06WWWCCCWWW", outputs)
            self.assertIn("07WWWDDDWWW", outputs)
            self.assertIn("08WWWEEEWWW", outputs)

    def test_grep_before(self):
        lines = [
            "00QQQ",
            "01QQQ",
            "02WWWQQQWWW",
            "03WWWRRRWWW",
            "04QQQ",
            "05WWWXXXWWW",
            "06WWWCCCWWW",
            "07WWWDDDWWW",
            "08WWWEEEWWW",
            "09WWWFFFWWW",
            "10WWWGGGWWW",
            "11WWWHHHWWW",
            "12WWWIIIWWW",
            "13WWWJJJWWW",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 2, "after": 0, "patterns": ["XXX"], "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(3, len(output))
            outputs = "".join(output)
            self.assertIn("03WWWRRRWWW", outputs)
            self.assertIn("04QQQ", outputs)
            self.assertIn("05WWWXXXWWW", outputs)

    def test_grep_after_before(self):
        lines = [
            "00QQQ",
            "01QQQ",
            "02WWWQQQWWW",
            "03WWWRRRWWW",
            "04QQQ",
            "05WWWXXXWWW",
            "06WWWCCCWWW",
            "07WWWDDDWWW",
            "08WWWEEEWWW",
            "09WWWFFFWWW",
            "10WWWGGGWWW",
            "11WWWHHHWWW",
            "12WWWIIIWWW",
            "13WWWJJJWWW",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 2, "after": 3, "patterns": ["XXX"], "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(6, len(output))
            outputs = "".join(output)
            self.assertIn("03WWWRRRWWW", outputs)
            self.assertIn("04QQQ", outputs)
            self.assertIn("05WWWXXXWWW", outputs)
            self.assertIn("06WWWCCCWWW", outputs)
            self.assertIn("07WWWDDDWWW", outputs)
            self.assertIn("08WWWEEEWWW", outputs)

    def test_grep_after_before_found_again(self):
        lines = [
            "00QQQ",
            "01QQQ",
            "02WWWQQQWWW",
            "03WWWRRRWWW",
            "04QQQ",
            "05WWWXXXWWW",
            "06WWWCCCWWW",
            "07WWWXXXWWW",
            "08WWWEEEWWW",
            "09WWWFFFWWW",
            "10WWWGGGWWW",
            "11WWWHHHWWW",
            "12WWWIIIWWW",
            "13WWWJJJWWW",
            "14WWWKKKWWW",
            "15WWWLLLWWW",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 2, "after": 3, "patterns": ["XXX"], "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(8, len(output))
            outputs = "".join(output)
            self.assertIn("03WWWRRRWWW", outputs)
            self.assertIn("04QQQ", outputs)
            self.assertIn("05WWWXXXWWW", outputs)
            self.assertIn("06WWWCCCWWW", outputs)
            self.assertIn("07WWWXXXWWW", outputs)
            self.assertIn("08WWWEEEWWW", outputs)
            self.assertIn("09WWWFFFWWW", outputs)
            self.assertIn("10WWWGGGWWW", outputs)

    def test_grep_after_before_found_again2(self):
        lines = [
            "00QQQ",
            "01QQQ",
            "02WWWQQQWWW",
            "03WWWRRRWWW",
            "04QQQ",
            "05WWWXXXWWW",
            "06WWWCCCWWW",
            "07WWWXXXWWW",
            "08WWWEEEWWW",
            "09WWWFFFWWW",
            "10WWWXXXWWW",
            "11WWWHHHWWW",
            "12WWWIIIWWW",
            "13WWWJJJWWW",
            "14WWWKKKWWW",
            "15WWWLLLWWW",
            "16WWWMMMWWW",
            "17WWWNNNWWW",
            "18WWWOOOWWW",
            "19WWWPPPWWW",
            "20WWWQQQWWW",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 2, "after": 3, "patterns": ["XXX"], "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(11, len(output))
            outputs = "".join(output)
            self.assertIn("03WWWRRRWWW", outputs)
            self.assertIn("04QQQ", outputs)
            self.assertIn("05WWWXXXWWW", outputs)
            self.assertIn("06WWWCCCWWW", outputs)
            self.assertIn("07WWWXXXWWW", outputs)
            self.assertIn("08WWWEEEWWW", outputs)
            self.assertIn("09WWWFFFWWW", outputs)
            self.assertIn("10WWWXXXWWW", outputs)
            self.assertIn("11WWWHHHWWW", outputs)
            self.assertIn("12WWWIIIWWW", outputs)
            self.assertIn("13WWWJJJWWW", outputs)

    def test_grep_after_before_found_again2_separate(self):
        lines = [
            "00QQQ",
            "01QQQ",
            "02WWWQQQWWW",
            "03WWWXXXWWW",
            "04QQQ",
            "05WWWCCCWWW",
            "06WWWCCCWWW",
            "07WWWCCCWWW",
            "08WWWEEEWWW",
            "09WWWFFFWWW",
            "10WWWXXXWWW",
            "11WWWHHHWWW",
            "12WWWIIIWWW",
            "13WWWJJJWWW",
            "14WWWKKKWWW",
            "15WWWLLLWWW",
            "16WWWMMMWWW",
            "17WWWNNNWWW",
            "18WWWOOOWWW",
            "19WWWPPPWWW",
            "20WWWQQQWWW",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 2, "after": 3, "patterns": ["XXX"], "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(12, len(output))
            outputs = "".join(output)
            self.assertIn("01QQQ", outputs)
            self.assertIn("02WWWQQQWWW", outputs)
            self.assertIn("03WWWXXXWWW", outputs)
            self.assertIn("04QQQ", outputs)
            self.assertIn("05WWWCCCWWW", outputs)
            self.assertIn("06WWWCCCWWW", outputs)

            self.assertIn("08WWWEEEWWW", outputs)
            self.assertIn("09WWWFFFWWW", outputs)
            self.assertIn("10WWWXXXWWW", outputs)
            self.assertIn("11WWWHHHWWW", outputs)
            self.assertIn("12WWWIIIWWW", outputs)
            self.assertIn("13WWWJJJWWW", outputs)

    def test_grep_after_before_near_start(self):
        lines = [
            "00QQQ",
            "01XXX",
            "02WWWQQQWWW",
            "03WWWCCCWWW",
            "04QQQ",
            "05WWWCCCWWW",
            "06WWWCCCWWW",
            "07WWWCCCWWW",
            "08WWWCCCWWW",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 2, "after": 3, "patterns": ["XXX"], "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(5, len(output))
            outputs = "".join(output)
            self.assertIn("00QQQ", outputs)
            self.assertIn("01XXX", outputs)
            self.assertIn("02WWWQQQWWW", outputs)
            self.assertIn("03WWWCCCWWW", outputs)
            self.assertIn("04QQQ", outputs)

    def test_grep_after_before_near_end(self):
        lines = [
            "00QQQ",
            "01WWWCCCWWW",
            "02WWWQQQWWW",
            "03WWWCCCWWW",
            "04QQQ",
            "05WWWCCCWWW",
            "06WWWCCCWWW",
            "07WWWXXXWWW",
            "08WWWCCCWWW",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 2, "after": 3, "patterns": ["XXX"], "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(4, len(output))
            outputs = "".join(output)
            self.assertIn("05WWWCCCWWW", outputs)
            self.assertIn("06WWWCCCWWW", outputs)
            self.assertIn("07WWWXXXWWW", outputs)
            self.assertIn("08WWWCCCWWW", outputs)

    def test_grep_after_before_at_start(self):
        lines = [
            "00WWWXXXWWW",
            "01WWWHHHWWW",
            "02WWWQQQWWW",
            "03WWWCCCWWW",
            "04QQQ",
            "05WWWCCCWWW",
            "06WWWCCCWWW",
            "07WWWCCCWWW",
            "08WWWCCCWWW",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 2, "after": 3, "patterns": ["XXX"], "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(4, len(output))
            outputs = "".join(output)
            self.assertIn("00WWWXXXWWW", outputs)
            self.assertIn("01WWWHHHWWW", outputs)
            self.assertIn("02WWWQQQWWW", outputs)
            self.assertIn("03WWWCCCWWW", outputs)

    def test_grep_after_before_at_end(self):
        lines = [
            "00QQQ",
            "01WWWCCCWWW",
            "02WWWQQQWWW",
            "03WWWCCCWWW",
            "04QQQ",
            "05WWWCCCWWW",
            "06WWWCCCWWW",
            "07WWWRRRWWW",
            "08XXX",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 2, "after": 3, "patterns": ["XXX"], "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(3, len(output))
            outputs = "".join(output)
            self.assertIn("06WWWCCCWWW", outputs)
            self.assertIn("07WWWRRRWWW", outputs)
            self.assertIn("08XXX", outputs)

    def test_grep_regex2(self):
        lines = [
            "00QQQ",
            "01XXX",
            "abXXY",
            "02CCC",
            "03DDD",
        ]
        with tempfile.TemporaryDirectory() as temp:
            file_address = self.write(temp, "file.log", lines)
            params = {"before": 0, "after": 0, "patterns": [r"[a-z]+"], "is_regex": True, "address": file_address}
            output = grep_service.grep(params)
            self.assertEqual(1, len(output))
            outputs = "".join(output)
            self.assertIn("abXXY", outputs)
