FROM python:3

ADD . tv_dict/src/backend

RUN pip install -r tv_dict/src/backend/requirements.txt

WORKDIR tv_dict/src/backend

# Start backend micro-service
CMD ["python", "entry_point.py"]