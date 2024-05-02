const terminalContainer = document.getElementById('terminal-container');
const term = new Terminal();
term.open(terminalContainer);
const socket = new WebSocket('ws://your-terminal-server-url');
term.attach(socket);