#!/bin/bash

# Script para corrigir problemas de permissão no projeto agenda-sys
# Deve ser executado com privilégios de usuário adequados

echo "🔧 Corrigindo permissões dos diretórios do projeto..."

# Verifica e corrige permissões do node_modules
if [ -d "./node_modules" ]; then
    echo "📁 Ajustando permissões do diretório node_modules..."
    chmod -R 755 ./node_modules
    echo "✅ Permissões de node_modules ajustadas!"
else
    echo "⚠️ Diretório node_modules não encontrado."
fi

# Verifica e cria diretórios .output e .nuxt com permissões adequadas
echo "📁 Verificando diretórios .output e .nuxt..."

# Configurando .output
if [ -d "./.output" ]; then
    echo "📁 Limpando e recriando diretório .output..."
    rm -rf ./.output
fi
mkdir -p ./.output
mkdir -p ./.output/public
chmod -R 777 ./.output
echo "✅ Diretório .output configurado com permissões adequadas!"

# Configurando .nuxt
if [ -d "./.nuxt" ]; then
    echo "📁 Limpando e recriando diretório .nuxt..."
    rm -rf ./.nuxt
fi
mkdir -p ./.nuxt
chmod -R 777 ./.nuxt
echo "✅ Diretório .nuxt configurado com permissões adequadas!"

# Limpa o cache do npm
echo "🧹 Limpando cache do npm..."
npm cache clean --force
echo "✅ Cache limpo com sucesso!"

echo "🔍 Verificando conflitos de dependências..."
npx npm-check

echo "📝 Instruções adicionais:"
echo "- Para reconstruir o ambiente Docker com as novas configurações, execute:"
echo "  docker-compose down -v"
echo "  docker-compose up --build"

echo "✨ Processo de correção finalizado!"
