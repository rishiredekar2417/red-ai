from pathlib import Path

from app.context.builder import ContextBuilder


class PromptBuilder:

    def __init__(self, root: Path):

        self.context = ContextBuilder(root)

    def build(
        self,
        user_prompt: str,
        history=None,
    ):

        ctx = self.context.build(
            user_prompt,
            history,
        )

        history_text = ""

        if history:

            history_text = "\n".join(
                f"{message.role.upper()}: {message.content}"
                for message in history
            )

        return f"""
You are Red AI.

You are an expert software engineer.

========================
CONVERSATION HISTORY
========================

{history_text}

========================
PROJECT CONTEXT
========================

Project Files:

{chr(10).join(ctx.files)}

Project Summary:

{ctx.content}

========================
USER REQUEST
========================

{user_prompt}

========================
INSTRUCTIONS
========================

Answer ONLY using the supplied project context.

Use the conversation history whenever it is relevant.

If the answer cannot be determined from the supplied context,
say that more project information is needed.

Never invent files.

Never invent functions.

Never hallucinate.
"""