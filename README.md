# NL-to-SQL

- [NL-to-SQL](#nl-to-sql)
  - [Overview](#overview)
  - [Approach](#approach)
    - [Database](#database)
    - [LLM](#llm)
    - [User Interface](#user-interface)
    - [Examples](#examples)
  - [Challenges](#challenges)
    - [Price](#price)
    - [Comparing the method with traditional methods](#comparing-the-method-with-traditional-methods)
  - [Key Takeaways](#key-takeaways)
  - [More Examples](#more-examples)

## Overview

I have chosen to work on option 1, to solve a real-world problem using LLMs.
The problem I have tried to solve is automating SQL queries from natural language. This way non-technical users can interact with their databases without having to know SQL.
I knew little about how to use LLMs before starting this project, so it has been both fun to see how powerful they are, and rewarding to learn how to use them.

The files in this repository are:

- `nl2sql_app.py` - The main file for the project. It contains the code for the user interface and the logic for the LLM.
- `music.db` - The database I have used for the project.
- `nl2sql_music_db.ipynb` - A notebook where I have tested the LLM on the database.

## Approach

A disclaimer is that I have used my own API key.

### Database

I have used a database from a course I am taking on NTNU, TDT4145 Datamodellering og Databasesystemer. The database is a small music database, it contains information about songs, artists, albums, and collaborations between artists. The database is in SQLite format, and I have used the sqlite3 library in Python to interact with it.

### LLM

The LLM I have used is OpenAI´s GPT4o model. OpenAI have an easy to use API and their models are good, so I think it works well for a proof of concept. The way I have used the model is to split up the problem into three parts. 

1. First I give the model the question from the user alongside a [prompt](nl2sql_app.py#L13-L99). The prompt consist of both the entire SQL schema and a description of the models task. Here the model is asked to generate a SQL query based on the users question. In the prompt I have tried to give specific instructions to make sure the result is a valid SQL query.

2. Then the SQL query is executed on the database and the result is used in a [second prompt](nl2sql_app.py#L136-L146). 

3. This second prompt gives the model both the first prompt, the result of the SQL query, and an instruction to generate a natural language response.
I present both the SQL query and the natural language response to the user in the user interface.

I have gotten the general concept from an Azure Architecuture Blog, [NL to SQL Architecture Alternatives](https://techcommunity.microsoft.com/blog/azurearchitectureblog/nl-to-sql-architecture-alternatives/4136387)

### User Interface

For the user interface, I have used the Streamlit library in Python. It is a lightweight library that´s easy to use, and it is good for sketching a proof of concept. I have not seen the library before this project, but I will definitely use it again in the future.

### Examples

```Markdown
Question:
Find the artist who has collaborated with the most distinct other artists (as a featured or main artist on a song), but has never released a song as a solo artist, along with the number of unique collaborators they have worked with.
```

![alt text](./images/image-3.png)

```Markdown
Question:
Jeg trenger å finne artistnavn og sangnavn for alle låttitler som inkluderer tekststrengen “the”
```

![alt text](./images/image-6.png)

## Challenges

### Price

One drawback with using OpenAI is that you have to pay for using the API. For this project I paid 5$ for the credits. As of now, I have used 0.5$ of the credits and 230 000 tokens. I assume that when scaling up the usage it can become expensive. To overcome this, I think it might be an idea to host open source models locally. But, this again can require a lot of computational power, so I guess one have to adjust the solution to each specific case.

### Comparing the method with traditional methods

I wanted to do a quantitative comparison of my method against other LLM methods. [WikiSQL](https://github.com/salesforce/WikiSQL/blob/master/README.md) can be used to benchmark nl-2-sql models on large datasets. This would have been interesting, but I would have needed to do a lot of changes. Since the project is about making a proof of concept, I have chosen to focus on the qualitative aspects instead.

## Key Takeaways

The solution works really well. I have tested it on a lot of the questions from the database course, and it solves all questions correctly. I think the solution is a lot better than using a normal LLM chatbot, because the prompt engineering makes it more precise. For a company I think it can be a cheaper solution than using vector databases and RAG models.

I think the method can be quite useful for companies, because by using prompt engineering, it is possible to make the model more precise than using a normal LLM chatbot. By letting the SQL specialist create the prompts, the entire company can have a more user-friendly way to interact with the database, even though they don´t know SQL.

## More Examples

Streamlit application
![alt text](./images/image-10.png)

```Markdown
Question:
Songs longer than 220 seconds
```

![alt text](./images/image-8.png)
![alt text](./images/image-9.png)

```Markdown
Question:
Finn artistnavnet og antallet gjesteopptredener for den artisten med flest gjesteopptredener 
```

![alt text](./images/image-7.png)

```Markdown
Question:
Find the name of the artist who has released the most songs, but has never been a featured artist on any song, along with the total number of songs they have released.
```

![alt text](./images/image-1.png)

```Markdown
Question:
I wonder which artist who has released songs in the most distinct years, but has never released a song on an album, along with the number of distinct years they have released songs.
```

![alt text](./images/image-2.png)
