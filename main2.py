import dotenv
import typer
import uvicorn
import webbrowser
from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def index():
    return 'index'


@app.on_event('startup')
def on_startup():
    webbrowser.open(f'http://{app.state.host}:{app.state.port}')


def main(
    host: str = typer.Option('localhost', envvar='WEB_HOST'),
    port: int = typer.Option(8888, envvar='WEB_PORT'),
):
    app.state.host = host
    app.state.port = port
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    dotenv.load_dotenv()
    typer.run(main)
