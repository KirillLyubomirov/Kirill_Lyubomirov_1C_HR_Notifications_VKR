"""Local SMTP acceptance fixture: receive DATA, close without a final reply.

This receiver deliberately gives the client an unknown result. It does not
forward messages. Recorded payloads let the operator inspect the outcome.
"""
import argparse
import json
import socket
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--count', type=int, default=10)
    args = parser.parse_args()
    args.evidence.mkdir(parents=True, exist_ok=True)
    facts = []
    with socket.socket() as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', 1025))
        server.listen(8)
        (args.evidence / 'READY.txt').write_text('127.0.0.1:1025', encoding='utf-8')
        server.settimeout(180)
        for index in range(args.count):
            connection, _ = server.accept()
            fact = {'index': index + 1, 'commands': []}
            with connection:
                connection.settimeout(20)
                with connection.makefile('rb') as stream:
                    connection.sendall(b'220 vkr-disconnect SMTP\r\n')
                    in_data = False
                    payload = []
                    while True:
                        line = stream.readline()
                        if not line:
                            raise RuntimeError('Client closed before DATA was received')
                        if in_data:
                            if line == b'.\r\n':
                                filename = f'message_{index + 1:02d}.eml'
                                (args.evidence / filename).write_bytes(b''.join(payload))
                                fact.update(received_at=datetime.now(timezone.utc).isoformat(),
                                            payload_file=filename, final_250_sent=False)
                                break
                            payload.append(line)
                            continue
                        fact['commands'].append(line.decode('ascii', 'replace').rstrip())
                        verb = line.split(b' ', 1)[0].strip().upper()
                        if verb in (b'EHLO', b'HELO'):
                            connection.sendall(b'250-vkr-disconnect\r\n250 8BITMIME\r\n')
                        elif verb in (b'MAIL', b'RCPT', b'RSET'):
                            connection.sendall(b'250 OK\r\n')
                        elif verb == b'DATA':
                            connection.sendall(b'354 End with dot\r\n')
                            in_data = True
                        else:
                            connection.sendall(b'500 Unsupported\r\n')
            facts.append(fact)
            (args.evidence / 'smtp_disconnect.json').write_text(
                json.dumps(facts, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()

