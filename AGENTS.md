# Agents Guide

This workspace is a thin wrapper for an OpenCode environment and does not contain a first-party application source tree. Development and operational behavior are driven by the installed `@opencode-ai` plugin and SDK.

## Project Layout

- `.opencode/`: Local configuration and dependency state.
  - `config.json`: Local OpenCode system prompt and configuration.
  - `package.json` / `package-lock.json`: Pins the `@opencode-ai/plugin` dependency.
- `.omo/`: Local session and runtime metadata (ignore for source analysis).
- `node_modules/@opencode-ai/`: Contains the core logic for the environment.
  - `plugin`: Owns plugin-facing exports (`tool`, `tui`) and hook definitions.
  - `sdk`: Owns architectural glue, including client/server creation and CLI spawning.

## Operational Truths

### Development Commands
There are no scripts defined in the root `package.json`. Tooling is provided by the installed dependencies:
- **Typechecking**: Defined in `@opencode-ai` packages via `tsgo --noEmit`.
- **Building**: Defined in `@opencode-ai` packages via `tsc` or `bun ./script/build.ts`.

### Runtime Entry Points
The system is driven by the `opencode` CLI. Key patterns include:
- **Server**: `opencode serve --hostname=127.0.0.1 --port=4096`
- **Session**: `opencode --project=... --model=... --session=... --agent=...`

### Architectural Entry Points
If extending the system, refer to the following exports in `node_modules`:
- **Plugin Hooks**: `@opencode-ai/plugin` exposes hooks for `auth`, `provider`, `tool`, `event`, `config`, `chat.*`, `permission.ask`, and `command.execute.before`.
- **SDK Bootstrap**: `@opencode-ai/sdk` exposes `createOpencode()`, `createOpencodeClient()`, and `createOpencodeServer()`.

## Local Conventions
- **System Prompt**: The local configuration in `.opencode/config.json` specifies that the agent should write Python and respond in Korean.
- **Ignore Rules**: `.opencode/.gitignore` treats the `.opencode` folder as local runtime state rather than source code.
