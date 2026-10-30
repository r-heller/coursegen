import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("new_project", ROOT / "scripts/new_project.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ScaffoldTests(unittest.TestCase):
    def test_standalone_project_and_literal_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = module.create(Path(temporary) / "project with spaces", 'Title: "quoted"', "R. Heller", "de")
            config = json.loads((target / "_quarto.yml").read_text())
            self.assertEqual(config[config['project']['type']]['title'], 'Title: "quoted"')
            self.assertEqual(config['author'], 'R. Heller')
            self.assertEqual(config['lang'], 'de')
            self.assertTrue((target / 'index.qmd').is_file())
            self.assertEqual((target / 'LICENSE').read_bytes(), (ROOT / 'LICENSE').read_bytes())
            self.assertFalse((target / '.git').exists())

    def test_existing_work_and_invalid_input_are_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'existing'
            target.mkdir()
            sentinel = target / 'notes.txt'
            sentinel.write_text('keep')
            with self.assertRaises(FileExistsError):
                module.create(target, 'Title', 'Author')
            self.assertEqual(sentinel.read_text(), 'keep')
            with self.assertRaises(ValueError):
                module.create(Path(temporary) / 'invalid', ' ', 'Author')
            self.assertFalse((Path(temporary) / 'invalid').exists())

    def test_recursive_destination_is_rejected(self):
        with self.assertRaises(ValueError):
            module.create(ROOT / 'template/nested', 'Title', 'Author')


if __name__ == '__main__':
    unittest.main()
