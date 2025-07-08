from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()


def get_product_details():
    return {
        "name": "SuperPhone X",
        "category": "Smartphones",
        "specifications": "8GB RAM, 256GB Storage, 5000mAh Battery",
        "price": "$699",
        "brand": "Apple",
    }


def main():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    get_product_function = {
        "name": "get_product_details",
        "description": "Fetches product details including name, category, specifications, and price",
        "parameters": {"type": "object", "properties": {}, "required": []},
    }

    tools = types.Tool(function_declarations=[get_product_function])
    config = types.GenerateContentConfig(tools=[tools])

    print("Product Assistant - Ask me about Stuff")

    while True:
        user_query = input("You: ").strip()

        if user_query.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        if not user_query:
            continue

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash", contents=user_query, config=config
            )

            function_call_found = False
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    function_call = part.function_call
                    print(f"Calling function: {function_call.name}()")
                    function_call_found = True

                    if function_call.name == "get_product_details":
                        result = get_product_details()

                        function_response_part = types.Part.from_function_response(
                            name=function_call.name,
                            response={"result": result},
                        )

                        contents = [
                            types.Content(
                                role="user", parts=[types.Part(text=user_query)]
                            )
                        ]
                        contents.append(response.candidates[0].content)
                        contents.append(
                            types.Content(role="user", parts=[function_response_part])
                        )

                        final_response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            config=config,
                            contents=contents,
                        )

                        final_text_parts = [
                            part.text
                            for part in final_response.candidates[0].content.parts
                            if part.text
                        ]
                        if final_text_parts:
                            print(f"Assistant: {' '.join(final_text_parts)}")
                        else:
                            print(
                                "Assistant: I got the product details but couldn't format a response."
                            )
                    else:
                        print(f"Unknown function: {function_call.name}")
                    break

            if not function_call_found:
                text_parts = [
                    part.text
                    for part in response.candidates[0].content.parts
                    if part.text
                ]
                if text_parts:
                    print(f"Assistant: {' '.join(text_parts)}")
                else:
                    print("Assistant: I can only help with product details.")

        except Exception as e:
            print(f"Error: {e}")
            print("Make sure you have set the GEMINI_API_KEY environment variable")

        print()


main()
