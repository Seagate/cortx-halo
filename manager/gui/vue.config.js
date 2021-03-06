module.exports = {
  transpileDependencies: ["vuetify"],
  pluginOptions: {
    i18n: {
      locale: "en",
      fallbackLocale: "en",
      localeDir: "locales",
      enableInSFC: true,
      enableBridge: true,
    },
  },
  css: {
    loaderOptions: {
      scss: {
        additionalData: `@import "@/scss/config.scss";@import "@/scss/style.scss";`,
      },
    },
  },
};
