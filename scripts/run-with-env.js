const { execSync } = require('child_process');
const os = require('os');
const path = require('path');
const fs = require('fs');

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

// Check if virtual environment exists
const venvActivateScript = isWindows
    ? path.join(venvPath, 'Scripts', 'activate')
    : path.join(venvPath, 'bin', 'activate');
const venvExists = fs.existsSync(venvActivateScript);

// Determine if the command starts with a Node/JS-based tool
const shouldSkipVenv = skipVenvCommands.some((tool) =>
    command.startsWith(tool)
);

// Build the final shell command
// Use venv only if it exists and command requires it
const finalCommand =
    shouldSkipVenv || !venvExists
        ? command
        : isWindows
          ? `"${venvActivateScript}" && ${command}`
          : `. "${venvActivateScript}" && ${command}`;

try {
    execSync(finalCommand, {
        stdio: 'inherit',
        shell: true,
    });
} catch (err) {
    console.error(
        `❌ Failed to run the command${shouldSkipVenv || !venvExists ? '' : ' inside the Python virtual environment'}.`
    );
    console.error(`Command: ${finalCommand}`);
    process.exit(1);
}
