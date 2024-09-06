module.exports = {
    extends: [
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended",
        "next",
    ],
    rules: {
        indent: ['error', 4],
        "no-unused-vars": "off",
        "@typescript-eslint/no-explicit-any": "off",
        "@typescript-eslint/no-unused-vars": ["error"],
        'react/jsx-indent': ['error', 4],
        'max-len': ['error', { code: 140 }],
    },
};
