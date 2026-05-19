FROM node:20-slim

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@10.33.4 --activate

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .

CMD ["pnpm", "dev", "--host", "0.0.0.0"]
