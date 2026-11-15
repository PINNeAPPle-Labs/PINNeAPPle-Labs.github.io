"""Regression tests for the approved two-product landing generator.

Run with: python3 -m unittest discover -s tests
No network access or third-party dependencies required.
"""
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import build
from twin_pages import catalog_items, detail_page

class LandingTests(unittest.TestCase):
    def test_homepage_has_exactly_two_commercial_products(self):
        for lang, first, second in (
            ("pt", "01 · Consultoria em Physics AI", "02 · PINNeAPPle Studio"),
            ("en", "01 · Physics AI Consulting", "02 · PINNeAPPle Studio"),
        ):
            with self.subTest(lang=lang):
                html = build.page_home(lang)
                self.assertIn(first, html)
                self.assertIn(second, html)
                self.assertLess(html.index(first), html.index(second))
                self.assertNotIn("03 ·", html)
                self.assertNotIn("04 ·", html)
                self.assertIn("id=\"produtos\"", html)

    def test_generated_home_matches_approved_public_baseline(self):
        for lang, path in (("pt", "index.html"), ("en", "en/index.html")):
            with self.subTest(lang=lang):
                expected = (ROOT / path).read_text(encoding="utf-8")
                self.assertEqual(build.page_home(lang), expected,
                    "Regenerate and review before publishing: build.py and committed HTML differ")

    def test_engineering_capabilities_are_not_extra_products(self):
        for lang in ("pt", "en"):
            with self.subTest(lang=lang):
                html = build.page_home(lang)
                for label in ("Engineering Automation", "Design Optimization",
                              "Simulation Acceleration", "Industrial Intelligence"):
                    self.assertIn(label, html)
                self.assertIn("digital-twins/", html)
                self.assertIn("physics-ai-models/", html)
                self.assertEqual(html.count("01 · "), 1)
                self.assertEqual(html.count("02 · "), 1)

    def test_all_100_bilingual_twin_pages_are_reproducible(self):
        for lang in ("pt", "en"):
            items = catalog_items(lang)
            self.assertEqual(len(items), 50)
            prefix = "en/" if lang == "en" else ""
            for item in items:
                with self.subTest(lang=lang, slug=item["slug"]):
                    expected = detail_page(lang, item)
                    path = ROOT / f"{prefix}digital-twins/{item['slug']}/index.html"
                    self.assertTrue(path.is_file(), str(path))
                    self.assertEqual(path.read_text(encoding="utf-8"), expected)
                    self.assertIn(f"/issues/{item['issue']}", expected)
                    self.assertIn(f"/{prefix}digital-twins/{item['slug']}/", expected)

    def test_sitemap_lists_all_100_twins(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for lang in ("pt", "en"):
            prefix = "en/" if lang == "en" else ""
            for item in catalog_items(lang):
                self.assertIn(f"/{prefix}digital-twins/{item['slug']}/", sitemap)

    def test_realistic_visual_assets_are_consistent(self):
        import json
        manifest = json.loads((ROOT / "assets/twin-visuals/manifest.json").read_text(encoding="utf-8"))
        slugs = {item["slug"] for item in catalog_items("pt")}
        for slug, record in manifest["images"].items():
            with self.subTest(slug=slug):
                self.assertIn(slug, slugs)
                self.assertTrue(record["file"].startswith("assets/twin-visuals/"))
                self.assertTrue(record["file"].endswith(".webp"))
                self.assertTrue(record["alt_pt"])
                self.assertTrue(record["alt_en"])
                # Binary upload is required before enabling an image.
                if (ROOT / record["file"]).is_file():
                    from twin_pages import image_for_twin
                    item = next(x for x in catalog_items("pt") if x["slug"] == slug)
                    self.assertIn("<img", image_for_twin("pt", item))
                    self.assertIn("../../../assets/", image_for_twin("en", item))

    def test_generator_has_required_routes(self):
        self.assertEqual(build.url("pt", "home"), "")
        self.assertEqual(build.url("en", "home"), "en/")
        self.assertIn("studio", build.PAGES)
        self.assertIn("artigos", build.PAGES)

if __name__ == "__main__":
    unittest.main()
