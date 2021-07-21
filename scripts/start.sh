#!/bin/bash
export $(cat .env)
alembic upgrade head
python main.py