import asyncio
import json
import os
import pty
import shutil
import signal
import struct
import tempfile
import fcntl
import termios
import subprocess
import sys
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "board_games_data.db"

app = FastAPI()


@app.get("/")
async def home():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Board Games Terminal</title>
    <link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@xterm/xterm/css/xterm.css">
    <style>
        body {
            margin: 0;
            padding: 30px;
            background: #111827;
            color: white;
            font-family: Arial, sans-serif;
        }
        h1 { margin-top: 0; }
        #terminal {
            height: 70vh;
            padding: 12px;
            background: #000;
            border-radius: 8px;
        }
        .note { color: #cbd5e1; }
    </style>
</head>
<body>
    <h1>Board Games CLI</h1>
    <p class="note">
        Try the actual Python board games application.
        Type a menu option and press Enter.
    </p>
    <div id="terminal"></div>

    <script src="https://cdn.jsdelivr.net/npm/@xterm/xterm/lib/xterm.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@xterm/addon-fit/lib/addon-fit.js"></script>
    <script>
        const terminal = new Terminal({
            cursorBlink: true,
            convertEol: true,
            theme: {
                background: "#000000",
                foreground: "#eeeeee"
            }
        });

        const fitAddon = new FitAddon.FitAddon();
        terminal.loadAddon(fitAddon);
        terminal.open(document.getElementById("terminal"));
        fitAddon.fit();

        const protocol = location.protocol === "https:" ? "wss:" : "ws:";
        const socket = new WebSocket(
            protocol + "//" + location.host + "/ws"
        );

        socket.onopen = () => {
            terminal.writeln("Connected to the board games application.");
            terminal.writeln("");
            socket.send(JSON.stringify({
                type: "resize",
                cols: terminal.cols,
                rows: terminal.rows
            }));
        };

        socket.onmessage = (event) => {
            terminal.write(event.data);
        };

        socket.onclose = () => {
            terminal.writeln("\\r\\nConnection closed.");
        };

        socket.onerror = () => {
            terminal.writeln("\\r\\nConnection error.");
        };

        terminal.onData(data => {
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({
                    type: "input",
                    data: data
                }));
            }
        });

        window.addEventListener("resize", () => {
            fitAddon.fit();
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({
                    type: "resize",
                    cols: terminal.cols,
                    rows: terminal.rows
                }));
            }
        });
    </script>
</body>
</html>
    """)


@app.websocket("/ws")
async def terminal(websocket: WebSocket):
    await websocket.accept()

    if not DATABASE.exists():
        await websocket.send_text("Demo database not found.")
        await websocket.close()
        return

    session_dir = tempfile.mkdtemp(prefix="boardgames-")
    session_db = Path(session_dir) / "board_games_data.db"
    shutil.copy2(DATABASE, session_db)

    master_fd, slave_fd = pty.openpty()

    # Give the terminal a sensible initial size.
    fcntl.ioctl(
        slave_fd,
        termios.TIOCSWINSZ,
        struct.pack("HHHH", 24, 100, 0, 0)
    )

    environment = os.environ.copy()
    environment["DB_PATH"] = str(session_db)
    environment["PYTHONUNBUFFERED"] = "1"
    environment["TERM"] = "xterm-256color"

    process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        cwd=str(BASE_DIR),
        env=environment,
        start_new_session=True
    )

    os.close(slave_fd)

    async def send_output():
        while True:
            try:
                output = await asyncio.to_thread(os.read, master_fd, 4096)
                if not output:
                    break
                await websocket.send_text(
                    output.decode("utf-8", errors="replace")
                )
            except (OSError, WebSocketDisconnect):
                break

    async def receive_input():
        while True:
            message = json.loads(await websocket.receive_text())

            if message.get("type") == "input":
                data = message.get("data", "")
                os.write(master_fd, data.encode("utf-8"))

            elif message.get("type") == "resize":
                cols = max(20, min(int(message.get("cols", 100)), 200))
                rows = max(5, min(int(message.get("rows", 24)), 60))

                fcntl.ioctl(
                    master_fd,
                    termios.TIOCSWINSZ,
                    struct.pack("HHHH", rows, cols, 0, 0)
                )

    output_task = asyncio.create_task(send_output())
    input_task = asyncio.create_task(receive_input())

    try:
        done, pending = await asyncio.wait(
            [output_task, input_task],
            return_when=asyncio.FIRST_COMPLETED
        )

    except WebSocketDisconnect:
        pass

    finally:
        for task in [output_task, input_task]:
            if not task.done():
                task.cancel()

        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=3)
            except Exception:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass

        os.close(master_fd)
        shutil.rmtree(session_dir, ignore_errors=True)

        try:
            await websocket.close()
        except Exception:
            pass