"""
Notion 에 작성된 나의 블로그 database 를 jekyll post 형태의 markdown 으로 변환하는 스크립트
"""

import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import notion_client
import pytz
import requests
from dateutil import parser
from dotenv import load_dotenv
from notion2md.exporter.block import StringExporter

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
JEKYLL_POSTS_DIR = os.getenv("JEKYLL_POSTS_DIR")
JEKYLL_IMG_DIR = os.getenv("JEKYLL_IMG_DIR")

jekyll_posts_dir = Path(JEKYLL_POSTS_DIR)
jekyll_posts_dir.mkdir(parents=True, exist_ok=True)

jekyll_img_dir = Path(JEKYLL_IMG_DIR)
jekyll_img_dir.mkdir(parents=True, exist_ok=True)

timezone = pytz.timezone("Asia/Seoul")


class PageMetadata:
    """블로그 글이 저장된 notion database 의 Page 1개에 대한 Metadata"""

    FORMAT_DATE = "%Y-%m-%d"
    FORMAT_DATETIME = "%Y-%m-%d %H:%M:%S %z"

    id: str
    title: str
    simple_name: str
    category: str
    subcategory: str
    has_toc: bool
    has_comments: bool
    has_mermaid: bool
    has_math_jax: bool
    is_published: bool
    tags: list[str]
    created_time: datetime
    last_edited_time: datetime

    def __init__(self, **kwargs):
        self.id = kwargs["id"]

        properties = kwargs["properties"]
        page_emoji = kwargs["icon"].get("emoji")
        self.title = properties["title"]["title"][0]["plain_text"]
        if page_emoji:
            self.title = f"{page_emoji} {self.title}"
        self.simple_name = properties["simple_name"]["rich_text"][0]["plain_text"]
        self.category = properties["category"]["select"]["name"]
        self.subcategory = properties["subcategory"]["select"]["name"]
        self.has_toc = properties["toc"]["checkbox"]
        self.has_comments = properties["comments"]["checkbox"]
        self.has_mermaid = properties["mermaid"]["checkbox"]
        self.has_math_jax = properties["math"]["checkbox"]
        self.is_published = properties["is_published"]["checkbox"]
        self.tags = [select["name"] for select in properties["tags"]["multi_select"]]

        self.created_time = parser.parse(kwargs["created_time"])
        self.created_time = self.created_time.astimezone(timezone)

        self.last_edited_time = parser.parse(kwargs["last_edited_time"])
        self.last_edited_time = self.last_edited_time.astimezone(timezone)

    @property
    def jekyll_post_file_name(self) -> str:
        """Jekyll 포스트 파일 이름 생성 (예: YYYY-MM-DD-title.md)"""
        date_part = self.created_time.strftime(self.FORMAT_DATE)

        # 공백을 하이픈으로
        title_part = self.simple_name.lower().replace(" ", "-")

        return f"{date_part}-{title_part}.md"

    def make_front_matter(self) -> str:
        front_matter = "---"
        front_matter += f"\ntitle: {self.title}"
        front_matter += f"\ndate: {self.created_time.strftime(self.FORMAT_DATETIME)}"
        front_matter += f"\ncategories: [{self.category}, {self.subcategory}]"
        front_matter += f"\ntags: {self.tags}"
        front_matter += f"\ntoc: {self.has_toc}".lower()
        front_matter += f"\ncomments: {self.has_comments}".lower()
        front_matter += f"\nmermaid: {self.has_mermaid}".lower()
        front_matter += f"\nmath: {self.has_math_jax}".lower()
        front_matter += "\n---"
        return front_matter


def fetch_unpublished_pages_metadata(notion: notion_client.Client) -> list[dict]:
    """
    블로그 글이 저장된 notion database 로 부터,
    블로그로 발행되지 않은 page 목록에 대한 metadata 를 반환
    """
    database = notion.databases.query(
        database_id=NOTION_DATABASE_ID,
        filter={
            "and": [
                {"property": "is_done", "checkbox": {"equals": True}},  # 다 작성했고,
                {  # 블로그 글로 발행되지 않았다.
                    "property": "is_published",
                    "checkbox": {"equals": False},
                },
            ]
        },
    )
    return database["results"]


def download_and_replace_image_url(match: re.Match) -> str:
    """image url 을 찾아서 다운로드 한 뒤, 그 파일 경로를 가지로 markdown 형식의 이미지를 반환하는 함수"""
    alt_text = match.group(1)
    image_url = match.group(2)
    print("    ", "downloading and replacing an image;", alt_text)

    parsed_url = urlparse(image_url)
    filename = os.path.basename(parsed_url.path)
    if not os.path.splitext(filename)[1]:  # 확장자 없으면 추가
        filename += ".jpg"
    local_image_path = jekyll_img_dir / filename

    res = requests.get(image_url, stream=True)
    if res.status_code != 200:  # 이미지 다운로드 못 받으면, 그대로 사용하도록
        return match.group(0)

    with open(local_image_path, "wb") as img_file:
        for chunk in res.iter_content(chunk_size=4096):
            img_file.write(chunk)

    return f"![{alt_text}](/{local_image_path})"


def convert_to_jekyll_md(notion: notion_client.Client):
    raw_pages_meta = fetch_unpublished_pages_metadata(notion)

    if not raw_pages_meta:
        print("Nothing to convert.")
        return

    for raw_page_meta in raw_pages_meta:
        print("-" * 80)

        page_meta = PageMetadata(**raw_page_meta)
        print("Start converting a page;", page_meta.title)

        filename = jekyll_posts_dir / page_meta.jekyll_post_file_name
        md_content = StringExporter(
            block_id=page_meta.id, token=NOTION_API_KEY
        ).export()

        print("    ", "processing images...")
        image_pattern = r"!\[(.*?)\]\((https?://[^)]+)\)"
        final_content = re.sub(
            image_pattern, download_and_replace_image_url, md_content
        )

        with open(filename, "w") as f:
            f.write(page_meta.make_front_matter())
            f.write("\n\n")
            f.write(final_content)

        print("Done")
        print("-" * 80)


def main():
    try:
        if not NOTION_API_KEY:
            raise RuntimeError("Notion API Key is not set")

        if not NOTION_DATABASE_ID:
            raise RuntimeError("Notion Database ID is not set")

        if not JEKYLL_POSTS_DIR:
            raise RuntimeError("Jekyll post directory is not set")

        if not JEKYLL_IMG_DIR:
            raise RuntimeError("Jekyll image directory is not set")

        notion = notion_client.Client(auth=NOTION_API_KEY)

        convert_to_jekyll_md(notion)
    except Exception as e:
        print("=" * 80)
        print("ERROR!")
        print(e)


if __name__ == "__main__":
    main()
