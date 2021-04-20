#extend the official Rasa SDK image
FROM rasa/rasa-sdk:2.1.2
#change back to root user to install dependencies
USER root

#to install packages from PyPI
RUN pip install --no-cache-dir beautifulsoup4
RUN pip install --no-cache-dir pymongo

#switch back to non-root to run code

USER 1001
