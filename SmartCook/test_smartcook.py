import unittest
from unittest.mock import patch
from generator import generate_recipe

class TestSmartCook(unittest.TestCase):
    @patch("generator.openai.Completion.create")
    def test_generate_recipe_returns_text(self, mock_openai):
        # Mock response
        mock_openai.return_value = type("obj", (object,), {
            "choices": [type("obj", (object,), {"text": "\nRecipe Title\nStep 1\nStep 2"})]
        })()

        # Test normal input
        ingredients = "chicken, rice, garlic"
        result = generate_recipe(ingredients, language="en", style="fun")

        self.assertIn("Recipe Title", result)
        self.assertIn("Step 1", result)
        self.assertIsInstance(result, str)

    @patch("generator.openai.Completion.create")
    def test_generate_recipe_with_surprise_keyword(self, mock_openai):
        mock_openai.return_value = type("obj", (object,), {
            "choices": [type("obj", (object,), {"text": "Surprise Recipe Generated"})]
        })()

        result = generate_recipe("surprise", language="tr", style="grandma")

        self.assertIn("Surprise Recipe Generated", result)

if __name__ == "__main__":
    unittest.main()
