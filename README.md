# HR_Agent

Simple HR SQL Agent powered by LangGraph and LLMs . It generates SQL from a natural language question, executes it on a local SQLite DB (`resume.db`), and returns an answer.

```bash
# step 1 : clone repo 

# step 2 : uv init 

# step 3 : uv sync 

# step 4 : create .env file 

# step 5 : streamlit run app.py   
```
## Graph workflow 
![](sql_graph.png)

Then open the provided local URL in your browser. Type a question like:

- How many rows are there?
- List names of candidates with 2 years of experience.


## OutPut 
![](output.jpeg)

## Notes
- The agent uses `langgraph` to orchestrate nodes that write SQL, execute it, and generate a final answer.

