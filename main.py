from src.graph.sqlgraph import sqlGraph
from src.sqlData.data import SQLData

db=SQLData()
# db.create_data()
db=db.get_data()
print(db.dialect)
print(db.get_usable_table_names())

# builder=sqlGraph()
# graph=builder.workflow()

# print(graph.invoke({"question": "How many rows are there?"}))
# for step in graph.stream(
#     {"question": "How many employees are there?"}, stream_mode="updates"
# ):
#     print(step)