import openai


# Ortam değişkeninden API anahtarını al
openai.api_key = "REMOVED"

MODEL_MAP = {
    "en": "gpt2",
    "tr": "hakurei/gpt2-turkish",
}

PROMPTS = {
    "en": (
        "You are a world-class chef known for creating delicious and engaging recipes.\n"
        "Write a recipe that is fun, friendly, and full of character.\n\n"
        "Example:\n"
        "Ingredients: chicken, rice, garlic\n"
        "Recipe: Let’s make something heartwarming! First, wash the rice and set it aside. "
        "In a large skillet, heat some oil and sauté the garlic until fragrant. Add chicken pieces, "
        "season with salt and pepper, and cook until golden brown. Stir in the rice and pour in chicken broth to cover. "
        "Simmer for 20 minutes with a lid on. Fluff with a fork and enjoy your cozy dish!\n\n"
    ),
    "tr": (
        "Sen dünyaca ünlü bir şefsin. Samimi, detaylı ve lezzetli yemek tarifleri yazıyorsun.\n"
        "Yemek tarifin sade, eğlenceli ve anlaşılır olsun. Her adımı açıklayıcı yaz.\n\n"
        "Örnek:\n"
        "Malzemeler: tavuk, pirinç, sarımsak\n"
        "Tarif: Hadi içimizi ısıtacak bir yemek yapalım! Önce pirinci güzelce yıka ve süz. "
        "Bir tavada yağı ısıt, ardından sarımsağı hafifçe kavur. Tavukları ekle, güzelce pişir. "
        "Pirinç ve suyu ilave et. 20 dakika kapağı kapalı şekilde pişir. Afiyet olsun!\n\n"
    ),
}


def generate_recipe(
    ingredients: str,
    max_tokens: int = 300,
    temperature: float = 0.9,
    language: str = "en",
) -> str:
    """
    Generate a multilingual recipe using OpenAI API.

    Args:
        ingredients (str): Ingredients input by the user.
        max_tokens (int): Maximum tokens to generate.
        temperature (float): Sampling temperature.
        language (str): Language code ('en' or 'tr').

    Returns:
        str: Generated recipe text.
    """
    prompt_intro = PROMPTS.get(language, PROMPTS["en"])
    ingredients_label = "Ingredients" if language == "en" else "Malzemeler"
    recipe_label = "Recipe" if language == "en" else "Tarif"

    full_prompt = f"{prompt_intro}{ingredients_label}: {ingredients.strip()}\n{recipe_label}:"

    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=full_prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return response.choices[0].text.strip()
