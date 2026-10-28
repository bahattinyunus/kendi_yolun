#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import sys
from io import StringIO
import kendi_yolun

class TestKendiYolun(unittest.TestCase):
    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        sys.stdout = self.old_stdout

    def test_quotes_structure(self):
        self.assertGreaterEqual(len(kendi_yolun.QUOTES), 15)
        for q in kendi_yolun.QUOTES:
            self.assertIn("quote", q)
            self.assertIn("author", q)
            self.assertIn("topic", q)
            self.assertIn("doc", q)
            self.assertIn("insight", q)

    def test_debug_scenarios_structure(self):
        expected_keys = [
            "dogma", "golge", "zaman", "kontrol", "tukenmislik",
            "olum_kaygisi", "anlamsizlik", "suru_baskisi", "ask_acisi"
        ]
        for key in expected_keys:
            self.assertIn(key, kendi_yolun.DEBUG_SCENARIOS)
            item = kendi_yolun.DEBUG_SCENARIOS[key]
            self.assertTrue(item["code"].startswith("ERR_"))
            self.assertIn("fix", item)
            self.assertIsInstance(item["fix"], list)

    def test_practices_structure(self):
        self.assertGreaterEqual(len(kendi_yolun.PRACTICES), 4)
        for p in kendi_yolun.PRACTICES:
            self.assertIn("title", p)
            self.assertIn("category", p)
            self.assertIn("summary", p)
            self.assertIn("rule", p)
            self.assertIn("doc", p)

    def test_tree_data_structure(self):
        self.assertEqual(len(kendi_yolun.TREE_DATA), 7)
        total_files = sum(len(files) for _, _, files in kendi_yolun.TREE_DATA)
        self.assertEqual(total_files, 28)

    def test_cmd_quote(self):
        kendi_yolun.cmd_quote(None)
        out = sys.stdout.getvalue()
        self.assertIn("FELSEFİ AFORİZMA", out)

    def test_cmd_debug_specific(self):
        class Args:
            issue = "olum_kaygisi"
        kendi_yolun.cmd_debug(Args())
        out = sys.stdout.getvalue()
        self.assertIn("ERR_MORTALITY_PANIC", out)

    def test_cmd_practice(self):
        kendi_yolun.cmd_practice(None)
        out = sys.stdout.getvalue()
        self.assertIn("GÜNLÜK PRATİK", out)

    def test_cmd_journal(self):
        class ArgsStoic:
            type = "stoic"
        kendi_yolun.cmd_journal(ArgsStoic())
        out_stoic = sys.stdout.getvalue()
        self.assertIn("STOACI AKŞAM MUHASEBESİ", out_stoic)

        class ArgsShadow:
            type = "shadow"
        kendi_yolun.cmd_journal(ArgsShadow())
        out_shadow = sys.stdout.getvalue()
        self.assertIn("GÖLGE ÇALIŞMASI", out_shadow)

    def test_cmd_search(self):
        class Args:
            query = "nehir"
        kendi_yolun.cmd_search(Args())
        out = sys.stdout.getvalue()
        self.assertIn("ARAMA SONUÇLARI", out)
        self.assertIn("eşleşme bulundu", out)

    def test_cmd_matrix(self):
        kendi_yolun.cmd_matrix(None)
        out = sys.stdout.getvalue()
        self.assertIn("Budizm", out)
        self.assertIn("Taoizm", out)
        self.assertIn("Stoacılık", out)

    def test_cmd_explore(self):
        kendi_yolun.cmd_explore(None)
        out = sys.stdout.getvalue()
        self.assertIn("01-ogretilerin-reddi", out)
        self.assertIn("05-bireylesme-ve-varolus", out)
        self.assertIn("06-karsilastirmali-metin-okumalari", out)
        self.assertIn("07-gunluk-pratikler-ve-meditasyonlar", out)

if __name__ == "__main__":
    unittest.main()
