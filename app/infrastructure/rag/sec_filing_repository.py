import requests

from app.domain.entities.filing import Filing
from app.domain.repositories.filing_repository import FilingRepository


class SECFilingRepository(FilingRepository):

    TICKER_URL = "https://www.sec.gov/files/company_tickers.json"

    SUBMISSIONS_URL = (
        "https://data.sec.gov/submissions/CIK{cik}.json"
    )

    ARCHIVES_URL = (
        "https://www.sec.gov/Archives/edgar/data/"
        "{cik}/{accession}/{document}"
    )

    def __init__(
        self,
        user_agent: str,
        timeout: int = 30,
    ):
        self.headers = {
            "User-Agent": user_agent,
            "Accept-Encoding": "gzip, deflate",
        }

        self.timeout = timeout

    def get_filing(
        self,
        ticker: str,
        filing_type: str,
    ) -> Filing:

        ticker = ticker.upper()

        cik = self._get_cik(
            ticker
        )

        submission = self._get_submission(
            cik
        )

        recent = submission["filings"]["recent"]

        for index, form in enumerate(
            recent["form"]
        ):

            if form == filing_type:

                accession_number = (
                    recent["accessionNumber"][index]
                )

                filing_date = (
                    recent["filingDate"][index]
                )

                primary_document = (
                    recent["primaryDocument"][index]
                )

                filing_url = self._build_filing_url(
                    cik=cik,
                    accession_number=accession_number,
                    primary_document=primary_document,
                )

                content = self._download_filing(
                    filing_url
                )

                return Filing(
                    ticker=ticker,
                    filing_type=filing_type,
                    filing_date=filing_date,
                    content=content,
                    source=filing_url,
                )

        raise ValueError(
            f"No {filing_type} filing found for {ticker}"
        )

    def _get_cik(
        self,
        ticker: str,
    ) -> str:

        response = requests.get(
            self.TICKER_URL,
            headers=self.headers,
            timeout=self.timeout,
        )

        response.raise_for_status()

        companies = response.json()

        for company in companies.values():

            if company["ticker"].upper() == ticker:

                return str(
                    company["cik_str"]
                ).zfill(10)

        raise ValueError(
            f"Ticker not found in SEC data: {ticker}"
        )

    def _get_submission(
        self,
        cik: str,
    ) -> dict:

        url = self.SUBMISSIONS_URL.format(
            cik=cik
        )

        response = requests.get(
            url,
            headers=self.headers,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def _build_filing_url(
        self,
        cik: str,
        accession_number: str,
        primary_document: str,
    ) -> str:

        cik_without_leading_zeros = str(
            int(cik)
        )

        accession_without_dashes = (
            accession_number.replace("-", "")
        )

        return self.ARCHIVES_URL.format(
            cik=cik_without_leading_zeros,
            accession=accession_without_dashes,
            document=primary_document,
        )

    def _download_filing(
        self,
        filing_url: str,
    ) -> str:

        response = requests.get(
            filing_url,
            headers=self.headers,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.text