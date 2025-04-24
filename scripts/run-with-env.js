const { execSync } = require("child_process");
const os = require("os");
const path = require("path");

const isWindows = os.platform() === "win32";
const venvPath = path.join(__dirname, "..", "env");
const command = process.argv.slice(2).join(" ");

// Build the activation command depending on the OS
const activateCommand = isWindows
  ? `"${path.join(venvPath, "Scripts", "activate")}" && ${command}`
  : `. "${path.join(venvPath, "bin", "activate")}" && ${command}`;

try {
  execSync(activateCommand, {
    stdio: "inherit",
    shell: true
  });
} catch (err) {
  console.error("❌ Failed to run the command inside the Python virtual environment.");
  console.error(`Command: ${activateCommand}`);
  process.exit(1);
}
