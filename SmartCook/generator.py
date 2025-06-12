import openai
import pyperclip
import pyttsx3
import random

openai.api_key = "REMOVED"

MODEL_NAME = "gpt-3.5-turbo-instruct"

STYLE_PROMPTS = {
    "fun": "Tarif eğlenceli, sıcak ve konuşur gibi bir dille yazılsın.",
    "pro": "Tarif profesyonel bir şef edasıyla net ve teknik bir şekilde yazılsın.",
    "grandma": "Tarif bir anneanne gibi sıcacık, nostaljik ve samimi bir şekilde yazılsın.",
    "blogger": "Tarif bir yemek blog yazarı gibi yazılsın, kişisel ve hikâye dolu olsun."
}

MESSAGES = {
    "en": {
        "welcome": "\n👩‍🍳 Welcome to SmartCook – Your AI Sous Chef!",
        "start": "Let’s whip up something delicious together. 🍲\n",
        "input_prompt": "🧺 Enter ingredients (comma-separated, e.g., chicken, rice, garlic): ",
        "input_empty": "⚠️ Please enter at least one ingredient.\n",
        "input_few": "⚠️ Please enter at least two ingredients for a better recipe.\n",
        "language_prompt": "🌍 Choose a language / Dil seç (en/tr): ",
        "style_prompt": "🎭 Choose a recipe style:\n1. Fun\n2. Professional\n3. Grandma\n4. Blogger\nSelection (1-4): ",
        "generating": "\n🍽️ Generating your unique recipe...\n",
        "result": "📄 Here’s your recipe:\n",
        "copy_prompt": "🔹 Copy recipe to clipboard? (y/n): ",
        "copied": "✅ Recipe copied to clipboard!",
        "voice_prompt": "🔊 Would you like it read aloud? (y/n): ",
        "closing": "\n🌟 Bon appétit!\n"
    },
    "tr": {
        "welcome": "\n👩‍🍳 SmartCook’a hoş geldin – Yapay zekalı yardımcı şefin burada!",
        "start": "Hadi birlikte lezzetli bir şeyler yapalım. 🍲\n",
        "input_prompt": "🧺 Malzemeleri gir (virgülle ayır, örn: tavuk, pirinç, sarımsak): ",
        "input_empty": "⚠️ Lütfen en az bir malzeme gir.\n",
        "input_few": "⚠️ Daha iyi bir tarif için en az iki malzeme gir.\n",
        "language_prompt": "🌍 Choose a language / Dil seç (en/tr): ",
        "style_prompt": "🎭 Tarif tarzını seç:\n1. Eğlenceli\n2. Profesyonel\n3. Anneanne\n4. Blog yazarı gibi\nSeçimin (1-4): ",
        "generating": "\n🍽️ Tarif oluşturuluyor...\n",
        "result": "📄 İşte tarifin:\n",
        "copy_prompt": "🔹 Tarifi panoya kopyala? (e/h): ",
        "copied": "✅ Tarif panoya kopyalandı!",
        "voice_prompt": "🔊 Okunmasını ister misin? (e/h): ",
        "closing": "\n🌟 Afiyet olsun!\n"
    }
}


def speak_text(text: str, language: str = "en"):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    if language == "tr":
        # Türkçe ses: macOS'ta "Yelda", Windows'ta "Hazal", "Tolga", "Microsoft Tolga"
        turkish_voice = next(
            (
                v for v in voices
                if "Yelda" in v.name or "Hazal" in v.name or "Tolga" in v.name or "Microsoft Tolga" in v.name
            ),
            None
        )
        if turkish_voice:
            engine.setProperty('voice', turkish_voice.id)
        else:
            print("Türkçe ses bulunamadı, varsayılan ses kullanılacak.")
    else:
        # İngilizce ses: macOS'ta "Alex", "Samantha"; Windows'ta "Microsoft David", "Microsoft Zira" vs.
        english_voice = next(
            (
                v for v in voices
                if "en" in v.id.lower()
                or "english" in v.name.lower()
                or "Alex" in v.name
                or "Samantha" in v.name
                or "Microsoft David" in v.name
                or "Microsoft Zira" in v.name
            ),
            None
        )
        if english_voice:
            engine.setProperty('voice', english_voice.id)

    engine.say(text)
    engine.runAndWait()


def generate_recipe(ingredients: str, language: str = "en", style: str = "fun") -> str:
    style_instruction = STYLE_PROMPTS.get(style, STYLE_PROMPTS["fun"])

    if language == "tr":
        prompt = (
            "Sen dünyaça ünlü bir şefsin. Tarifin hem bilgilendirici hem de karakter dolu olsun.\n"
            f"{style_instruction}\n"
            "Tarife yaratıcı ve dikkat çekici bir başlıkla başla.\n"
            "Hazırlık ve pişirme sürelerini belirt.\n"
            "Tahmini kalori bilgisini ve sağlık tavsiyesi ekle.\n"
        )

        if ingredients.lower() in ("surprise", "sürpriz", "random"):
            ingredients = ", ".join(random.sample([
                "tavuk", "patates", "biber", "yumurta", "yoğurt", "domates", "makarna", "ıspanak", "süt"
            ], 3))
            prompt += f"Bu malzemelerle sürpriz bir tarif yaz: {ingredients}\n"
        else:
            prompt += f"Malzemeler: {ingredients}\nTarif:"

    else:  # English
        style_instruction_en = {
            "fun": "Write the recipe in a fun, friendly, conversational tone.",
            "pro": "Write the recipe like a professional chef, precise and technical.",
            "grandma": "Write the recipe like a sweet, nostalgic grandma would.",
            "blogger": "Write the recipe like a food blogger with personal anecdotes."
        }.get(style, "Write the recipe in a fun, friendly, conversational tone.")

        prompt = (
            "You are a world-class chef. Your recipe should be informative and full of personality.\n"
            f"{style_instruction_en}\n"
            "Start with a creative and catchy title.\n"
            "Include preparation and cooking times.\n"
            "Add estimated calories and a health tip.\n"
        )

        if ingredients.lower() in ("surprise", "sürpriz", "random"):
            ingredients = ", ".join(random.sample([
                "chicken", "potato", "pepper", "egg", "yogurt", "tomato", "pasta", "spinach", "milk"
            ], 3))
            prompt += f"Create a surprise recipe using these ingredients: {ingredients}\n"
        else:
            prompt += f"Ingredients: {ingredients}\nRecipe:"

    response = openai.Completion.create(
        model=MODEL_NAME,
        prompt=prompt,
        max_tokens=1000,
        temperature=0.9,
    )

    return response.choices[0].text.strip()


def get_language() -> str:
    while True:
        lang = input(MESSAGES["en"]["language_prompt"]).strip().lower()
        if lang in ("en", "tr"):
            return lang
        print("⚠️ Please enter 'en' or 'tr'.")


def get_style(language: str) -> str:
    choice = input(MESSAGES[language]["style_prompt"]).strip()
    return {
        "1": "fun",
        "2": "pro",
        "3": "grandma",
        "4": "blogger"
    }.get(choice, "fun")


def get_ingredients(msgs: dict[str, str]) -> str:
    while True:
        user_input = input(msgs["input_prompt"]).strip()
        if not user_input:
            print(msgs["input_empty"])
            continue
        if user_input.lower() in ("surprise", "sürpriz", "random"):
            return user_input

        ingredients = [item.strip() for item in user_input.split(",") if item.strip()]
        if len(ingredients) < 2:
            print(msgs["input_few"])
            continue
        return ", ".join(ingredients)


def main() -> None:
    language = get_language()
    msgs = MESSAGES[language]

    print(msgs["welcome"])
    print(msgs["start"])

    style = get_style(language)
    ingredients = get_ingredients(msgs)

    print(msgs["generating"])
    recipe = generate_recipe(ingredients, language=language, style=style)

    lines = recipe.split("\n")
    title = lines[0]
    body = "\n".join(lines[1:])

    print(msgs["result"])
    print(f"{title}\n{body}")

    if input(msgs["voice_prompt"]).strip().lower() in ("y", "e"):
        speak_text(recipe, language)

    if input(msgs["copy_prompt"]).strip().lower() in ("y", "e"):
        pyperclip.copy(recipe)
        print(msgs["copied"])

    print(msgs["closing"])


if __name__ == "__main__":
    main()
