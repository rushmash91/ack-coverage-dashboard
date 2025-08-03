FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY main.py .
COPY ack_dashboard/ ack_dashboard/
COPY results/ results/

# Install uv
RUN pip install uv

# Install dependencies
RUN uv sync

# Expose port
EXPOSE 8501

CMD ["uv", "run", "python", "-m", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.fileWatcherType=none"]