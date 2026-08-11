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
