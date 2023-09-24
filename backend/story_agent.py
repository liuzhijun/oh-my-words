import traceback
from typing import List, Tuple

from loguru import logger
from pydantic import BaseModel, Field
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import (
    PydanticOutputParser,
    OutputFixingParser,
)

from LLM import OpenAIChat


TEMPLATE = """\
please write a story at least 5 sentences long, using the words [{words}].
The word should be in the same order as the words in the prompt.
The word should be surrounded by square brackets.
Please response the story in the following format.
English: ...[word1]...[word2]...
Chinese: ...[单词1]...[单词2]..

{format}
"""

class Story(BaseModel):
    story: str = Field(description="the story")
    translated_story: str = Field(description="the translated story")

llm = OpenAIChat(model_name="gpt-3.5-turbo", temperature=0.3)
parser = PydanticOutputParser(pydantic_object=Story)
prompt_template = PromptTemplate(
    template=TEMPLATE,
    input_variables=["words"],
    partial_variables={
        "format": parser.get_format_instructions(),
    }
)
parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    output_parser=parser,
    verbose=True,
)

def tell_story(words: List[str]):
    while True:
        try:
            resp: Story = chain.run(", ".join(words))
            return resp
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error("retrying...")
            continue

def generate_story_and_translated_story(words: List[str]) -> Tuple[str, str]:
    resp = tell_story(words)
    return resp.story, resp.translated_story


