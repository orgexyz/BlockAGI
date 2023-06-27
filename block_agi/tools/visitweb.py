from playwright.sync_api import sync_playwright
from pydantic import BaseModel, Field
from readability import Document
from html2text import HTML2Text
from block_agi.schema import BaseResourcePool


def extract_data(url: str) -> str:
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context()
            page = context.new_page()

            page.goto(url)

            # Get page content
            page_content = page.content()
            browser.close()

            doc = Document(page_content)

            h = HTML2Text()
            h.ignore_links = False

            content_html = doc.summary()
            content_markdown = h.handle(content_html)

            # Serialize everything into a JSON string
            # Limit the size of the string to 20,000 characters
            return content_markdown[:20000]
    except Exception as e:
        return "Error: Could not extract data from website."


from langchain.tools import Tool

# Visit Web Tool =================================


class VisitWebSchema(BaseModel):
    url: str = Field(title="URL", description="A url of website.")


def VisitWebTool(resource_pool: BaseResourcePool):
    def func(url: str) -> str:
        resource_pool.visit(url)
        return extract_data(url)

    return Tool.from_function(
        name="VisitWeb",
        func=func,
        description="Useful for when you need to visit a KNOWN website listed under RELEVANT LINKS and extract information from it.",
        args_schema=VisitWebSchema,
    )
