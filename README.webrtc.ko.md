### WebRTC 테스트 프론트엔드

신호 기능을 간단히 시험해볼 수 있도록 `/static/webrtc_test.html` 경로에 예제 HTML 페이지가 포함되어 있습니다. 백엔드 서버를 실행한 뒤 브라우저에서 다음 주소로 접속하세요:

http://localhost:8000/static/webrtc_test.html

방 이름과 사용자명을 입력하고 **Join** 버튼을 누르면 연결됩니다. 다른 브라우저나 기기에서 같은 방에 접속하면 화상 채팅을 할 수 있습니다.
페이지는 여러 명의 참가자를 위해 사용자별로 `RTCPeerConnection`을 생성하며, WebSocket 연결 전에 미디어 스트림을 확보하여 협상 안정성을 높입니다. 페이지가 HTTP인지 HTTPS인지에 따라 스크립트가 `ws://` 또는 `wss://`를 자동으로 선택하고, 참가자가 종료될 때 `leave` 메시지를 브로드캐스트하여 다른 사용자의 피어 연결을 정리합니다.

**주의:** 최근 브라우저들은 평문 `ws://` 연결을 차단하고 있습니다. `localhost` (`127.0.0.1` 등)이 아닌 실제 배포라면 반드시 HTTPS 환경에서 유효한 인증서를 적용하고 `wss://`로 접속하도록 구성해야 합니다.

### TURN 서버 설정

기본 예제는 퍼블릭 STUN 서버만 사용하므로 동일 네트워크 내에서 가장 잘 동작합니다. 다른 네트워크 환경에서도 연결하려면 TURN 서버 정보를 `.env` 파일에 추가합니다.

```env
TURN_SERVER_URL=turn:your.turn.server:3478
TURN_USERNAME=optional-user
TURN_PASSWORD=optional-password
STUN_SERVER_URL=stun:stun.l.google.com:19302
```

브라우저에서 `/static/webrtc_test.html` 페이지를 열면 `/api/v1/ws/ice-config` 경로에서 ICE 서버 설정을 받아와 `RTCPeerConnection` 생성 시 사용합니다.
