Title: Using Alternate Models with Claude Code via Claude Code Router
Date: 2026-07-07
Author: Ashley Kleynhans
Modified: 2026-07-07
Category: AI
Tags: ai, claude, deepseek, devops
Summary: How I set up Claude Code Router with the DeepSeek provider to use deepseek-v4-pro and deepseek-v4-flash models in Claude Code, and the Gemini 3.5 Flash issues I hit along the way.
Status: Published
Cover: images/covers/using-alternate-models-with-claude-code-via-claude-code-router.png

## Why Use Alternate Models?

Claude Code is fantastic, but the default models can get expensive when
you are running long sessions. [Claude Code Router](https://github.com/musistudio/claude-code-router)
(CCR) is a local proxy that translates Anthropic's API protocol to other
providers, letting you use models from Gemini, DeepSeek, OpenAI, and others
directly inside Claude Code. You get the full Claude Code experience (slash
commands, tools, MCP, hooks) backed by cheaper models of your choice.

## Setup

### Installing CCR

CCR uses SQLite for its config, which means the `better-sqlite3` native
module needs to compile during install. You need to allow scripts for that
package:

```bash
npm install -g --allow-scripts=better-sqlite3 @musistudio/claude-code-router
```

### Configuring DeepSeek

You will need a [DeepSeek account](https://platform.deepseek.com/).
Sign up, grab your API key from the dashboard, and check out the
[pricing page](https://api-docs.deepseek.com/quick_start/pricing).
DeepSeek's API pricing is significantly cheaper than Anthropic's,
especially for the flash model.

Start CCR and open the admin UI:

```bash
ccr start
ccr ui
```

In the UI, configure three things:

1. **Provider**: add the DeepSeek provider with your API key
2. **Models**: add the models you want to use
    (`deepseek-v4-pro` for heavy lifting,
    `deepseek-v4-flash` for the small/fast model)
3. **Agent**: set default models for your Claude Code agent

CCR automatically writes the required config to
`~/.claude/settings.json`: the `apiKeyHelper` path, model environment
variables, and the local proxy base URL.

Once configured, launch Claude Code through the router:

```bash
ccr 'Claude Code'
```

Claude Code will now use DeepSeek models through the local proxy without
noticing anything is different.

## The Gemini Dead End

I initially tried using Gemini 3.5 Flash (`gemini/gemini-3.5-flash`) as
my model. Single-turn requests worked perfectly:

```bash
curl -s "http://127.0.0.1:3456/v1/messages" \
  -H "Content-Type: application/json" \
  -H "x-api-key: ccr-profile-..." \
  -H "anthropic-version: 2023-06-01" \
  -d '{"model":"gemini/gemini-3.5-flash","max_tokens":500,
       "messages":[{"role":"user","content":"Who made you?"}]}'
```

That returned a clean response without issues. But Claude Code broke
immediately with an `API Error: 400 All target providers failed` on
anything involving tool use, which is pretty much everything Claude Code
does (skills, file reads, bash commands).

### The Root Cause

The problem is Google's Gemini 3 API requirement for a `thought_signature`
on function call parts. When Claude Code sends a tool call, CCR translates
it from Anthropic's `tool_use` format to Gemini's `functionCall` format.
On the follow-up turn, when CCR sends the tool result back, Gemini rejects
the request because the `thought_signature` is missing. Anthropic's API
has no equivalent field, so there is nothing for CCR to pass through.

I reproduced the exact failure with a minimal curl that simulated a
tool-use conversation:

```bash
curl -sv http://127.0.0.1:3456/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: ccr-profile-..." \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model":"gemini/gemini-3.5-flash",
    "max_tokens":1000,
    "tools":[{"name":"get_weather",
      "description":"Get the weather for a location",
      "input_schema":{"type":"object",
        "properties":{"location":{"type":"string"}},
        "required":["location"]}}],
    "messages":[
      {"role":"user",
       "content":"What is the weather in Paris?"},
      {"role":"assistant",
       "content":[{"type":"tool_use","id":"tool_1",
         "name":"get_weather",
         "input":{"location":"Paris"}}]},
      {"role":"user",
       "content":[{"type":"tool_result",
         "tool_use_id":"tool_1",
         "content":"18°C, partly cloudy"}]}
    ]
  }'
```

The response confirmed it:

```
Function call is missing a thought_signature in functionCall parts.
This is required for tools to work correctly, and missing
thought_signature may lead to degraded model performance.
```

This is a known issue in CCR. Gemini 2.x models
(`gemini/gemini-2.5-flash` or `gemini/gemini-2.5-pro`) do not have the
`thought_signature` requirement and should work fine, but I wanted to
try something different.

## Switching to DeepSeek

I switched to the DeepSeek provider with two models:

- **deepseek-v4-pro**: for the main Claude Code model, handling code
  generation, reasoning and complex tasks
- **deepseek-v4-flash**: for the small/fast model, handling quick
  completions, light edits and background tasks

The switch was seamless. No `thought_signature` issues, no protocol
translation bugs, no mysterious 400 errors. Tool use works correctly
across multi-turn conversations, which means skills, file operations,
bash execution and MCP tools all function as expected.

Pricing is also reasonable. DeepSeek charges per million tokens and
both the flash and pro models are considerably cheaper than
Anthropic's equivalents. For long Claude Code sessions that rack up
hundreds of thousands of tokens, the savings add up quickly.

## Summary

Claude Code Router is a solid way to use cheaper models inside Claude
Code. If you go the Gemini route, stick to 2.x models to avoid the
`thought_signature` issue. I landed on DeepSeek with
`deepseek-v4-pro` and `deepseek-v4-flash` and have been happy with
the balance of cost and capability.
