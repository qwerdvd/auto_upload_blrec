import asyncio
from aioflask import Flask, render_template

app = Flask(__name__)

@app.route('/')
async def index():
    await asyncio.sleep(1)
    return await render_template('index.html')