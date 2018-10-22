FROM jupyter/pyspark-notebook

COPY run_server.py /home/jovyan/
COPY requirements.txt /home/jovyan/
COPY models /home/jovyan/models

RUN pip install -r /home/jovyan/requirements.txt

EXPOSE 5000

CMD python /home/jovyan/run_server.py