"""
title: Thinking Indicator
description: Adds a "Thinking..." visual indicator during API response processing and displays elapsed time.
author: Ryan526
author_url: https://github.com/Ryan526/Thinking
funding_url: https://github.com/open-webui
version: 0.2.0
license: MIT
requirements: asyncio, pydantic
environment_variables:
disclaimer: This filter is provided as is without any guarantees.
            Please ensure that it meets your requirements.
"""

import time
import asyncio
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
        self.is_thinking = False

    async def _update_thinking_status(
        self, __event_emitter__: Callable[[Any], Awaitable[None]]
    ):
        """
        Continuously update "Thinking..." status with elapsed time every second.
        """
        while self.is_thinking:
            elapsed_time = int(time.time() - self.start_time)
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"Still Thinking... for {elapsed_time} seconds so far",
                        "done": False,
                    },
                }
            )
            await asyncio.sleep(1)

    async def inlet(
        self,
        body: dict,
        __event_emitter__: Callable[[Any], Awaitable[None]] = None,
    ) -> dict:
        """
        This hook is invoked at the start of processing to show a "Thinking..." indicator.
        """
        self.start_time = time.time()
        self.is_thinking = True

        # Start a background task to update the "Thinking..." status
        asyncio.create_task(self._update_thinking_status(__event_emitter__))

        return body

    async def outlet(
        self,
        body: dict,
        __event_emitter__: Callable[[Any], Awaitable[None]] = None,
    ) -> dict:
        """
        This hook is invoked after the processing to calculate the elapsed time and show it.
        """
        self.is_thinking = False
        end_time = time.time()
        elapsed_time = end_time - self.start_time

        # Emit final "done" status with total elapsed time
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
