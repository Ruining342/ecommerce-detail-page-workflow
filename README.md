# Ecommerce Detail Page Workflow v3.2

一个面向 Codex 的电商视觉 Skill：从一张或多张产品图出发，完成产品信息分流、白底精修、多角度/细节素材、6–8 屏详情页、客观纠错与无损长图拼接。

适用于淘宝、天猫、小红书、TEMU 等平台的商品详情页、商品主图、首屏 KV、分屏海报与完整详情页长图。

## v3.2 的核心流程

1. 收到产品图后只询问发布平台。
2. 信息齐全时跳过调研，直接生成最小素材组。
3. 信息不足时，先结合小红书和其他公开资料整理详情页文案确认稿；用户确认后继续。
4. 默认生成三张素材组：白底精修主图、多角度组合图、细节组合图。
5. 使用统一视觉与产品身份约束，完成 6–8 屏差异化详情页。
6. 只在字体崩溃或画面崩溃时定向纠错一次；设计偏好交给用户判断。
7. 保留独立分屏，并用脚本无损拼接完整长图。

## 安装

在 Codex 中直接发送：

```text
请安装这个 Skill：https://github.com/Ruining342/ecommerce-detail-page-workflow/tree/main/ecommerce-detail-page-workflow
```

也可以使用 Codex 自带的 Skill 安装脚本：

```bash
python "$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo Ruining342/ecommerce-detail-page-workflow \
  --path ecommerce-detail-page-workflow
```

如果没有设置 `CODEX_HOME`，通常可以改用：

```bash
python "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo Ruining342/ecommerce-detail-page-workflow \
  --path ecommerce-detail-page-workflow
```

安装后重新启动 Codex，使 Skill 被重新发现。

## 快速使用

上传产品图片后发送：

```text
使用 $ecommerce-detail-page-workflow 为这个产品制作淘宝详情页。
```

主图任务可直接发送：

```text
使用 $ecommerce-detail-page-workflow 为这个产品制作 5 张 TEMU 商品主图。
```

## 目录

```text
ecommerce-detail-page-workflow/
├── SKILL.md
├── agents/openai.yaml
├── references/
├── scripts/stitch_long_page.py
└── tests/
```

仓库内的 `ecommerce-detail-page-workflow/` 与本机通过测试的 v3.2 Skill 源码一致，可直接通过上面的仓库路径安装。

## 运行测试

需要 Python 3 和 Pillow：

```bash
python -m pip install pillow
python -m unittest discover -s ecommerce-detail-page-workflow/tests -v
```

## 安全与数据边界

- Skill 源码不包含广告注入、第三方 API 端点、密钥收集或强制外部路由。
- 仅在产品信息不足时，按工作流使用公开网页资料补充候选文案。
- 产品源图是最高优先级依据；不得把无证据的尺寸、材质、认证、检测结果或隐藏结构伪装成产品事实。
- 发布前已通过 18 项 SOP 与无损拼接测试。

## 版本

当前公开版本：`v3.2.0`。

本仓库当前未附加开源许可证；公开可见和可安装不等同于授予再分发、修改或商业使用许可。
