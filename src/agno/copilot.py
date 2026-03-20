from agno.models.openai import OpenAILike


class Copilot(OpenAILike):
    def __init__(self, id: str, api_key: str, **kwargs):
        super().__init__(
            id=id,
            base_url="https://api.githubcopilot.com/",
            api_key=api_key,
            extra_headers={
                "editor-version": "vscode/1.104.0",
                "editor-plugin-verion": "copilot.vim/1.16.0",
                "user-agent": "GithubCopilot/1.155.0",
                "Copilot-Vision-Request": "true",
            },
            **kwargs,
        )
