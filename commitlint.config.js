module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation changes
        'style',    // Changes that don't affect code meaning
        'refactor', // Changes that neither fix bugs nor add features
        'test',     // Adding or fixing tests
        'chore',    // Changes to build process or auxiliary tools
        'perf',     // Performance improvements
        'ci',       // CI/CD related changes
        'build',    // Build system changes
        'revert',   // Revert previous changes
        'wip',      // Work in progress
      ]
    ],
    'type-case': [2, 'always', 'lower-case'],
    'type-empty': [0, 'never'],
    'scope-case': [2, 'always', 'lower-case'],
    'subject-case': [2, 'always', 'lower-case'],
    'subject-empty': [0, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'header-max-length': [2, 'always', 150],
    'body-leading-blank': [2, 'always'],
    'body-max-line-length': [2, 'always', 250],
    'footer-leading-blank': [2, 'always'],
    'footer-max-line-length': [2, 'always', 250]
  }
}; 