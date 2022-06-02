module.exports = {
  preset: "@vue/cli-plugin-unit-jest/presets/typescript-and-babel",
  transformIgnorePatterns: [
    "/node_modules/(?!@babel)",
    "<rootDir>/node_modules/(?!vuetify)",
  ],
  setupFiles: ["./tests/setup.js"],
};
