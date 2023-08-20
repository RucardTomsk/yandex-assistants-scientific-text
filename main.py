from fastapi import FastAPI, Response
from pydantic import BaseModel
from starlette.responses import FileResponse
import requests
from docxtpl import DocxTemplate

app = FastAPI()
PASSPORT_TOKEN = '<YOUR_YANDEX_PASSPORT_TOKEN>'
FOLDER_TOKEN = 'YOUR_FOLDER_TOKEN'
class UserBody(BaseModel):
    name: str
    tem: str
    zak: str
    str_count: int
    id: str


@app.post("/")
async def root(body: UserBody):
    response = requests.post(
        'https://iam.api.cloud.yandex.net/iam/v1/tokens',
        params={'yandexPassportOauthToken': PASSPORT_TOKEN},
    )

    json_response = response.json()
    iam_token = json_response["iamToken"]
    print(iam_token)
    folder_id = FOLDER_TOKEN

    promt = {
        "model": "general",
        "instruction_text": "Найди ошибки в тексте и исправь их",
        "request_text": "Ламинат подойдет для укладке на кухне или в детской комнате – он не боиться влаги и механических повреждений благодаря защитному слою из облицованных меламиновых пленок толщиной 0,2 мм и обработанным воском замкам",
        "generation_options": {
            "max_tokens": 1500,
            "temperature": 1000
        },
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + iam_token,
        "x-folder-id": folder_id,
    }

    response = requests.post(
        'https://llm.api.cloud.yandex.net/llm/v1alpha/instruct',
        params=promt,
        headers=headers,
    )

    # json_response = response.json()
    # moke
    json_response = ("В будущем тут должен быть текст, но доступа к YandexGPT мне не выдали(очень обидно, исчезает мотивация что-то делать). Спасибо за то что "
                     "попробовали уважаемый/ая " + body.name + "!\n"
                     "Я знаю что тема твоей работы: " + body.tem + "\n"
                     "Да за тобой следят :)")

    print(json_response)

    doc = DocxTemplate("template.docx")
    doc.render({"text": json_response})

    doc.save("аннотация_" + body.id + ".docx")

    return Response(content=f"Ссылка на твою аннотацию: http://92.63.64.241:1111/anot/{body.id}", media_type="text/plain")


@app.get("/anot/{id}")
async def say_hello(id: str):
    return FileResponse(path="аннотация_" + id + ".docx", filename='АвтоАннотация.docx',
                        media_type='multipart/form-data')
