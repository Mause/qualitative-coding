from tests.fixtures import QCTestCase

class TestStats(QCTestCase):
    def test_stats_shows_stats(self):
        self.run_in_testpath("qc import macbeth.txt --importer verbatim")
        self.set_mock_editor()
        self.run_in_testpath("qc code chris")
        self.run_in_testpath("qc codebook")
        result = self.run_in_testpath("qc stats --format tsv")
        table = self.read_stats_tsv(result.stdout)
        self.assertEqual(table['line']['Count'], 2)


