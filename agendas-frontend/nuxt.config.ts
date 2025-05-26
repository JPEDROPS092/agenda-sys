// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: {
    enabled: true,

    timeline: {
      enabled: true,
    },
  },

  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxt/icon',
    '@vueuse/nuxt'
  ],
  
  // Configuração explícita para resolver conflito de dependências
  vite: {
    optimizeDeps: {
      include: [
        '@preact/signals',
        'preact',
        '@schedule-x/calendar',
        '@schedule-x/vue'
      ],
      exclude: []
    },
    resolve: {
      dedupe: ['vue', '@preact/signals', 'preact']
    },
    build: {
      commonjsOptions: {
        transformMixedEsModules: true,
        include: [/node_modules/]
      }
    }
  },
  
  vueuse: {
    ssrHandlers: true,
  },

  css: [
    '@/assets/css/globals.css'
  ],

  // Configuração para evitar os warnings de componentes duplicados
  components: {
    dirs: [
      {
        path: '~/components/ui',
        pathPrefix: false,
        ignore: ['**/*/index.ts'] // Ignora os arquivos index.ts
      }
    ]
  },

  colorMode: {
    classSuffix: '',
    preference: 'system',
    fallback: 'light'
  },

  app: {
    head: {
      title: 'Sistema de Agendas',
      meta: [
        { name: 'description', content: 'Sistema para gerenciamento de agendas' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
      ]
    }
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000/api'
    }
  },

  compatibilityDate: '2025-03-13',
})