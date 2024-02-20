from tests.fixtures import QCTestCase
from pathlib import Path

class TestCrosstab(QCTestCase):
    def test_crosstab_shows_counts(self):
        self.run_in_testpath("qc import macbeth.txt --importer verbatim")
        self.set_mock_editor()
        self.run_in_testpath("qc code chris")
        self.run_in_testpath("qc codebook")
        result = self.run_in_testpath("qc crosstab one two line --format tsv")
        table = self.read_stats_tsv(result.stdout)
        self.assertEqual(table['two']['line'], 1)

    def test_crosstab_with_probs_shows_probs(self):
        self.run_in_testpath("qc import macbeth.txt --importer verbatim")
        self.set_mock_editor()
        self.run_in_testpath("qc code chris")
        self.run_in_testpath("qc codebook")
        result = self.run_in_testpath("qc crosstab one two line --probs --format tsv")
        table = self.read_stats_tsv(result.stdout)
        self.assertEqual(table['line']['two'], 0.5)
