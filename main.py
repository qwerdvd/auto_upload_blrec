from server.__init__ import get_app

app = get_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=5000, reload=True)
