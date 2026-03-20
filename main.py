from agno.agent import Agent

from src.agno.copilot import Copilot
from src.agno.lib import get_access_token_from_copilot


def main():
    agent = Agent(
        name="MyAgent",
        description="An example agent that performs a simple task.",
        model=Copilot(id="gpt-4.1", api_key=get_access_token_from_copilot()),
    )

    agent.print_response("Hello, I'm Satadeep")


if __name__ == "__main__":
    main()
