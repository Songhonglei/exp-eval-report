# 仓库迁移 Repository migration

`Songhonglei/orcarouter-local-eval` 升级为 `Songhonglei/exp-eval-report`，从单篇文章仓库改为多项目实验报告集合。原有 Git 历史保留。

| 原位置 | 新位置 |
|---|---|
| 仓库根目录的 OrcaRouter 正文、图表与样式 | `reports/orcarouter/` 与共享 `assets/` |
| 根目录中文文章网页 | `reports/orcarouter/zh/` |
| 新增 OrcaRouter 英文网页 | `reports/orcarouter/en/` |
| Qwen-Image 2.1 中文与英文网页 | `reports/qwen-image-2-1/zh/` 与 `reports/qwen-image-2-1/en/` |
| 根目录主页 | 中英文报告门户 |

GitHub 的仓库旧地址在改名后由平台重定向。GitHub Pages 的项目站点前缀随仓库名称变化，旧的 `orcarouter-local-eval` Pages 地址不保证跳转；分享链接应更新为以下入口。

- [中文门户](https://songhonglei.github.io/exp-eval-report/)
- [English collection](https://songhonglei.github.io/exp-eval-report/en/)
- [OrcaRouter 中文](https://songhonglei.github.io/exp-eval-report/reports/orcarouter/zh/)
- [OrcaRouter English](https://songhonglei.github.io/exp-eval-report/reports/orcarouter/en/)
- [Qwen-Image 中文](https://songhonglei.github.io/exp-eval-report/reports/qwen-image-2-1/zh/)
- [Qwen-Image English](https://songhonglei.github.io/exp-eval-report/reports/qwen-image-2-1/en/)

根目录 `ARTICLE.zh-CN.md` 保留迁移指引。新站根目录对旧式 `#section-N` 锚点转到 OrcaRouter 中文文章；这一兼容处理只适用于新站前缀，不能使已停止托管的旧 Pages 前缀自动恢复。

The repository keeps its Git history and organizes the original OrcaRouter article as an independent report. GitHub repository redirects and GitHub Pages project URLs are separate mechanisms. Update shared Pages links to the new prefix. No new model experiments were performed for this migration.
