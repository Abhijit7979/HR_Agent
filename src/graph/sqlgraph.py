from langgraph.graph import START, StateGraph,END
from src.state.sqlState import State
from src.nodes.sql_nodes import write_query,execute_query,generate_answer
from IPython.display import Image, display

class sqlGraph:

    def workflow(self):
        builder=StateGraph(State)
        builder.add_node("write_query",write_query)
        builder.add_node("execute_query",execute_query)
        builder.add_node("generate_answer",generate_answer)

        builder.add_edge(START,"write_query")
        builder.add_edge("write_query","execute_query")
        builder.add_edge("execute_query","generate_answer")
        builder.add_edge("generate_answer",END)
        graph = builder.compile()

        return graph
    
    def graph_img(self):
        graph=self.workflow()
        graph.get_graph().draw_mermaid_png(output_file_path="sql_graph.png")
        

