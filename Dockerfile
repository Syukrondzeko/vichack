# Stage 1: Build ReactJS app
FROM node:18 AS react-build
WORKDIR /app
COPY restaurant-website/package*.json ./
RUN npm install
COPY restaurant-website/ ./
RUN npm run build

# Stage 2: Build NodeJS app
FROM node:18 AS node-build
WORKDIR /app
COPY restaurant-website/package*.json ./
RUN npm install
COPY restaurant-website/ .

# Stage 3: Build FastAPI app
FROM python:3.12 AS fastapi-build
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile
COPY . .

# Final Stage: Combine all components
FROM python:3.12

# Install NodeJS, npm, and pipenv
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm \
    && pip install pipenv

# Set working directory
WORKDIR /app

# Copy FastAPI app and install dependencies
COPY --from=fastapi-build /app /app
RUN pipenv install --deploy --ignore-pipfile

# Copy NodeJS and ReactJS apps
COPY --from=node-build /app /app/restaurant-website
COPY --from=react-build /app/build /app/restaurant-website/build

# Expose ports
EXPOSE 3000 3001 8000

# Start services
CMD ["sh", "-c", "cd /app/restaurant-website && node server.js & cd /app/restaurant-website && npm start & cd /app && pipenv run uvicorn app:app --host 0.0.0.0 --port 8000"]