from generator import generate_recipe


MESSAGES = {
    "en": {
        "welcome": "\n👩‍🍳 Welcome to SmartCook – Your AI Sous Chef!",
        "start": "Let’s whip up something delicious together. 🍲\n",
        "input_prompt": "🧺 Enter ingredients (comma-separated, e.g., chicken, rice, garlic): ",
        "input_empty": "⚠️ Please enter at least one ingredient.\n",
        "input_few": "⚠️ Please enter at least two ingredients for a better recipe.\n",
        "language_prompt": "🌍 Choose a language / Dil seç (en/tr): ",
        "generating": "\n🍽️ Generating your unique recipe...\n",
        "result": "📄 Here’s your recipe:\n",
        "closing": "\n🌟 Bon appétit!\n"
    },
    "tr": {
        "welcome": "\n👩‍🍳 SmartCook’a hoş geldin – Yapay zekalı yardımcı şefin burada!",
        "start": "Hadi birlikte lezzetli bir şeyler yapalım. 🍲\n",
        "input_prompt": "🧺 Malzemeleri gir (virgülle ayır, örn: tavuk, pirinç, sarımsak): ",
        "input_empty": "⚠️ Lütfen en az bir malzeme gir.\n",
        "input_few": "⚠️ Daha iyi bir tarif için en az iki malzeme gir.\n",
        "language_prompt": "🌍 Choose a language / Dil seç (en/tr): ",
        "generating": "\n🍽️ Tarif oluşturuluyor...\n",
        "result": "📄 İşte tarifin:\n",
        "closing": "\n🌟 Afiyet olsun!\n"
    }
}


def get_language() -> str:
    """Dil seçimi alır ve geçerli dil kodunu döner."""
    while True:
        lang = input(MESSAGES["en"]["language_prompt"]).strip().lower()
        if lang in ("en", "tr"):
            return lang
        print("⚠️ Please enter 'en' or 'tr'.")


def get_ingredients(msgs: dict[str, str]) -> str:
    """Kullanıcıdan malzeme listesini alır ve temizler."""
    while True:
        user_input = input(msgs["input_prompt"]).strip()
        if not user_input:
            print(msgs["input_empty"])
            continue

        ingredients = [item.strip() for item in user_input.split(",") if item.strip()]
        if len(ingredients) < 2:
            print(msgs["input_few"])
            continue

        return ", ".join(ingredients)


def main() -> None:
    """SmartCook tarif üreticisinin ana giriş noktası."""
    language = get_language()
    msgs = MESSAGES[language]

    print(msgs["welcome"])
    print(msgs["start"])

    ingredients = get_ingredients(msgs)

    print(msgs["generating"])
    recipe = generate_recipe(ingredients, language=language)

    print(msgs["result"])
    print(recipe)
    print(msgs["closing"])


if __name__ == "__main__":
    main()
