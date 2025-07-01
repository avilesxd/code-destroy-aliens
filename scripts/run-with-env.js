const { execSync } = require('child_process');
const os = require('os');
const path = require('path');

const isWindows = os.platform() === 'win32';
const venvPath = path.join(__dirname, '..', 'env');
const command = process.argv.slice(2).join(' ');

// List of tools that do NOT require the Python virtual environment
const skipVenvCommands = [
    'prettier',
    'eslint',
    'npm',
    'npx',
    'node',
    'husky',
    'mkdocs',
    'commitlint',
];

// Determine if the command starts with a Node/JS-based tool
const shouldSkipVenv = skipVenvCommands.some((tool) =>
    command.startsWith(tool)
);

// Build the final shell command
const finalCommand = shouldSkipVenv
    ? command
    : isWindows
      ? `"${path.join(venvPath, 'Scripts', 'activate')}" && ${command}`
      : `. "${path.join(venvPath, 'bin', 'activate')}" && ${command}`;

try {
    execSync(finalCommand, {
        stdio: 'inherit',
        shell: true,
    });
} catch (err) {
    console.error(
        `❌ Failed to run the command${shouldSkipVenv ? '' : ' inside the Python virtual environment'}.`
    );
    console.error(`Command: ${finalCommand}`);
    process.exit(1);
}
