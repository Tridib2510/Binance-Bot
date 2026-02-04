from tools.binance_tools import tools
from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_classic.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
from dotenv import load_dotenv
from logger import setup_logger

logger = setup_logger(__name__)
load_dotenv()


def create_agent():
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        logger.error("GROQ_API_KEY environment variable is required")
        raise ValueError("GROQ_API_KEY environment variable is required")

    logger.info(f"Creating Groq agent with model: llama-3.3-70b-versatile")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=groq_api_key)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a Binance Futures trading assistant. You help users place orders and check their account information on the Binance Futures Testnet.

Available tools:
- place_market_order: Place MARKET orders (BUY or SELL)
- place_limit_order: Place LIMIT orders with a specified price
- get_account_balance: Check account balance
- get_position_info: Get position information for a trading pair

When users want to place an order:
1. Ask for all required parameters if not provided
2. Confirm the order details before placing it
3. Use the appropriate tool to place the order
4. Report the result

Be concise and professional in your responses.""",
            ),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
    )

    return agent_executor


def main():
    logger.info("Starting Binance Futures Trading Assistant")
    print("🤖 Binance Futures Trading Assistant (Groq)")
    print("Type 'exit' or 'quit' to end the conversation\n")

    agent_executor = create_agent()
    chat_history = []

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            logger.info("User requested to exit")
            print("Goodbye! 👋")
            break

        if not user_input:
            continue

        logger.debug(f"User input: {user_input}")

        try:
            response = agent_executor.invoke(
                {"input": user_input, "chat_history": chat_history}
            )

            print(f"\nAssistant: {response['output']}\n")

            chat_history.append(("human", user_input))
            chat_history.append(("ai", response["output"]))

        except Exception as e:
            logger.error(f"Error processing user input: {str(e)}")
            print(f"\n❌ Error: {str(e)}\n")


if __name__ == "__main__":
    main()
