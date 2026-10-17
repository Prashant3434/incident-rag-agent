from openai import OpenAI


class LLM:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    def call(self, messages, tools, model_name):

        response_stream = self.client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools,
            stream=True,
        )


        response_content = ""
        tool_responses = {}

        for response_chunk in response_stream:
            if not response_chunk.choices:
                continue

            choice = response_chunk.choices[0]
            delta = choice.delta

            if delta.content:
                response_content += delta.content

            if delta.tool_calls:
                for tool_chunk in delta.tool_calls:
                    tool_index = tool_chunk.index

                    if tool_index not in tool_responses:
                        tool_responses[tool_index] = {
                            "id": "",
                            "type": "function",
                            "function": {
                                "name": "",
                                "arguments": "",
                            },
                        }

                    if tool_chunk.id is not None:
                        tool_responses[tool_index]["id"] += tool_chunk.id

                    if tool_chunk.function:
                        if tool_chunk.function.name:
                            tool_responses[tool_index]["function"]["name"] += (
                                tool_chunk.function.name
                            )

                        if tool_chunk.function.arguments:
                            tool_responses[tool_index]["function"]["arguments"] += (
                                tool_chunk.function.arguments
                            )

            if choice.finish_reason == "tool_calls":
                return {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        tool_responses[index]
                        for index in sorted(tool_responses)
                    ],
                }

            if choice.finish_reason is not None:
                return {
                    "role": "assistant",
                    "content": response_content,
                }

        return {
            "role": "assistant",
            "content": response_content,
        }