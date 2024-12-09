"""
title: Thinking Indicator
description: Adds a "Thinking..." visual indicator during API response processing and displays elapsed time.
author: Ryan526
author_url: https://github.com/Ryan526/Thinking
funding_url: https://github.com/open-webui
version: 0.1.1
license: MIT
requirements: asyncio, pydantic
environment_variables:
disclaimer: This filter is provided as is without any guarantees.
            Please ensure that it meets your requirements.
"""

import time
from typing import Any, Awaitable, Callable
from pydantic import BaseModel, Field


class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=15, description="Priority for executing the filter"
        )
        pass

    def __init__(self):
        self.start_time = None

    async def inlet(
        self,
        body: dict,
        __event_emitter__: Callable[[Any], Awaitable[None]] = None,
    ) -> dict:
        """
        This hook is invoked at the start of processing to show a "Thinking..." indicator.
        """
        self.start_time = time.time()

        # Emit "Thinking..." status to the event emitter
        await __event_emitter__(
            {
                "type": "status",
                "data": {"description": "Thinking...", "done": False},
            }
        )
        return body

    async def outlet(
        self,
        body: dict,
        __event_emitter__: Callable[[Any], Awaitable[None]] = None,
    ) -> dict:
        """
        This hook is invoked after the processing to calculate the elapsed time and show it.
        """
        end_time = time.time()
        elapsed_time = end_time - self.start_time

        # Emit elapsed time in seconds
        await __event_emitter__(
            {
                "type": "status",
                "data": {
                    "description": f"Thought for {int(elapsed_time)} seconds",
                    "done": True,
                },
            }
        )
        return body
