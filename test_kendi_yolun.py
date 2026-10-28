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
        self.assertGreater(len(kendi_yolun.QUOTES), 0)
        for q in kendi_yolun.QUOTES:
            self.assertIn("quote", q)
            self.assertIn("author", q)
            self.assertIn("topic", q)
            self.assertIn("doc", q)
            self.assertIn("insight", q)

    def test_debug_scenarios_structure(self):
        expected_keys = ["dogma", "golge", "zaman", "kontrol", "tukenmislik"]
        for key in expected_keys:
            self.assertIn(key, kendi_yolun.DEBUG_SCENARIOS)
            item = kendi_yolun.DEBUG_SCENARIOS[key]
            self.assertTrue(item["code"].startswith("ERR_"))
            self.assertIn("fix", item)
            self.assertIsInstance(item["fix"], list)

    def test_cmd_quote(self):
        kendi_yolun.cmd_quote(None)
        out = sys.stdout.getvalue()
        self.assertIn("FELSEFİ AFORİZMA", out)

    def test_cmd_debug_specific(self):
        class Args:
            issue = "dogma"
        kendi_yolun.cmd_debug(Args())
        out = sys.stdout.getvalue()
        self.assertIn("ERR_DOGMA_INFINITY_LOOP", out)

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
        self.assertIn("04-kavram-haritalari", out)

if __name__ == "__main__":
    unittest.main()
