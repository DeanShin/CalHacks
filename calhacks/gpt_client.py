import os
import asyncio
import openai
import pickle


if not os.environ.get("OPENAI_API_KEY"):
    raise Exception("OpenAI api key not set")


class ChatGPT:
    def __init__(self, user_context: str, user_answer: str):
        """
        Parameters
        ----------
        user_context : str
            Frontend input that lets user define scope of interview
            questions
        """
        self.user_context = user_context
        self.count = 0
        self.questions = list[str]
        self.advice = ""
        self.user_answer = ""

    async def _generate_questions(self) -> dict:
        print('\t-generating questions')
        prompt = f"""Generate me a list of 10 technical interview questions.
                    5 of which will focus on {self.user_context}. The remaining 5 will be behavioural.
                    Just output the list numbered 1-10. Do not include labels. Do not a response verifying my message"""

        # Prompt chatgpt
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful interviewer that will help me prep for my {self.user_context} interview",
                },
                {"role": "user", "content": f"{prompt}"},
            ],
        )
        # return response["choices"][0]["message"]["content"]
        return response

    def _parse_questions(self, questions_raw: dict) -> list[str]:
        print('\t-parsing questions')
        raw = questions_raw["choices"][0]["message"]["content"]
        #with open('questions_raw.txt', 'a+') as f:
        #    f.write(raw)
        #    f.write("\n")

        return raw.split("\n")

    async def set_questions(self) -> None:
        print('\t-set questions')
        questions = await self._generate_questions()
        self.questions = self._parse_questions(questions)

    async def _generate_advice(self) -> str:
        print('\t-generating advice')
        prompt = f"""I was asked as an interviewee {self.user_context} And I responded with {self.user_answer}. What advice do you have for me?"""

        # prompt chatgpt
        advice = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You will act as a coding interview coach that gives concise advice."
                    },
                    {"role": "user", "content": f"{prompt}"},
                ],
        )
        return advice

    def _parse_advice(self, advice_raw: dict) -> list[str]:
        print('\t-parsing advice')
        raw = advice_raw["choices"][0]["message"]["content"]
        with open('advice_raw.txt', 'a+') as f:
            f.write(raw)

        return raw

    async def get_advice(self) -> None:
        print('\t-get advice')
        advice = await self._generate_advice()
        self.advice = self._parse_advice(advice)

"""
async def main():
    client = ChatGPT("What is chmod in Linux?")
    #questions = await client.set_questions()
    #print(client.questions)
    advice = await client.get_advice()
    print(client.advice)
if __name__ == "__main__":
    asyncio.run(main())
"""
