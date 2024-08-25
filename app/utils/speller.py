from typing import Iterable, Optional

import httpx


class Speller:
    def __init__(self):
        self._lang = ["ru", "en"]
        self._api_query = (
            "https://speller.yandex.net/services/spellservice.json/checkTexts"
        )

    async def spelled_texts(self, *texts: Iterable[str]) -> list[str]:
        changes = await self._spell_texts(*texts)
        return self._apply_suggestions(texts, changes)

    async def _spell_texts(self, *texts: Iterable[str]) -> list[list[Optional[dict]]]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self._api_query,
                data={"text": texts, "lang": ",".join(self._lang)},
            )
            return response.json()

    def _apply_suggestions(
        self, texts: Iterable[str], all_changes: list[list[Optional[dict]]]
    ) -> list[str]:
        corrected_texts = []
        for text, text_changes in zip(texts, all_changes):
            if text_changes:
                for change in text_changes:
                    if change and "word" in change and "s" in change and change["s"]:
                        word = change["word"]
                        suggestion = change["s"][0]
                        text = text.replace(word, suggestion)
            corrected_texts.append(text)

        return corrected_texts


speller = Speller()
