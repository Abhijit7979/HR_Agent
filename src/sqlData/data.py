import sqlite3
from langchain_community.utilities import SQLDatabase
class SQLData:
    def create_data(self):
        conn = sqlite3.connect('resume.db')
        c = conn.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS resume (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            skills TEXT,
            experience INTEGER,
            job_role TEXT,
            date DATE
        )
        ''')
        # print("Table created.")

        # Insert data
        c.execute('''
        INSERT INTO resume (name, skills, experience, job_role, date) VALUES
('Abhijit Rao', 'Python, TensorFlow, Keras, OpenCV', 2, 'Machine Learning Engineer', '2025-10-01'),
('Priya Sharma', 'Python, Pandas, Scikit-learn, SQL', 1, 'Data Scientist', '2025-09-15'),
('Ravi Patel', 'PyTorch, CNN, NLP, Hugging Face', 3, 'AI Research Intern', '2025-08-10'),
('Sneha Iyer', 'R, Python, Matplotlib, Data Visualization', 2, 'Data Scientist', '2025-07-25'),
('Karan Mehta', 'Deep Learning, PyTorch, Computer Vision', 4, 'Machine Learning Engineer', '2025-06-18'),
('Ananya Das', 'NLP, Transformers, LLMs, LangChain', 2, 'AI Research Intern', '2025-05-22'),
('Rahul Nair', 'Machine Learning, Feature Engineering, Flask', 3, 'Machine Learning Engineer', '2025-04-11'),
('Meera Joshi', 'Data Cleaning, EDA, Statistical Modeling', 1, 'Data Scientist', '2025-03-05'),
('Vikram Singh', 'Reinforcement Learning, DQN, Gym', 2, 'AI Research Intern', '2025-02-28'),
('Divya Rao', 'Time Series Forecasting, XGBoost, MLflow', 3, 'Machine Learning Engineer', '2025-01-19');

                   ''')
        # print("Data inserted.")
        conn.commit()
        conn.close()

    def get_data(self):
        db = SQLDatabase.from_uri("sqlite:///src/sqlData/resume.db")
        
        # print("DB connected.")

        return db
        



# conn = SQLData()
# # conn.create_data()

# data = conn.get_data()
# rows=data.run("SELECT * FROM resume;")
# # print(rows)
# print(data.get_table_info())
       
# # for row in rows:
# #     print(f"ID: {row[0]}, Name: {row[1]}, Skills: {row[2]}, Experience: {row[3]} years, Job Role: {row[4]}, Date: {row[5]}")
