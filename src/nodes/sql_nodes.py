from typing_extensions import Annotated
from typing_extensions import TypedDict
from src.state.sqlState import State
from src.prompts.sys_msg import sys_pro
from src.llms.groqllm import Groqllm
from src.sqlData.data import SQLData 
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool

class QueryOutput(TypedDict):
    """Generated SQL query."""

    query: Annotated[str, ..., "Syntactically valid SQL query."]


def write_query(state: State):
        """Generate SQL query to fetch information."""
        query_prompt_template=sys_pro.get_prompt(state["question"])
        groq = Groqllm()
        llm = groq.get_llm()
        data=SQLData()
        db=data.get_data()
        prompt = query_prompt_template.invoke(
            {
                "dialect": db.dialect,
                "top_k": 10,
                "table_info": db.get_table_info(),
                "input": state["question"],
            }
        )
        structured_llm = llm.with_structured_output(QueryOutput)
        result = structured_llm.invoke(prompt)
        return {"query": result["query"]}

def execute_query(state: State):
        """Execute SQL query."""
        data=SQLData()
        db=data.get_data()
        execute_query_tool = QuerySQLDatabaseTool(db=db)
        return {"result": execute_query_tool.invoke(state["query"])}

def generate_answer(state: State):
        """Answer question using retrieved information as context."""
        groq = Groqllm()
        llm = groq.get_llm()
        prompt = (
            "Given the following user question, corresponding SQL query, "
            "and SQL result, answer the user question.\n\n"
            f"Question: {state['question']}\n"
            f"SQL Query: {state['query']}\n"
            f"SQL Result: {state['result']}"
        )
        response = llm.invoke(prompt)
        return {"answer": response.content} 