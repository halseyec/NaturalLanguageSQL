import json
from openai import OpenAI
import os
import sqlite3
from time import time

print("Running db_bot.py!")

fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

# SQLITE
sqliteDbPath = getPath("music_db.sqlite")
setupSqlPath = getPath("setup.sql")
setupSqlDataPath = getPath("setupData.sql")

# Erase previous db
if os.path.exists(sqliteDbPath):
    os.remove(sqliteDbPath)

sqliteCon = sqlite3.connect(sqliteDbPath) # create new db
sqliteCursor = sqliteCon.cursor()

with open(setupSqlPath) as setupSqlFile:
    with open(setupSqlDataPath) as setupSqlDataFile:
        setupSqlScript = setupSqlFile.read()
        setupSqlDataScript = setupSqlDataFile.read()

sqliteCursor.executescript(setupSqlScript) # setup tables and keys
sqliteCursor.executescript(setupSqlDataScript) # setup initial data

def runSql(query):
    result = sqliteCursor.execute(query).fetchall()
    return result

# OPENAI
configPath = getPath("config.json")
print(configPath)
with open(configPath) as configFile:
    config = json.load(configFile)

openAiClient = OpenAI(
    api_key = config["openaiKey"],
    organization = config["orgId"]
)

def getChatGptResponse(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    responseList = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            responseList.append(chunk.choices[0].delta.content)

    result = "".join(responseList)
    return result

# strategies
commonSqlOnlyRequest = " Give me a sqlite select statement that answers the question. Only respond with sqlite syntax. If there is an error, do not explain it!"
strategies = {
    "zero_shot": setupSqlScript + commonSqlOnlyRequest,
    "single_domain_double_shot": (setupSqlScript +
                   " Which albums are released by artists in the 'Rock' genre? " +
                   " \nSELECT a.title\nFROM album a JOIN artist ar ON a.artist_id = ar.artist_id WHERE ar.genre = 'Rock';\n " +
                   commonSqlOnlyRequest)
}

questions = [
    "What are the top 3 albums by duration?",
    "Which artist has the most songs?",
    "Which playlists contain songs by Bob Dylan?",
    "Which albums were released before 1970?",
    "Which listeners have created the most playlists?",
    "What are the songs in the 'Girly pop' playlist?",
    "Which songs are longer than 5 minutes?",
    "Which artist has the most albums?",
    "Which song would you recommend for listener Halsey Curry?"
]

def sanitizeForJustSql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]

    return value

for strategy in strategies:
    responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
    questionResults = []
    for question in questions:
        print(question)
        error = "None"
        sqlSyntaxResponse = ""
        queryRawResponse = ""
        friendlyResponse = ""
        try:
            sqlSyntaxResponse = getChatGptResponse(strategies[strategy] + " " + question)
            sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
            print(sqlSyntaxResponse)
            queryRawResponse = str(runSql(sqlSyntaxResponse))
            print(queryRawResponse)
            friendlyResultsPrompt = f'I asked a question "{question}" and the response was "{queryRawResponse}" Please, give a concise response in a more friendly way?'
            friendlyResponse = getChatGptResponse(friendlyResultsPrompt)
            print(friendlyResponse)
        except Exception as err:
            error = str(err)
            print(err)

        questionResults.append({
            "question": question,
            "sql": sqlSyntaxResponse,
            "queryRawResponse": queryRawResponse,
            "friendlyResponse": friendlyResponse,
            "error": error
        })

    responses["questionResults"] = questionResults

    with open(getPath(f"response_{strategy}_{time()}.json"), "w") as outFile:
        json.dump(responses, outFile, indent = 2)

sqliteCursor.close()
sqliteCon.close()
print("Done!")
