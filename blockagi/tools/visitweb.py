from playwright.sync_api import sync_playwright
from pydantic import BaseModel, Field
from html2text import HTML2Text
from blockagi.schema import BaseResourcePool


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

            # Convert HTML to Markdown
            h = HTML2Text()
            h.ignore_links = False

            content_markdown = h.handle(page_content)

            # Serialize everything into a JSON string
            # Limit the size of the string to 20,000 characters
            return content_markdown[:20000]
    except Exception as e:
        return "Error: Could not extract data from website."


from langchain.tools import Tool

# Visit Web Tool =================================


class VisitWebSchema(BaseModel):
    url: str = Field(title="URL", description="A url in RESOURCE POOL.")


def VisitWebTool(resource_pool: BaseResourcePool):
    def func(url: str) -> str:
        resource_pool.visit(url)
        return extract_data(url)

    return Tool.from_function(
        name="VisitWeb",
        func=func,
        description="Useful for when you need to visit a website in the RESOURCE POOL and extract information from it.",
        args_schema=VisitWebSchema,
    )
