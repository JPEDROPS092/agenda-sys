FROM node:20-slim

# Criar diretório da aplicação
WORKDIR /app

# Copia package.json e package-lock.json para aproveitar cache de camadas
COPY package*.json ./

# Instala as dependências
RUN npm install

# Copia o resto dos arquivos
COPY . .

# Limpa qualquer diretório .output existente e cria um novo com permissões adequadas
RUN rm -rf ./.output && \
    mkdir -p ./.output && \
    mkdir -p ./.output/public && \
    chmod -R 777 ./.output && \
    mkdir -p ./.nuxt && \
    chmod -R 777 ./.nuxt && \
    chmod -R 777 ./node_modules

# Expõe a porta de desenvolvimento do Nuxt
EXPOSE 3000

# Comando para iniciar o servidor de desenvolvimento
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]