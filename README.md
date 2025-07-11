# Codeground Backend
[한국어 README](README.ko.md)


This repository contains a FastAPI based backend service. It provides authentication APIs and uses PostgreSQL through SQLAlchemy and Alembic for migrations.

## Requirements

- Python 3.11+
- [Poetry](https://python-poetry.org/) for dependency management
- PostgreSQL instance

## Installation

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd Codeground-Backend
   ```

2. **Install dependencies**

   Use Poetry to install the project requirements:

   ```bash
   poetry install
   ```

3. **Configure environment variables**

   The application loads variables from a `.env` file located **one directory above** the project root. Create `../.env` relative to the repository with values similar to the following:

   ```env
   SECRET_KEY=your-secret-key
   SECRET_KEY_AUTH=your-auth-key
   DB_HOST=localhost
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_NAME=codeground
   ```

   These variables are used to construct the database URL for PostgreSQL.

4. **Database setup**

   Initialize the database using Alembic. If no migration files exist, create one:

   ```bash
   alembic revision --autogenerate -m "init"
   alembic upgrade head
   ```

## Running the Service

Start the FastAPI application with Uvicorn:

```bash
poetry run uvicorn src.app.main:app --reload
```

The API will be available at `http://localhost:8000/`. Authentication endpoints are prefixed with `/api/v1` (e.g. `/api/v1/auth/sign-up`).

### WebRTC Signaling

CodeArena provides a WebRTC signaling endpoint so players can negotiate peer-to-peer
audio/video connections. Connect to the WebSocket endpoint using a room name and
username:

```text
/api/v1/ws/webrtc/<room>?username=<your-name>
```

Any message sent over this socket will be broadcast to the other participants in the same room.

### Sample WebRTC Frontend

A minimal HTML page is provided at `/static/webrtc_test.html` to try out the signaling endpoint.
Run the backend server, then open the page in your browser:

```bash
poetry run uvicorn src.app.main:app --reload
# then visit http://localhost:8000/static/webrtc_test.html
```

Enter a room name and username and press **Join**. Open the same page in other
browsers or devices and join the same room to establish a video chat. The page
supports any number of participants by opening a separate `RTCPeerConnection`
for each remote user. Media is obtained before connecting to the WebSocket for
more reliable negotiation, and the script automatically chooses `ws://` or
`wss://` based on whether the page is served over HTTP or HTTPS. When a
participant disconnects, a `leave` message is broadcast so others can clean up
their peer connections.

**Important:** modern browsers increasingly block plain `ws://` connections.
When deploying anywhere other than `localhost`, run the server behind HTTPS and
connect using `wss://` with a valid certificate.

### TURN Server Configuration

The default demo relies on public STUN only and works best when all participants
are on the same network. To support connecting across different networks, supply
a TURN server via environment variables. Add the following to your `.env` file:

```env
# Address of your TURN server
TURN_SERVER_URL=turn:your.turn.server:3478
TURN_USERNAME=optional-user
TURN_PASSWORD=optional-password
# Optionally override the default STUN server
STUN_SERVER_URL=stun:stun.l.google.com:19302
```

The page at `/static/webrtc_test.html` automatically fetches the ICE server
configuration from `/api/v1/ws/ice-config` and uses it when creating
`RTCPeerConnection` objects.
