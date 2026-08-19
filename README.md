# DeepSeek Quick Ask for Alfred

一个无需第三方 Python 依赖的 Alfred 5 工作流。输入 `ds 问题`，确认后向 DeepSeek 提问；回答会自动复制到剪贴板，并在 Alfred Large Type 中显示。

> 非 DeepSeek 官方产品。你需要自行提供 DeepSeek API Key，并承担相应 API 费用。

## 安装与使用

1. 双击 `DeepSeek-Quick-Ask-v1.3.0.alfredworkflow` 导入 Alfred。
2. 打开 Alfred Preferences → Workflows，选中 **DeepSeek Quick Ask**，点击右上角 `[x]`。
3. 在 **Workflow Variables** 中填写 `DEEPSEEK_API_KEY`，点击保存。
4. 输入 `ds 解释一下量子纠缠`，按回车发送。

输入 `dsconfig` 可再次查看配置位置提示。

## 切换模型

- 输入 `dsmodel`：在 Alfred 中选择模型。
- 输入 `dsmodel flash`：切换到 `deepseek-v4-flash`（默认，速度与成本优先）。
- 输入 `dsmodel pro`：切换到 `deepseek-v4-pro`（复杂推理与效果优先）。

切换会立即生效，并自动清除当前会话，避免不同模型共用历史上下文。

## 思考过程显示

DeepSeek V4 默认开启思考模式。此工作流默认明确关闭它，并且只显示最终答案，不会把 API 的 `reasoning_content` 当作正文显示。

- 输入 `dsthink`：选择思考模式。
- 输入 `dsthink disabled`：关闭思考（默认，推荐）。
- 输入 `dsthink enabled`：开启思考，适用于复杂推理；插件仍只显示最终答案。

切换思考模式会自动清除当前会话。

## 连续追问

- `ds 解释一下量子纠缠`：开始一段新对话。
- `dsf 它在现实中有什么应用？`：携带最近对话的上下文继续提问。
- `dsclear`：按回车清除当前会话。

最近 6 轮问答会保存于本机的 Alfred Workflow Data 目录，供 `dsf` 使用；API Key 不会存入该目录。再次使用 `ds` 会开始并替换为一段新对话。

## 高级配置

在 Alfred 的 Workflow Variables 中可选设置：

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com/v1` | 兼容代理或自建网关 |
| `DEEPSEEK_TEMPERATURE` | `0.7` | 生成随机性，范围 0–2 |
| `DEEPSEEK_MAX_TOKENS` | `1024` | 单次回答上限，范围 1–8192 |
| `DEEPSEEK_SYSTEM_PROMPT` | 中文助手提示词 | 默认回答风格 |
| `DEEPSEEK_THINKING` | `disabled` | `enabled` 或 `disabled`；通常请使用 `dsthink` 切换 |

`DEEPSEEK_MODEL` 默认是 `deepseek-v4-flash`。通常请使用 `dsmodel` 切换，而非手动修改变量。

## 隐私与安全

- API Key 保存在 Alfred 的本机 Workflow Variables 中，且标记为“不导出”；不会被包含在工作流压缩包或打印到日志中。
- 最近 6 轮问答保存在本机 Alfred Workflow Data 目录，仅用于 `dsf` 连续追问；使用 `dsclear` 可立即删除。
- 输入的问题会发送给用户配置的 DeepSeek API 地址。

## 开发与测试

```bash
python3 -m unittest discover -s tests -v
plutil -lint info.plist
```

需要 Python 3 和 Alfred 5（含 Powerpack）。

## License

[MIT](LICENSE)

## 项目主页

源码、更新记录与安装包发布在 [fug990/alfred-deepseek-quick-ask](https://github.com/fug990/alfred-deepseek-quick-ask)。
