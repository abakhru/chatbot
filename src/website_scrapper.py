#!/usr/bin/env python
import uuid
from pathlib import Path

from pywebcopy import save_website


class WebsiteScrapper:
    def __init__(self, project_name=None, page_url=None):
        self.url = None
        self.dest_dir = "/tmp"
        if project_name is None:
            self.project_name = str(uuid.uuid4())
        self.page_url = page_url

    def scrap_website(self):
        kwargs = {"project_name": self.project_name}
        save_website(url=self.page_url, project_folder=self.dest_dir, **kwargs)

    def gather_all_htmls(self):
        html_files = Path(self.dest_dir, self.project_name).rglob("*.html")
        return html_files


if __name__ == "__main__":
    p = WebsiteScrapper(project_name="mitre", page_url="https://attack.mitre.org/")
    p.scrap_website()
