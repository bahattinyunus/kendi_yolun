#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import sys
from io import StringIO
import json
import kendi_yolun

class TestKendiYolun(unittest.TestCase):
    def setUp(self):
        self.old_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        sys.stdout = self.old_stdout

    def test_quotes_structure(self):
        self.assertGreaterEqual(len(kendi_yolun.QUOTES), 18)
        for q in kendi_yolun.QUOTES:
            self.assertIn("quote", q)
            self.assertIn("author", q)
            self.assertIn("topic", q)
            self.assertIn("doc", q)
            self.assertIn("insight", q)

    def test_debug_scenarios_structure(self):
        expected_keys = [
            "dogma", "golge", "zaman", "kontrol", "tukenmislik",
            "olum_kaygisi", "anlamsizlik", "suru_baskisi", "ask_acisi",
            "karma_korlugu"
        ]
        for key in expected_keys:
            self.assertIn(key, kendi_yolun.DEBUG_SCENARIOS)
            item = kendi_yolun.DEBUG_SCENARIOS[key]
            self.assertTrue(item["code"].startswith("ERR_"))
            self.assertIn("fix", item)
            self.assertIsInstance(item["fix"], list)

    def test_practices_structure(self):
        self.assertGreaterEqual(len(kendi_yolun.PRACTICES), 5)
        for p in kendi_yolun.PRACTICES:
            self.assertIn("title", p)
            self.assertIn("category", p)
            self.assertIn("summary", p)
            self.assertIn("rule", p)
            self.assertIn("doc", p)

    def test_tree_data_structure(self):
        self.assertEqual(len(kendi_yolun.TREE_DATA), 8)
        total_files = sum(len(files) for _, _, files in kendi_yolun.TREE_DATA)
        self.assertEqual(total_files, 32)

    def test_cmd_quote(self):
        kendi_yolun.cmd_quote(None)
        out = sys.stdout.getvalue()
        self.assertIn("FELSEFİ AFORİZMA", out)

    def test_cmd_debug_specific(self):
        class Args:
            issue = "karma_korlugu"
        kendi_yolun.cmd_debug(Args())
        out = sys.stdout.getvalue()
        self.assertIn("ERR_SECOND_ORDER_BLINDNESS", out)

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

    def test_cmd_export_json(self):
        class Args:
            format = "json"
        kendi_yolun.cmd_export(Args())
        out = sys.stdout.getvalue()
        parsed = json.loads(out)
        self.assertEqual(parsed["modules_count"], 8)

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
        self.assertIn("08-zihinsel-modeller-ve-felsefi-notasyonlar", out)

if __name__ == "__main__":
    unittest.main()
