# My Blog

这是我的个人博客，使用 Python 静态博客生成器构建。

## 特性

- 支持 Markdown 写作
- 自动代码高亮
- 响应式设计
- 支持明暗主题切换
- 标签分类

## 项目结构

```
blog/
├── templates/          # 模板文件
├── styles/            # CSS 样式文件
├── posts/             # Markdown 文章
├── public/            # 生成的静态文件
└── static_blog_generator.py  # 生成器脚本
```

## 初始设置

### 1. 环境准备
```bash
# 安装依赖
pip install pyyaml markdown pygments

# 配置 Git
git config --global user.name "shisuiyi"
git config --global user.email "你的邮箱"
```

### 2. 获取代码
```bash
# 克隆源码仓库
git clone git@github.com:shisuiyi/blog-source.git
cd blog-source

# 给部署脚本添加执行权限
chmod +x deploy.sh
```

## 写作指南

### 1. 创建新文章
- 在 `blog/posts/` 目录下创建 `.md` 文件
- 添加文章元数据：
```yaml
---
title: 文章标题
date: YYYY-MM-DD
tags: [标签1, 标签2]
---
```
- 使用 Markdown 语法编写内容

### 2. 本地预览
```bash
# 生成静态文件
python blog/static_blog_generator.py

# 可以使用 Python 的 http 服务器预览
python -m http.server --directory blog/public 8000
# 然后访问 http://localhost:8000
```

## 部署流程

### 1. 提交源码更新
```bash
# 添加更改
git add .

# 提交更改
git commit -m "更新说明"

# 推送到源码仓库
git push origin main
```

### 2. 部署到 GitHub Pages
```bash
# 执行部署脚本
./deploy.sh
```

## 自动部署

本项目配置了 GitHub Actions：
- 当推送到 main 分支时自动部署
- 配置文件：`.github/workflows/deploy.yml`
- 部署目标：`shisuiyi.github.io`

## 仓库说明

- 源码仓库：`github.com/shisuiyi/blog-source`
  - 存放博客源代码
  - 包含模板、样式、文章等

- 部署仓库：`github.com/shisuiyi/shisuiyi.github.io`
  - 存放生成的静态文件
  - 通过 GitHub Pages 提供访问

## 文件说明

- `deploy.sh`: 部署脚本
- `.gitignore`: Git 忽略文件配置
- `blog/templates/`: 网站模板
- `blog/styles/`: 样式文件
- `blog/posts/`: 博客文章
- `.github/workflows/`: GitHub Actions 配置

## 许可证

MIT 