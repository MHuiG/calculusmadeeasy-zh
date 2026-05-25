# Calculus Made Easy 中文版

《微积分其实很容易》是《Calculus Made Easy》的非官方简体中文版本。

仓库保留英文 HTML 快照，并在 `zh/` 中提供中文 HTML。

## 阅读

中文站点已发布到：[https://keen-ginger-62hw.here.now/](https://keen-ginger-62hw.here.now/)

```bash
open zh/index.html
```

## 仓库结构

```text
.
├── original/                 # 英文 HTML 快照，作为翻译和校对基准
├── zh/                       # 简体中文 HTML，可直接浏览
├── tools/
│   └── verify_translation.py # 结构与翻译风险校验脚本
└── TRANSLATION_NOTES.md      # 翻译约定、术语表和固定文案
```

## 原文来源

英文原文来源于 [calculusmadeeasy.org](https://calculusmadeeasy.org/)。

本仓库未经过 `calculusmadeeasy.org` 官方授权，也不代表原站、原站运营方或相关权利方。仓库中的英文快照仅作为中文翻译、校对和本地阅读的基础材料。

## 翻译约定

见 [TRANSLATION_NOTES.md](TRANSLATION_NOTES.md)。

## 质量检查

```bash
python3 tools/verify_translation.py
```

## 免责声明

本仓库为非官方翻译项目，仅供学习、研究和个人阅读使用。仓库内容不构成任何形式的官方出版物、授权版本或法律意见。

本仓库包含多类材料：原书文本、HTML 页面、样式、脚本、字体、图片和中文译文。它们的来源和授权可能不同，请以各文件内保留的版权与许可证声明为准。使用、分发或改编本仓库内容前，请自行确认相关权利状态。
