import os, sys
sys.path.append('../')

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from serialization import dict_layout
from DataBase.db_api import db_start

app = FastAPI()

@app.get('/')
async def json_data_get():
	await db_start()
	json_data = await dict_layout()
	return JSONResponse(content=json_data)

if __name__ == '__main__':
	os.system("uvicorn json_api:app --reload")