import streamlit as st
from langchain_groq import ChatGroq
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_classic.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.schema import HumanMessage, AIMessage
from tools.streamlit_tools import get_tools


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent_executor" not in st.session_state:
        st.session_state.agent_executor = None


def create_agent(groq_api_key: str, binance_api_key: str, binance_api_secret: str):
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=groq_api_key)

    tools = get_tools()

    # Add API keys to each tool call
    def add_api_keys_to_agent():
        pass

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a Binance Futures trading assistant. You help users place orders and check their account information on the Binance Futures Testnet.

Available tools:
- place_market_order: Place MARKET orders (BUY or SELL). Requires: symbol, side, quantity, api_key, api_secret
- place_limit_order: Place LIMIT orders with a specified price. Requires: symbol, side, quantity, price, api_key, api_secret
- get_account_balance: Check account balance. Requires: api_key, api_secret
- get_position_info: Get position information for a trading pair. Requires: symbol, api_key, api_secret

IMPORTANT: Always pass these parameters when calling tools:
- api_key: {binance_api_key}
- api_secret: {binance_api_secret}

When users want to place an order:
1. Ask for all required parameters if not provided
2. Confirm the order details before placing it
3. Use the appropriate tool to place the order
4. Report the result

Be concise and professional in your responses.""".format(
                    binance_api_key=binance_api_key,
                    binance_api_secret=binance_api_secret,
                ),
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


def display_message(role: str, content: str):
    with st.chat_message(role):
        st.markdown(content)


def main():
    st.set_page_config(
        page_title="Binance Futures Trading Assistant", page_icon="🤖", layout="wide"
    )

    init_session_state()

    st.title("🤖 Binance Futures Trading Assistant")
    st.markdown(
        "Chat with AI to place orders and manage your Binance Futures Testnet account"
    )

    with st.sidebar:
        st.header("🔑 API Configuration")

        binance_api_key = st.text_input(
            "Binance API Key",
            type="password",
            placeholder="Enter your Binance API Key",
            help="Get this from Binance Testnet API Management",
        )

        binance_api_secret = st.text_input(
            "Binance API Secret",
            type="password",
            placeholder="Enter your Binance API Secret",
            help="Get this from Binance Testnet API Management",
        )

        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="Enter your Groq API Key",
            help="Get this from console.groq.com",
        )

        st.divider()

        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.divider()

        st.subheader("ℹ️ Help")
        st.markdown("""
        **Example Commands:**
        - "Place a market buy order for 0.001 BTC"
        - "Sell 0.5 ETH at 3000"
        - "Check my account balance"
        - "What's my position on BTCUSDT?"
        
        **Note:** This uses Binance Futures Testnet. Make sure you have testnet API keys.
        """)

    if not all([binance_api_key, binance_api_secret, groq_api_key]):
        st.info("👈 Please enter your API keys in the sidebar to get started")
        return

    if st.session_state.agent_executor is None:
        with st.spinner("Initializing AI assistant..."):
            st.session_state.agent_executor = create_agent(
                groq_api_key, binance_api_key, binance_api_secret
            )
            st.success("AI assistant ready! Start chatting below.")

    for message in st.session_state.messages:
        display_message(message["role"], message["content"])

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_message("user", prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    chat_history = []
                    for msg in st.session_state.messages[:-1]:
                        if msg["role"] == "user":
                            chat_history.append(HumanMessage(content=msg["content"]))
                        else:
                            chat_history.append(AIMessage(content=msg["content"]))

                    response = st.session_state.agent_executor.invoke(
                        {"input": prompt, "chat_history": chat_history}
                    )

                    assistant_response = response["output"]
                    st.markdown(assistant_response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": assistant_response}
                    )

                except Exception as e:
                    error_message = f"❌ Error: {str(e)}"
                    st.error(error_message)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_message}
                    )


if __name__ == "__main__":
    main()
