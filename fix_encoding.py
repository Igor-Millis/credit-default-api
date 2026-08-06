from pathlib import Path

path = Path("streamlit/app.py")

# Backup
backup = path.with_name("app_before_encoding_fix.py")
backup.write_bytes(path.read_bytes())

text = path.read_text(encoding="utf-8-sig")

replacements = {
    "Ã¡": "á",
    "Ã¢": "â",
    "Ã£": "ã",
    "Ã¤": "ä",
    "Ã©": "é",
    "Ãª": "ê",
    "Ã­": "í",
    "Ã³": "ó",
    "Ã´": "ô",
    "Ãµ": "õ",
    "Ãº": "ú",
    "Ã§": "ç",
    "Ã€": "À",
    "Ã‰": "É",
    "Ã“": "Ó",
    "Ãš": "Ú",
    "Ã‡": "Ç",
    "NÃ­vel": "Nível",
    "PÃ³s-graduaÃ§Ã£o": "Pós-graduação",
    "Ensino mÃ©dio": "Ensino médio",
    "crÃ©dito": "crédito",
    "inadimplÃªncia": "inadimplência",
    "previsÃ£o": "previsão",
    "histÃ³ricos": "históricos",
    "atravÃ©s": "através",
    "InformaÃ§Ãµes": "Informações",
    "Limite de crÃ©dito": "Limite de crédito",
    "educaÃ§Ã£o": "educação",
    "ausÃªncia": "ausência",
    "situaÃ§Ãµes": "situações",
    "especÃ­ficas": "específicas",
    "atrÃ¡s": "atrás",
    "ClassificaÃ§Ã£o": "Classificação",
    "Probabilidade de inadimplÃªncia": "Probabilidade de inadimplência",
    "requisiÃ§Ã£o": "requisição",
    "NÃ£o": "Não",
    "possÃ­vel": "possível",
    "Ã ": "à",
    "estÃ¡": "está",
    "execuÃ§Ã£o": "execução",
    "demorou": "demorou",
    "mÃªs": "mês",
    "mÃªses": "meses",
    "informaÃ§Ã£o": "informação",
    "classificaÃ§Ã£o": "classificação",
    "determina": "determina",
    "realizar previsÃ£o": "realizar previsão",
    "Resultado da previsÃ£o": "Resultado da previsão",
    "Como a classificaÃ§Ã£o": "Como a classificação",
    "inadimplÃªncia de": "inadimplência de",
    "thresholde": "threshold",
}

for old, new in replacements.items():
    text = text.replace(old, new)

# Emojis corrompidos
emoji_replacements = {
    "ðŸ’³": "💳",
    "ðŸ‘¤": "👤",
    "ðŸ“Š": "📊",
    "ðŸ’°": "💰",
    "ðŸ’µ": "💵",
    "ðŸ”Ž": "🔎",
    "ðŸ“ˆ": "📈",
    "âš ï¸\x8f": "⚠️",
    "âœ…": "✅",
    "â„¹ï¸\x8f": "ℹ️",
    "âŒ": "❌",
    "â±ï¸\x8f": "⏱️",
    "â€”": "—",
}

for old, new in emoji_replacements.items():
    text = text.replace(old, new)

path.write_text(text, encoding="utf-8")

print("Correção concluída.")
print(f"Backup criado em: {backup}")