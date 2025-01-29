import sys
from LLM import LLMClient
from CodeToXML import convert_code_to_xml
from IssueToXML import convert_issue_to_xml
import constants

class Chatbot:
    def __init__(self, code_input):
        self.llm_client = LLMClient(code_input)

    def run(self):

        print("\nNOW, TYPE YOUR QUERY BELOW: "
               "\n'generate documentation' TO AUTOMATICALLY GENERATE A MARKDOWN DESCRIPTION FOR YOUR CODE."
                "\n'investigate issue' TO UNDERSTAND A GITHUB ISSUE FOR YOUR CODE AND GET HELP IN RESOLVING IT."
                "\n'exit' TO QUIT."
                "\nANY QUESTION THAT YOU MAY HAVE ABOUT THE CODE.")

        while True:
            query = input("\nQuery: ").strip()

            # Exit condition
            if query.lower() == "exit":
                print("Goodbye!")
                break

            try:
                if query.lower() == "generate documentation":
                    prompt = constants.DOCUMENT_GENERATION_QUERY
                    print("Generating a write-up..")

                elif query.lower() == "investigate issue":
                    issue_url = input("Please enter the issue URL.\n")
                    convert_issue_to_xml(issue_url)
                    with open("compressed_Issue_XML_output.txt") as compressed_xml_issue_file:
                        issue_data = compressed_xml_issue_file.read()

                    prompt = constants.ISSUE_INVESTIGATION_PROMPT + issue_data

                else:
                    prompt = query

                response = self.llm_client.get_response_to_query(prompt)
                print("\nResponse:\n")
                print(response)
            except Exception as e:
                print(f"An error occurred while generating a response: {e}")

if __name__ == "__main__":

    print("THANK YOU FOR USING CODECHAT!"
          "\nYOUR CODE WILL FIRST BE CONVERTED TO XML AS THAT MAKES LLM INFERENCE MORE ACCURATE."
          "\nAN INITIAL SUMMARY WILL BE GENERATED, YOU CAN ASK ME QUESTIONS AFTER THAT!")

    url_or_path = input("\nPlease input the local path or the URL of a code repository.\n")

    convert_code_to_xml(url_or_path)

    with open("compressed_XML_output.txt") as compressed_xml_code_file:
        code_data = compressed_xml_code_file.read()

    chatbot = Chatbot(code_data)
    chatbot.run()
