import streamlit as st
from openai import OpenAI
import sqlite3


client = OpenAI()

# Generatate SQL queries
def generate_sql(question):
    
    # Database schema for the music database
    schema = '''
    CREATE TABLE album (
    albumID INTEGER PRIMARY KEY,
    name VARCHAR(40),
    year INTEGER,
    artistID INTEGER,
    FOREIGN KEY (artistID) REFERENCES artist (artistID) ON DELETE CASCADE
    )
    CREATE TABLE artist (
    artistID INTEGER PRIMARY KEY,
    name VARCHAR(40)
    )
    CREATE TABLE featuredOn (
    artistID INTEGER NOT NULL,
    songID INTEGER NOT NULL,
    PRIMARY KEY (artistID, songID),
    FOREIGN KEY (artistID) REFERENCES artist (artistID) ON DELETE CASCADE,
    FOREIGN KEY (songID) REFERENCES song (songID) ON DELETE CASCADE
    )
    CREATE TABLE song (
    songID INTEGER PRIMARY KEY,
    name VARCHAR(40),
    duration INTEGER,
    year INTEGER,
    artistID,
    FOREIGN KEY (artistID) REFERENCES artist (artistID) ON DELETE CASCADE
    )
    CREATE TABLE songOnAlbum (
    songID INTEGER NOT NULL,
    albumID INTEGER NOT NULL,
    PRIMARY KEY (songID, albumID),
    FOREIGN KEY (songID) REFERENCES song (songID) ON DELETE CASCADE,
    FOREIGN KEY (albumID) REFERENCES album (albumID) ON DELETE CASCADE
    )
    '''
    prompt = f'''
    You are an SQL expert specializing in SQLite3 queries. 
    Your task is to generate a correct SQLite3 query based on a user question.
    Given the user question, produce a SQLite3 query which, following the exact database schema provided below

    SQL Schema: {schema}

    Instructions
    Only return the raw SQL query without any explanations, formatting, markdown, or extra text.
    Do NOT include backticks (```) or language markers like ```sql.
    Use only the tables and columns from the provided schema**. Do not assume additional tables or fields.
    Ensure that the SQL query is correctly formatted for execution in SQLite3.

    Examples of correct SQL queries:

    User Question: How many artists are there in the database?
    Answer: SELECT COUNT(*) FROM artist;

    User Question: Which artist has the most songs?
    Answer: SELECT artist.name
            FROM artist
            JOIN song ON artist.artistID = song.artistID
            GROUP BY artist.artistID
            ORDER BY COUNT(song.songID) DESC
            LIMIT 1;

    
    Common mistakes to avoid, with examples:
    Incorrect Formatting (DO NOT return queries inside markdown blocks)

    User Question: How many artists are there in the database?
    Answer: ```sql
            SELECT COUNT(*) FROM artist;
            ```
    
    User Question: Which artist has the most songs?
    Answer: ```sql
            SELECT artist.name
            FROM artist
            JOIN song ON artist.artistID = song.artistID
            GROUP BY artist.artistID
            ORDER BY COUNT(song.songID) DESC
            LIMIT 1;
            ```

    Adding Explanations (DO NOT include extra text)
    User Question: How many artists are there in the database?
    Answer: Here is your SQL query: SELECT COUNT(*) FROM artist;

    

    User Question: {question}
    '''

    completion = client.chat.completions.create(
    model="gpt-4o",  
    messages=[
        {"role": "user", "content": prompt}
    ]
    )

    result = completion.choices[0].message.content  
    print(result)
    return result





# Run SQL query
def run_sql_query(sql_query):
    conn = sqlite3.connect('musikk.db')
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        print(results)
    except sqlite3.Error as e:
        print("Error executing query:", e)
    
    conn.close()

    return results

# Generate an answer with natural language to the original question
def generate_nl(sql_result, question):

    prompt = f'''
    Given the original question, the corresponding SQLite3 query, 
    and the execution results, produce a truthful and accurate natural language response to the original question.
    The answer should not mention that the data was fetched from a database.
    The user is not interested in knowing how the answer was generated, only the answer itself.
    Give the response as short and concise as possible.
    Your response should be in the same language as the original question, which will be in English or Norwegian.
    

    User Question: {question}
    SQL Query: {sql_query}
    SQL Execution Results: {sql_result}  
    '''

    completion = client.chat.completions.create(
    model="gpt-4o",  
    messages=[
        {"role": "user", "content": prompt}
    ]
    )

    answer = completion.choices[0].message.content  
    return answer

# Create a Streamlit app
st.title("Music DB Assistant 🎵")
st.write("Ask a question about your music collection")

user_input = st.text_input("Enter your question:", "")

if user_input:
    try:
        sql_query = generate_sql(user_input)
        results = run_sql_query(sql_query)
        nl_answer = generate_nl(results, user_input)

        st.write("### Answer:")
        st.write(nl_answer)

        st.write("### SQL Query:")
        st.code(sql_query, language="sql")

        st.write("### SQL Results:")
        st.table(results)

    except Exception as e:
        st.error(f"An error occurred: {e}")




