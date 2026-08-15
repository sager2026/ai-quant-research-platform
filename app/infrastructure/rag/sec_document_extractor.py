from bs4 import BeautifulSoup


class SECDocumentExtractor:

    def extract(
        self,
        content: str,
    ) -> str:

        soup = BeautifulSoup(
            content,
            "html.parser",
        )

        for element in soup(
            [
                "script",
                "style",
                "noscript",
            ]
        ):
            element.decompose()

        text = soup.get_text(
            separator="\n"
        )

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        return "\n".join(lines)