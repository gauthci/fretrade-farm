FROM freqtradeorg/freqtrade:stable

USER root
RUN apt-get update && apt-get install -y gettext && rm -rf /var/lib/apt/lists/*
# Installer plotly pour les graphiques
RUN pip install plotly
RUN pip install influxdb influxdb-client
USER ftuser

